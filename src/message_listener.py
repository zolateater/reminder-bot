#!/usr/bin/python3

import json
from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from telegram.client import TelegramFactory

config = ConfigFactory.get_default()
telegram = TelegramFactory.get_client(config.get(Config.API_TOKEN))
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_MESSAGES), config)

def callback(body: bytearray):
    msg = json.loads(str(body, encoding='utf-8'))
    print(msg)
    telegram.send_message(chat_id=msg['message']['chat']['id'], text='Ok', parse_mode='html')

queue.set_handler(callback)

print('Listening for messages in a queue')
queue.start_listening()