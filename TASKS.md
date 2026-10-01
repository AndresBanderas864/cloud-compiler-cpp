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

## Fase 3: migración PaaS

- [x] Crear imagen `compiler-runner` sin Docker-in-Docker.
- [x] Crear adaptador OCI Container Instances y puente WebSocket.
- [ ] Crear VCN/subnet privada y permisos IAM.
- [ ] Publicar imágenes en OCIR.
- [ ] Configurar y probar Container Instance web.
- [ ] Probar creación y eliminación real de runners OCI.
