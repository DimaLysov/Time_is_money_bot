import asyncio

from create_bot import bot, dp
from handlers import routers


async def main():
    for router in routers:
        dp.include_router(router)
    print('bot ready')
    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot)
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")