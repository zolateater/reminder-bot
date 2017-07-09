from ..dateparser import AbstractDateParser, DateSearchStatus, TimeAlreadyFoundError, DateAlreadyFoundError
from datetime import timedelta
import re

class AfterHoursParser(AbstractDateParser):
    """
    Парсер указаний вида "через час / через X часов"
    """
    ONE_HOUR_REGEX = r'через\s+час'
    MULTIPLE_HOURS_REGEX = r'через\s+(\d+)\s+час'

    def search(self, msg: str, status: DateSearchStatus):
        self.search_one_hour(msg, status)
        self.search_multiple_hours(msg, status)


    def search_multiple_hours(self, msg, status):
        # TODO: make function wrapper.
        search = re.search(self.MULTIPLE_HOURS_REGEX, msg, re.IGNORECASE | re.UNICODE)
        if not search:
            return

        self.check_if_date_or_time_found(status)

        hours = int(search.group(1))
        reminder_datetime = status.current_datetime + timedelta(hours=hours)
        status.time = reminder_datetime.time()
        status.date = reminder_datetime.date()

    def check_if_date_or_time_found(self, status: DateSearchStatus):
        """
        :param status:
        :return:
        """
        if status.time:
            raise TimeAlreadyFoundError()

        if status.date:
            raise DateAlreadyFoundError()

    def search_one_hour(self, msg: str, status: DateSearchStatus):
        search = re.search(self.ONE_HOUR_REGEX, msg, re.IGNORECASE | re.UNICODE)
        if not search:
            return

        self.check_if_date_or_time_found(status)

        reminder_datetime = status.current_datetime + timedelta(hours=1)
        status.time = reminder_datetime.time()
        status.date = reminder_datetime.date()