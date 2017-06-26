import dotenv
import os


class Config():
    """
    This class encapsulates how we store config settings
    Below are constants from .env file
    """
    API_TOKEN = 'API_TOKEN'
    RABBITMQ_HOST = 'RABBITMQ_HOST'
    RABBITMQ_PORT = 'RABBITMQ_PORT'
    RABBITMQ_QUEUE_UPDATES = 'RABBITMQ_QUEUE_UPDATES'
    RABBITMQ_QUEUE_MESSAGES = 'RABBITMQ_QUEUE_MESSAGES'
    DB_DRIVER = 'DB_DRIVER'
    DB_HOST = 'DB_HOST'
    DB_PORT = 'DB_PORT'
    DB_USER = 'DB_USER'
    DB_PASSWORD = 'DB_PASSWORD'
    DB_DATABASE = 'DB_DATABASE'
    LOG_LEVEL = "LOG_LEVEL"

    def __init__(self, file_name: str):
        dotenv.load_dotenv(file_name)

    def get(self, key: str) -> str:
        return os.environ.get(key)

# This class allows us to build config easily
class ConfigFactory():
    # Path to .env from current file
    DEFAULT_PATH = "../../.env"

    @classmethod
    def get_default(cls) -> Config:
        """
        returns Config which is constructed from DEFAULT_PATH
        :return Config:
        """
        file_path = os.path.dirname(__file__)
        config_path = os.path.join(file_path, ConfigFactory.DEFAULT_PATH)

        return Config(config_path)