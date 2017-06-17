#!/usr/bin/python3

import json
from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from telegram.client import TelegramFactory
from telegram.typebuilder import UpdateBuilder, ParseError

config = ConfigFactory.get_default()
telegram = TelegramFactory.get_client(config.get(Config.API_TOKEN))
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_UPDATES), config)
update_builder = UpdateBuilder()

def callback(body: bytearray):
    update_dict = json.loads(str(body, encoding='utf-8'))
    try:
        update = update_builder.build(update_dict)
        if update.message is None:
            print(update.__dict__)
            return

        for ent in update.message.entities:
            print(ent.type)
            print(ent.user)
            print(ent.length)
            print(ent.offset)
            print(ent.url)

        telegram.send_message(update.message.chat.id, "Hello, {}.".format(update.message.chat.first_name), "html")

    except ParseError as e:
        print(e.class_name)
        print(e.previous)

queue.set_handler(callback)

print('Listening for messages in a queue...')
queue.start_listening()