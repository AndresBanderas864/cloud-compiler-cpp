# Despliegue PaaS en Amazon ECS Fargate

## Prerrequisitos

- Proyecto AWS en la región seleccionada `us-east-2`.
- VPC con subnets públicas para el ALB y privadas para web/runners.
- NAT Gateway o endpoints privados para ECR, S3 y CloudWatch Logs.
- Security Groups separados para ALB, web y runners.
- Repositorios privados ECR para `cloud-compiler-web` y `cloud-compiler-runner`.
- Execution role y task role web configurados con mínimo privilegio.

## Publicar imágenes

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com
docker build -t cloud-compiler-web:latest -f Dockerfile.web.aws .
docker build -t cloud-compiler-runner:latest -f runner/Dockerfile .
docker tag cloud-compiler-web:latest <account-id>.dkr.ecr.us-east-2.amazonaws.com/cloud-compiler-web:latest
docker tag cloud-compiler-runner:latest <account-id>.dkr.ecr.us-east-2.amazonaws.com/cloud-compiler-runner:latest
docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/cloud-compiler-web:latest
docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/cloud-compiler-runner:latest
```

Usa tags inmutables por versión en producción y activa el escaneo de imágenes.

## Crear las tareas ECS

### Runner

- Launch type: Fargate.
- Network mode: `awsvpc`.
- Puerto: `8001`.
- Sin IP pública.
- Imagen: repositorio ECR `cloud-compiler-runner`.
- Container name: `compiler-runner`.
- CloudWatch Logs habilitados.

### Web

- Launch type: Fargate.
- Puerto: `8000`.
- Task role con `ecs:RunTask`, `ecs:StopTask`, `ecs:DescribeTasks`, `ec2:DescribeNetworkInterfaces` e `iam:PassRole` limitados a los recursos del proyecto.
- Variables de entorno según `.env.aws.example`.

## Servicio web y ALB

1. Crea un ECS Service con al menos una tarea web.
2. Asócialo a un Application Load Balancer.
3. Usa un target group en el puerto `8000`.
4. Configura el health check en `/api/health`.
5. Publica HTTPS; no expongas el puerto `8001`.

## Verificación

1. Comprueba `/api/health`.
2. Ejecuta Hola Mundo.
3. Ejecuta un programa con `cin`.
4. Comprueba un error de compilación.
5. Comprueba cancelación y timeout.
6. Confirma que cada tarea runner pasa a `STOPPED`.
7. Revisa CloudWatch Logs y ECR sin exponer código ni tokens.

Docker Compose queda reservado para desarrollo local y conserva su flujo con `docker.sock` únicamente en ese entorno.
