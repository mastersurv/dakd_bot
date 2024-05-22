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
                KeyboardButton(text='Назад 🔙')
            ]
        ], resize_keyboard=True)
    return keyboard


def choice_engine() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=f"qlik01 (ttk)", callback_data=f"qlik01"),
        InlineKeyboardButton(text=f"qlik02 (dev)", callback_data=f"qlik02"),
        InlineKeyboardButton(text=f"qlik03 (pl)", callback_data=f"qlik03")
    ]

    builder.row(*buttons, width=1)
    return builder


def back_to_engines() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=f"Удалить сообщение 🧹", callback_data=f"back_engines")
    ]

    builder.row(*buttons, width=1)
    return builder