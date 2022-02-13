from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    ERROR = 3


class Logger:
    def __init__(self, log_level: LogLevel):
        self.log_level = log_level

    def debug(self, msg: str) -> None:
        self.log(msg, LogLevel.DEBUG)

    def info(self, msg: str) -> None:
        self.log(msg, LogLevel.INFO)

    def error(self, msg: str) -> None:
        self.log(msg, LogLevel.ERROR)

    def log(self, msg: str, log_level: LogLevel) -> None:
        if log_level.value >= self.log_level.value:
            print(msg)

    def is_debug_enabled(self) -> bool:
        return self.log_level.value <= LogLevel.DEBUG.value
