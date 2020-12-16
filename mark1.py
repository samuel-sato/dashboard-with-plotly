import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

#teste1

df_base = pd.read_csv('olist_classified_public_dataset.csv')

df_base=df_base.dropna(thresh=33)

df_base.order_purchase_timestamp = pd.to_datetime(df_base.order_purchase_timestamp)

df_base['tempo de venda'] = df_base.order_purchase_timestamp.dt.to_period('M').astype(str)

aux_data=df_base.values.tolist()
tempo = []
valor_tempo=[]
for x in range (len(aux_data)):
        y=(aux_data[x][3])
        z=(aux_data[x][34])
        valor_tempo.append([y,z])


for x in range (len(valor_tempo)):
    if(valor_tempo[x][1] not in tempo):
        tempo.append(valor_tempo[x][1])

tempo.sort()

valor = []
soma = 0
for c in range(len(tempo)):
    for x in range(len(valor_tempo)):
        if (valor_tempo[x][1]==tempo[c]):
            soma+=valor_tempo[x][0]
    valor.append(soma)
    soma=0


data = [go.Bar(x=tempo,
               y=valor,
               marker = {'color': 'blue',
                         'line': {'color': 'black',
                                  'width': 3}
                        },
              )
       ]

# Criando Layout
configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

# Objeto figura

fig0 = go.Figure(data=data, layout=configuracoes_layout)

# plotando o grafico
'''py.iplot(fig0)'''

# Relacionando categorias por valor
categorias_valor=[]
for c in range (len(aux_data)):
    x=aux_data[c][14]
    y=aux_data[c][3]
    categorias_valor.append([x,y])
categorias_valor[0:5]

#Laço que inclui apenas as categorias dentro da lista
categorias = []
for c in range (len(aux_data)):
    categorias.append(aux_data[c][14])
categorias[0:5]

# Laço que soma valor de cada categoria por mês
valor_por_categoria=[]
soma=0
for c in range(len(categorias)):
    for x in range (len(categorias_valor)):
        if (categorias_valor[x][0]==categorias[c]):
            soma+=categorias_valor[x][1]
    valor_por_categoria.append(soma)
    soma=0        
valor_por_categoria[0:5] 

trace0 = go.Bar(y=valor_por_categoria,
                x=categorias,
                marker = {'color': 'red'},
                orientation='v'
              )

data = [trace0]

# Criando Layout
configuracoes_layout = go.Layout(title='Vendas por categoria de Produtos',
                   xaxis=dict(titlefont=dict(size=50,color='green'),tickangle=55),
                   yaxis={'title': 'Quantidade vendida'})

# Objeto figura

fig1 = go.Figure(data=data, layout=configuracoes_layout)

# plotando o grafico
'''py.iplot(fig)'''

satisfação = []
for c in range (len(aux_data)):
    satisfação.append(aux_data[c][33])
#satisfação

classificação_satisfação=[]
good=bad=very_bad=0
for c in range (len(satisfação)):
    if satisfação[c]=='satisfeito_com_pedido':
        good+=1
    if satisfação[c]=='problemas_de_entrega':
        bad+=1
    if satisfação[c]=='problemas_de_qualidade':
        very_bad+=1
classificação_satisfação.append(good)
classificação_satisfação.append(bad)
classificação_satisfação.append(very_bad)

classificação_satisfação 

#Tipos de classificação
tipos_classificação=[]
for x in range (len(satisfação)):
    if satisfação[x] not in tipos_classificação:
        tipos_classificação.append(satisfação[x])
'''tipos_classificação'''

tipos_classificação_relação=[]

for c in range (len(tipos_classificação)):
    x=tipos_classificação[c]
    y=classificação_satisfação[c]
    tipos_classificação_relação.append([x,y])
'''tipos_classificação_relação'''


# Criando gráfico

trace = go.Pie(labels = tipos_classificação,
               values = classificação_satisfação
              )

# Armazenando gráfico em uma lista

data = [trace]

# Criando Layout

layout = go.Layout(title='Classificação de Clientes sobre Pedidos')

# Criando figura que será exibida
fig2 = go.Figure(data=data, layout=layout)

'''py.iplot(fig)'''

# valor_produto
valor=[]
for c in range (len(aux_data)):
    valor.append(aux_data[c][3])

len(valor)

# valor frete
frete=[]
for c in range (len(aux_data)):
    frete.append(aux_data[c][4])
len(frete)


#relação_valor_frete_produto
frete_produto=[]
for c in range (len(aux_data)):
    y=frete[c]
    z=valor[c]
    frete_produto.append([y,z])
frete_produto[0:5]


# Criando gráfico
trace = go.Scatter(x = frete,
                   y = valor,
                   mode = 'markers',
                   marker = {'color':'#941229'}
                  )
# Armazenando gráfico em uma lista
data = [trace]

# Criando Layout
layout = go.Layout(title='Valor de Frete x Valor de Produto',
                   yaxis={'title':'Valor do Produto'},
                   xaxis={'title': 'Valor do Frete'})

# Criando figura que será exibida
fig3 = go.Figure(data=data, layout=layout)

'''py.iplot(fig3)'''


app = dash.Dash()


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Ecommerce - Análise de dados
    '''),
    dcc.Graph(fig0),
    html.Br(),
    dcc.Graph(fig1),
    dcc.Graph(fig2),
    dcc.Graph(fig3),


    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': tempo , 'y': valor , 'type': 'bar', 'name': 'Tempo'},
                {'x': tempo, 'y': valor , 'type': 'bar', 'name': u'Valor'},
            ],
            'layout': {
                'title': 'Análise de dados'
            }
        }
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)