# Decisiones

## ADR-001: repositorio independiente

El compilador se desarrollará en un repositorio nuevo y privado, separado de proyectos existentes para evitar mezclar dominios, dependencias y documentación.

## ADR-002: alcance del MVP

La primera versión tendrá una sola pantalla con dos apartados claramente identificados: un editor de código C++ y una terminal de resultados. No se incluirán inicialmente cuentas, colaboración, múltiples archivos ni persistencia de proyectos.

## ADR-003: ejecución segura como requisito de diseño

El código enviado por el usuario se tratará como no confiable. La compilación y ejecución deberán ocurrir en un entorno aislado, con límites de tiempo, memoria, CPU, procesos y salida; nunca directamente en el proceso principal de la aplicación.
