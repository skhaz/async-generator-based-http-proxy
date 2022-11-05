import pytest

from app.helpers import as_int_or_zero


def test_as_int_or_zero():
    assert as_int_or_zero(None) == 0  # nosec B101
    assert as_int_or_zero(0) == 0  # nosec B101
    assert as_int_or_zero(2**10) == 1024  # nosec B101


def test_as_int_or_zero_typeerror_on_invalid_default():
    with pytest.raises(TypeError):
        as_int_or_zero(0, "abc")
