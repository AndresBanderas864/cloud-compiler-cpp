# Arquitectura PaaS con Amazon ECS Fargate

## Objetivo

Ejecutar la aplicación web y cada compilación en tareas Fargate separadas, sin `docker.sock` ni acceso público a los runners.

## Componentes

```text
Navegador
   │ HTTP/WebSocket (HTTPS pendiente de dominio y ACM)
   ▼
Application Load Balancer
   ▼
ECS Fargate: cloud-compiler-web
   ├── FastAPI + frontend
   ├── boto3
   └── gestor de tareas efímeras
          │ ecs:RunTask / ecs:StopTask
          ▼
ECS Fargate: compiler-runner
   ├── imagen privada de ECR
   ├── g++ C++17/C++20/C++23
   ├── WebSocket privado
   ├── límites del proceso
   └── parada al finalizar
```

## Flujo de un trabajo

1. La aplicación valida código, estándar y capacidad.
2. Genera un token aleatorio de un solo trabajo.
3. Solicita una tarea Fargate en subnets privadas mediante `RunTask`.
4. Pasa `RUNNER_TOKEN` mediante un override temporal del contenedor.
5. Espera el estado `RUNNING` y obtiene la IP privada de la ENI.
6. Abre un WebSocket privado hacia `/ws/run?token=...`.
7. Reenvía estados, salida e `stdin` entre navegador y runner.
8. Detiene la tarea mediante `StopTask` al finalizar o abandonar la sesión.

## Límites y seguridad

- Los runners usan `awsvpc` sin IP pública.
- El Security Group del runner solo permite TCP `8001` desde el Security Group web.
- La tarea web usa un task role con permisos mínimos para ECS y EC2.
- El runner no necesita permisos AWS.
- El código se mantiene en memoria y almacenamiento temporal de la tarea.
- El runner ejecuta como usuario sin privilegios y limita memoria, CPU, procesos, archivos y tiempo.
- No se montan sockets Docker ni directorios del host.

## Variables requeridas

```text
EXECUTION_BACKEND=ecs
AWS_REGION=us-east-2
ECS_CLUSTER=<nombre-cluster>
ECS_RUNNER_TASK_DEFINITION=<familia-o-arn-task-definition>
ECS_RUNNER_SUBNET_IDS=<subnet-1>,<subnet-2>
ECS_RUNNER_SECURITY_GROUP=<security-group-id>
ECS_RUNNER_CONTAINER_NAME=compiler-runner
ECS_RUNNER_PORT=8001
```
