from aiogram.types import Message, FSInputFile
from utils.functions.get_bot_and_db import get_bot_and_db
from aiogram.exceptions import TelegramBadRequest
from blanks.bot_markup import choice_engines_status, choice_status_task, choice_start, choice_engine
from threading import Thread


async def return_status(percent) -> str:
    last_value = percent[0]['Последнее_значение']
    last_value_rounded = round(last_value)
    if last_value_rounded < 20:
        status = "low 😴"
    elif 20 <= last_value <= 80:
        status = "normal 🆗"
    else:
        status = "high ❗"
    return status


async def text_handler(message: Message):
    bot, db, db_cpu = get_bot_and_db()
    tg_id = message.from_user.id
    m_id = message.message_id
    chat_type = message.chat.type
    text = message.text

    async def write_to_file_and_send(filename: str, status):
        try:
            with open(filename, 'w', encoding='utf-8') as st:
                text = await db.get_tasks_table(status)
                print(text)
                st.write(text)
            await message.answer_document(document=FSInputFile(filename))
        except Exception as e:
            print(e)

    if text == 'Состояние сервера ⚙':
        await message.answer("Выберите посмотреть состояние серверов в QMS или нагрузку по CPU/RAM:",
                                reply_markup=choice_engines_status())

    elif text == 'Контроль тасков 📋':
        await message.answer("Выберите интересующий статус тасков:",
                             reply_markup=choice_status_task())

    elif text == 'Состояние CPU/RAM 📈':  # TODO ----------------
        await bot.send_chat_action(message.chat.id, action="typing", request_timeout=5)

        # qlik01 ttk
        record_central = await db_cpu.return_cpu_or_memory_ttk(1, 'CPU')
        last_value = record_central[0]['Последнее_значение']
        last_value_rounded = round(last_value)
        formatted_string = f"qlik01 (ttk) <b>{last_value_rounded}% - {await return_status(record_central)}</b>"
        await bot.send_chat_action(message.chat.id, action="typing", request_timeout=5)

        # qlik02 dev
        record_dev = await db_cpu.return_cpu_or_memory_dev(1, 'CPU')
        last_value = record_dev[0]['Последнее_значение']
        last_value_rounded = round(last_value)
        formatted_string += f"\n\nqlik02 (dev) <b>{last_value_rounded}% - {await return_status(record_dev)}</b>"
        await bot.send_chat_action(message.chat.id, action="typing", request_timeout=5)

        # qlik03 pl
        record_qlik03 = await db_cpu.return_cpu_or_memory_pl(1, 'CPU')
        last_value = record_qlik03[0]['Последнее_значение']
        last_value_rounded = round(last_value)
        formatted_string += (f"\n\nqlik03 (pl) <b>{last_value_rounded}% - {await return_status(record_qlik03)}</b>\n\n"
                             f"Выберите сервер для детальной информации:")
        await bot.send_chat_action(message.chat.id, action="typing", request_timeout=5)

        await message.answer(text=formatted_string, parse_mode='html', reply_markup=choice_engine().as_markup())

    elif text == 'Started 🔁':
        try:
            await message.answer(text=await db.get_tasks(2), parse_mode='html')
        except TelegramBadRequest as tbr:
            if not await db.get_tasks(2):
                await message.answer(text='Запущенных тасков нет 🎈', parse_mode='html')
            else:
                await write_to_file_and_send('started_tasks.txt', 2)

    elif text == 'Aborted ❎':
        try:
            await message.answer(text=await db.get_tasks(6), parse_mode='html')
        except TelegramBadRequest:
            await write_to_file_and_send('aborted_tasks.txt', 6)

    elif text == 'Failed ❌':
        try:
            await message.answer(text=await db.get_tasks(8), parse_mode='html')
        except TelegramBadRequest:
            await write_to_file_and_send('failed_tasks.txt', 8)

    elif text == 'Success ✔':
        await write_to_file_and_send('success_tasks.txt', 7)

    elif text == 'Назад 🔙':
        await message.answer(text="Выберите нужное:", reply_markup=choice_start())
