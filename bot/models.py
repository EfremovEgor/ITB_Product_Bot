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


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)


Column("id", Integer, primary_key=True),
Column("marketplace", String, nullable=False),
Column("notification_id", Integer, nullable=False),
Column("market_place_id", Integer, nullable=False),
Column("importance", String, nullable=False),
Column("last_sent_notification", DateTime),
Column("available", Boolean),
