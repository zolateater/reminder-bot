from typing import Union

from ..dateparser import AbstractDateParser, DateSearchStatus, DateAlreadyFoundError
from ..dateparser.time_parser import TimeParser
from datetime import date
from enum import Enum, unique
import re

@unique
class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class DayMonthParser(AbstractDateParser):
    """
    Парсер указаний вида "число, месяц"
    """

    # Выражение для поиска чисел
    NUMBER_REGEX = r'\d\d?'

    MONTH_NAMES = {
        Month.JANUARY: ['янв'],
        Month.FEBRUARY: ['фев'],
        Month.MARCH: ['март'],
        Month.APRIL: ['апр'],
        Month.MAY: ['май', 'мая'],
        Month.JUNE: ['июн'],
        Month.JULY: ['июл'],
        Month.AUGUST: ['авг'],
        Month.SEPTEMBER: ['сен'],
        Month.OCTOBER: ['окт'],
        Month.NOVEMBER: ['ноя'],
        Month.DECEMBER: ['дек'],
    }

    def search(self, msg: str, status: DateSearchStatus):
        # Нам нужен номер числа месяца, но в строке может встретиться время.
        # Поэтому нам нужно вытащить время, и попробовать найти число
        msg_without_time = self.remove_time(msg)

        # Ищем число месяца
        day_number_search = re.search(self.NUMBER_REGEX, msg_without_time, re.IGNORECASE | re.UNICODE)
        if not day_number_search:
            return
        day = int(day_number_search.group())

        # Ищем месяц
        month = self.find_month(msg_without_time)
        if month == False:
            return

        # Дата уже установлена
        if status.date:
            raise DateAlreadyFoundError()

        # Актуален ли установленный год?
        dt = date(year=status.current_datetime.year, month=month.value, day=day)
        if status.current_datetime.date() > dt:
            dt = dt.replace(year=dt.year + 1)

        status.date = dt

    def remove_time(self, msg: str) -> str:
        """
        Убирает вхождения со временем из строки.
        :param msg:
        :return:
        """
        if re.search(TimeParser.TIME_REGEX, msg):
            return re.sub(TimeParser.TIME_REGEX, str(), msg)
        return msg

    def find_month(self, msg: str) -> Union[Month, bool]:
        """
        Возвращает месяц, найденный в строке, либо False
        :param msg:
        :return:
        """
        for index, names in self.MONTH_NAMES.items():
            for name in names:
                if re.search(r'\b{}\b'.format(name), msg):
                    return Month(index)

        return False