# Implemented:
#
# At:
# через X минут
# в 12:40
# через час / через 2 часа / через X часов
# завтра
# послезавтра
# в понедельник
# в пн
# 26 ноя в 11:00
# 26 ноября в 11:00

# To be implemented:
# At:
# через день / через X дня / через X дней
# через день, пять часов и семь минут

# Intervals:
# каждый час
# каждый день в 12:30
# каждый понедельник
# каждый понедельник в 11:00
# каждое N число
# каждое последнее число

from src.bot.dateparser import DateSearcher, DateSearchStatus
from datetime import datetime, date, time

DEFAULT_FORMAT = "%Y-%m-%d %H:%M"

def assert_parse_date(msg: str, current_dt: str, expected_dt: str):
    """
    Функция для быстрого парсинга дат.
    Ожидает дату, указанную в DEFAULT FORMAT
    :param msg:
    :param current_dt:
    :param expected_dt:
    :return:
    """
    status = DateSearcher().parse(msg, datetime.strptime(current_dt, DEFAULT_FORMAT))
    datetime_found = datetime.combine(date=status.date, time=status.time)
    assert expected_dt == datetime_found.strftime(DEFAULT_FORMAT)

def test_minutes_interval():
    assert_parse_date("Через 20 минут", "2017-01-01 12:30", "2017-01-01 12:50")

def test_case_sensitivity():
    assert_parse_date("ЧеРеЗ 20 МИНУТ", "2017-01-01 12:30", "2017-01-01 12:50")

def test_many_minutes_interval():
    assert_parse_date("Через 55 минут", "2017-01-01 12:30", "2017-01-01 13:25")

def test_minutes_interval_next_day():
    assert_parse_date("Через 1440 минут", "2017-01-01 12:30", "2017-01-02 12:30")

def test_after_hour_parser():
    assert_parse_date("Через час", "2017-01-01 12:30", "2017-01-01 13:30")

def test_after_hours_parser():
    assert_parse_date("Через 5 часов", "2017-01-01 12:30", "2017-01-01 17:30")

def test_tomorrow():
    assert_parse_date("Завтра в 11:00", "2017-01-01 17:30", "2017-01-02 11:00")

def test_after_tomorrow():
    assert_parse_date("Послезавтра в 11:00", "2017-01-01 17:30", "2017-01-03 11:00")

def test_weekday_today_week_end():
    assert_parse_date("В пн в 10:00", "2017-01-01 17:30", "2017-01-02 10:00")

def test_weekday_current():
    assert_parse_date("В Воскресенье в 12:03", "2017-01-01 17:30", "2017-01-08 12:03")

def test_weekday_previous():
    assert_parse_date("В субботу в 12:03", "2017-01-01 17:30", "2017-01-07 12:03")

def test_date_month_may_time_last_format():
    assert_parse_date("25 мая в 10:10", "2017-01-01 10:00", "2017-05-25 10:10")

def test_date_month_time_first_format():
    assert_parse_date("12:13 май 1", "2017-01-01 10:00", "2017-05-01 12:13")

def test_date_month_expired_date():
    assert_parse_date("1 фев в 2:45", "2017-03-01 10:00", "2018-02-01 02:45")