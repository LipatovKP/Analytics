import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('А.csv')
df['Total_Cost'] = df['Цена, ₽'] * df['Остаток']

app = Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.H1('Умный дашборд склада', style={'display': 'inline-block', 'fontFamily': 'Segoe UI'}),

        html.Div([
            html.Small("Оцененная стоимость выборки:"),
            html.Div(id='total-stock-value', style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#2c3e50'})
        ], style={
            'float': 'right', 'backgroundColor': '#f1f2f6', 'padding': '20px',
            'borderRadius': '15px', 'textAlign': 'right', 'minWidth': '250px'
        })
    ], style={'padding': '20px'}),

    html.Div([
        html.Div([
            html.Label("Категории:"),
            dcc.Dropdown(
                id='cat-drop',
                options=[{'label': c, 'value': c} for c in sorted(df['Категория'].unique())],
                multi=True,
                clearable=True,
                placeholder="Выберите категории..."
            ),
        ], style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%'}),

        html.Div([
            html.Label("Бренды:"),
            dcc.Dropdown(
                id='brand-drop',
                multi=True,
                placeholder="Выберите бренды..."
            ),
        ], style={'width': '45%', 'display': 'inline-block'}),
    ], style={'padding': '20px', 'backgroundColor': '#ffffff', 'boxShadow': '0px 4px 6px rgba(0,0,0,0.1)',
              'margin': '20px', 'borderRadius': '10px'}),

    dcc.Graph(id='main-price-graph'),

], style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '10px'})

@app.callback(
    Output('brand-drop', 'options'),
    Input('cat-drop', 'value')
)
def update_brand_list(selected_cats):
    if not selected_cats:
        brands = df['Бренд'].unique()
    else:
        brands = df[df['Категория'].isin(selected_cats)]['Бренд'].unique()

    return [{'label': b, 'value': b} for b in sorted(brands)]

@app.callback(
    Output('main-price-graph', 'figure'),
    Output('total-stock-value', 'children'),
    Input('cat-drop', 'value'),
    Input('brand-drop', 'value')
)
def update_dashboard(selected_cats, selected_brands):
    dff = df.copy()

    if selected_cats:
        dff = dff[dff['Категория'].isin(selected_cats)]

    if selected_brands:
        dff = dff[dff['Бренд'].isin(selected_brands)]

    total_val = dff['Total_Cost'].sum()
    formatted_total = f"{total_val:,.0f} ₽".replace(',', ' ')

    fig = px.bar(
        dff,
        x='Цена, ₽',
        y='Название товара',
        color='Категория',
        orientation='h',
        hover_data=['Бренд', 'Артикул', 'Остаток'],
        height=max(500, len(dff) * 30),
        template='plotly_white',
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending', 'title': ''},
        xaxis={'title': 'Цена за единицу (₽)'},
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig, formatted_total


if __name__ == '__main__':
    app.run(debug=True)