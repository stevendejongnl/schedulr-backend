import logging
from typing import Any

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s"
)


def log_info(message: str, *args: Any, **kwargs: Any) -> None:
    logging.info(message, *args, **kwargs)


def log_error(message: str, *args: Any, **kwargs: Any) -> None:
    logging.error(message, *args, **kwargs)
