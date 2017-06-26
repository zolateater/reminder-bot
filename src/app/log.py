import os
import logging
from app.config import ConfigFactory, Config

class LogFactory():

    FILE_PATH = "../../log/bot.log"
    LOG_NAME = "Application"

    @classmethod
    def from_config(cls) -> logging.Logger:
        """
        Создает Logger из конфигурационного файла.
        :return:
        """
        config = ConfigFactory.get_default()
        file_path = os.path.dirname(__file__)
        log_path = os.path.join(file_path, cls.FILE_PATH)

        logger = logging.getLogger(cls.LOG_NAME)
        logger.setLevel(int(config.get(Config.LOG_LEVEL)))

        # create file handler and set level to .env
        file_handler = logging.FileHandler(log_path)

        # create formatter
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s', datefmt="%y.%m.%d %H:%M:%S")

        # add formatter to ch
        file_handler.setFormatter(formatter)

        # add file to logger
        logger.addHandler(file_handler)

        return logger


