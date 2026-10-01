# Despliegue PaaS en OCI Container Instances

## Prerrequisitos

- Tenancy y compartment en Oracle Cloud.
- Región y availability domain elegidos.
- VCN con una subnet privada para web y runners.
- Reglas de red: HTTPS hacia web y puerto 8001 solo entre subnets privadas.
- Repositorio OCIR y permisos IAM para publicar imágenes y crear/eliminar Container Instances.
- Variables `OCI_*` documentadas en `docs/arquitectura-oci.md`.

## Publicar imágenes en OCIR

Construir las imágenes localmente:

```bash
docker build -t cloud-compiler-sandbox:latest .
docker build -t compiler-runner:latest -f runner/Dockerfile .
docker build -t cloud-compiler-web:latest -f Dockerfile.web .
```

Etiquetar y publicar en el repositorio de OCI Container Registry. Sustituir los valores entre corchetes sin guardar credenciales en el repositorio:

```bash
docker tag compiler-runner:latest [region-key].ocir.io/[tenancy-namespace]/cloud-compiler-runner:latest
docker push [region-key].ocir.io/[tenancy-namespace]/cloud-compiler-runner:latest
docker tag cloud-compiler-web:latest [region-key].ocir.io/[tenancy-namespace]/cloud-compiler-web:latest
docker push [region-key].ocir.io/[tenancy-namespace]/cloud-compiler-web:latest
```

## Crear la instancia web

Crear una Container Instance desde la consola o Terraform con la imagen `cloud-compiler-web`. Configurar:

- `EXECUTION_BACKEND=oci`.
- Las variables `OCI_COMPARTMENT_ID`, `OCI_AVAILABILITY_DOMAIN`, `OCI_SUBNET_ID` y `OCI_RUNNER_IMAGE`.
- Autenticación mediante principal de instancia cuando sea posible.
- Memoria y CPU suficientes para la API, sin reservar recursos de los runners.
- Puerto público únicamente para HTTPS.

La aplicación web debe estar en la misma VCN que los runners para usar sus IP privadas.

## Prueba posterior

1. Consultar `/api/health`.
2. Ejecutar Hola Mundo.
3. Ejecutar un programa con `cin`.
4. Provocar un error de compilación y verificar `CC-006`.
5. Confirmar en OCI que la instancia runner se elimina al terminar.
6. Revisar que no haya código del usuario en logs ni Object Storage.

## Operación

La aplicación web es persistente; los runners son efímeros. No se debe dejar `docker.sock` montado en la instancia web de OCI. Docker Compose se mantiene únicamente para desarrollo local.
