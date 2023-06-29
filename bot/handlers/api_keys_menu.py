from aiogram import F, Router
from aiogram.types import Message
from keyboards import (
    kb_api_keys_menu,
    kb_choosing_marketplace,
    kb_start_menu,
    kb_go_to_start_menu,
    kb_available_accounts,
    kb_edit_account,
    kb_return,
)
from states import MenuNavigation, AvailableButtonNames
from aiogram.fsm.context import FSMContext
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


@router.message(MenuNavigation.api_keys, F.text == "Список кабинетов")
async def investigate_accounts(message: Message, state: FSMContext):
    kb = kb_available_accounts()
    await message.answer("Выберите аккаунт", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts)


@router.message(MenuNavigation.api_keys_existing_accounts)
async def edit_account(message: Message, state: FSMContext):
    account = (
        session.query(Account)
        .where(Account.name == message.text.split("Маркетплейс:")[0].strip())
        .first()
    )
    if account is None:
        kb = kb_available_accounts()
        await message.answer("Неверный аккаунт", reply_markup=kb)
        await state.set_state(MenuNavigation.api_keys_existing_accounts)
        return
    kb = kb_edit_account()
    await message.answer(
        f"{account.name}\nМаркетплейс: {account.marketplace}\nAPI ключ:{(len(str(account.api_key))-4)*'*'}{str(account.api_key)[-4:]}"
    )
    await message.answer("Выберите действие", reply_markup=kb)
    await state.update_data(chosen_id=account.id)
    await state.set_state(MenuNavigation.api_keys_existing_accounts_edit_account)


@router.message(
    MenuNavigation.api_keys_existing_accounts_edit_account, F.text == "Назад"
)
async def delete_account_back(message: Message, state: FSMContext):
    kb = kb_available_accounts()
    await message.answer("Выберите аккаунт", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts)


@router.message(
    MenuNavigation.api_keys_existing_accounts_edit_account, F.text == "Удалить"
)
async def delete_account(message: Message, state: FSMContext):
    data = await state.get_data()
    account_id = data["chosen_id"]
    account = session.query(Account).where(Account.id == account_id).first()
    session.delete(account)
    session.commit()
    kb = kb_available_accounts()
    await message.answer("Аккаунт успешно удален", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts)


@router.message(
    MenuNavigation.api_keys_existing_accounts_edit_account, F.text == "Изменить имя"
)
async def edit_account_name(message: Message, state: FSMContext):
    kb = kb_return()
    await message.answer("Введите новое имя", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts_choosing_name)


@router.message(MenuNavigation.api_keys_existing_accounts_choosing_name)
async def edit_account_name_new(message: Message, state: FSMContext):
    if message.text.strip().lower() != "назад":
        data = await state.get_data()
        account_id = data["chosen_id"]
        account = session.query(Account).where(Account.id == account_id).first()
        account.name = message.text.strip()
        session.commit()
    kb = kb_edit_account()
    await message.answer("Выберите действие", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts_edit_account)


@router.message(
    MenuNavigation.api_keys_existing_accounts_edit_account,
    F.text == "Изменить API ключ",
)
async def edit_account_api_key(message: Message, state: FSMContext):
    kb = kb_return()
    await message.answer("Введите новый ключ", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts_choosing_api_key)


@router.message(MenuNavigation.api_keys_existing_accounts_choosing_api_key)
async def edit_account_api_key_new(message: Message, state: FSMContext):
    if message.text.strip().lower() != "назад":
        data = await state.get_data()
        account_id = data["chosen_id"]
        account = session.query(Account).where(Account.id == account_id).first()
        account.api_key = message.text.strip()
        session.commit()
    kb = kb_edit_account()
    await message.answer("Выберите действие", reply_markup=kb)
    await state.set_state(MenuNavigation.api_keys_existing_accounts_edit_account)


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
    if session.query(Account).where(Account.name == message.text.strip()).all():
        await message.answer("Имя занято", reply_markup=kb)
        state.set_state(MenuNavigation.api_keys_choosing_marketplace_on_creation)
        return
    await state.update_data(chosen_name=message.text.strip())
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
