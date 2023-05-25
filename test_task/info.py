import sqlite3
import pandas as pd
from datetime import datetime


def get_info_client():
    """Информация о клиенте в первой карточке"""
    with sqlite3.connect(r'../testDB.db') as conn:
        df = pd.read_sql_query('SELECT * FROM sources', conn)

    info = df.iloc[0]
    # Клиент
    client_name = info['client_name']
    # Сменный день
    shift_day = info['shift_day']
    # Точка учета
    endpoint_name = info['endpoint_name']
    # Начало периода
    dt_state_begin = datetime.strptime(info['state_begin'], '%Y-%m-%d %H:%M:%S.%f')
    state_begin = dt_state_begin.strftime('%H:%M:%S (%d.%m)')

    # Конец периода
    dt_state_end = datetime.strptime(df.iloc[-1]['state_end'], '%Y-%m-%d %H:%M:%S.%f')
    state_end = dt_state_end.strftime('%H:%M:%S (%d.%m)')

    return {'Клиент': client_name,
            'Сменный день': shift_day,
            'Точка учета': endpoint_name,
            'Начало периода': state_begin,
            'Конец периода': state_end}

