import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px 
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd 
from dash.dependencies import Input, Output



df = pd.read_csv('olist_classified_public_dataset.csv')
df = df.dropna(thresh=33)

df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)

df['tempo de venda'] = df.order_purchase_timestamp.dt.to_period('M').astype(str)


lista = df.values.tolist()
tempo = []
ft = []
for x in range(len(lista)):
    y = lista[x][3]
    z = lista[x][34]
    a = ft.append([y,z])
    if (ft[x][1]not in tempo):
        tempo.append(ft[x][1])

tempo.sort()

valor = []
soma = 0
for c in range(len(tempo)):
    for x in range(len(ft)):
        if (ft[x][1]==tempo[c]):
            soma+=ft[x][0]
    valor.append(soma)
    soma=0


data0 = [go.Bar(x=tempo,
               y=valor,
               marker = {'color': '#13D6C0',
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

fig0 = go.Figure(data=data0, layout=configuracoes_layout)
fig0.update_layout(plot_bgcolor="#242423")
fig0.update_layout(paper_bgcolor="#242423")

'''-----------'''
# Relacionando categorias por valor
categorias_valor=[]
for c in range (len(lista)):
    x=lista[c][14]
    y=lista[c][3]
    categorias_valor.append([x,y])
categorias_valor[0:5]

#Laço que inclui apenas as categorias dentro da lista
categorias = []
for c in range (len(lista)):
    if categorias_valor [c][0] not in categorias:
        categorias.append(categorias_valor[c][0])
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

trace1 = go.Bar(y=valor_por_categoria,
                x=categorias,
                marker = {'color': '#13D6C0'},
                orientation='v'
              )

data1 = [trace1]

# Criando Layout
configuracoes_layout = go.Layout(title='Vendas por categoria de Produtos',
                   xaxis=dict(titlefont=dict(size=50,color='black'),tickangle=55),
                   yaxis={'title': 'Quantidade vendida'},
                   
                   )

# Objeto figura

fig1 = go.Figure(data=data1, layout=configuracoes_layout)
fig1.update_layout(plot_bgcolor="#242423")
fig1.update_layout(paper_bgcolor="#242423")



'''------------'''
satisfação = []
for c in range (len(lista)):
    satisfação.append(lista[c][33])
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

trace2 = go.Pie(labels = tipos_classificação,
               values = classificação_satisfação
              )

# Armazenando gráfico em uma lista

data2 = [trace2]

# Criando Layout

layout = go.Layout(title='Classificação de Clientes sobre Pedidos')

# Criando figura que será exibida
fig2 = go.Figure(data=data2, layout=layout)
fig2.update_layout(plot_bgcolor="#242423")
fig2.update_layout(paper_bgcolor="#242423")

'''------------'''
# valor_produto
valor1=[]
for c in range (len(lista)):
    valor1.append(lista[c][3])

len(valor)

# valor frete
frete=[]
for c in range (len(lista)):
    frete.append(lista[c][4])
len(frete)


#relação_valor_frete_produto
frete_produto=[]
for c in range (len(lista)):
    y=frete[c]
    z=valor1[c]
    frete_produto.append([y,z])
frete_produto[0:5]


# Criando gráfico
trace3 = go.Scatter(x = frete,
                   y = valor1,
                   mode = 'markers',
                   marker = {'color':'#13D6C0'}
                  )
# Armazenando gráfico em uma lista
data3 = [trace3]

# Criando Layout
layout = go.Layout(title='Valor de Frete x Valor de Produto',
                   yaxis={'title':'Valor do Produto'},
                   xaxis={'title': 'Valor do Frete'})

# Criando figura que será exibida
fig3 = go.Figure(data=data3, layout=layout)
fig3.update_layout(plot_bgcolor="#242423")
fig3.update_layout(paper_bgcolor="#242423")



'''-------------'''
app = dash.Dash(__name__)

opcoes = {
    'Barras': ['Média', 'Trimestre', 'Semestre'],
    'Linhas': []
}

app.layout = html.Div(children=[
    html.H1(children= 'TESTE DASH', style = {"text-align":"center"}),
    

    html.Div([
        dcc.Dropdown(
            id='drop',
            options=[
                {'label': x, 'value': x} for x in opcoes.keys()],
            value = 'Barras'
        ),dcc.RadioItems(id='valores' )],style ={'width':'30%'}),
      

    html.Hr(),
    
    dcc.Graph(id='g0'),
    
    html.Hr(),

    dcc.Graph(id= 'g1'),

    html.Hr(),

    dcc.Graph(figure=fig2),

    html.Hr(),

    dcc.Graph(figure=fig3),

    
])
    

# função linhas barras
@app.callback(
    [Output('valores', 'options'),
    Output('g0', 'figure'),
    Output('g1', 'figure')],
    [Input('drop', 'value'),
    Input ('valores','value')])
def funcao (variavel, filtro):
    if variavel == 'Linhas':

        data0 = [go.Line(x=tempo,
           y=valor,
           marker = {'color': '#13D6C0',
                     'line': {'color': 'black',
                              'width': 3}
                    },
          )]
        configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

        fig00 = go.Figure(data=data0, layout=configuracoes_layout)
        fig00.update_layout(plot_bgcolor="#242423") #background grafico
        fig00.update_layout(paper_bgcolor="#242423") #background grafico


        trace1 = go.Line(y=valor_por_categoria,
                x=categorias,
                marker = {'color': '#13D6C0'},
                orientation='v'
              )

        data1 = [trace1]

        # Criando Layout
        configuracoes_layout = go.Layout(title='Vendas por categoria de Produtos',
                        xaxis=dict(titlefont=dict(size=50,color='black'),tickangle=55),
                        yaxis={'title': 'Quantidade vendida'},
                        
                        )

        # Objeto figura

        fig11 = go.Figure(data=data1, layout=configuracoes_layout)
        fig11.update_layout(plot_bgcolor="#242423")
        fig11.update_layout(paper_bgcolor="#242423")
        
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig11
    if filtro == 'Média':
        #laço soma valores 
        total = 0
        for y in range(len(ft)):
            total += ft[y][0]

        media = total/len(tempo)

        
        soma=0
        for c in range(len(tempo)):
            for x in range(len(ft)):
                if (ft[x][1]==tempo[c]):
                    soma+=ft[x][0]
            valor.append(soma)    
            soma=0

        cor=[]
        for x in valor:
            if x < media:
                cor.append('red')
            else: 
                cor.append('#13D6C0')
        

        data0 = [go.Bar(x=tempo,
           y=valor,
           marker = {'color': cor, 
                     'line': {'color': 'black',
                              'width': 3}
                    },
          )]
        configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

        fig00 = go.Figure(data=data0, layout=configuracoes_layout)
        fig00.update_layout(plot_bgcolor="#242423") #background grafico
        fig00.update_layout(paper_bgcolor="#242423") #background grafico

        '''--------'''
        a = 0
        for x in range(len(valor_por_categoria)):
            a += valor_por_categoria[x]
        #print(a)

        cor1=[]
        for x in valor_por_categoria:
            if x < media:
                cor1.append('red')
            else: 
                cor1.append('#13D6C0')


                trace1 = go.Bar(y=valor_por_categoria,
                x=categorias,
                marker = {'color': cor1,},
                orientation='v'
              )

        data1 = [trace1]

        # Criando Layout
        configuracoes_layout = go.Layout(title='Vendas por categoria de Produtos',
                        xaxis=dict(titlefont=dict(size=50,color='black'),tickangle=55),
                        yaxis={'title': 'Quantidade vendida'},
                        
                        )

        # Objeto figura

        fig11 = go.Figure(data=data1, layout=configuracoes_layout)
        fig11.update_layout(plot_bgcolor="#242423")
        fig11.update_layout(paper_bgcolor="#242423")
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig11

    
    if filtro == 'Trimestre':
        trimestre=[]
        valor_trimestre=[]
        for c in range (0,len(tempo),3):
            trimestre.append(tempo[c])

        primeiro_trimestre=[]
        segundo_trimestre=[]
        terceiro_trimestre=[]
        quarto_trimestre=[]
        quinto_trimestre=[]

        for c in range (0,3):
            primeiro_trimestre.append(tempo[c])

        for c in range (3,6):   
            segundo_trimestre.append(tempo[c])

        for c in range (6,9):
            terceiro_trimestre.append(tempo[c])

        for c in range (9,12):
            quarto_trimestre.append(tempo[c])
            
        for c in range (12,15):
            quinto_trimestre.append(tempo[c])

        ''' Valor Primeiro Trimestre '''

        soma=0

        for c in range (len(primeiro_trimestre)):
            for x in range (len(tempo)):
                if primeiro_trimestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
        
                

        valor_trimestre.append(y)

        ''' Valor Segundo Trimestre '''

        soma=0

        for c in range (len(segundo_trimestre)):
            for x in range (len(tempo)):
                if segundo_trimestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_trimestre.append(y)

        ''' Valor Terceiro Trimestre '''

        soma=0

        for c in range (len(terceiro_trimestre)):
            for x in range (len(tempo)):
                if terceiro_trimestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_trimestre.append(y)


        ''' Valor Quarto Trimestre '''

        soma=0

        for c in range (len(quarto_trimestre)):
            for x in range (len(tempo)):
                if quarto_trimestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_trimestre.append(y)


        ''' Valor Quinto Trimestre '''

        soma=0

        for c in range (len(quinto_trimestre)):
            for x in range (len(tempo)):
                if quinto_trimestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_trimestre.append(y)


        teste = [1,2,3,4,5]
        data0 = [go.Bar(x=teste,
           y=valor_trimestre,
           marker = {'color': '#13D6C0',
                     'line': {'color': 'black',
                              'width': 3}
                    },
          )]
        configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

        fig00 = go.Figure(data=data0, layout=configuracoes_layout)
        fig00.update_layout(plot_bgcolor="#242423") #background grafico
        fig00.update_layout(paper_bgcolor="#242423") #background grafico

        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig1

    if filtro =='Semestre':
        semestre=[]
        valor_semestre=[]
        for c in range (0,len(tempo),6):
            semestre.append(tempo[c])


        primeiro_semestre=[]
        segundo_semestre=[]
        terceiro_semestre=[]

        for c in range (0,6):
            primeiro_semestre.append(tempo[c])

        for c in range (6,12):
            segundo_semestre.append(tempo[c])

        for c in range (12,len(tempo)):
            terceiro_semestre.append(tempo[c])

        ''' Valor Primeiro Semestre '''

        soma=0

        for c in range (len(primeiro_semestre)):
            for x in range (len(tempo)):
                if primeiro_semestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_semestre.append(y)

        ''' Valor Segundo Semestre '''

        soma=0

        for c in range (len(primeiro_semestre)):
            for x in range (len(tempo)):
                if segundo_semestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_semestre.append(y)

        ''' Valor Terceiro Semestre '''

        soma=0

        for c in range (len(terceiro_semestre)):
            for x in range (len(tempo)):
                if terceiro_semestre[c]==tempo[x]:
                    soma+=valor[x]
                    
                y=soma
                

        valor_semestre.append(y)

        teste = [1,2,3,4,5]
        data0 = [go.Bar(x=teste,
           y=valor_semestre,
           marker = {'color': '#13D6C0',
                     'line': {'color': 'black',
                              'width': 3}
                    },
          )]
        configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

        fig00 = go.Figure(data=data0, layout=configuracoes_layout)
        fig00.update_layout(plot_bgcolor="#242423") #background grafico
        fig00.update_layout(paper_bgcolor="#242423") #background grafico
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig1

    else:
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig0, fig1



if __name__== '__main__':
    app.run_server(debug=True)
