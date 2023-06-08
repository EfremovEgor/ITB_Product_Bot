from aiogram.fsm.state import StatesGroup, State
import utils
from marketplaces.yandex_market.yandex_market import YandexMarketCabinet
from marketplaces.wildberries.wildberries import WildberriesCabinet


class AvailableButtonNames:
    main_menu = ["Добавить товар", "Список товаров", "Пользователи", "API ключи"]
    marketplaces = utils.AVAILABLE_MARKETPLACES
    accounts = list()
    notifications = {
        "yandex market": YandexMarketCabinet.available_notifications,
        "wildberries": WildberriesCabinet.available_notifications,
    }


class MenuNavigation(StatesGroup):
    # Главное меню
    main_menu = State()
    add_goods = State()
    manage_users = State()
    goods_list = State()
    api_keys = State()
    # Добавить товар
    add_goods_choosing_marketplace = State()
    add_goods_choosing_account = State()
    add_goods_choosing_notification = State()
    add_goods_inserting_id = State()
    # Список товаров
    # Пользователи
    manage_users_adding_new_employee = State()
    manage_users_grant_access = State()
    manage_users_investigating_employees = State()
    manage_users_remove_access = State()
    # API ключи
