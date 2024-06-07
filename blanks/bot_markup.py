from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def choice_start() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Состояние сервера ⚙'),
                KeyboardButton(text='Контроль тасков 📋')
            ]
        ], resize_keyboard=True)
    return keyboard


def choice_engines_status() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Engine из QMS ⚙'),
                KeyboardButton(text='Состояние CPU/RAM 📈')
            ],
            [
                KeyboardButton(text='Назад 🔙')
            ]
        ], resize_keyboard=True)
    return keyboard


def choice_type_tasks() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Manually 🔧'),
                KeyboardButton(text='Scheduler ⏳')
            ],
            [
                KeyboardButton(text='Назад 🔙')
            ]
        ], resize_keyboard=True)
    return keyboard


def choice_status_task() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Started 🔁'),
                KeyboardButton(text='Aborted ❎')
            ],
            [
                KeyboardButton(text='Failed ❌'),
                KeyboardButton(text='Success ✔')
            ],
            [
                KeyboardButton(text='Назад ⏪')
            ]
        ], resize_keyboard=True)
    return keyboard


def choice_engine() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=f"qlik01 (ttk)", callback_data=f"qlik01 1"),  # 1 - час, за который берутся данные
        InlineKeyboardButton(text=f"qlik02 (dev)", callback_data=f"qlik02 1"),
        InlineKeyboardButton(text=f"qlik03 (pl)", callback_data=f"qlik03 1")
    ]

    builder.row(*buttons, width=1)
    return builder


def choice_another_interval(callback) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    buttons = [  # f"{callback.split()[0]} 4"  - замена значения колбэка, Example: qlik01 1 -> qlik01 4
        InlineKeyboardButton(text=f"4️⃣ часа", callback_data=f"{callback.split()[0]} 4"),  # 4 - часа, за которые берутся данные
        InlineKeyboardButton(text=f"1️⃣2️⃣ часов", callback_data=f"{callback.split()[0]} 12"),
        InlineKeyboardButton(text=f"2️⃣4️⃣ часа", callback_data=f"{callback.split()[0]} 24"),
        InlineKeyboardButton(text=f"Удалить сообщение 🧹", callback_data=f"back_engines")
    ]

    builder.row(*buttons, width=1)
    return builder