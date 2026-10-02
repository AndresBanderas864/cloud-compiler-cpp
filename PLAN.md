# Plan del proyecto

## Fases

1. [En progreso] Levantar, validar y priorizar requisitos.
2. [Completada] Diseñar la arquitectura PaaS y el contrato de ejecución segura.
3. [Completada] Construir un MVP con editor y terminal en una misma pantalla.
4. [En progreso] Probar accesibilidad, responsive, seguridad y comportamiento funcional.
5. [Completada] Desplegar temporalmente el MVP en AWS y documentar operación, verificación y limpieza.

## Alcance inicial

El MVP permitirá escribir código C++, elegir C++17, C++20 o C++23, proporcionar entrada estándar cuando sea necesario, solicitar su compilación y visualizar la salida o los errores en una interfaz con dos apartados: IDE y terminal. No requerirá autenticación ni guardará proyectos.

## Estado de la entrega

La integración AWS está verificada con ECS Fargate en `us-east-2`. El entorno de evaluación es temporal y debe eliminarse después de la revisión para evitar costes.
