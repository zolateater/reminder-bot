from bot.command.base import Command, TelegramClient, Message


class HelpCommand(Command):
    START_TEXT = """
    Бот для создания напоминаний.
    Команды:
    <b>/help</b> - выводит текущую справку
    <b>/setreminder когда, что напомнить</b> - создание напоминания.
    Примеры:
    <b>/setreminder 23.04, день рождения</b>
    <b>/setreminder каждый вторник в 11:15, лекция по английскому</b>
    Если присутствует слово "каждый/кождое", то напоминание будет повторяться.
    Допустимые форматы дат (пример в скобках):
    ДД.ММ (23.14)
    ДД месяц (23 ноября)
    день недели (понедельник)
    Время указывается в формате ЧЧ:ММ (12:15)

    <b>/myreminders</b> - выводит ваши напоминания. Каждому из них назначен номер.

    <b>/removereminder номер</b> - удалить напоминание.

    <b>/clearall</b> - удалить все напоминания.
    """

    def execute(self, client: TelegramClient, message: Message):
        client.send_message(message.chat.id, self.START_TEXT, 'html')
