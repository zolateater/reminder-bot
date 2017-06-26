from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime

class Reminder(declarative_base()):
    """
    Модель, представляющая напоминание.
    """
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    message_text = Column(Text)
    remind_at = Column(DateTime)
    is_repeatable = Column(Boolean)
    interval_text = Column(String)