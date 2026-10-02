# Catálogo inicial de requisitos

Este documento contiene la línea base funcional y no funcional del MVP. La validación de producto y QA debe continuar para cerrar los requisitos todavía marcados como propuestos.

## Requisitos funcionales

### RF-001 — Editar código C++

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema debe permitir escribir o pegar código C++ en un editor sencillo, con numeración de líneas y un programa de Hola Mundo precargado.
- **Criterio:** Dado que el usuario está en la pantalla principal, cuando escriba o pegue código en el editor, entonces el contenido debe permanecer visible, editable y mostrar su numeración de líneas.
- **Estado:** propuesto.

### RF-002 — Solicitar compilación y ejecución

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema debe permitir enviar el contenido del editor a compilación y ejecución.
- **Criterio:** Dado que existe código en el editor, cuando el usuario solicite ejecutar, entonces el sistema debe iniciar un trabajo y mostrar su estado.
- **Estado:** propuesto.

### RF-003 — Mostrar resultado

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el apartado terminal debe mostrar la salida del programa, los errores de compilación o los errores de ejecución con mensajes simplificados y el identificador del error.
- **Criterio:** Dado que finalizó el trabajo, cuando haya salida o error, entonces la terminal debe mostrar el resultado diferenciando estado exitoso y fallido, junto con el identificador del error cuando corresponda.
- **Estado:** propuesto.

### RF-004 — Cancelar ejecución

- **Actor:** usuario.
- **Prioridad:** Should.
- **Descripción:** el usuario debe poder cancelar un trabajo que aún esté ejecutándose.
- **Criterio:** Dado que hay un trabajo activo, cuando el usuario lo cancele, entonces el sistema debe detenerlo y mostrar el estado cancelado.
- **Estado:** propuesto.

### RF-005 — Seleccionar versión de C++

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema debe permitir compilar y ejecutar código usando C++17, C++20 o C++23.
- **Criterio:** Dado que el usuario tiene código en el editor, cuando seleccione o cambie entre C++17, C++20 y C++23 y ejecute, entonces el trabajo debe usar la versión seleccionada.
- **Estado:** propuesto.

### RF-006 — Proporcionar entrada estándar

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el usuario debe poder proporcionar datos de entrada estándar desde la terminal interactiva para programas que utilicen `cin`.
- **Criterio:** Dado que el programa lee entrada estándar, cuando el usuario escriba datos en la terminal y presione Enter, entonces el proceso debe recibirlos y continuar la ejecución.
- **Estado:** propuesto.

### RF-007 — Eliminar la sesión volátil

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema no debe conservar código ni resultados después del cierre de la página o de la expiración de la sesión.
- **Criterio:** Dado que existe una sesión activa, cuando el usuario cierre la página, entonces el sistema debe invalidar la sesión y eliminar los datos temporales asociados dentro del plazo definido.
- **Estado:** propuesto; requiere definir detección de cierre y plazo de limpieza.

### RF-008 — Enviar entrada estándar durante la ejecución

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el usuario debe poder enviar datos a la entrada estándar mientras el programa está ejecutándose.
- **Criterio:** Dado que el programa está esperando datos en `cin`, cuando el usuario escriba y envíe una entrada, entonces el proceso debe recibirla y la terminal debe continuar mostrando el resultado.
- **Estado:** propuesto; requiere canal bidireccional entre navegador y backend.

## Requisitos no funcionales iniciales

### RNF-001 — Aislamiento de ejecución

El código del usuario debe ejecutarse en un entorno aislado, sin acceso innecesario a la red, al host ni a secretos del servicio.

### RNF-002 — Límites de recursos

Cada trabajo debe tener límites configurables de tiempo, memoria, CPU, procesos y tamaño de salida.

### RNF-003 — Accesibilidad y responsive

Los controles deben ser operables con teclado, tener nombres accesibles y mantener editor y terminal utilizables en pantallas pequeñas.

### RNF-004 — Trazabilidad

Cada requisito aprobado debe enlazar con al menos un criterio de aceptación y una prueba.

### RNF-005 — Uso sin cuenta

El usuario debe poder utilizar el MVP sin registrarse ni iniciar sesión.

### RNF-006 — Tiempo máximo de ejecución

La compilación y ejecución de cada programa deben finalizar, ser canceladas o marcarse como excedidas al alcanzar cinco minutos.

### RNF-007 — Infraestructura inicial

El despliegue inicial se evaluará sobre AWS ECS Fargate en la región seleccionada `us-east-2`, priorizando tareas efímeras, aislamiento de runners y limpieza reproducible del entorno temporal.

### RNF-008 — Capacidad concurrente

El MVP se dimensionará para cinco usuarios simultáneos en condiciones normales y hasta diez en el peor caso previsto. Si se alcanza el límite máximo, una nueva solicitud se rechazará con un mensaje claro y no se utilizará cola.

### RNF-009 — Recursos por ejecución

Como referencia inicial, cada trabajo podrá requerir entre 50 MB y 150 MB de RAM durante la compilación, aproximadamente 1 vCPU y entre 100 KB y 500 KB de almacenamiento temporal. Estos valores deberán convertirse en límites del sandbox y validarse durante la implementación.

### RNF-010 — Datos temporales y limpieza

El código, binario, entrada y resultados se almacenarán únicamente de forma temporal en memoria o almacenamiento efímero. Al cerrar o abandonar la página, los datos deberán eliminarse; el backend también debe aplicar una expiración de seguridad cuando no pueda detectar el cierre.

### RNF-011 — Límites de comunicación

La solución deberá considerar como referencia entre 15 KB y 30 KB de tráfico por ejecución, una carga inicial aproximada de 1.5 MB y un límite máximo de 100 KB para la salida de la terminal.
