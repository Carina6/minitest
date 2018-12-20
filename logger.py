import logging


def init_logging():
    logger = logging.getLogger("minitest")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


init_logging()


def get_logger(name):
    logger = logging.getLogger(name)
    return logger
