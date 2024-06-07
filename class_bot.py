from aiogram import Bot, Dispatcher, F, types
import logging
from utils.db_api.database import DataBase
from aiogram.filters import Command
from aiogram.types import Message, BotCommand
from blanks.bot_markup import choice_status_task, choice_start
from handlers.callback_handler import callback_handler
from handlers.text_handler import text_handler
from utils.functions.connection_api_qliksense import get_data


logging.basicConfig(level=logging.INFO)


class MyBot:
    def __init__(self, bot: Bot, dp: Dispatcher, db: DataBase):
        self.bot = bot
        self.dp = dp
        self.db = db

    async def start_handler(self, message: Message):
        chat = message.chat.id
        tg_id = message.from_user.id
        username = message.from_user.username

        await self.bot.send_message(
            chat_id=chat,
            text="Здесь можно выбрать:\n"
                 "<b>Состояние сервера</b> - нагрузка на сервера по CPU/RAM\n"
                 "<b>Контроль тасков</b> - информация по таскам:",
            reply_markup=choice_start(),
            parse_mode='html'
        )

    async def register_handlers(self):
        self.dp.callback_query.register(callback=callback_handler)

        self.dp.message.register(self.start_handler, Command('start'))
        self.dp.message.register(get_data, Command('get_data'))
        self.dp.message.register(text_handler, F.text)
        self.dp.callback_query.register(callback_handler)

    async def run(self):
        await self.bot.set_my_commands(commands=
                                       [BotCommand(command='start', description='Запустить'),
                                        BotCommand(command='get_data', description='API QlikSense')],
                                       scope=types.BotCommandScopeAllPrivateChats())
        await self.register_handlers()
        await self.dp.start_polling(self.bot)
