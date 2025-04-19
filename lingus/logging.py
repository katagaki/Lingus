from logging import basicConfig, getLogger, Logger, StreamHandler, Formatter, DEBUG
from os import environ
from sys import stdout


def configure_docling_logging():
    # Enable PyTorch logging
    environ["TORCH_CPP_LOG_LEVEL"] = "INFO"
    environ["TORCH_SHOW_CPP_STACKTRACES"] = "1"
    environ["TRANSFORMERS_VERBOSITY"] = "debug"

    basicConfig(
        level=DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Enable log output for Docling and Torch loggers
    logger_names: list[str] = [
        "docling",
        "docling.pipeline",
        "docling.pdf",
        "docling.ocr",
        "docling.structure",
        "docling.image",
        "docling.tables",
        "docling.doc",
        "docling.markdown",
        "torch",
        "transformers"
    ]

    for logger_name in logger_names:
        logger: Logger = getLogger(logger_name)
        logger.setLevel(DEBUG)
        if not logger.hasHandlers():
            handler = StreamHandler(stream=stdout)
            handler.setFormatter(Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ))
            logger.addHandler(handler)
