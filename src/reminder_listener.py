#!/usr/bin/python3

from app.config import ConfigFactory, Config
from app.queue import QueueFactory
from bot.listeners.reminder import ReminderListener
from telegram.client import TelegramFactory

# Зависимости слушателя.
config = ConfigFactory.get_default()
telegram = TelegramFactory.get_client(config.get(Config.API_TOKEN))
queue = QueueFactory.queue_from_config(config.get(Config.RABBITMQ_QUEUE_MESSAGES), config)

print("Listening reminders queue...")
listener = ReminderListener(queue, telegram)
listener.start_listening()
