from app.db import Session
from datetime import datetime, timedelta
from bot.entity.reminder import Reminder
from typing import List

class DatabaseListener():
    """
    Слушатель базы данных.
    Отправляет запрос на получение актуальных напоминаний, отправляет их в очередь.
    """
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def fetch(self, now: datetime) -> List[Reminder]:
        """
        Получает текушие актульные напоминания
        :param now:
        :return:
        """
        next_min = now + timedelta(minutes=1)
        query = self.db_session.query(Reminder)\
            .filter(Reminder.remind_at >= now.strftime('%Y-%m-%d %H:%M:00'))\
            .filter(Reminder.remind_at <= next_min.strftime('%Y-%m-%d %H:%M:00'))

        reminders = query.all()
        return reminders
