import asyncio

from create_bot import bot, dp
from db.models import async_main
from handlers import routers


async def main():
    await async_main()
    for router in routers:
        dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")