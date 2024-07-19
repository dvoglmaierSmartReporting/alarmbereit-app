from kivy.logger import Logger, KivyFormatter, FileHandler, ConsoleHandler
# from kivy.logger import Logger, KivyFormatter


from inspect import getframeinfo, stack
import logging
from functools import wraps
import os


# class CustomFormatter(logging.Formatter):
class CustomFormatter(KivyFormatter):
    """Custom formatter, overrides funcName with value of name_override if it exists"""

    def format(self, record):
        if hasattr(record, "name_override"):
            record.funcName = record.name_override
        if hasattr(record, "file_override"):
            record.filename = record.file_override
        if hasattr(record, "line_override"):
            record.lineno = record.line_override
        return super(CustomFormatter, self).format(record)


class CustomFileHandler(FileHandler):
    def _write_message(self, record):
        if FileHandler.fd in (None, False):
            return

        msg = self.format(record)
        stream = FileHandler.fd
        fs = "%s\n"
        stream.write('[%-7s] ' % record.levelname)
        stream.write(fs % msg)
        stream.flush()

# setup logger and handler
# logger = logging.getLogger(__file__)
# handler = logging.StreamHandler()
# logger.setLevel(logging.DEBUG)
# handler.setLevel(logging.DEBUG)
handler.setFormatter(
    CustomFormatter(
        # "%(asctime)s - %(filename)s:%(lineno)s - %(funcName)s - %(levelname)s - %(message)s"
        "[%(levelname)-18s] > {%(filename)s:%(lineno)-18s} > [%(funcName)-18s] %(message)s"
    )
)
# logger.addHandler(handler)


def log_and_call(statement):
    def decorator(func):
        caller = getframeinfo(stack()[1][0])

        @wraps(func)
        def wrapper(*args, **kwargs):
            # set name_override to func.__name__
            logger.info(
                statement,
                extra={
                    "name_override": func.__name__,
                    "file_override": os.path.basename(caller.filename),
                    "line_override": caller.lineno,
                },
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


# @log_and_call("This should be logged by 'decorated_function'")
# def decorated_function():  # <- the logging in the wrapped function will point to/log this line for lineno.
#     logger.info("I ran")


# decorated_function()
