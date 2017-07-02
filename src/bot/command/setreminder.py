from bot.command.base import Command
from telegram.client import TelegramClient
from telegram.type import Message
from bot.dateparser import DateSearchStatus
from bot.entity.reminder import Reminder
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pickle import dumps
from pickle import loads

class SetReminderCommand(Command):
    """
    Разделитель аргументов, введенных пользователем в команду
    """
    ARGUMENT_SEPARATOR = ","
    REMINDER_LIMIT = 50

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def execute(self, client: TelegramClient, message: Message):
        """
        Пытается создать напоминание, уведомляет пользователя.
        При успешной попытке (зависит от парсинга), напоминание создается в БД.
        """
        reminder = self.build_remainder(message)

        if reminder is None:
            client.send_message(message.chat.id, "Я не понимаю что от меня нужно!")
            return

        self.db_session.add(reminder)
        self.db_session.commit()

        client.send_message(message.chat.id, "setting...", "html")

    def get_default_datetime(self, current_date_time: datetime) -> datetime:
        """
        Возвращает дату/время по умолчанию.
        Используется для построения дат, для которых не указанов время, а также для относительных дат.
        :param datetime current_date_time:
        :return:
        """
        return current_date_time.replace(hour=10, minute=0)

    def build_remainder(self, msg: Message) -> Optional[Reminder]:
        """
        TODO: дописать логику выбора времени
        :param msg:
        :return:
        """

        # TODO: really build reminder
        msg_text = msg.get_text_without_entities().strip()
        remind_at_text, reminder_text = '', None

        if msg_text.find(self.ARGUMENT_SEPARATOR) != -1:
            remind_at_text, reminder_text = msg_text.split(self.ARGUMENT_SEPARATOR)
        else:
            remind_at_text = msg_text

        now = datetime.now()

        reminder = Reminder()
        reminder.chat_id = msg.chat.id
        reminder.interval_serialized = None
        reminder.message_text = reminder_text
        reminder.is_repeatable = False
        reminder.time_text = remind_at_text
        reminder.remind_at = now.replace(minute=now.minute + 1)

        return reminder
