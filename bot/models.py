from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql.schema import Column
from database import Base
from datetime import datetime


class UnregisteredUser(Base):
    __tablename__ = "unregistered_users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, primary_key=False, nullable=False)
    name = Column(String, nullable=False)
    last_sent_message = Column(DateTime, default=datetime.utcnow)


class RegisteredUser(Base):
    __tablename__ = "registered_users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, primary_key=False, nullable=False)
    name = Column(String, nullable=False)
    last_sent_message = Column(DateTime, default=datetime.utcnow)
