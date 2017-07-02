from ..dateparser import AbstractDateParser, DateSearchStatus
import re

class AfterMinutesParser(AbstractDateParser):
    """
    Парсер указаний вида "через X минут"
    """
    TIME_REGEX = r'через\s+?(\d\d?)\s+?минут'

    def search(self, msg: str, status: DateSearchStatus):
        search = re.search(self.TIME_REGEX, msg)
        if not search:
            return