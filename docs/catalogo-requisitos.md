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

## Requisitos no funcionales iniciales

### RNF-001 — Aislamiento de ejecución

El código del usuario debe ejecutarse en un entorno aislado, sin acceso innecesario a la red, al host ni a secretos del servicio.

### RNF-002 — Límites de recursos

Cada trabajo debe tener límites configurables de tiempo, memoria, CPU, procesos y tamaño de salida.

### RNF-003 — Accesibilidad y responsive

Los controles deben ser operables con teclado, tener nombres accesibles y mantener editor y terminal utilizables en pantallas pequeñas.

### RNF-004 — Trazabilidad

Cada requisito aprobado debe enlazar con al menos un criterio de aceptación y una prueba.
