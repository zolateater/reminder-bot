from telegram.client import TelegramClient
from telegram.type import *
from abc import ABC, abstractmethod

class Command(ABC):
    """
    An interface which every command must implement.
    """
    @abstractmethod
    def execute(self, client: TelegramClient, message: Message):
        pass