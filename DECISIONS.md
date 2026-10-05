# Decisiones

## ADR-001: repositorio independiente

El compilador se desarrollará en un repositorio independiente, separado de proyectos existentes para evitar mezclar dominios, dependencias y documentación. El repositorio es público para facilitar la revisión académica; no se deben almacenar secretos.

## ADR-002: alcance del MVP

La primera versión tendrá una sola pantalla con dos apartados claramente identificados: un editor de código C++ y una terminal de resultados. No se incluirán inicialmente cuentas, colaboración, múltiples archivos ni persistencia de proyectos.

## ADR-003: ejecución segura como requisito de diseño

El código enviado por el usuario se tratará como no confiable. La compilación y ejecución deberán ocurrir en un entorno aislado, con límites de tiempo, memoria, CPU, procesos y salida; nunca directamente en el proceso principal de la aplicación.

## ADR-004: estándares soportados

El MVP soportará C++17, C++20 y C++23. La versión se seleccionará por ejecución y deberá estar disponible de forma explícita en la imagen o entorno seguro de compilación.

## ADR-005: sesiones sin persistencia ni autenticación

El MVP no tendrá registro ni inicio de sesión. El código, la entrada y los resultados serán datos temporales; no se guardarán como proyectos ni en una base de datos persistente. La estrategia exacta de limpieza al cerrar la página y la expiración de sesiones queda pendiente de diseño.

## ADR-006: proveedor cloud inicial

Se usará Amazon Web Services como proveedor inicial, con ECS Fargate en la región seleccionada `us-east-2`. La elección prioriza tareas efímeras, aislamiento de runners y compatibilidad con WebSockets. El entorno de evaluación se elimina después de la revisión para evitar costes.

## ADR-007: capacidad inicial del MVP

El alcance académico se dimensionará para cinco usuarios simultáneos en condiciones normales y hasta diez en el peor caso previsto. No tendrá cola: cuando se alcance el máximo de diez usuarios, el backend rechazará temporalmente nuevas solicitudes. La región seleccionada de AWS es `us-east-2`.

## ADR-008: entrada estándar interactiva

La entrada estándar podrá enviarse durante la ejecución, no únicamente antes de iniciarla. La interfaz deberá proporcionar un control de entrada y el backend un canal bidireccional; esta decisión puede aumentar la complejidad frente a una solicitud HTTP única.

## ADR-009: estimaciones de consumo

Para dimensionar el prototipo se utilizarán como referencias 15–30 KB de tráfico por ejecución, 1.5 MB de carga inicial, 50–150 MB de RAM por compilación, aproximadamente 1 vCPU y 100–500 KB de almacenamiento temporal por trabajo. Son estimaciones, no garantías de capacidad.

## ADR-010: arquitectura técnica inicial

Se propone FastAPI, frontend estático con HTML/CSS/JavaScript, WebSocket para la terminal interactiva y Docker para cada sandbox efímero. La propuesta prioriza simplicidad, bajo costo y separación de responsabilidades; deberá validarse antes del despliegue.

## ADR-011: migración a Amazon ECS Fargate

La arquitectura de producción usará Amazon ECS Fargate para la aplicación web y para runners efímeros. El backend no creará contenedores mediante `docker.sock`; solicitará y detendrá tareas mediante boto3. Docker Compose queda limitado al desarrollo local.
