# Validación del alcance del MVP

Este taller corresponde al paso de validar y aprobar el alcance después de las entrevistas. El prototipo y el despliegue temporal ya permiten revisar el flujo real; la aprobación final de producto y QA sigue siendo una actividad pendiente.

## Objetivo

Confirmar que el MVP sea suficientemente pequeño para la tarea y que cubra el flujo principal: escribir código, compilar, ejecutar y observar resultados.

## Participantes

- Responsable del producto.
- Responsable técnico.
- Una persona que esté aprendiendo C++.
- Una persona que ya haya utilizado un compilador.

## Dinámica de 30 minutos

1. Presentar el problema en dos minutos, sin mostrar una solución terminada.
2. Revisar el flujo: editor, selección de estándar, entrada estándar, ejecución y terminal.
3. Clasificar cada función usando Must, Should, Could o Won't.
4. Revisar riesgos de seguridad, privacidad, capacidad y accesibilidad.
5. Resolver preguntas pendientes o registrarlas como decisiones diferidas.
6. Aprobar o rechazar la línea base provisional.

## Preguntas de validación

1. ¿El editor y la terminal son suficientes para la primera pantalla?
2. ¿C++17, C++20 y C++23 son necesarios en el MVP?
3. ¿La entrada de `cin` durante la ejecución es imprescindible?
4. ¿Cinco usuarios normalmente y diez como máximo representan el alcance esperado?
5. ¿Es aceptable rechazar una solicitud cuando se alcance la capacidad máxima, sin cola?
6. ¿Es aceptable perder código y resultados al cerrar o abandonar la página?
7. ¿Qué límite de salida evita bloquear la interfaz o consumir recursos?
8. ¿Qué debe ver el usuario cuando una ejecución exceda cinco minutos?

## Lista de aprobación

- [x] El problema está descrito con evidencia de la entrevista del responsable del producto.
- [x] Los actores y escenarios principales están identificados.
- [ ] Cada requisito tiene criterio de aceptación; falta completar los requisitos no funcionales.
- [x] El alcance no incluye persistencia, cuentas ni colaboración.
- [x] La ejecución aislada y los límites de recursos son obligatorios.
- [x] Se definió qué ocurre al alcanzar diez usuarios simultáneos.
- [x] Se definió el comportamiento ante cierre de página.
- [x] Se registraron requisitos fuera del MVP.
- [ ] Producto, técnica y QA aprobaron la línea base; falta la aprobación formal de producto y QA.

## Acta

| Campo | Registro |
|---|---|
| Fecha | 2026-10-01 |
| Participantes | Responsable del producto |
| Decisión | aprobado con cambios |
| Cambios acordados | Editor sencillo con Hola Mundo y numeración; selección C++17/C++20/C++23; terminal interactiva; límite de salida de 100 KB; mensajes de error simplificados con identificador. |
| Requisitos afectados | RF-001, RF-003, RF-005, RF-008, RNF-006, RNF-011 |
| Próxima revisión | Después de la evaluación del despliegue AWS y la revisión formal de QA |
