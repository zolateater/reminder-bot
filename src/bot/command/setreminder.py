from bot.command.base import Command
from telegram.client import TelegramClient
from telegram.type import Message


class SetReminderCommand(Command):
    """
    Команда для создания
    """
    def execute(self, client: TelegramClient, message: Message):
        pass
