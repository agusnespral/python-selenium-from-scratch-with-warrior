from functools import wraps
from src.helpers.logger_helper import LoggerHelper


def log_step(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger = LoggerHelper.get_instance()
        logger.info(f"🔹 Executing step: {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper
