from bot.command import Command, HelpCommand, SetReminderCommand
from telegram.type import Message, MessageEntity, MessageEntityType
from enum import Enum, unique
from app.db import Session

@unique
class CommandEnum(Enum):
    HELP_COMMAND = '/help'
    START_COMMAND = '/start'
    SET_REMINDER_COMMAND = '/setreminder'
    MY_REMINDERS_COMMAND = '/myreminders'

class CommandFactory():
    """
    Фабрика команд.
    Создает команду, выбирая команду по сообщению
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def choose_command(self, msg: Message) -> Command:
        """
        Выбор команды по сообщению.
        :param Message msg:
        :return:
        """

        # Фильтруем entity по коммандам для бота
        bot_commands = [e for e in msg.entities if e.type == MessageEntityType.TYPE_BOT_COMMAND]

        if len(bot_commands) == 0:
            # TODO: добавить реакцию на отсутсвие команды
            return HelpCommand()
        if len(bot_commands) > 1:
            # TODO: добавить отдельную команду на последовательность комманд
            return HelpCommand()

        command = bot_commands[0]

        if command.text in [CommandEnum.START_COMMAND.value, CommandEnum.HELP_COMMAND.value]:
            return HelpCommand()

        if command.text == CommandEnum.SET_REMINDER_COMMAND.value:
            return SetReminderCommand(self.db_session)

        return HelpCommand()


def extract_command(msg: Message):
    pass
