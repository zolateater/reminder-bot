#!/usr/bin/python3

from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from app.log import LogFactory
from app.db import DBConnectionFactory
from bot.listeners.database import DatabaseListener
from datetime import datetime
from time import sleep
from pickle import dumps

# Зависимости слушателя.
config = ConfigFactory.get_default()
log = LogFactory.from_config()
db_session = DBConnectionFactory.get_session()

listener = DatabaseListener(db_session)

while True:
    reminders = listener.fetch(datetime.now())
    queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_MESSAGES), config)

    for reminder in reminders:
        queue.push_message(dumps(reminder))

    print("Sent {} messages...".format(len(reminders)))

    # TODO: sched расписальщик
    sleep(59)