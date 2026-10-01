# Arquitectura PaaS con OCI Container Instances

## Objetivo

Eliminar la dependencia de `docker.sock` del backend y usar OCI Container Instances como plataforma administrada para la aplicación y para cada runner efímero.

## Componentes

```text
Navegador
   │ WebSocket
   ▼
OCI Container Instance: cloud-compiler-web
   ├── FastAPI + frontend
   ├── OCI SDK
   └── gestor de trabajos
          │ crea y elimina mediante API OCI
          ▼
OCI Container Instance: compiler-runner
   ├── imagen compiler-runner
   ├── g++ C++17/C++20/C++23
   ├── WebSocket privado
   ├── límites del proceso
   └── eliminación al finalizar
```

## Flujo de un trabajo

1. La aplicación valida código, estándar y capacidad.
2. Genera un token aleatorio de un solo trabajo.
3. Solicita a `ContainerInstanceClient` una instancia en una subnet privada.
4. OCI crea el runner con `RUNNER_TOKEN` y la imagen publicada en OCIR.
5. La aplicación espera a que el runner esté `ACTIVE` y obtiene su IP privada.
6. La aplicación abre un WebSocket privado hacia `/ws/run?token=...`.
7. El navegador y el runner intercambian estados, salida e `stdin`.
8. Al finalizar o abandonar la sesión, OCI elimina la instancia.

## Límites y seguridad

- El runner no recibe una IP pública.
- La regla de red solo permite el puerto del runner desde la subnet de la aplicación.
- La aplicación usa una identidad dinámica o principal de instancia, no claves privadas en la imagen.
- El código se envía por memoria y se elimina con la instancia.
- El runner ejecuta como usuario sin privilegios y limita memoria, CPU, procesos, archivos y tiempo.
- No se montan sockets Docker ni directorios del host.

## Configuración requerida

```text
EXECUTION_BACKEND=oci
OCI_COMPARTMENT_ID=<OCID>
OCI_AVAILABILITY_DOMAIN=<dominio>
OCI_SUBNET_ID=<OCID subnet privada>
OCI_RUNNER_IMAGE=<OCIR>/cloud-compiler-runner:version
OCI_RUNNER_SHAPE=<shape disponible>
OCI_RUNNER_PORT=8001
```

La creación real requiere una cuenta OCI, permisos IAM, una VCN/subnet y una imagen publicada en OCIR. Hasta contar con esos valores, el backend local seguirá siendo el adaptador de desarrollo.
