from aiogram import F, Router
from aiogram.types import Message
from keyboards import (
    kb_manage_users_menu,
    kb_manage_users_add_new_employee,
    kb_manage_users_grant_access,
    kb_start_menu,
    kb_manage_users_investigate_employees,
    kb_manage_users_remove_access,
)
from states import MenuNavigation
from aiogram.fsm.context import FSMContext
from filters import UserAccessFilter
from database import session
from models import UnregisteredUser, RegisteredUser

router = Router()
router.message.filter(UserAccessFilter())


@router.message(MenuNavigation.main_menu, F.text == "Пользователи")
async def manage_users(message: Message, state: FSMContext):
    kb = kb_manage_users_menu()
    await message.answer("Выберите действие", reply_markup=kb)
    await state.set_state(MenuNavigation.manage_users)


@router.message(MenuNavigation.manage_users, F.text == "Новый сотрудник")
async def show_unregistered_users(message: Message, state: FSMContext):
    kb = kb_manage_users_add_new_employee()
    await message.answer("Выберите пользователя", reply_markup=kb)
    await state.set_state(MenuNavigation.manage_users_adding_new_employee)


@router.message(MenuNavigation.manage_users_adding_new_employee)
async def manage_users(message: Message, state: FSMContext):
    if message.text in ["Меню", "/start"]:
        kb = kb_start_menu()
        await state.clear()
        await state.set_state(MenuNavigation.main_menu)
        await message.answer(text="Меню", reply_markup=kb)

        return
    try:
        text = int(message.text.split(" ID:")[1])
        user = (
            session.query(UnregisteredUser)
            .filter(UnregisteredUser.telegram_id == text)
            .first()
        )
        kb = kb_manage_users_grant_access()
        if user is None:
            raise Exception
        await message.answer(
            f"Ник: {user.name}\nTелеграм id: {user.telegram_id}\nПоследнее сообщение отправлено в:\n{user.last_sent_message}",
            reply_markup=kb,
        )
        await state.update_data(chosen_id=user.telegram_id)
        await state.set_state(MenuNavigation.manage_users_grant_access)
    except:
        kb = kb_manage_users_add_new_employee()
        await message.answer("Выберите пользователя", reply_markup=kb)
        await state.set_state(MenuNavigation.manage_users_adding_new_employee)


@router.message(MenuNavigation.manage_users_grant_access)
async def grant_access(message: Message, state: FSMContext):
    if message.text == "Назад":
        kb = kb_manage_users_add_new_employee()
        await message.answer("Выберите пользователя", reply_markup=kb)
        await state.set_state(MenuNavigation.manage_users_adding_new_employee)
    elif message.text == "Дать доступ":
        data = await state.get_data()

        user = (
            session.query(UnregisteredUser)
            .filter(UnregisteredUser.telegram_id == data["chosen_id"])
            .first()
        )
        session.delete(user)
        session.add(
            RegisteredUser(
                telegram_id=user.telegram_id,
                name=user.name,
                last_sent_message=user.last_sent_message,
            )
        )
        session.commit()
        kb = kb_start_menu()
        await message.answer("Доступ дан", reply_markup=kb)
        await state.clear()
        await state.set_state(MenuNavigation.main_menu)
    else:
        kb = kb_manage_users_grant_access()
        await message.answer(
            "Выберите действие",
            reply_markup=kb,
        )
        await state.set_state(MenuNavigation.manage_users_grant_access)


@router.message(MenuNavigation.manage_users, F.text == "Список сотрудников")
async def show_employees(message: Message, state: FSMContext):
    kb = kb_manage_users_investigate_employees()
    await message.answer("Выберите пользователя", reply_markup=kb)
    await state.set_state(MenuNavigation.manage_users_investigating_employees)


@router.message(MenuNavigation.manage_users_investigating_employees)
async def manage_employee(message: Message, state: FSMContext):
    if message.text in ["Меню", "/start"]:
        kb = kb_start_menu()
        await state.clear()
        await state.set_state(MenuNavigation.main_menu)
        await message.answer(text="Меню", reply_markup=kb)
        return
    try:
        text = int(message.text.split(" ID:")[1])
        user = (
            session.query(RegisteredUser)
            .filter(RegisteredUser.telegram_id == text)
            .first()
        )
        kb = kb_manage_users_remove_access()
        if user is None:
            raise Exception
        await message.answer(
            f"Ник: {user.name}\nTелеграм id: {user.telegram_id}\nПоследнее сообщение отправлено в:\n{user.last_sent_message}",
            reply_markup=kb,
        )
        await state.update_data(chosen_id=user.telegram_id)
        await state.set_state(MenuNavigation.manage_users_remove_access)
    except:
        kb = kb_manage_users_investigate_employees()
        await message.answer("Выберите пользователя", reply_markup=kb)
        await state.set_state(MenuNavigation.manage_users_investigating_employees)


@router.message(MenuNavigation.manage_users_remove_access)
async def remove_access(message: Message, state: FSMContext):
    if message.text == "Назад":
        kb = kb_manage_users_investigate_employees()
        await message.answer("Выберите пользователя", reply_markup=kb)
        await state.set_state(MenuNavigation.manage_users_investigating_employees)
    elif message.text == "Забрать доступ":
        data = await state.get_data()

        user = (
            session.query(RegisteredUser)
            .filter(RegisteredUser.telegram_id == data["chosen_id"])
            .first()
        )
        session.delete(user)
        session.add(
            UnregisteredUser(
                telegram_id=user.telegram_id,
                name=user.name,
                last_sent_message=user.last_sent_message,
            )
        )
        session.commit()
        kb = kb_start_menu()
        await message.answer("Доступ убран", reply_markup=kb)
        await state.clear()
        await state.set_state(MenuNavigation.main_menu)
    else:
        kb = kb_manage_users_remove_access()
        await message.answer(
            "Выберите действие",
            reply_markup=kb,
        )
        await state.set_state(MenuNavigation.manage_users_remove_access)
