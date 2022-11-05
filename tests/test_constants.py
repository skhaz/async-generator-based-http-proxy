from app import constants


def test_counter_key():
    assert constants.COUNTER_KEY == "counter"  # nosec B101


def test_uptime_key():
    assert constants.UPTIME_KEY == "uptime"  # nosec B101


def test_number_of_constants():
    n = len([c for c in dir(constants) if not c.startswith("__")])

    assert n == 2  # nosec B101
