from datetime import datetime as Datetime, date as Date, time as Time, timedelta as Timedelta
from typing import Optional

class DateSearchStatus():
    """
    Класс, представляющий статус поиска даты, времени и интервала.
    Используется для того чтобы передавать данные между парсерами дат и представлять результат парсинга.
    """
    def __init__(self, current_date: Datetime):
        self.__current_date = current_date
        self.__date = None
        self.__time = None
        self.__interval = None

    @property
    def date(self) -> Optional[Date]:
        return self.__date

    @date.setter
    def date(self, dt: Date):
        self.__date = dt

    @property
    def time(self) -> Optional[Time]:
        return self.__time

    @time.setter
    def time(self, tm: Time):
        self.__time = tm

    @property
    def interval(self) -> Optional[Timedelta]:
        return self.__interval

    @interval.setter
    def interval(self, delta: Timedelta):
        self.__interval = delta
