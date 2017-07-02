from ..dateparser import DateSearchStatus
from abc import ABC, abstractmethod

class AbstractDateParser(ABC):
    """
    Интерфейс для парсинга дат из текста сообщения.
    Каждый парсер обновляет статус поиска даты.
    Такой подход дает возможность построить Chain of Responsibility,
    где каждый класс отвечает за свой кусок парсинга даты.
    """
    @abstractmethod
    def search(self, msg: str, status: DateSearchStatus):
        pass