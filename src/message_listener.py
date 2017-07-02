#!/usr/bin/python3

import json
# TODO: too many dependencies.
from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from app.log import LogFactory
from app.db import DBConnectionFactory
from telegram.client import TelegramFactory
from telegram.typebuilder import UpdateBuilder, ParseError
from bot.command import CommandFactory

# Зависимости слушателя.
config = ConfigFactory.get_default()
telegram_client = TelegramFactory.get_client(config.get(Config.API_TOKEN))
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_UPDATES), config)
log = LogFactory.from_config()
db_session = DBConnectionFactory.get_session()
update_builder = UpdateBuilder()
command_factory = CommandFactory(db_session)

def callback(body: bytearray):
    """
    Функция обработки сообщения из очереди.
    Сюда попадают сообщения, принятые в telegram_listener.py
    :param bytearray body:
    :return:
    """
    update_dict = json.loads(str(body, encoding='utf-8'))
    try:
        log.debug(str(body, 'utf-8'))

        # Создаем объект из json.
        update = update_builder.build(update_dict)

        # Обновления без сообщений мы не рассматриваем - нам нечего в них обрабатывать
        if update.message is None:
            return

        msg = update.message

        # Выбор подходящей команды по сообщению
        cmd = command_factory.choose_command(msg)
        cmd.execute(client=telegram_client, message=msg)
    except ParseError as e:
        log.error("Parse error: class - {}, reason - {}".format(e.class_name, e.previous.__cause__))

queue.set_handler(callback)

print('Listening for messages in a queue...')
queue.start_listening()