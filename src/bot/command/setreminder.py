from bot.command.base import Command
from telegram.client import TelegramClient
from telegram.type import Message
from bot.dateparser import DateSearchStatus, DateSearcher, TimeAlreadyFoundError, DateAlreadyFoundError
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
        try:
            reminder = self.build_remainder(message)

            if reminder is None:
                client.send_message(message.chat.id, "Извините, но я не вижу даты в том, что вы написали.")
                return

            self.db_session.add(reminder)
            self.db_session.commit()

            client.send_message(message.chat.id, self.build_success_message(reminder))
        except TimeAlreadyFoundError:
            client.send_message(message.chat.id, "Упс! Кажется, вы указали время несколько раз подряд.")
        except DateAlreadyFoundError:
            client.send_message(message.chat.id, "Ой, а я не понимаю. Я не могу понять какую именно дату сопоставить.")
        except Exception:
            client.send_message(message.chat.id, "Так, а в этом месяце есть столько дней?")

    def build_remainder(self, msg: Message) -> Optional[Reminder]:
        """
        TODO: refactor, методы не соответсвуют действиям
        Вызывает DateSearcher для получения текущего времени
        :param msg:
        :return:
        """

        msg_text = msg.get_text_without_entities().strip()
        remind_at_text, reminder_text = '', None

        if msg_text.find(self.ARGUMENT_SEPARATOR) != -1:
            remind_at_text, reminder_text = msg_text.split(self.ARGUMENT_SEPARATOR)
        else:
            remind_at_text = msg_text

        # Сложный процесс получения Даты/Времени
        # TODO: inject зависимость
        search_date_status = DateSearcher().parse(remind_at_text, datetime.now())

        if not search_date_status.date and not search_date_status.time:
            return

        reminder = Reminder()
        reminder.chat_id = msg.chat.id
        reminder.interval_serialized = None
        reminder.message_text = reminder_text
        reminder.is_repeatable = False
        reminder.time_text = remind_at_text
        reminder.remind_at = datetime.combine(search_date_status.date, search_date_status.time)

        return reminder

    def build_success_message(self, reminder: Reminder) -> str:
        """
        Создание сообщения для напоминания.
        :param reminder:
        :return:
        """
        date_formatted = reminder.remind_at.strftime('%c')
        text = reminder.message_text if reminder.message_text is not None else "без текста"
        return """
Напоминание установлено на:
<pre>{}</pre>
Напомнить: <i>{}</i>
        """.format(date_formatted, text)
