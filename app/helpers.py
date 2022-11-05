import typing as t


def as_int_or_zero(value: t.Optional[t.Any], default: int = 0) -> int:
    value = t.cast(int, value)

    if not isinstance(default, int):
        raise TypeError("Default value must be of integer type")

    try:
        return int(value)
    except (TypeError, ValueError):
        return default
