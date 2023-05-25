from dash import html, Output, Input, State, dcc
from dash_extensions.enrich import (DashProxy,
                                    ServersideOutputTransform,
                                    MultiplexerTransform)
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate

from info import get_info_client
from pie_chart import pie_chart
from gantta_chart import gantt_chart


CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '400px'})


class EncostDash(DashProxy):
    def __init__(self, **kwargs):
        self.app_container = None
        super().__init__(transforms=[ServersideOutputTransform(),
                                     MultiplexerTransform()], **kwargs)


app = EncostDash(name=__name__)


def get_layout():
    # Получаем данные клиента
    client_info = get_info_client()

    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                        html.Div([
                            html.H1(f"Клиент: {client_info['Клиент']}"),
                            html.H3(f"Сменный день: {client_info['Сменный день']}"),
                            html.H3(f"Точка учета: {client_info['Точка учета']}"),
                            html.H3(f"Начало периода: {client_info['Начало периода']}"),
                            html.H3(f"Конец периода: {client_info['Конец периода']}")
                        ]),
                        dmc.TextInput(
                            label='Введите что-нибудь',
                            id='input'),
                        dmc.Button(
                            'Первая кнопка',
                            id='button1'),
                        dmc.Button(
                            'Вторая кнопка',
                            id='button2'),
                        html.Div(
                            id='output')],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(
                            id='pie-chart',
                            figure=pie_chart(),
                            style={'height': '450px', 'position': 'relative', 'top': '40%', 'left': '50%',
                                   'transform': 'translate(-50%, -50%)'}
                        )
                    ],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(
                            id='gantt-chart',
                            figure=gantt_chart(),
                            style={'height': '400px'}  # Высота диаграммы на 40 пикселей меньше высоты карточки
                        )
                    ], **CARD_STYLE)
                ], span=12),
            ], gutter="xl",)
        ])
    ])



app.layout = get_layout()


@app.callback(
    Output('output', 'children'),
    State('input', 'value'),
    Input('button1', 'n_clicks'),
    prevent_initial_call=True,
)
def update_div1(
    value,
    click
):
    if click is None:
        raise PreventUpdate

    return f'Первая кнопка нажата, данные: {value}'


@app.callback(
    Output('output', 'children'),
    State('input', 'value'),
    Input('button2', 'n_clicks'),
    prevent_initial_call=True,
)
def update_div2(
    value,
    click
):
    if click is None:
        raise PreventUpdate

    return f'Вторая кнопка нажата, данные: {value}'


if __name__ == '__main__':
    app.run_server(debug=True)

