# Verificación inicial

Fecha de actualización: 2026-10-02

## Estado del repositorio

- Repositorio público: <https://github.com/AndresBanderas864/cloud-compiler-cpp>.
- `git diff --check`: correcto.
- No se encontraron OCID, claves privadas ni credenciales AWS en el código versionado.

## Pruebas automatizadas

- `python -m pytest -q`: **3 passed**.
- `python -m compileall -q app runner tests`: correcto.
- `docker compose up -d --build`: correcto.
- `GET http://localhost:8000/api/health`: respondió 200.

## Verificación de seguridad

- El backend local usa sandbox Docker con límites de recursos y red deshabilitada.
- La imagen web de producción (`Dockerfile.web.aws`) no incluye ni monta `docker.sock`.
- Los runners AWS usan Fargate, subnets privadas, sin IP pública y Security Group restringido.
- Los runners ejecutan con usuario sin privilegios, token temporal y eliminación al finalizar.
- ECR usa repositorios privados, cifrado AES256, escaneo al publicar y tags inmutables.

## Verificación AWS

- Región: `us-east-2`.
- Stack temporal: `cloud-compiler-cpp-paas`, alcanzó `UPDATE_COMPLETE` y luego fue eliminado.
- ECS Service web: llegó a `1/1` tareas en ejecución y estado `ACTIVE` durante la evaluación.
- `/api/health` público temporal: respondió 200 durante la evaluación.
- WebSocket real: creó un runner Fargate, compiló C++20, recibió entrada `4`, devolvió `5` y finalizó correctamente.
- El runner probado pasó a estado `STOPPED`.

## Limitaciones conocidas

- El endpoint temporal usa HTTP, no HTTPS, porque aún no se configuró dominio ni certificado ACM.
- No hay autenticación ni persistencia, conforme al alcance del MVP.
- El stack, NAT Gateway, ALB, Fargate y repositorios ECR fueron eliminados después de la evaluación para evitar costes.
