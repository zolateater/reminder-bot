#!/usr/bin/python3

from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from app.log import LogFactory
from app.db import DBConnectionFactory
from bot.listeners.database import DatabaseListener
from datetime import datetime
from time import sleep

# Зависимости слушателя.
config = ConfigFactory.get_default()
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_MESSAGES), config)
log = LogFactory.from_config()
db_session = DBConnectionFactory.get_session()

listener = DatabaseListener(db_session, queue)

while True:
    # TODO: sched расписальщик
    listener.fetch(datetime.now())
    sleep(1)