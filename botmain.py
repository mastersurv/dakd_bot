from aiogram import Dispatcher, Bot
import asyncio
from class_bot import MyBot
from utils.db_api.database import DataBase
from config import TOKEN, db_name, user, password, host
from aiogram.client.session.aiohttp import AiohttpSession



bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, session=AiohttpSession())
db = DataBase(db_name, user, password, host)

my_bot = MyBot(bot=bot, dp=dp, db=db)
asyncio.run(my_bot.run())
