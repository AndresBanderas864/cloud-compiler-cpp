"""Validación de solicitudes antes de crear un sandbox."""

from dataclasses import dataclass


SUPPORTED_STANDARDS = {"c++17", "c++20", "c++23"}
MAX_CODE_BYTES = 100 * 1024
MAX_OUTPUT_BYTES = 100 * 1024
MAX_CONCURRENT_USERS = 10
MAX_RUNTIME_SECONDS = 300


@dataclass(frozen=True)
class RunRequest:
    code: str
    standard: str


class ValidationError(ValueError):
    """Error de entrada que puede mostrarse al usuario."""

    def __init__(self, error_id: str, message: str) -> None:
        super().__init__(message)
        self.error_id = error_id
        self.message = message


def validate_run_request(code: str, standard: str) -> RunRequest:
    if not isinstance(code, str) or not code.strip():
        raise ValidationError("CC-001", "Escribe código C++ antes de ejecutar.")
    if len(code.encode("utf-8")) > MAX_CODE_BYTES:
        raise ValidationError("CC-002", "El código supera el límite de 100 KB.")
    if standard not in SUPPORTED_STANDARDS:
        raise ValidationError("CC-003", "La versión de C++ seleccionada no está disponible.")
    return RunRequest(code=code, standard=standard)
