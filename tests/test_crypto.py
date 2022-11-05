import uuid
from unittest.mock import patch

from freezegun import freeze_time

from app.crypto import generate_token


@freeze_time("2022-01-01")
@patch.object(uuid, "uuid4")
def test_generate_token(patched_uuid):
    patched_uuid.return_value.hex = "42"
    actual = generate_token("username", "supersecret")
    expected = b"eyJhbGciOiJIUzUxMiIsImlhdCI6MTY0MDk5NTIwMCwianRpIjoiNDIiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyIjoidXNlcm5hbWUiLCJkYXRlIjoiMjAyMi0wMS0wMVQwMDowMDowMCswMDowMCJ9.7UCIpyDpkMTAQdFFrUWMdktLKrLY_VmgiO3voNX1g_lgErf6cXLziv_52VkDbEElAbtgyAHB1jl5fgfkNoI-rQ"  # noqa

    assert actual == expected  # nosec B101
