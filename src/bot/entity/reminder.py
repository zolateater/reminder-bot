from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime

class Reminder(declarative_base()):
    """
    Модель, представляющая напоминание.
    """
    __tablename__ = 'reminders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, index=True)
    time_text = Column(Text)
    message_text = Column(Text, nullable=True)
    interval_serialized = Column(Text, nullable=True)
    remind_at = Column(DateTime, index=True)
    is_repeatable = Column(Boolean)