# Catálogo inicial de requisitos

Este documento contiene hipótesis iniciales. Ningún requisito queda aprobado hasta completar el proceso de validación.

## Requisitos funcionales

### RF-001 — Editar código C++

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema debe permitir escribir o pegar código C++ en el apartado IDE.
- **Criterio:** Dado que el usuario está en la pantalla principal, cuando escriba código en el editor, entonces el contenido debe permanecer visible y editable.
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
- **Descripción:** el apartado terminal debe mostrar la salida del programa o los errores de compilación.
- **Criterio:** Dado que finalizó el trabajo, cuando haya salida o error, entonces la terminal debe mostrar el resultado diferenciando estado exitoso y fallido.
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
- **Criterio:** Dado que el usuario tiene código en el editor, cuando seleccione una de las tres versiones soportadas y ejecute, entonces el trabajo debe usar esa versión del estándar.
- **Estado:** propuesto.

### RF-006 — Proporcionar entrada estándar

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el usuario debe poder proporcionar datos de entrada estándar para programas que utilicen `cin`.
- **Criterio:** Dado que el programa lee entrada estándar, cuando el usuario proporcione datos y ejecute, entonces el proceso debe recibirlos y la terminal debe mostrar el resultado.
- **Estado:** propuesto.

### RF-007 — Eliminar la sesión volátil

- **Actor:** usuario.
- **Prioridad:** Must.
- **Descripción:** el sistema no debe conservar código ni resultados después del cierre de la página o de la expiración de la sesión.
- **Criterio:** Dado que existe una sesión activa, cuando el usuario cierre la página, entonces el sistema debe invalidar la sesión y eliminar los datos temporales asociados dentro del plazo definido.
- **Estado:** propuesto; requiere definir detección de cierre y plazo de limpieza.

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

La ejecución de cada programa debe finalizar, ser cancelada o marcarse como excedida al alcanzar cinco minutos. El tiempo máximo de compilación y las excepciones deberán definirse con la infraestructura.

### RNF-007 — Infraestructura inicial

El despliegue inicial se evaluará sobre Oracle Cloud, priorizando servicios gratuitos o de costo cero compatibles con el presupuesto del proyecto.
