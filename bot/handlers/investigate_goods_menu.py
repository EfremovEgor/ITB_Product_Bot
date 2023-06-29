from aiogram import F, Router
from aiogram.types import Message
from keyboards import (
    kb_choosing_marketplace,
    kb_available_goods,
    kb_delete_good,
)
from states import MenuNavigation, AvailableButtonNames
from aiogram.fsm.context import FSMContext
from filters import UserAccessFilter
from database import session
from models import Good

router = Router()
router.message.filter(UserAccessFilter())


@router.message(MenuNavigation.main_menu, F.text == "Список товаров")
async def investigate_goods(message: Message, state: FSMContext):
    kb = kb_choosing_marketplace()
    await message.answer("Выберите площадку", reply_markup=kb)
    await state.set_state(MenuNavigation.investigate_goods_choosing_marketplace)


@router.message(
    MenuNavigation.investigate_goods_choosing_marketplace,
    F.text.in_(AvailableButtonNames.marketplaces),
)
async def marketplace_choosen(message: Message, state: FSMContext):
    await state.update_data(chosen_marketplace=message.text.strip())
    kb = kb_available_goods(message.text.strip())
    await message.answer("Выберите товар", reply_markup=kb)
    await state.set_state(MenuNavigation.investigate_goods_choosing_good)


@router.message(MenuNavigation.investigate_goods_choosing_good)
async def marketplace_choosen(message: Message, state: FSMContext):
    chosen_good_id = message.text
    data = await state.get_data()
    if (
        session.query(Good)
        .where(
            Good.market_place_id == int(chosen_good_id)
            and Good.marketplace == data["chosen_marketplace"].capitalize()
        )
        .all()
    ):
        await state.update_data(chosen_good_id=int(message.text))
    kb = kb_delete_good()
    await message.answer("Выберите действие", reply_markup=kb)
    await state.set_state(MenuNavigation.investigate_goods_edit_good)


@router.message(MenuNavigation.investigate_goods_edit_good)
async def delete_account(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.strip() == "Удалить":
        good = (
            session.query(Good)
            .where(
                Good.market_place_id == data["chosen_good_id"]
                and Good.marketplace == data["chosen_marketplace"].capitalize()
            )
            .first()
        )

        session.delete(good)
        session.commit()
        kb = kb_available_goods(data["chosen_marketplace"])
        await message.answer("Товар успешно удален", reply_markup=kb)
        await state.set_state(MenuNavigation.investigate_goods_choosing_good)
    if message.text.strip() == "Назад":
        kb = kb_available_goods(data["chosen_marketplace"])
        await message.answer("Выберите товар", reply_markup=kb)
        await state.set_state(MenuNavigation.investigate_goods_choosing_good)
