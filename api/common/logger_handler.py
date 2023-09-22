import logging, logstash, re


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(
        "\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s"
    )

    console = logging.StreamHandler()
    console.setLeve(logging.INFO)
    console.setFormatter(log_format)
    logger.addHandler(console)

    logger.addHandler(logstash.TCPLogstashHandler("localhost", 5044, version=1))

    return logger
