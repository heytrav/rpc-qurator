# main qurator module
import os
import logging
import logging.config
from logging import LoggerAdapter

from .settings import LOGGING_CONFIG, DEPLOY_ENVIRONMENT


def get_logger(name=None, config=None):
    """Top level logger initialiser thingy.

    :name: str identifying logger
    :returns: logging logger object

    """
    if config is not None and name is not None:
        LOGGING_CONFIG['loggers'][name] = config
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)
    adapter = LoggerAdapter(logger, {"deploy_environment": DEPLOY_ENVIRONMENT})
    adapter.debug(
        "Just created logger with config {!r}".format(LOGGING_CONFIG))
    adapter.debug("Environment: %s" % os.environ.get('QURATOR_SETTINGS_DIR'))
    return adapter