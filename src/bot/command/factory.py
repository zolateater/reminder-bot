from bot.command.start import *
from telegram.type import Message

class CommandFactory():
    """
    A command for
    """

    @classmethod
    def choose_command(cls, msg: Message) -> Command:
        """
        Выбор команды по сообщению.
        :param Message msg:
        :return:
        """
        return HelpCommand()


def extract_command(msg: Message):
    pass
