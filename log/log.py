import os
import sys
import logging
import logging.config

from .handlers import MultiProcessSafeHandler

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PATH, 'logfiles')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


FORMAT = '%(asctime)s [%(ip)s] [%(username)s] [%(levelname)s] [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] - %(message)s'
DEFAULT_IP = '0.0.0.0'
DEFAULT_USERNAME = 'USERNAME'


class RequestLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        if 'extra' not in kwargs:
            kwargs["extra"] = self.extra
        return msg, kwargs


def init_stream_handler():
    fmt = logging.Formatter(FORMAT)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(fmt)

    return handler


def init_file_handler():
    fmt = logging.Formatter(FORMAT)
    handler = MultiProcessSafeHandler(
        filename=os.path.join(LOG_DIR, 'general'),
        when='midnight',
        backupCount=20,
        encoding='utf-8'
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(fmt)

    return handler


def get_logger(name='', db=False):
    init_logger = logging.getLogger(name)
    init_logger.addHandler(init_stream_handler())
    init_logger.addHandler(init_file_handler())
    init_logger.setLevel(logging.DEBUG)

    extra_dict = {"ip": DEFAULT_IP, "username": DEFAULT_USERNAME}
    return RequestLoggerAdapter(init_logger, extra=extra_dict)
