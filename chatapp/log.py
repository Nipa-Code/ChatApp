import logging
from logging import handlers


def setup() -> None:
    format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        handlers=[
            logging.FileHandler("chatapp/api.log", mode="a"),
            logging.StreamHandler(),
        ],
        format=format_string,
        level=logging.INFO,
    )
