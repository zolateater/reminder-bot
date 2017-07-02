from app.queue import QueueConnection
from telegram.client import TelegramClient
from pickle import loads
from bot.entity.reminder import Reminder

class ReminderListener():
    """
    Слушает очередь напоминаний, которые следует разослать.
    """
    def __init__(self, queue: QueueConnection, client: TelegramClient):
        """

        :param queue:
        :param client:
        """
        self.queue = queue
        self.client = client

    def start_listening(self) -> None:
        """
        Блокирует выполнение, слушая сообщения и обрабатывая.
        :return:
        """
        self.queue.set_handler(self.send_message)
        self.queue.start_listening()

    def send_message(self, message: bytes) -> None:
        """
        Посылает напоминания.
        :param message:
        :return:
        """
        reminder = self.decode_reminder(message)
        self.client.send_message(reminder.chat_id, reminder.message_text)

    @classmethod
    def decode_reminder(cls, message: bytes) -> Reminder:
        """
        Десериализует напоминания из очереди.
        :param message:
        :return:
        """
        return loads(message)

