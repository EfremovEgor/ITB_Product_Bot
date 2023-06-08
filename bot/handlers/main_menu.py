from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, invert_f
from keyboards import kb_start_menu
from states import MenuNavigation
from aiogram.fsm.context import FSMContext
from filters import UserAccessFilter

router = Router()
# router.message.filter(UserAccessFilter())


@router.message()
@router.message(F.text.in_(["Меню", "/start"]))
async def start_handler(message: Message, state: FSMContext):
    kb = kb_start_menu()
    await message.answer(
        "Вас приветствует продуктовый телеграм бот, для продолжения, нажмите на нужную вам кнопку.",
        reply_markup=kb,
    )
    await state.set_state(MenuNavigation.main_menu)


@router.message(invert_f(UserAccessFilter()))
async def checker(message: Message, state: FSMContext):
    await message.answer("Пожалуйста обратитесь к администратору для получания доступа")
    state.set_state(MenuNavigation.main_menu)
