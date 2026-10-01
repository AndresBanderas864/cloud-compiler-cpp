# Arquitectura técnica del MVP

## Estado

Propuesta para implementar y validar antes del despliegue.

## Componentes

```text
Navegador
  ├── Editor sencillo + selector de estándar
  ├── Terminal interactiva + entrada de usuario
  └── Cliente WebSocket/HTTP
          │
          ▼
API web
  ├── Validación de solicitud y límites
  ├── Control de capacidad (5 normal / 10 máximo)
  ├── Estado temporal en memoria
  └── Orquestador de trabajos
          │
          ▼
Sandbox efímero por trabajo
  ├── Compilación C++17/C++20/C++23
  ├── Ejecución sin red ni secretos
  ├── Entrada/salida por canal controlado
  └── Tiempo, memoria, CPU, procesos y salida limitados
```

## Tecnologías propuestas

- **Backend:** Python con FastAPI.
- **Frontend:** HTML, CSS y JavaScript sin framework pesado.
- **Comunicación:** HTTP para crear trabajos y WebSocket para salida e `stdin` interactivos.
- **Sandbox:** contenedor efímero con Docker y usuario sin privilegios.
- **Compilador:** toolchain con `g++` y banderas `-std=c++17`, `-std=c++20` o `-std=c++23`.
- **Despliegue:** máquina virtual de Oracle Cloud; la región se elegirá según cercanía y disponibilidad.

Estas tecnologías son una propuesta de bajo costo y baja complejidad para el proyecto académico, no una decisión irreversible.

## Flujo de ejecución

1. El navegador envía código, versión seleccionada y estado de la sesión.
2. La API valida tamaño, versión y capacidad disponible.
3. El orquestador crea un directorio temporal y un sandbox aislado.
4. El sandbox compila con la versión solicitada.
5. Si compila, inicia el binario con límites de recursos.
6. La salida, los errores y el estado se envían por el canal controlado.
7. La entrada escrita en la terminal se envía al `stdin` del proceso.
8. Al terminar, cancelar, exceder cinco minutos o abandonar la sesión, se destruye el sandbox y se borran los datos temporales.

## Límites iniciales

| Límite | Valor |
|---|---:|
| Tiempo total de compilación y ejecución | 5 minutos |
| Salida de terminal | 100 KB |
| Usuarios simultáneos normales | 5 |
| Usuarios simultáneos máximos | 10 |
| Persistencia | Ninguna |
| Acceso de red del sandbox | Denegado |

La memoria y CPU se configurarán después de probar el entorno de Oracle Cloud; las estimaciones actuales son 50–150 MB de RAM y aproximadamente 1 vCPU por trabajo.

## Responsabilidades por capa

- **Interfaz:** edición, selección, accesibilidad, estados y terminal; no compila ni ejecuta.
- **API:** valida entradas, autoriza operaciones de la sesión anónima y traduce estados; no contiene reglas de sandbox.
- **Aplicación:** coordina trabajos y estados; depende de contratos, no de Docker directamente.
- **Adaptador de sandbox:** crea, limita, comunica y destruye el entorno de ejecución.
- **Política de recursos:** concentra límites y evita valores dispersos.

Esta separación permite cambiar Docker, el proveedor cloud o la interfaz sin mezclar responsabilidades.

## Riesgos y controles

- Código malicioso: sandbox sin privilegios, sin red, con límites y eliminación obligatoria.
- Bucle infinito: timeout total y cancelación del proceso y sus descendientes.
- Salida excesiva: truncamiento a 100 KB y estado explícito.
- Cierre no detectado: TTL de seguridad en el backend.
- Saturación: rechazo controlado al alcanzar diez usuarios, sin cola.
- Filtración de datos: no guardar código, resultados, secretos ni logs con el contenido completo.

## Nota de desarrollo local

El `docker-compose.yml` monta el socket de Docker únicamente para facilitar el desarrollo local. Ese montaje otorga privilegios elevados al proceso web y no debe trasladarse sin revisión a producción. En Oracle Cloud se deberá usar Docker rootless, un runtime dedicado o un servicio de sandbox con permisos mínimos.
