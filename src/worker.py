from datetime import datetime, time
import asyncio
from src.create_bot import bot
from src.db.Payments.get_data_time_db import get_data_time


async def infinity_worker():
    while True:
        now_time = time(datetime.now().time().hour, datetime.now().time().minute, 0)
        now_day = datetime.now().date().day
        answer = await get_data_time(now_day, now_time)
        print(now_day, now_time, datetime.now().time())
        if answer:
            for data in answer:
                print(data)
                await bot.send_message(chat_id=data['chat_id'], text=f'Вам нужно оплатить:\n'
                                                                     f'Платеж {data["name_payment"]}\n'
                                                                     f'Сумма {data["cost_payment"]}\n')
        await asyncio.sleep(60)
