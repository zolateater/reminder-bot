from src.bot.dateparser import DateSearchStatus, TimeAlreadyFoundError, TimeParser
from datetime import datetime, time
from pytest import raises

"""
Тесты вычленения времени из текста сообщения
"""


def test_correct_time_in_message():
    status = DateSearchStatus(datetime.now())
    TimeParser().search("в 12:15", status)
    assert isinstance(status.time, time)
    assert status.time.hour == 12
    assert status.time.minute == 15
    # По умолчанию секунды равны нулю
    assert status.time.second == 0


def test_trailing_zeros():
    status = DateSearchStatus(datetime.now())

    TimeParser().search("в 09:09", status)
    assert isinstance(status.time, time)
    assert status.time.hour == 9
    assert status.time.minute == 9

def test_no_trailing_zeros():
    status = DateSearchStatus(datetime.now())

    TimeParser().search("в 1:09", status)
    assert isinstance(status.time, time)
    assert status.time.hour == 1
    assert status.time.minute == 9


def test_incorrect_time_in_message():
    status = DateSearchStatus(datetime.now())

    TimeParser().search("в 35:15", status)
    assert status.time is None

    TimeParser().search("в 15:60", status)
    assert status.time is None


def test_time_already_found_and_time_is_correct():
    status = DateSearchStatus(datetime.now())
    status.time = time()

    # Никаких ошибок - время некорректно, мы его не указываем.
    TimeParser().search("в 35:15", status)


def test_time_in_message_is_correct_and_time_is_set():
    status = DateSearchStatus(datetime.now())
    status.time = time()
    with raises(TimeAlreadyFoundError):
        TimeParser().search("в 10:15", status)
