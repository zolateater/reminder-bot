from ..dateparser import AbstractDateParser, DateSearchStatus, DateAlreadyFoundError
from datetime import timedelta, date
from typing import Union
import re
from enum import Enum, unique

@unique
class WeekDay(Enum):
    """
    Перечисление дней недели.
    Совместимо с функцией weekday() класса datetime
    """
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class WeekDayParser(AbstractDateParser):
    """
    Парсер относительных указаний дня недели
    """

    DAYS_IN_WEEK = 7

    # Соответствия между номером и названием.
    # TODO: добавить расстояние левенштейна для опечаток в названиях дней.
    WEEKDAY_NAMES_DICT = {
        WeekDay.MONDAY: ['понедельник', 'пн'],
        WeekDay.TUESDAY: ['вторник', 'вт'],
        WeekDay.WEDNESDAY: ['среда', 'среду', 'ср'],
        WeekDay.THURSDAY: ['четверг', 'чт'],
        WeekDay.FRIDAY: ['пятница', 'пт'],
        WeekDay.SATURDAY: ['суббота', 'субботу', 'сб'],
        WeekDay.SUNDAY: ['воскресенье', 'вс'],
    }

    def find_weekday(self, msg: str) -> Union[WeekDay, bool]:
        """
        Поиск указания дня недели в строке по словарю.
        Если день недели не найден, возвращает False.
        :param msg:
        :return:
        """
        for index, names in self.WEEKDAY_NAMES_DICT.items():
            for name in names:
                search = re.search(r'\b{}\b'.format(name), msg, re.IGNORECASE | re.UNICODE)
                if search:
                    return WeekDay(index)

        return False


    def search(self, msg: str, status: DateSearchStatus):
        weekday = self.find_weekday(msg)
        if weekday == False:
            return

        if status.date:
            raise DateAlreadyFoundError()

        next_weekday = self.get_closest_weekday(weekday, status.current_datetime.date())

        # Устанавливаем время и дату
        status.date = next_weekday

    def get_closest_weekday(self, weekday: WeekDay, dt: date) -> date:
        """
        Поиск ближайшего переданного дня недели.
        Если текущий день недели совпадает с переданным, вернет дату через неделю.

        :param weekday:
        :param dt:
        :return:
        """
        diff_in_days = abs(dt.weekday() - weekday.value)
        till_next_day = 7 - diff_in_days
        print(diff_in_days, till_next_day, dt, weekday)

        return dt + timedelta(days=till_next_day)