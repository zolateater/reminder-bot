from ..dateparser import AbstractDateParser, DateSearchStatus, TimeAlreadyFoundError
from datetime import time
import re

class TimeParser(AbstractDateParser):
    TIME_REGEX = r'(\d\d):(\d\d)'
    MAX_HOURS = 23
    MAX_MINUTES = 59

    def search(self, msg: str, status: DateSearchStatus):
        search = re.search(self.TIME_REGEX, msg, re.IGNORECASE | re.UNICODE)
        if search is None:
            return

        # Группа 0 содержит все совпадение целиком.
        hours = int(search.group(1))
        minutes = int(search.group(2))

        if (0 <= hours <= self.MAX_HOURS and 0 <= minutes <= self.MAX_MINUTES):
            if (status.time is not None):
                raise TimeAlreadyFoundError()
            status.time = time(hour=hours, minute=minutes)