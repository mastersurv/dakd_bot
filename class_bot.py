from aiogram import Bot, Dispatcher, F, types
import asyncio
import logging
from utils.db_api.database import DataBase
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from handlers.callback_handler import callback_handler
from blanks.bot_markup import choice_status_task, choice_start
from handlers.callback_handler import callback_handler
from handlers.text_handler import text_handler


logging.basicConfig(level=logging.INFO)


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message):
        chat = message.chat.id
        print(chat)
        tg_id = message.from_user.id
        username = message.from_user.username

        await self.bot.send_message(
            chat_id=chat,
            text="Выберите нужное:",
            reply_markup=choice_start()
        )


    async def register_handlers(self):
        self.dp.callback_query.register(callback=callback_handler)

        self.dp.message.register(self.start_handler, Command('start'))
        self.dp.message.register(text_handler, F.text)
        self.dp.callback_query.register(callback_handler)

    async def run(self):
        await self.bot.set_my_commands(commands=[BotCommand(command='start', description='Запустить')],
                                       scope=types.BotCommandScopeAllPrivateChats())
        await self.register_handlers()
        await self.dp.start_polling(self.bot)
