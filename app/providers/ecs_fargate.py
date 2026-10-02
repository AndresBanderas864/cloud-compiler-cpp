"""Provisionamiento de runners efímeros en Amazon ECS Fargate."""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from dataclasses import dataclass
from urllib.parse import quote

import boto3
from botocore.exceptions import ClientError


class EcsConfigurationError(RuntimeError):
    """La configuración necesaria para ECS no está disponible."""


@dataclass(frozen=True)
class RunnerEndpoint:
    task_arn: str
    websocket_url: str
    token: str


class EcsFargateProvisioner:
    def __init__(self) -> None:
        required = (
            "ECS_CLUSTER",
            "ECS_RUNNER_TASK_DEFINITION",
            "ECS_RUNNER_SUBNET_IDS",
            "ECS_RUNNER_SECURITY_GROUP",
        )
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise EcsConfigurationError(f"Faltan variables ECS: {', '.join(missing)}")
        self.cluster = os.environ["ECS_CLUSTER"]
        self.task_definition = os.environ["ECS_RUNNER_TASK_DEFINITION"]
        self.subnets = [value.strip() for value in os.environ["ECS_RUNNER_SUBNET_IDS"].split(",") if value.strip()]
        self.security_group = os.environ["ECS_RUNNER_SECURITY_GROUP"]
        self.container_name = os.getenv("ECS_RUNNER_CONTAINER_NAME", "compiler-runner")
        self.port = int(os.getenv("ECS_RUNNER_PORT", "8001"))
        if not self.subnets:
            raise EcsConfigurationError("ECS_RUNNER_SUBNET_IDS no contiene subnets válidas.")

        profile = os.getenv("AWS_PROFILE")
        session = boto3.Session(profile_name=profile) if profile else boto3.Session()
        self.ecs = session.client("ecs", region_name=os.getenv("AWS_REGION", "us-east-2"))
        self.ec2 = session.client("ec2", region_name=os.getenv("AWS_REGION", "us-east-2"))

    def _private_ip(self, task: dict) -> str:
        for attachment in task.get("attachments", []):
            if attachment.get("type") != "ElasticNetworkInterface":
                continue
            eni_id = next(
                (detail["value"] for detail in attachment.get("details", []) if detail.get("name") == "networkInterfaceId"),
                None,
            )
            if eni_id:
                interfaces = self.ec2.describe_network_interfaces(NetworkInterfaceIds=[eni_id]).get("NetworkInterfaces", [])
                if interfaces and interfaces[0].get("PrivateIpAddress"):
                    return interfaces[0]["PrivateIpAddress"]
        raise EcsConfigurationError("ECS no devolvió una IP privada para el runner.")

    def _create(self) -> RunnerEndpoint:
        token = secrets.token_urlsafe(32)
        try:
            response = self.ecs.run_task(
                cluster=self.cluster,
                taskDefinition=self.task_definition,
                launchType="FARGATE",
                count=1,
                platformVersion="LATEST",
                networkConfiguration={
                    "awsvpcConfiguration": {
                        "subnets": self.subnets,
                        "securityGroups": [self.security_group],
                        "assignPublicIp": "DISABLED",
                    }
                },
                overrides={
                    "containerOverrides": [
                        {
                            "name": self.container_name,
                            "environment": [{"name": "RUNNER_TOKEN", "value": token}],
                        }
                    ]
                }
            )
        except ClientError as error:
            detail = error.response.get("Error", {}).get("Message", "error desconocido")
            raise EcsConfigurationError(f"ECS rechazó el runner: {detail}") from error
        failures = response.get("failures", [])
        if failures or not response.get("tasks"):
            reason = failures[0].get("reason", "sin detalles") if failures else "ECS no creó la tarea."
            raise EcsConfigurationError(f"ECS no pudo crear el runner: {reason}")

        task_arn = response["tasks"][0]["taskArn"]
        try:
            deadline = time.monotonic() + 120
            while time.monotonic() < deadline:
                task = self.ecs.describe_tasks(cluster=self.cluster, tasks=[task_arn])["tasks"][0]
                if task.get("lastStatus") == "RUNNING":
                    ip = self._private_ip(task)
                    return RunnerEndpoint(task_arn, f"ws://{ip}:{self.port}/ws/run?token={quote(token)}", token)
                if task.get("lastStatus") == "STOPPED":
                    reason = task.get("stoppedReason", "sin detalles")
                    raise EcsConfigurationError(f"ECS detuvo el runner al iniciar: {reason}")
                time.sleep(2)
            raise EcsConfigurationError("ECS agotó el tiempo de inicio del runner.")
        except Exception:
            try:
                self.ecs.stop_task(cluster=self.cluster, task=task_arn, reason="runner startup failed")
            except Exception:
                pass
            raise

    def _delete(self, task_arn: str) -> None:
        self.ecs.stop_task(cluster=self.cluster, task=task_arn, reason="compiler run finished")

    async def create(self) -> RunnerEndpoint:
        return await asyncio.to_thread(self._create)

    async def delete(self, task_arn: str) -> None:
        await asyncio.to_thread(self._delete, task_arn)
