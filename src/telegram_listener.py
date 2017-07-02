#!/usr/bin/python3
from app.config import Config, ConfigFactory
from app.queue import QueueFactory
from telegram.client import TelegramFactory
import threading
import json
from app.log import LogFactory

# TODO: добавить обработку сигналов
# TODO: добавить класс приложения для инкапсуляции зависимостей
# TODO: перенести запуск процесса в docker

config = ConfigFactory.get_default()
log = LogFactory.from_config()
telegram = TelegramFactory.get_client(config.get(Config.API_TOKEN))

def send_messages_to_queue(messages: list):
    """
    Посылает каждое сообщение в очередь.
    :param messages:
    :return:
    """
    queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_UPDATES), config)
    for msg in messages:
        queue.push_message(json.dumps(msg))
    queue.close()

def start_sending_messages_thread(messages: list):
    send_to_queue_thread = threading.Thread(target=send_messages_to_queue, args=(messages,), daemon=True)
    send_to_queue_thread.start()

telegram.set_on_message_handler(start_sending_messages_thread)

print("Listening telegram API...")

while True:
    try:
        telegram.listen()
    except Exception as e:
        log.error(str(e))
        print(str(e))