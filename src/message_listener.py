#!/usr/bin/python3

import json
from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from app.log import LogFactory
from telegram.client import TelegramFactory
from telegram.typebuilder import UpdateBuilder, ParseError
from bot.command.factory import CommandFactory


config = ConfigFactory.get_default()
telegram_client = TelegramFactory.get_client(config.get(Config.API_TOKEN))
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_UPDATES), config)
log = LogFactory.from_config()
update_builder = UpdateBuilder()

def callback(body: bytearray):
    """
    Функция обработки сообщения из очереди.
    Сюда попадают сообщения из Telegram.
    :param bytearray body:
    :return:
    """
    update_dict = json.loads(str(body, encoding='utf-8'))
    try:
        # Создаем объект из json.
        update = update_builder.build(update_dict)

        # Обновления без сообщений мы не рассматриваем,
        # нам нечего в них обрабатывать
        if update.message is None:
            return

        msg = update.message

        # Выбор подходящей команды по сообщению
        cmd = CommandFactory.choose_command(msg)
        cmd.execute(client=telegram_client, message=msg)

        # Для целей отладки
        log.debug("Executed command: {}, message_id = {}, chat_id = {}".format(cmd.__class__, msg.id, msg.chat.id))

    except ParseError as e:
        log.error("Parse error: class - {}, reason - {}".format(e.class_name, e.previous.__cause__))

queue.set_handler(callback)

print('Listening for messages in a queue...')
queue.start_listening()