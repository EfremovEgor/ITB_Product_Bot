from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import utils
from database import session
from models import UnregisteredUser, RegisteredUser


def kb_go_to_start_menu() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text="Меню")]]
    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return kb


def kb_start_menu() -> ReplyKeyboardMarkup:
    kb = list()
    kb.append(
        [KeyboardButton(text="Добавить товар"), KeyboardButton(text="Список товаров")]
    )
    kb.append([KeyboardButton(text="Пользователи"), KeyboardButton(text="API ключи")])
    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return kb


def kb_add_goods_choosing_marketplace() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for market in utils.AVAILABLE_MARKETPLACES:
        builder.add(KeyboardButton(text=market))
    builder.adjust(2)
    builder.row(KeyboardButton(text="Меню"))
    kb = builder.as_markup(resize_keyboard=True)
    return kb


def kb_add_goods_choosing_account(accounts: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for account in accounts:
        builder.add(KeyboardButton(text=account))
    builder.adjust(3)
    builder.row(KeyboardButton(text="Меню"))
    kb = builder.as_markup(resize_keyboard=True)

    return kb


def kb_add_goods_choosing_notification(notifications: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for notification in notifications:
        builder.add(KeyboardButton(text=notification))
    builder.adjust(3)
    builder.row(KeyboardButton(text="Меню"))
    kb = builder.as_markup(resize_keyboard=True)

    return kb


def kb_manage_users_remove_access() -> ReplyKeyboardMarkup:
    kb = list()
    kb.append([KeyboardButton(text="Забрать доступ"), KeyboardButton(text="Назад")])
    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return kb


def kb_manage_users_grant_access() -> ReplyKeyboardMarkup:
    kb = list()
    kb.append([KeyboardButton(text="Дать доступ"), KeyboardButton(text="Назад")])
    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return kb


def kb_manage_users_add_new_employee() -> ReplyKeyboardMarkup:
    users = session.query(UnregisteredUser).limit(10).all()
    builder = ReplyKeyboardBuilder()
    for user in users:
        builder.add(KeyboardButton(text=f"{user.name} ID:{user.telegram_id}"))
    builder.adjust(1)
    builder.row(KeyboardButton(text="Меню"))
    kb = builder.as_markup(resize_keyboard=True)
    return kb


def kb_manage_users_investigate_employees() -> ReplyKeyboardMarkup:
    users = session.query(RegisteredUser).all()
    builder = ReplyKeyboardBuilder()
    for user in users:
        builder.add(KeyboardButton(text=f"{user.name} ID:{user.telegram_id}"))
    builder.adjust(2)
    builder.row(KeyboardButton(text="Меню"))
    kb = builder.as_markup(resize_keyboard=True)
    return kb


def kb_manage_users_menu():
    kb = list()
    kb.append(
        [
            KeyboardButton(text="Новый сотрудник"),
            KeyboardButton(text="Список сотрудников"),
        ]
    )
    kb.append([KeyboardButton(text="Меню")])

    kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return kb
