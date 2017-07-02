from app.db import Session
from app.queue import QueueConnection
from datetime import datetime, timedelta
from bot.entity.reminder import Reminder
from pickle import dumps

class DatabaseListener():
    """
    Слушатель базы данных.
    Отправляет запрос на получение актуальных напоминаний, отправляет их в очередь.
    """
    def __init__(self, db_session: Session, queue: QueueConnection):
        self.db_session = db_session
        self.queue = queue

    def fetch(self, now: datetime):
        next_min = now + timedelta(minutes=1)
        query = self.db_session.query(Reminder)\
            .filter(Reminder.remind_at >= now.strftime('%Y-%m-%d %H:%M:00'))\
            .filter(Reminder.remind_at <= next_min.strftime('%Y-%m-%d %H:%M:00'))

        reminders = query.all()
        print(len(reminders))
        for reminder in reminders:
            # TODO: подумать, как избежать проблем с обновлением сущностей при сериализации/десериализации.
            self.queue.push_message(dumps(reminder))