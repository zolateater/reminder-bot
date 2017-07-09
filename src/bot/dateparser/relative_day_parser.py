from ..dateparser import AbstractDateParser, DateSearchStatus, DateAlreadyFoundError
from datetime import timedelta
import re

class RelativeDayParser(AbstractDateParser):
    """
    Парсер относительных указаний дня: завтра, и т.д.
    """
    TIME_TOMORROW = r'\завтра'
    TIME_AFTER_TOMORROW = r'послезавтра'

    def search(self, msg: str, status: DateSearchStatus):
        days_to_add = 2
        search = re.search(self.TIME_AFTER_TOMORROW, msg, re.IGNORECASE)

        if not search:
            search = re.search(self.TIME_TOMORROW, msg, re.IGNORECASE)
            days_to_add = 1

        if not search:
            return

        if status.date:
            raise DateAlreadyFoundError()

        # Устанавливаем время и дату
        reminder_datetime = status.current_datetime + timedelta(days=days_to_add)
        status.date = reminder_datetime.date()