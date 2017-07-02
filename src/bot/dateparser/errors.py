"""
Классы ошибок, которые могут возникать при парсинге дат.
"""

class DateParseError(Exception):
    pass

class DateAlreadyFoundError(DateParseError):
    pass

class TimeAlreadyFoundError(DateParseError):
    pass

class IntervalAlreadyFoundException(DateParseError):
    pass