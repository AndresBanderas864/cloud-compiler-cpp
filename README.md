# Cloud Compiler C++

PaaS educativo para escribir, compilar y ejecutar programas pequeños de C++ desde la nube.

## Estado

En fase de levantamiento y validación de requisitos.

## Visión del MVP

Una pantalla con dos apartados:

1. **IDE:** editor donde el usuario escribe o pega código C++.
2. **Terminal:** salida del programa, errores de compilación y mensajes de estado.

El servicio debe priorizar una experiencia rápida y comprensible, sin ejecutar código no confiable fuera de un entorno aislado.

## Documentación

- [Proceso de levantamiento de requisitos](docs/proceso-levantamiento-requisitos.md)
- [Guion de entrevistas](docs/entrevistas-usuarios.md)
- [Validación del alcance del MVP](docs/validacion-alcance-mvp.md)
- [Arquitectura técnica del MVP](docs/arquitectura-mvp.md)
- [Catálogo inicial de requisitos](docs/catalogo-requisitos.md)
- [Plan del proyecto](PLAN.md)
- [Decisiones](DECISIONS.md)

## Principios

- Separación de responsabilidades y diseño orientado a SOLID.
- Seguridad por defecto para compilación y ejecución remotas.
- Accesibilidad y diseño responsive desde el MVP.
- Requisitos trazables a criterios de aceptación y pruebas.

## Ejecutar localmente

Requisitos: Python 3.11+, Docker y Docker Compose.

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows PowerShell
pip install -r requirements.txt
docker build -t cloud-compiler-sandbox:latest .
uvicorn app.main:app --reload
```

Abrir `http://localhost:8000`. El backend no ejecuta C++ directamente en Python: cada trabajo se envía al sandbox Docker con red deshabilitada y límites de recursos.

Para ejecutar las pruebas de validación:

```bash
python -m pytest -q
```
