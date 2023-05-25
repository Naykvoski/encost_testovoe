import sqlite3
import pandas as pd
import plotly.express as px
import locale


def gantt_chart():
    """Третья диаграмма ганта"""
    locale.setlocale(locale.LC_TIME, 'ru_RU')

    # Подключение к базе данных SQLite
    with sqlite3.connect(r'../testDB.db') as conn:
        df = pd.read_sql_query('SELECT * FROM sources', conn)

    # Преобразование столбца 'state_begin' в формат даты и времени
    df['state_begin'] = pd.to_datetime(df['state_begin'])
    df['state_end'] = pd.to_datetime(df['state_end'])

    # Форматирование начала интервала в требуемом формате
    df['state_begin_formatted'] = df['state_begin'].dt.strftime('%H:%M:%S (%d.%m)')

    # Преобразование столбца 'duration_min' в формат с двумя цифрами после запятой
    df['duration_min'] = df['duration_min'].round(2)

    # Создание дополнительных столбцов для наведения мыши
    df['shift_day_formatted'] = pd.to_datetime(df['shift_day']).dt.strftime('%d.%m.%Y')

    # Создание диаграммы Ганта с помощью Plotly
    fig = px.timeline(df, x_start="state_begin", x_end="state_end", y="endpoint_name",
                      hover_data=["state", "reason", "state_begin_formatted", "duration_min", "shift_day_formatted",
                                  "period_name", "operator"],
                      color="state",
                      color_discrete_sequence=px.colors.qualitative.Set1)

    # Настройка названий столбцов при наведении мыши
    fig.update_traces(hovertemplate='<b>Клиент:</b> %{y}<br>' +
                                    '<b>Состояние:</b> %{customdata[0]}<br>' +
                                    '<b>Причина:</b> %{customdata[1]}<br>' +
                                    '<b>Начало:</b> %{customdata[2]}<br>' +
                                    '<b>Длительность:</b> %{customdata[3]} мин<br>' +
                                    '<b>Сменный день:</b> %{customdata[4]}<br>' +
                                    '<b>Смена:</b> %{customdata[5]}<br>' +
                                    '<b>Оператор:</b> %{customdata[6]}<br>' +
                                    '<extra></extra>')

    # Инвертирование оси Y для отображения клиентов сверху вниз
    fig.update_yaxes(autorange="reversed")

    # Добавление каждого часа на диаграмму
    min_start = df['state_begin'].min().floor("H")
    max_end = df['state_end'].max().ceil("H")
    num_hours = int((max_end - min_start).total_seconds() / 3600)  # Количество часов
    tickvals = [min_start + pd.Timedelta(hours=i) for i in range(num_hours + 1)]  # Метки для каждого часа
    ticktext = [dt.strftime('%H:%M') for dt in tickvals]  # Формат времени для меток

    # Обновление оси X с метками для каждого часа
    fig.update_xaxes(
        tickvals=tickvals,
        ticktext=ticktext,
        title_text="Время"
    )

    # Настройка стилей для таблицы при наведении
    fig.update_layout(hovermode="closest")  # Активация ближайшего режима наведения
    fig.update_layout(hoverlabel=dict(bgcolor="white", font=dict(color="black")))  # Установка белого фона и черного цвета шрифта для таблицы

    fig.update_layout(title_text="График Состояний", title_x=0.5)

    return fig
