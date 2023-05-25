import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px


def pie_chart():
    """Круговая диаграмма"""
    with sqlite3.connect(r'../testDB.db') as conn:
        df = pd.read_sql_query('SELECT * FROM sources', conn)

    # Вычисляем общее время работы и добавляем столбец 'total_duration', содержащий значение в минутах
    df['total_duration'] = df['duration_hour'] * 60 + df['duration_min']

    # Группируем данные по статусу и вычисляем сумму 'total_duration' для каждого статуса
    grouped = df.groupby('reason')['total_duration'].sum()

    # Вычисляем процент времени для каждого статуса
    percentages = (grouped / grouped.sum() * 100).sort_values(ascending=False)

    # Создаем диаграмму с использованием Plotly
    fig = go.Figure(data=[go.Pie(labels=percentages.index, values=percentages, marker_colors=px.colors.qualitative.Set1)])

    return fig

