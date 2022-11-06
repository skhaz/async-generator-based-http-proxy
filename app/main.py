import asyncio
import os

import arrow
from httpx import AsyncClient
from redis import asyncio as aioredis
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.responses import StreamingResponse

from app.constants import ALLOWED_METHODS
from app.constants import COUNTER_KEY
from app.constants import UPTIME_KEY
from app.crypto import generate_token
from app.helpers import as_int_or_zero

app = Starlette()

http = AsyncClient(base_url=os.environ["UPSTREAM_URL"])

redis = aioredis.from_url(os.environ["REDIS_DSN"], decode_responses=True)


@app.on_event("startup")
async def startup():
    await redis.set(UPTIME_KEY, str(arrow.utcnow()))


@app.on_event("shutdown")
async def shutdown():
    await asyncio.gather(redis.close(), http.aclose())


@app.route("/status")
async def status(_: Request) -> Response:
    counter, uptime = await asyncio.gather(
        redis.get(COUNTER_KEY),
        redis.get(UPTIME_KEY),
    )

    return JSONResponse(
        {
            "counter": as_int_or_zero(counter),
            "uptime": (arrow.utcnow() - arrow.get(str(uptime))).seconds,
        }
    )


@app.route("/{path}", methods=ALLOWED_METHODS)
async def proxy(request: Request) -> Response:
    token = generate_token(user="username", secret=os.environ["SECRET"])

    response, _ = await asyncio.gather(
        http.send(
            http.build_request(
                content=request.stream(),
                headers=dict(request.headers.raw) | {b"X-My-Jwt": token},
                method=request.method,
                url=request.url.path,
            ),
            stream=True,
        ),
        redis.incr(COUNTER_KEY),
    )

    return StreamingResponse(
        response.aiter_raw(),
        headers=response.headers,
        status_code=response.status_code,
        background=BackgroundTask(response.aclose),
    )
