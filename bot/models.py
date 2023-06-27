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


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    marketplace = Column(String, nullable=False)


class Good(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True)
    marketplace = Column(String, nullable=False)
    notification_id = Column(Integer, nullable=False)
    market_place_id = Column(String, nullable=False)
    importance = Column(String, default="None")
    last_sent_notification = Column(DateTime, default=datetime.min)
    available = Column(Boolean, default=True)
