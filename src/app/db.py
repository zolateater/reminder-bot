from app.config import Config, ConfigFactory

class DBConnection():
    @staticmethod
    def format_connection_string(driver: str, host: str, port: str, user: str, password: str, database: str) -> str:
        return "{}://{}:{}@{}:{}/{}".format(driver, user, password, host, port, database)

    @classmethod
    def connection_string_from_config(cls) -> str:
        config = ConfigFactory.get_default()
        return cls.format_connection_string(
            config.get(Config.DB_DRIVER),
            config.get(Config.DB_HOST),
            config.get(Config.DB_PORT),
            config.get(Config.DB_USER),
            config.get(Config.DB_PASSWORD),
            config.get(Config.DB_DATABASE)
        )