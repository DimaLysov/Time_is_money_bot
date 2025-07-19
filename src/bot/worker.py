import calendar
from datetime import datetime, time, date
import asyncio

import pytz

from create_bot import bot
from db.Payments.get_data_time_db import get_data_time
from utils.all_time_zone import rus_time_zone


async def infinity_worker():
    while True:
        for time_zone in rus_time_zone:
            tz = pytz.timezone(rus_time_zone[time_zone])
            now_date = datetime.now(tz)
            now_time = time(now_date.time().hour, now_date.time().minute, 0)
            now_day = now_date.date().day
            days_in_month = calendar.monthrange(now_date.year, now_date.month)[1]
            answer = await get_data_time(now_day, now_time, days_in_month, time_zone)
            if answer:
                for data in answer:
                    print(data)
                    await bot.send_message(chat_id=data['chat_id'], text=f'<b>🔔Вам нужно оплатить:🔔</b>\n\n'
                                                                         f'<b>{data["name_payment"]}</b>\n\n'
                                                                         f'<b>Сумма:</b> {data["cost_payment"]} рублей\n\n'
                                                                         f'<b>До</b> {data["pyment_date"]} числа')
        await asyncio.sleep(60 - datetime.now().second)