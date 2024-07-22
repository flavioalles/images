import logging


def setup_logger() -> None:
    """
    Set up the logger configuration.

    This function creates a logger object, sets the log level to INFO,
    creates a console handler, sets the log level for the handler to INFO,
    creates a formatter, adds the formatter to the handler, and adds the
    handler to the logger.

    Returns:
        None
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
