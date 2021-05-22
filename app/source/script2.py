import source.module


def main():
    logger = source.module.set_logger(__name__, "/app/main.log")

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
