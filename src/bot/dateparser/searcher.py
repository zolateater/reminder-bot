from ..dateparser import DateSearchStatus, AbstractDateParser
from .time_parser import TimeParser
from .after_minutes_parser import AfterMinutesParser
from .after_hours_parser import AfterHoursParser
from .relative_day_parser import RelativeDayParser
from .day_month_parser import DayMonthParser
from .week_day_parser import WeekDayParser
from typing import List
from datetime import datetime, timedelta, time

class DateSearcher():
    """
    Класс, содержащий парсеры дат.
    Инкапсулирует конкретные парсеры.
    """
    PARSERS = [
        TimeParser(),
        AfterHoursParser(),
        AfterMinutesParser(),
        RelativeDayParser(),
        WeekDayParser(),
        DayMonthParser()
    ]

    # Время по умолчанию
    FALLBACK_TIME = time(hour=10, minute=0)

    def get_parsers(self) -> List[AbstractDateParser]:
        return self.PARSERS

    def parse(self, msg: str, current_datetime: datetime) -> DateSearchStatus:
        status = DateSearchStatus(current_datetime)
        for parser in self.get_parsers():
            parser.search(msg, status)

        if status.date and not status.time:
            self.add_fallback_time(status)

        if not status.date and status.time:
            self.add_fallback_date(status)

        return status

    def add_fallback_date(self, status: DateSearchStatus) -> None:
        """
        Добавляет дату по умолчанию.
        Используется, когда указано только время.
        Если сегодня больше времени, чем нужно, то напоминание будет установлено на завтра.
        :param status:
        :return:
        """
        if status.current_datetime.time() > status.time:
            status.date = status.current_datetime.date()
        else:
            status.date = status.current_datetime.date() + timedelta(days=1)

    def add_fallback_time(self, status: DateSearchStatus):
        """
        Добавляет время.
        Используется, когда указано только дата.
        Время по умолчанию захардкожено.
        :param status:
        :return:
        """
        status.time = self.FALLBACK_TIME

