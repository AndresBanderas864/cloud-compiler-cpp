from app.validation import validate_run_request
from app.validation import ValidationError


def test_accepts_supported_standard():
    request = validate_run_request("int main() {}", "c++23")
    assert request.standard == "c++23"


def test_rejects_unsupported_standard():
    try:
        validate_run_request("int main() {}", "c++14")
    except ValidationError as error:
        assert error.error_id == "CC-003"
    else:
        raise AssertionError("Se esperaba un error de validación")


def test_rejects_empty_code():
    try:
        validate_run_request("", "c++17")
    except ValidationError as error:
        assert error.error_id == "CC-001"
    else:
        raise AssertionError("Se esperaba un error de validación")
