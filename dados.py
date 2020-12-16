import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly_express as px
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_csv('olist_classified_public_dataset.csv')

df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)
df['order_purchase_month'] = df.order_purchase_timestamp.dt.to_period('M').astype(str)
#print(df.head())
def soma (valor):
    return 'valor:{}'.format(df[valor].sum())   
#print(df.order_purchase_month.head())
#print(df['order_purchase_month'].value_counts()) #numero de pedidos em cada mes

vendas_por_mes = df.groupby(by='order_purchase_month').order_products_value.sum()
#soma = df['order_purchase_month'].value_counts()
#print(soma())

data = [go.Bar(x=vendas_por_mes.index,
               y=vendas_por_mes.values,
               marker = {'color': 'lightblue',
                         'line': {'color': '#333',
                                  'width': 2}
                        },
               opacity= 0.7
              )
       ]
def num_list (lista):
    for x in range (len(lista)):
        return x

#a= num_list(lista)
# Criando Layout
configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})
lista = df.values.tolist()


# Objeto figura

fig = go.Figure(data=data, layout=configuracoes_layout)

teste = soma('order_products_value')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=
        'Dash:A web application framework for Python.'
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    html.Div(id='saida'),
    html.Div(teste),
    dcc.RangeSlider(
        id='my-range-slider',
        min=0,
        max=20,
        step=0.5,
        value=[5, 15]
    ),
    html.Div(id='output-container-range-slider')
])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


'''
if __name__ == '__main__':
    app.run_server(debug=True)

'''


