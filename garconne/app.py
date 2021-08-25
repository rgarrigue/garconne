import base64
import os
import sys

import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from loguru import logger
from pydantic import AnyUrl
from pydantic.tools import parse_obj_as
from starlette_exporter import (PrometheusMiddleware,  # type: ignore
                                handle_metrics)

# App creation
app = FastAPI()
# Add prometheus /metrics endpoint
app.add_middleware(PrometheusMiddleware, app_name="garconne", prefix="garconne", group_paths=True)
app.add_route("/metrics", handle_metrics)

# Backend connection
backend = redis.Redis(host=redis_host, port=redis_port)


async def backend_get(key: str) -> str:
    """Get the value matching the key from the backend, formatted as a UTF-8 string.
    Or an empty string if the key doesn't exist."""
    result = backend.get(key)
    if result is not None:
        value = result.decode("utf-8")
    else:
        value = ""
    logger.debug(f"Backend get {key} = {value}")
    return value


async def backend_set(key: str, value: str) -> bool:
    """Convert the value to an UTF-8 string and set it to the given key in the backend."""
    logger.debug(f"Backend set {key} = {value}")
    result = backend.set(key, str(value).encode("utf-8"))
    if result is None:
        result = False
    return result


async def generate_id() -> str:
    """
    Generate a random ID, making sure it doesn't already exist in Redis.
    """
    try:
        id: str = ""
        value: str = "enter_the_while"
        while value != "":
            id = base64.urlsafe_b64encode(os.urandom(32))[:6].decode("utf-8")
            logger.debug(f"Generated ID {id}")
            value = await backend_get(id)
            if value != "":
                logger.warning(f"Generated ID {id} already exists in Redis, trying again")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return id


@app.head("/health")
@app.get("/health")
@app.head("/ping")
@app.get("/ping")
@app.head("/status")
@app.get("/status")
async def health() -> bool:
    """
    Healthcheck endpoint.
    """
    if not backend.ping():
        raise HTTPException(status_code=500, detail="Couldn't ping Redis")
        return False
    return True


@app.post("/api/v1/shorten/{url:path}", response_class=PlainTextResponse, status_code=200)
async def shorten(url: str) -> str:
    """
    URL shortening endpoint.
    """
    # Validate the URL https://pydantic-docs.helpmanual.io/usage/types/#urls
    try:
        parse_obj_as(AnyUrl, url)
    except Exception:
        raise HTTPException(status_code=400, detail=f"URL {url} isn't valid")

    id = await generate_id()
    await backend_set(id, url)
    return id


@app.get("/api/v1/lookup/{id}", response_class=PlainTextResponse)
async def lookup(id: str) -> str:
    """
    Lookup endpoint. Get the initial URL given it's shortened ID.
    """
    url = await backend_get(id)
    if url == "":
        logger.warning(f"ID {id} coudln't be found in Redis")
        raise HTTPException(status_code=404, detail=f"ID {id} not found")

    return url


@app.get("/{id}")
async def redirect(id: str) -> RedirectResponse:
    """
    Shortened URL endpoint. Redirect to the initial URL.
    """
    url = await backend_get(id)
    logger.debug(f"Redirecting ID {id} to {url}")
    return RedirectResponse(url=url)


@app.get("/", response_class=HTMLResponse)
async def empty() -> str:
    """
    Empty homepage to avoid the ugly error message.
    """
    return ""


def main(redis_host: str = localhost, redis_port: int = 6379):
    # Loguru settings. We can't configure the default logger easily, hence replacing it
    logger.remove(0)
    logger.add(sys.stdout, colorize=True)

    # Redis connection
    backend = redis.Redis(host=redis_host, port=redis_port)

    # App creation
    app = FastAPI()
    # Add prometheus /metrics endpoint
    app.add_middleware(PrometheusMiddleware, app_name="garconne", prefix="garconne", group_paths=True)
    app.add_route("/metrics", handle_metrics)


if __name__ == "__main__":
    cli()
