from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import (
    kb_api_keys_menu,
    kb_choosing_marketplace,
    kb_start_menu,
    kb_go_to_start_menu,
)
from states import MenuNavigation, AvailableButtonNames
from aiogram.fsm.context import FSMContext
from utils import get_accounts
from filters import UserAccessFilter
from database import session
from models import Account

router = Router()
router.message.filter(UserAccessFilter())


@router.message(MenuNavigation.main_menu, F.text == "API ключи")
async def add_good(message: Message, state: FSMContext):
    kb = kb_api_keys_menu()
    await message.answer("Выберите действие", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys)


@router.message(MenuNavigation.api_keys, F.text == "Новый кабинет")
async def create_new_account(message: Message, state: FSMContext):
    kb = kb_choosing_marketplace()
    await message.answer("Выберите площадку", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_choosing_marketplace_on_creation)


@router.message(MenuNavigation.api_keys_choosing_marketplace_on_creation)
async def marketplace_chosen(message: Message, state: FSMContext):
    if message.text not in AvailableButtonNames.marketplaces:
        kb = kb_choosing_marketplace()
        state.set_state(MenuNavigation.api_keys_choosing_marketplace_on_creation)
        return
    await state.update_data(chosen_marketplace=message.text)
    kb = kb_go_to_start_menu()
    await state.update_data(chosen_marketplace=message.text)
    await message.answer("Введите название аккаунта", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_inserting_name_on_creation)


@router.message(
    MenuNavigation.api_keys_inserting_name_on_creation,
)
async def name_inserted(message: Message, state: FSMContext):
    kb = kb_go_to_start_menu()
    await state.update_data(chosen_name=message.text)
    await message.answer("Введите API ключ", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_inserting_key_on_creation)


@router.message(
    MenuNavigation.api_keys_inserting_key_on_creation,
)
async def key_inserted(message: Message, state: FSMContext):
    kb = kb_start_menu()
    await state.update_data(chosen_api_key=message.text)
    data = await state.get_data()
    session.add(
        Account(
            name=data["chosen_name"],
            marketplace=data["chosen_marketplace"],
            api_key=data["chosen_api_key"],
        )
    )
    session.commit()
    await message.answer("Аккаунт успешно добавлен", reply_markup=kb)
    await state.set_state(MenuNavigation.main_menu)
