from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards import (
    kb_add_goods_choosing_account,
    kb_add_goods_choosing_notification,
    kb_choosing_marketplace,
    kb_go_to_start_menu,
    kb_start_menu,
)
from states import MenuNavigation, AvailableButtonNames
from aiogram.fsm.context import FSMContext
from utils import get_accounts
from filters import UserAccessFilter

router = Router()
router.message.filter(UserAccessFilter())


@router.message(MenuNavigation.main_menu, F.text == "Добавить товар")
async def add_good(message: Message, state: FSMContext):
    kb = kb_choosing_marketplace()
    await message.answer("Выберите площадку", reply_markup=kb)
    await state.set_state(MenuNavigation.add_goods_choosing_marketplace)


@router.message(
    MenuNavigation.add_goods_choosing_marketplace,
    F.text.in_(AvailableButtonNames.marketplaces),
)
async def marketplace_choosen(message: Message, state: FSMContext):
    await state.update_data(chosen_marketplace=message.text)
    accounts = get_accounts()
    kb = kb_add_goods_choosing_account(accounts)
    await message.answer("Выберите аккаунт", reply_markup=kb)
    await state.set_state(MenuNavigation.add_goods_choosing_account)


@router.message(
    MenuNavigation.add_goods_choosing_account,
    F.text.in_(get_accounts()),
)
async def account_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_account=message.text)
    user_data = await state.get_data()
    kb = kb_add_goods_choosing_notification(
        AvailableButtonNames.notifications[user_data["chosen_marketplace"].lower()]
    )
    await message.answer("Выберите оповещение", reply_markup=kb)
    await state.set_state(MenuNavigation.add_goods_choosing_notification)


@router.message(MenuNavigation.add_goods_choosing_notification)
async def notification_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()

    if (
        message.text
        not in AvailableButtonNames.notifications[
            user_data["chosen_marketplace"].lower()
        ]
    ):
        kb = kb_add_goods_choosing_notification(
            AvailableButtonNames.notifications[user_data["chosen_marketplace"]]
        )
        await message.answer("Выберите оповещение", reply_markup=kb)
        await state.set_state(MenuNavigation.add_goods_choosing_notification)
        return
    kb = kb_go_to_start_menu()
    await state.update_data(chosen_notification=message.text.lower())
    await message.answer("Введите ID товара", reply_markup=kb)
    await state.set_state(MenuNavigation.add_goods_inserting_id)


@router.message(MenuNavigation.add_goods_inserting_id)
async def id_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_id=message.text)
    user_data = await state.get_data()
    kb = kb_start_menu()
    await message.answer("Товар успешно зарегистрирован.", reply_markup=kb)
    # f"{user_data['chosen_notification'],user_data['chosen_marketplace'],user_data['chosen_account'],user_data['chosen_id']}"
    await state.clear()
    await state.set_state(MenuNavigation.main_menu)
