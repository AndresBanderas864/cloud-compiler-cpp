# Tareas

## Fase 1: requisitos

- [ ] Validar problema, usuarios y alcance del MVP.
- [ ] Entrevistar usuarios potenciales.
- [ ] Completar el catálogo de requisitos funcionales y no funcionales.
- [ ] Definir criterios de aceptación y trazabilidad.
- [ ] Revisar y aprobar la línea base de requisitos.

## Fase 2: producto

- [x] Diseñar arquitectura por capas y límites de seguridad.
- [x] Implementar editor y terminal.
- [x] Implementar compilación aislada.
- [x] Automatizar pruebas y verificaciones de calidad.

## Fase 3: migración PaaS a AWS

- [x] Crear imagen `compiler-runner` sin Docker-in-Docker.
- [x] Crear adaptador ECS Fargate y puente WebSocket.
- [x] Crear VPC/subnets privadas, NAT y Security Groups.
- [x] Crear repositorios ECR y publicar imágenes.
- [x] Crear roles IAM y task definitions.
- [x] Configurar y probar el servicio web con ALB.
- [x] Probar creación y detención real de runners Fargate.
- [x] Eliminar el entorno AWS temporal después de la revisión académica.
