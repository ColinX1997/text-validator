import logging, os
from logging.handlers import RotatingFileHandler


class LoggerManager:
    _loggers = {}

    @classmethod
    def get_logger(cls, name, level=logging.INFO, log_dir="logs"):
        if name not in cls._loggers:
            log_file = os.path.join(log_dir, f"{name}.log")
            cls._loggers[name] = cls.setup_logger(name, log_file, level)

        return cls._loggers[name]

    @staticmethod
    def setup_logger(name, log_file, level):
        """Set up the logger with a rotating file handler."""
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=5)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger
