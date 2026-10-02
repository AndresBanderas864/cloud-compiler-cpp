# Cloud Compiler C++

PaaS educativo para escribir, compilar y ejecutar programas pequeños de C++ desde la nube.

## Estado actual

MVP desplegado temporalmente en AWS ECS Fargate, región `us-east-2`.

- Aplicación web en ECS Fargate detrás de un Application Load Balancer.
- Runners efímeros privados creados con `RunTask` y detenidos con `StopTask`.
- Imágenes privadas en Amazon ECR.
- WebSocket interactivo probado con C++20, `cin` y salida correcta.
- Repositorio público: <https://github.com/AndresBanderas864/cloud-compiler-cpp>

El entorno AWS se mantiene solo para evaluación. Después de la revisión, debe eliminarse con las instrucciones de [despliegue y limpieza](docs/despliegue-aws.md#eliminar-el-entorno-temporal).

## Visión del MVP

Una pantalla con dos apartados:

1. **IDE:** editor donde el usuario escribe o pega código C++.
2. **Terminal:** salida del programa, errores de compilación y mensajes de estado.

El servicio debe priorizar una experiencia rápida y comprensible, sin ejecutar código no confiable fuera de un entorno aislado.

## Documentación

- [Proceso de levantamiento de requisitos](docs/proceso-levantamiento-requisitos.md)
- [Guion de entrevistas](docs/entrevistas-usuarios.md)
- [Validación del alcance del MVP](docs/validacion-alcance-mvp.md)
- [Arquitectura técnica del MVP](docs/arquitectura-mvp.md)
- [Arquitectura PaaS con AWS ECS Fargate](docs/arquitectura-aws.md)
- [Despliegue en AWS](docs/despliegue-aws.md)
- [Catálogo inicial de requisitos](docs/catalogo-requisitos.md)
- [Plan del proyecto](PLAN.md)
- [Decisiones](DECISIONS.md)
- [Tareas](TASKS.md)
- [Verificación inicial](docs/verificacion-inicial.md)

## Principios

- Separación de responsabilidades y diseño orientado a SOLID.
- Seguridad por defecto para compilación y ejecución remotas.
- Accesibilidad y diseño responsive desde el MVP.
- Requisitos trazables a criterios de aceptación y pruebas.

## Ejecutar localmente

Requisitos: Python 3.11+, Docker y Docker Compose.

```powershell
python -m venv .venv
.venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
docker compose up --build
```

Abrir `http://localhost:8000`. En local, Docker Compose usa `docker.sock` únicamente para crear el sandbox; este flujo no se utiliza en AWS.

Para ejecutar las pruebas de validación:

```bash
python -m pytest -q
```

## Limpieza AWS

El stack temporal incluye NAT Gateway, ALB, ECS y CloudWatch Logs. Elimina el stack y los repositorios ECR después de la evaluación; los pasos reproducibles están en [despliegue-aws.md](docs/despliegue-aws.md#eliminar-el-entorno-temporal).
