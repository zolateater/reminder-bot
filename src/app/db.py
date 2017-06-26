from app.config import Config, ConfigFactory
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

class DBConnectionFactory():
    """
    Factory for creating DB connection and connection strings.
    """
    @staticmethod
    def format_connection_string(driver: str, host: str, port: str, user: str, password: str, database: str) -> str:
        return "{}://{}:{}@{}:{}/{}".format(driver, user, password, host, port, database)

    @classmethod
    def connection_string_from_config(cls) -> str:
        """
        Returns connections string for DB engine.
        Parameters are taken from the .env file.
        :return:
        """
        config = ConfigFactory.get_default()
        return cls.format_connection_string(
            config.get(Config.DB_DRIVER),
            config.get(Config.DB_HOST),
            config.get(Config.DB_PORT),
            config.get(Config.DB_USER),
            config.get(Config.DB_PASSWORD),
            config.get(Config.DB_DATABASE)
        )

    @classmethod
    def get_session(cls):
        """
        Get Session instance from engine created from config.
        :return:
        """
        engine = create_engine(cls.connection_string_from_config())
        return sessionmaker(engine)