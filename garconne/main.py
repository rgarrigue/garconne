import sys

import typer
from loguru import logger

app = typer.Typer()


def main(redis_host: str = localhost, redis_port: int = 6379):
    # Loguru settings
    # We can't configure the default logger easily, hence removing it
    logger.remove(0)
    # And replacing with a properly configured one
    logger.add(sys.stdout, colorize=True)


if __name__ == "__main__":
    app()
