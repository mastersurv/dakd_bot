import aiogram
from utils.functions.get_bot_and_db import get_bot_and_db

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
from datetime import datetime

bot, db = get_bot_and_db()


async def funnel():
    users = db.get_users()
    for tg_id in users:
        beginning_minutes, beginning_day, beginning_month = 0, 0, 0

        now_minutes = datetime.now().hour * 60 + datetime.now().minute
        now_day = datetime.now().day
        now_month = datetime.now().month

        beginning_time = db.get_beginning_time(tg_id=tg_id)
        try:
            beginning_minutes = int(beginning_time.split("_")[0])
            beginning_day = int(beginning_time.split("_")[1])
            beginning_month = int(beginning_time.split("_")[2])
        except IndexError:
            pass

        is_begin = db.get_is_begin(tg_id=tg_id)

        if is_begin and beginning_minutes == now_minutes and (
                (beginning_day == now_day - 1 and beginning_month == now_month) or (
                now_day == 1 and beginning_month == now_month - 1)):

            db.update_is_begin(tg_id=tg_id)




event_loop = asyncio.get_event_loop()
while True:
    # event_loop.run_until_complete(asyncio.sleep(60))
    event_loop.run_until_complete(funnel())
