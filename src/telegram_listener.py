from app.config import Config, ConfigFactory
from telegram.client import TelegramFactory
import threading
import pika
import json

# TODO: make config
# TODO: add signal handler

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='telegram_message', durable=True)

telegram = TelegramFactory.get_client(config['api_token'])

def send_messages_to_queue(messages: list):
    """
    Sends each message to rabbitmq
    :param messages:
    :return:
    """
    for msg in messages:
        channel.basic_publish(exchange='',
                              routing_key='telegram_message',
                              body=json.dumps(msg),
                              # make message persistent
                              properties=pika.BasicProperties(delivery_mode=2,)
                              )


def start_sending_messages_thread(messages: list):
    send_to_queue_thread = threading.Thread(target=send_messages_to_queue, args=(messages,), daemon=True)
    send_to_queue_thread.start()

telegram.set_on_message_handler(start_sending_messages_thread)
telegram.start_listening()

connection.close()