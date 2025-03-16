import asyncio

from create_bot import bot, dp
# from db.models import async_main
from handlers import routers
from worker import infinity_worker


async def main():
    # await async_main()
    for router in routers:
        dp.include_router(router)
    print('bot ready')
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        infinity_worker(),
        dp.start_polling(bot)
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")