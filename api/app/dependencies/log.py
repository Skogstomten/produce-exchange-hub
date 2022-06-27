"""Dependencies for logging"""
import functools
from abc import ABCMeta
from logging import DEBUG, StreamHandler, getLogger, Formatter, Handler
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Callable

LOG_LEVEL = DEBUG
LOG_FILE_PATH = "C:/logs/produce_exchange_hub.log"
# SLA_LOG_FILE_PATH = "C:/logs/produce_exchange_hub.sla.log"

DEFAULT_FORMATTER = Formatter("%(asctime)s|%(levelname)s|%(threadName)s|%(name)s|%(message)s")
# SLA_FORMATTER = Formatter("%(asctime)s|%(levelname)s|%(threadName)s|%(name)s|%(message)s")


@functools.lru_cache(None)
def get_file_handler() -> Handler | None:
    """Injection method for file handler for logger."""
    try:
        file_handler = TimedRotatingFileHandler(LOG_FILE_PATH, "midnight", 1, 5, "utf8", False, True)
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(DEFAULT_FORMATTER)
        return file_handler
    except Exception as err:
        print(f"Failed to create logging file handler: {str(err)}")
    return None


@functools.lru_cache(None)
def get_console_handler() -> Handler | None:
    """Injection method for console handler for logger."""
    try:
        console_handler = StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_handler.setFormatter(DEFAULT_FORMATTER)
        return console_handler
    except Exception as err:
        print(f"Failed to create logging console handler: {str(err)}")
    return None


# sla_handler = TimedRotatingFileHandler(SLA_LOG_FILE_PATH, "midnight", 1, 5, "utf8", False, True)
# sla_handler.setLevel(LOG_LEVEL)
# sla_handler.setFormatter(SLA_FORMATTER)


def _log(log_function: Callable, message: Any, exception: Exception = None) -> None:
    """Wraps the log function."""
    log_function(str(message), exc_info=exception)


class BaseLogger(metaclass=ABCMeta):
    """
    Wrapps python logger.

    A wrapper is being used because we want to provide a cleaner interface with better type checking for calls.
    """

    def __init__(self, logger_name: str, log_level: int, handlers: list[Handler]):
        self.logger = getLogger(logger_name)
        self.logger.setLevel(log_level)
        for handler in (h for h in handlers if h is not None):
            self.logger.addHandler(handler)

    def debug(self, message: Any, exception: Exception = None) -> None:
        """
        Logs message and exception information if any.

        :param message: Message can be of any type but will be converted to str using the str constructor.
        :param exception: Exception raised.
        :return: None.
        """
        _log(self.logger.debug, message, exception)

    def info(self, message: Any, exception: Exception = None) -> None:
        """Logs info level log."""
        _log(self.logger.info, message, exception)

    def warn(self, message: Any, exception: Exception = None) -> None:
        """Logs warning level message."""
        _log(self.logger.warning, message, exception)

    def error(self, message: Any, exception: Exception = None) -> None:
        """Logs error level message."""
        _log(self.logger.error, message, exception)


class AppLogger(BaseLogger):
    """Standard logger for logging debug, info, warning and error information"""

    def __init__(self, logger_name: str):
        super().__init__(logger_name, LOG_LEVEL, [get_console_handler(), get_file_handler()])


# class SLALogger(BaseLogger):
#     """Used for logging to SLA log"""
#
#     def __init__(self):
#         super().__init__("sla", LOG_LEVEL, [sla_handler])
#
#     def log_sla(
#         self,
#         call_start_time: datetime,
#         call_end_time: datetime,
#         request: Request,
#         response: Response | None = None,
#         exception: BaseException | None = None,
#     ) -> None:
#         """Logs call to sla log."""
#         time_delta = call_end_time - call_start_time
#         call_status = "OK" if exception is None else "FAILED"
#         http_status = response.status_code if response is not None else "NoResponse"
#         detail = "None"
#         if response is not None:
#             if not is_successfull(response.status_code):
#                 if response.body is not None:
#                     pass
#
#         message = f"{get_url(request)}"
#         message += f"|{time_delta.microseconds}"
#         message += f"|{call_start_time.strftime(DATE_FORMAT)}"
#         message += f"|{call_end_time.strftime(DATE_FORMAT)}"
#         message += f"|{call_status}"
#         message += f"|{http_status}"
#         message += f"|{detail}"
#
#         _log(self.logger.info, message)


class AppLoggerInjector:
    """
    Injector for AppLogger class.

    >>> injector = AppLoggerInjector("my_logger")
    >>> logger: AppLogger = injector()
    >>> isinstance(logger, AppLogger)
    True

    """

    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def __call__(self) -> AppLogger:
        return AppLogger(self.logger_name)
