from ..dateparser import AbstractDateParser, DateSearchStatus, TimeAlreadyFoundError, DateAlreadyFoundError
from datetime import timedelta
import re

class AfterMinutesParser(AbstractDateParser):
    """
    Парсер указаний вида "через X минут"
    """
    TIME_REGEX = r'через\s+?(\d+?)\s+?минут'

    def search(self, msg: str, status: DateSearchStatus):
        search = re.search(self.TIME_REGEX, msg, re.IGNORECASE)
        if not search:
            return

        if status.time:
            raise TimeAlreadyFoundError()

        if status.date:
            raise DateAlreadyFoundError()

        # Выделяем группу с минутами из результатов поиска
        minutes = int(search.group(1))

        # Устанавливаем время и дату
        reminder_datetime = status.current_datetime + timedelta(minutes=minutes)
        status.time = reminder_datetime.time()
        status.date = reminder_datetime.date()