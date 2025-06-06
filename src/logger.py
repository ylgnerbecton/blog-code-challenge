import logging
from enum import Enum

from src.application.utils.general import get_current_time
from src.settings import settings


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class Logger:
    def __init__(self):
        self._internal_logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)
        self.log_level_map = {
            LogLevel.INFO: self._internal_logger.info,
            LogLevel.ERROR: self._internal_logger.error,
            LogLevel.WARNING: self._internal_logger.warning,
            LogLevel.DEBUG: self._internal_logger.debug,
        }

    def log(self, level, context=None, message=None):
        timestamp_utc = get_current_time().isoformat()
        log_message = {
            "timestamp": timestamp_utc,
            "level": level.value,
            "context": context,
            "message": message,
            "service_name": settings.PROJECT_NAME,
        }
        log_function = self.log_level_map.get(level, self._internal_logger.info)
        log_function(log_message)

    def info(self, context=None, message=None):
        self.log(LogLevel.INFO, context, message)

    def warning(self, context=None, message=None):
        self.log(LogLevel.WARNING, context, message)

    def error(self, context=None, message=None):
        self.log(LogLevel.ERROR, context, message)

    def debug(self, context=None, message=None):
        self.log(LogLevel.DEBUG, context, message)


logger = Logger()
