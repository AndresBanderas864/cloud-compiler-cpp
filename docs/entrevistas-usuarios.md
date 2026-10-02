# Entrevistas con usuarios

## Objetivo

Validar el problema, el flujo esperado y las prioridades de Cloud Compiler C++ sin presentar la solución como una respuesta ya decidida.

## Muestra recomendada

Realizar entre 5 y 8 entrevistas de 15 a 20 minutos:

- 2 o 3 personas que estén aprendiendo C++.
- 2 o 3 personas con experiencia básica en C++.
- 1 o 2 personas que hayan usado un compilador en línea.

No se deben registrar nombres completos ni código personal. Usar un identificador como `U-01`.

## Guion

### Apertura

> Estamos investigando cómo las personas escriben, compilan y ejecutan C++. No estamos evaluando tus conocimientos. La entrevista durará aproximadamente 20 minutos. ¿Aceptas que tomemos notas sin registrar datos personales?

### Contexto actual

1. ¿Para qué utilizas C++ actualmente?
2. ¿Cuándo fue la última vez que compilaste un programa de C++?
3. ¿Qué herramienta utilizaste?
4. ¿Qué fue lo más difícil o lento del proceso?
5. ¿Qué haces normalmente cuando aparece un error de compilación?

### Flujo deseado

6. Si pudieras abrir una página y ejecutar C++ sin instalar nada, ¿qué programa probarías primero?
7. ¿Qué información esperas ver mientras el programa compila y ejecuta?
8. ¿Qué tan importante es ver los errores completos del compilador?
9. ¿Usas programas que solicitan datos mediante `cin`? ¿Cómo preferirías introducir esos datos?
10. ¿Necesitas enviar datos mientras el programa está ejecutándose o te basta con escribirlos antes?
11. ¿Qué versiones del estándar C++ utilizas o reconoces: C++17, C++20 o C++23?

### Restricciones y confianza

12. ¿Cuánto tiempo esperarías antes de considerar que una ejecución falló?
13. ¿Te parece aceptable que el código desaparezca al cerrar la página?
14. ¿Qué mensaje debería aparecer si el servicio está ocupado?
15. ¿Qué controles necesitas para usar la pantalla con teclado o en un dispositivo pequeño?

### Cierre

16. ¿Qué función sería imprescindible para que usaras la herramienta?
17. ¿Qué función no incluirías en una primera versión?
18. ¿Hay algo importante que no te haya preguntado?

## Hoja de respuestas

| Campo | Registro |
|---|---|
| Identificador | `U-__` |
| Perfil | principiante / básico / usuario de compilador web |
| Fecha | AAAA-MM-DD |
| Hallazgos principales | |
| Problemas repetidos | |
| Necesidades nuevas | |
| Requisitos afectados | RF/RNF-___ |
| Evidencia textual breve | |
| Decisión | propuesto / validado / rechazado / diferido |

## Reglas de análisis

- Separar hechos observados de opiniones del entrevistador.
- No convertir una preferencia aislada en requisito obligatorio.
- Considerar repetido un hallazgo cuando aparezca en al menos dos entrevistas o cuando represente un riesgo de seguridad o accesibilidad.
- Actualizar el catálogo solo después de revisar las respuestas.

## Registro completado: U-PO-01

| Campo | Registro |
|---|---|
| Identificador | `U-PO-01` |
| Perfil | Usuario principiante y avanzado; conoce bien C++ |
| Fecha | 2026-10-01 |
| Hallazgos principales | Necesita copiar código de clase y ejecutarlo rápidamente desde la web, sin usar el compilador de los computadores de la universidad. |
| Problemas repetidos | Instalación o uso de compiladores locales en equipos universitarios. |
| Necesidades nuevas | Selector de C++17/C++20/C++23 modificable, terminal interactiva para `cin`, editor sencillo con numeración y Hola Mundo, errores simplificados con identificador. |
| Requisitos afectados | RF-001, RF-003, RF-005, RF-008, RNF-006, RNF-011 |
| Evidencia textual breve | “Quiero copiar el código que hice en clase y ejecutarlo rápidamente en una web”. |
| Decisión | validado por responsable del producto; revisión técnica ejecutada mediante pruebas AWS; pendiente de aprobación formal de QA |
