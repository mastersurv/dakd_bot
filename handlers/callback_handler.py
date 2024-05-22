from aiogram.types import CallbackQuery, FSInputFile
import plotly.graph_objects as go
import plotly.io as pio
from utils.functions.get_bot_and_db import get_bot_and_db
from blanks.bot_markup import back_to_engines
from datetime import timedelta
import pandas as pd



async def visualize_data(records_cpu, records_ram):
    # Преобразование времени к строке для отображения
    times_with_offset_cpu = [(record['Время_проверки'] + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S') for record in records_cpu]
    loads_cpu = [f"{record['Последнее_значение']:.1f}" for record in records_cpu]

    # Преобразование времени к строке для отображения
    times_with_offset_ram = [(record['Время_проверки'] + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S') for record in records_ram]
    loads_ram = [f"{record['Последнее_значение']:.1f}" for record in records_ram]

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

    fig.show()


async def callback_handler(call: CallbackQuery):
    await call.answer()
    bot, db, db_cpu = get_bot_and_db()
    tg_id = call.from_user.id
    callback = call.data
    m_id = call.message.message_id
    print(callback)

    if callback.startswith('qlik01'):
        records_cpu = await db_cpu.return_cpu_or_memory_ttk(60, 'CPU')
        records_ram = await db_cpu.return_cpu_or_memory_ttk(60, 'Memory')
        await visualize_data(records_cpu, records_ram)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik01 (ttk)</b> - Центральная нода, которая '
                                                             'контролирует все перезагрузки в системе QlikSense',
                                        reply_markup=back_to_engines().as_markup(), parse_mode='html')

    elif callback.startswith('qlik02'):
        records_cpu = await db_cpu.return_cpu_or_memory_dev(60, 'CPU')
        records_ram = await db_cpu.return_cpu_or_memory_dev(60, 'Memory')
        await visualize_data(records_cpu, records_ram)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik02 (dev)</b> - Нода для разработчиков',
                                        reply_markup=back_to_engines().as_markup(), parse_mode='html')

    elif callback.startswith('qlik03'):
        records_cpu = await db_cpu.return_cpu_or_memory_pl(60, 'CPU')
        records_ram = await db_cpu.return_cpu_or_memory_pl(60, 'Memory')
        await visualize_data(records_cpu, records_ram)
        graph = FSInputFile('graph.png')
        await call.message.answer_photo(photo=graph, caption='<b>qlik03 (pl)</b> - Нода для ежедневной планёрки',
                                        reply_markup=back_to_engines().as_markup(), parse_mode='html')

    elif callback == "back_engines":
        await call.message.delete()