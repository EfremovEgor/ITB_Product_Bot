import asyncio
import logging

from aiogram import Bot, Dispatcher
import config
from handlers import add_goods_menu, main_menu, manage_users_menu, api_keys_menu


async def main():
    bot = Bot(token=config.BOT_TOKEN)

    dp = Dispatcher()

    dp.include_routers(
        main_menu.router,
        add_goods_menu.router,
        manage_users_menu.router,
        api_keys_menu.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
