from aiogram import Bot
from utils.db_api.database import DataBase, DataBaseCPU
from config import TOKEN, db_name, user, password, host, db_name_cpu, user_cpu, password_cpu, host_cpu


def get_bot_and_db():
    bot = Bot(TOKEN)
    db = DataBase(db_name, user, password, host)
    db_cpu_ram = DataBaseCPU(db_name_cpu, user_cpu, password_cpu, host_cpu)
    return bot, db, db_cpu_ram
