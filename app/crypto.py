import uuid

import arrow
import jwt
from typeguard import typechecked


@typechecked
def generate_token(user: str, secret: str) -> bytes:
    now = arrow.utcnow()

    payload = {"user": user, "date": str(now)}

    headers = {"iat": now.int_timestamp, "jti": uuid.uuid4().hex}

    return jwt.encode(
        payload=payload,
        headers=headers,
        key=secret,
        algorithm="HS512",
    ).encode()
