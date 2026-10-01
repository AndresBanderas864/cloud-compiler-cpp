"""Provisionamiento de runners efímeros en OCI Container Instances."""

from __future__ import annotations

import asyncio
import os
import secrets
import time
from dataclasses import dataclass
from urllib.parse import quote

import oci
from oci.container_instances import ContainerInstanceClient
from oci.container_instances.models import (
    CreateContainerDetails,
    CreateContainerInstanceDetails,
    CreateContainerInstanceShapeConfigDetails,
    CreateContainerResourceConfigDetails,
    CreateContainerVnicDetails,
)


class OciConfigurationError(RuntimeError):
    """La configuración necesaria para OCI no está disponible."""


@dataclass(frozen=True)
class RunnerEndpoint:
    instance_id: str
    websocket_url: str
    token: str


class OciContainerInstanceProvisioner:
    def __init__(self) -> None:
        required = ("OCI_COMPARTMENT_ID", "OCI_AVAILABILITY_DOMAIN", "OCI_SUBNET_ID", "OCI_RUNNER_IMAGE")
        missing = [name for name in required if not os.getenv(name)]
        if missing:
            raise OciConfigurationError(f"Faltan variables OCI: {', '.join(missing)}")
        self.compartment_id = os.environ["OCI_COMPARTMENT_ID"]
        self.availability_domain = os.environ["OCI_AVAILABILITY_DOMAIN"]
        self.subnet_id = os.environ["OCI_SUBNET_ID"]
        self.runner_image = os.environ["OCI_RUNNER_IMAGE"]
        self.shape = os.getenv("OCI_RUNNER_SHAPE", "CI.Standard.E4.Flex")
        self.port = int(os.getenv("OCI_RUNNER_PORT", "8001"))

    def _client(self) -> ContainerInstanceClient:
        if os.getenv("OCI_AUTH", "config_file") == "instance_principal":
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
            return ContainerInstanceClient({}, signer=signer)
        config = oci.config.from_file(profile=os.getenv("OCI_PROFILE", "DEFAULT"))
        return ContainerInstanceClient(config)

    def _create(self) -> RunnerEndpoint:
        client = self._client()
        token = secrets.token_urlsafe(32)
        container = CreateContainerDetails(
            display_name="compiler-runner",
            image_url=self.runner_image,
            command=["uvicorn"],
            arguments=["runner.main:app", "--host", "0.0.0.0", "--port", str(self.port)],
            environment_variables={"RUNNER_TOKEN": token},
            resource_config=CreateContainerResourceConfigDetails(vcpus_limit=1.0, memory_limit_in_gbs=1.0),
        )
        details = CreateContainerInstanceDetails(
            display_name=f"compiler-runner-{secrets.token_hex(5)}",
            compartment_id=self.compartment_id,
            availability_domain=self.availability_domain,
            shape=self.shape,
            shape_config=CreateContainerInstanceShapeConfigDetails(ocpus=1.0, memory_in_gbs=1.0),
            containers=[container],
            vnics=[CreateContainerVnicDetails(subnet_id=self.subnet_id, is_public_ip_assigned=False)],
            container_restart_policy="NEVER",
            graceful_shutdown_timeout_in_seconds=5,
        )
        instance = client.create_container_instance(details).data
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            current = client.get_container_instance(instance.id).data
            if current.lifecycle_state == "ACTIVE":
                if not current.vnics or not current.vnics[0].private_ip:
                    raise OciConfigurationError("OCI no devolvió una IP privada para el runner.")
                ip = current.vnics[0].private_ip
                return RunnerEndpoint(instance.id, f"ws://{ip}:{self.port}/ws/run?token={quote(token)}", token)
            if current.lifecycle_state == "FAILED":
                raise OciConfigurationError("OCI no pudo iniciar el runner efímero.")
            time.sleep(2)
        raise OciConfigurationError("OCI agotó el tiempo de inicio del runner.")

    def _delete(self, instance_id: str) -> None:
        self._client().delete_container_instance(instance_id)

    async def create(self) -> RunnerEndpoint:
        return await asyncio.to_thread(self._create)

    async def delete(self, instance_id: str) -> None:
        await asyncio.to_thread(self._delete, instance_id)
