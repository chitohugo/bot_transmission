import logging


class Logger:
    loggers = {}

    def __new__(cls, logger_name, level=logging.DEBUG):
        if logger_name in cls.loggers:
            return cls.loggers[logger_name]

        instance = super(Logger, cls).__new__(cls)
        cls.loggers[logger_name] = instance

        instance.logger = logging.getLogger(logger_name)
        instance.logger.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        if not instance.logger.hasHandlers():
            instance.logger.addHandler(console_handler)

        return instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

logger = Logger('BotTransmission', level=logging.INFO)

