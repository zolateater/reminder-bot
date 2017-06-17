from abc import ABC, abstractmethod
import pika
from .config import Config, ConfigFactory

# This class allows us to encapsulate what message queue we are using
class QueueConnection(ABC):
    @abstractmethod
    def set_handler(self, callback: callable) -> None:
        pass

    @abstractmethod
    def push_message(self, message: bytearray) -> None:
        pass

    @abstractmethod
    def start_listening(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

# Specific RabbitMQ implementation of Queue
class RabbitConnection(QueueConnection):
    def __init__(self, queue_name: str, host: str, port: int):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)

    def set_handler(self, callback: callable):

        def callback_wrapper(ch, method, properties, body):
            callback(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(callback_wrapper, queue=self.queue_name)

    def start_listening(self):
        self.channel.start_consuming()

    def push_message(self, message: bytearray):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            # make message persistent
            properties=pika.BasicProperties(delivery_mode=2, )
        )

    def close(self):
        self.connection.close()

# Allows to construct a queue easily
class QueueFactory():
    @staticmethod
    def queue_from_config(queue_name: str, config: Config) -> QueueConnection:
        return RabbitConnection(
            queue_name=queue_name,
            host=config.get(Config.RABBITMQ_HOST),
            port=int(config.get(Config.RABBITMQ_PORT))
        )