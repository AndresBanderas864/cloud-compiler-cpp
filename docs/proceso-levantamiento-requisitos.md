# Proceso de levantamiento de requisitos

## 1. Objetivo

Convertir la idea de Cloud Compiler C++ en requisitos claros, priorizados, verificables y trazables antes de implementar. El proceso seguirá un enfoque iterativo: descubrir, especificar, validar y gestionar cambios.

## 2. Participantes

| Participante | Responsabilidad |
|---|---|
| Usuario principiante | Explicar dificultades al compilar y ejecutar ejemplos pequeños. |
| Usuario con experiencia en C++ | Validar flujo, mensajes de error y expectativas técnicas. |
| Responsable del producto | Priorizar alcance y aceptar la línea base. |
| Responsable técnico | Evaluar viabilidad, arquitectura, seguridad y costos. |
| Responsable de QA | Convertir requisitos en escenarios verificables. |

## 3. Preparación

1. Confirmar el problema: ejecutar C++ rápidamente sin instalar un entorno local.
2. Delimitar el MVP y registrar explícitamente lo que queda fuera.
3. Identificar riesgos: ejecución de código no confiable, consumo de recursos, privacidad y disponibilidad.
4. Preparar guion de entrevista, encuesta breve y escenarios de uso.
5. Mantener cada hallazgo con fuente, fecha y estado: `propuesto`, `validado`, `rechazado` o `diferido`.

## 4. Descubrimiento

### Entrevistas semiestructuradas

Realizar entre 5 y 8 entrevistas de 20 minutos. Preguntar por el último intento de compilar C++, herramientas usadas, tiempo tolerable de espera, información necesaria ante un error y necesidades de accesibilidad.

### Encuesta breve

Consultar frecuencia de uso, sistema operativo, tamaño típico del código, necesidad de entrada estándar y preferencia entre ejecutar automáticamente o bajo demanda.

### Observación de escenarios

Observar tareas como pegar un programa corto, compilar con un error intencional, corregirlo y ejecutar un programa que solicite entrada.

## 5. Especificación

Documentar cada requisito en `catalogo-requisitos.md` usando esta estructura:

- Identificador y título.
- Descripción centrada en el comportamiento observable.
- Actor y prioridad (`Must`, `Should`, `Could`, `Won't`).
- Precondiciones y flujo principal.
- Criterios de aceptación en formato Dado/Cuando/Entonces.
- Dependencias, riesgos y fuente.

Separar requisitos funcionales (`RF`) de no funcionales (`RNF`). Los requisitos de seguridad, accesibilidad, rendimiento y límites de ejecución son obligatorios para el MVP cuando mitiguen un riesgo crítico.

## 6. Priorización

Usar MoSCoW y revisar la prioridad con producto y técnica:

- **Must:** editor, compilación, ejecución aislada y resultados visibles.
- **Should:** cancelar ejecución, limpiar terminal, copiar resultados y mensajes amigables.
- **Could:** temas, guardado temporal y ejemplos iniciales.
- **Won't (MVP):** colaboración en tiempo real, proyectos multiarchivo, autenticación y facturación.

## 7. Validación

1. Revisar ambigüedades, términos no definidos y requisitos duplicados.
2. Confirmar que cada requisito sea necesario, consistente, factible y comprobable.
3. Ejecutar una revisión con usuarios mediante prototipo o recorrido guiado.
4. Crear una matriz de trazabilidad requisito → criterio → prueba.
5. Obtener aprobación de la línea base y registrar cambios posteriores.

## 8. Entregables

- Mapa de actores y escenarios.
- Catálogo de requisitos funcionales y no funcionales.
- Glosario de términos.
- Matriz de riesgos y decisiones.
- Matriz de trazabilidad.
- Acta de validación de la línea base.

## 9. Preguntas pendientes

Las siguientes decisiones ya fueron propuestas para el MVP:

- Soporte para C++17, C++20 y C++23.
- Entrada estándar para programas que utilicen `cin`.
- Tiempo máximo de ejecución de cinco minutos.
- Sesiones sin autenticación y sin persistencia de código.
- Evaluación de Oracle Cloud como proveedor inicial.

### Respuestas registradas

- No hay cuenta de Oracle Cloud actualmente.
- Se elegirá la región disponible más cercana a los usuarios objetivo.
- Se esperan cinco usuarios simultáneos en condiciones normales y hasta diez en el peor caso previsto.
- No habrá cola; las solicitudes adicionales se rechazarán temporalmente.
- Los cinco minutos incluyen compilación y ejecución.
- Se estima entre 50 MB y 150 MB de RAM por compilación, aproximadamente 1 vCPU y entre 100 KB y 500 KB de almacenamiento temporal.
- La entrada estándar podrá enviarse durante la ejecución.
- Si la página se cierra, el código se perderá y no será recuperable.
- Se consideran como referencias entre 15 KB y 30 KB de tráfico por ejecución y una carga inicial aproximada de 1.5 MB.

### Decisiones aún necesarias

1. Definir el límite máximo de salida de la terminal.
2. Definir cuánto tiempo conservará el backend una sesión abandonada antes de limpiarla.
3. Confirmar la región de Oracle Cloud cuando se conozca la ubicación de los usuarios objetivo.
4. Confirmar si cada usuario podrá tener una sola ejecución activa o varias simultáneas.
5. Confirmar los límites exactos de CPU y memoria del sandbox, usando las estimaciones anteriores como punto de partida.
