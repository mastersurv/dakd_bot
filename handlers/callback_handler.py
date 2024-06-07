from aiogram.types import CallbackQuery, FSInputFile
import plotly.graph_objects as go
import plotly.io as pio
from utils.functions.get_bot_and_db import get_bot_and_db
from blanks.bot_markup import choice_another_interval
from datetime import timedelta
import pandas as pd


async def visualize_data(records_cpu, records_ram, interval=None):
    """Функция построения графика"""
    def get_intervals(records, interval):
        """Функция получения максимальных и минимальных значений для каждого интервала"""
        slice = 5 if interval == 12 else 10  # если выбран интервал 12 часов - то значения каждые 5 минут, для 24ч - 10м
        intervals = []
        for i in range(0, len(records), slice):
            chunk = records[i:i + slice]
            if chunk:
                max_record = max(chunk, key=lambda x: x['Последнее_значение'])
                # min_record = min(chunk, key=lambda x: x['Последнее_значение'])
                intervals.append(max_record)
                # intervals.append(min_record)
        return intervals

    if interval in [12, 24]:
        records_cpu = get_intervals(records_cpu, interval)
        records_ram = get_intervals(records_ram, interval)

    # Преобразование времени к строке для отображения для CPU
    times_with_offset_cpu = [(record['Время_проверки'] + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S') for record in records_cpu]
    loads_cpu = [f"{record['Последнее_значение']:.1f}" for record in records_cpu]

    last_time_cpu = records_cpu[0]['Время_проверки']  # самое недавнее значение времени нагрузки CPU
    first_time_cpu = records_cpu[-1]['Время_проверки']  # самое позднее значение времени нагрузки CPU
    time_limit_over = last_time_cpu + timedelta(minutes=5)  # граница от недавнего значения +5 минут
    time_limit_under = first_time_cpu - timedelta(minutes=5)  # граница от позднего значения -5 минут

    # берём значения по RAM, которые попадают по времени со значениями CPU (для одинаковой длины графиков)
    filtered_records_ram = [record for record in records_ram if time_limit_under <= record['Время_проверки'] <= time_limit_over]

    # берём каждое 10-ое значение для RAM
    times_with_offset_ram = [(record['Время_проверки'] + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S') for record in filtered_records_ram][::10]
    loads_ram = [f"{round(record['Последнее_значение'])}" for record in filtered_records_ram][::10]

    fig = go.Figure()

    # Добавление трассы для CPU
    fig.add_trace(go.Scatter(
        x=times_with_offset_cpu,
        y=[float(value) for value in loads_cpu],
        mode='lines+markers+text',
        name='CPU',
        line=dict(color='blue', width=2),
        marker=dict(color='red', size=7, symbol='circle'),
        text=loads_cpu,
        textposition='top center',
        showlegend=True
    ))

    # Добавление трассы для RAM
    fig.add_trace(go.Scatter(
        x=times_with_offset_ram,
        y=[float(value) for value in loads_ram],
        mode='lines+markers+text',
        name='RAM',
        line=dict(color='green', width=2),  # Используем зеленый цвет для линии RAM
        marker=dict(color='purple', size=7, symbol='square'),  # Используем фиолетовый цвет для маркеров RAM
        text=loads_ram,
        textposition='top center',
        showlegend=True
    ))

    # Настройка осей и заголовков
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            xanchor="right",
            x=1,
            y=1
        ),
        plot_bgcolor='rgb(230, 230, 230)',
        paper_bgcolor='rgb(255, 255, 255)',
    )
    fig.update_yaxes(range=[0, 100], zeroline=True, zerolinecolor='black')

    # Сохранение графика в виде изображения
    image_path = 'graph.png'
    pio.write_image(fig, image_path, format='png', width=1903, height=904)

    # fig.show()


async def callback_handler(call: CallbackQuery):
    await call.answer()
    bot, db, db_cpu = get_bot_and_db()
    tg_id = call.from_user.id
    callback = call.data
    m_id = call.message.message_id
    print(callback)

    if callback.startswith('qlik01'):
        interval = int(callback.split()[1])  # Example: callback=qlik01 1  (1 - 1 час) -> выборка на 60 записей
        inter_to_minutes = {1: 60, 4: 240, 12: 720, 24: 1440}
        count = inter_to_minutes[interval]  # If interval == 4 -> count = 240

        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)  # печатает...
        records_cpu = await db_cpu.return_cpu_or_memory('qlik01', count, 'CPU')
        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)
        records_ram = await db_cpu.return_cpu_or_memory('qlik01', count, 'Memory')
        await visualize_data(records_cpu, records_ram, interval)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik01 (ttk)</b> - Центральная нода, которая '
                                                             'контролирует все перезагрузки в системе QlikSense\n\n'
                                                             'Ниже можно выбрать нужный интервал',
                                        reply_markup=choice_another_interval(callback).as_markup(), parse_mode='html')

    elif callback.startswith('qlik02'):
        interval = int(callback.split()[1])  # Example: callback=qlik01 1  (1 - 1 час) -> выборка на 60 записей
        inter_to_minutes = {1: 60, 4: 240, 12: 720, 24: 1440}
        count = inter_to_minutes[interval]  # If interval == 4 -> count = 240

        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)  # печатает...
        records_cpu = await db_cpu.return_cpu_or_memory('qlik02', count, 'CPU')
        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)
        records_ram = await db_cpu.return_cpu_or_memory('qlik02', count, 'Memory')
        await visualize_data(records_cpu, records_ram, interval)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik02 (dev)</b> - Нода для разработчиков\n\n'
                                                             'Ниже можно выбрать нужный интервал',
                                        reply_markup=choice_another_interval(callback).as_markup(), parse_mode='html')

    elif callback.startswith('qlik03'):
        interval = int(callback.split()[1])  # Example: callback=qlik01 1  (1 - 1 час) -> выборка на 60 записей
        inter_to_minutes = {1: 60, 4: 240, 12: 720, 24: 1440}
        count = inter_to_minutes[interval]  # If interval == 4 -> count = 240

        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)  # печатает...
        records_cpu = await db_cpu.return_cpu_or_memory('qlik03', count, 'CPU')
        await bot.send_chat_action(call.message.chat.id, action="typing", request_timeout=5)
        records_ram = await db_cpu.return_cpu_or_memory('qlik03', count, 'Memory')
        await visualize_data(records_cpu, records_ram, interval)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik03 (pl)</b> - Нода для ежедневной планёрки\n\n'
                                                             'Ниже можно выбрать нужный интервал',
                                        reply_markup=choice_another_interval(callback).as_markup(), parse_mode='html')

    elif callback == "back_engines":
        await call.message.delete()
