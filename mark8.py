# importações 
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px 
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd 
from dash.dependencies import Input, Output

#Manuseio de dados 
df = pd.read_csv('olist_classified_public_dataset.csv') #leitura do csv realizada pelo pandas, adicionda a um dataframe 'df'
df = pd.read_csv('olist_classified_public_dataset.csv') #leitura do csv realizada pelo pandas, adicionda a um dataframe 'df'
df = df.dropna(thresh=33) # Retirada do not a number da coluna 33--> classificação
df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp) # Mudança do tipo, de object para datetime 
df['tempo de venda'] = df.order_purchase_timestamp.dt.to_period('M').astype(str) # Mudança para ano-mes 
aux_data = df.values.tolist() # Mudança do dataframe para uma matrix/lista




'''Grafico Barras'''

# Relação mês_valor
tempo = []          # lista vazia para adição do tempo 
vendas_periodo = [] # Lista vazia para relação do tempo com o valor
valor = 3           # Variável valor recebendo 3 para melhor comprensão do que se trata a coluna "valores"
mes_ano = 34        # Variável mes_ano recebendo 34 para melhor comprensão do que se trata a coluna "mes_ano" 
qtd = 5             # coluna do numero de itens
        
for linha in range(len(aux_data)):                              # Laço que irá percorrer a aux_data  
    vendas = (aux_data[linha][valor])*(aux_data[linha][qtd])    # vendas irá receber o valor do produto de acordo com a leitura da linha valor e quantidade 
    periodo = aux_data[linha][mes_ano]                          # periodo irá receber a tempo de venda de acordo com a leitura da linha 
    vendas_periodo.append([vendas,periodo])                     # agregando valor e com o periodo, criando assim a relação vendas_perido
    if (vendas_periodo[linha][1] not in tempo):                 # Se o periodo de vendas dado ainda nn estiver adicionado na lista tempo,ele será agregado
        tempo.append(vendas_periodo[linha][1])  

tempo.sort()  #colocando tempo em ordem
preço = []    #lista vazia para agreção do preço 
soma = 0      #contador inicia com 0

for cont in range(len(tempo)):                      # Cont ira pecorrer a quantidade do tempo
    for linha in range(len(vendas_periodo)):        # linha ira percorrer a lista vendas_periodo                                              
        if (vendas_periodo[linha][1]==tempo[cont]): # Conferir se o tempo do periodo é corresponde ao tempo crescente dos meses
            soma+=vendas_periodo[linha][0]          # somando os valores que satisfazem a condição acima
    preço.append(soma)                              # Adicionando a soma na lista preço                         
    soma=0                                          # Zerando o contador   

''' Plotagem do gráfico '''      

data0 = [go.Bar(x=tempo,                             # data0 Armazena informações a respeito do gráfico, bem tipo "go.bar"                           
                y=preço,                             # A correspondenciado dos eixos, "x=tempo" e "y=tempo"
                marker = {'color': '#13D6C0',        # maker=recebe caracterísca de layout da barra, sendo color sua cor, line sendo linha, com sua respectivas
                          'line': {'color': 'black', # caracteristicas como cor e espessura "width"
                                   'width': 3}
                        },
              )
       ]

# Criando Layout                                                    
configuracoes_layout = go.Layout(title='Vendas no Periodo',             # Definição da legenda das linhas como título
                                 yaxis={'title':'Valores em Vendas'},   # Definição da legenda do eixo y e x    
                                 xaxis={'title':'Periodo'})

# Objeto figura

fig0 = go.Figure(data=data0, layout=configuracoes_layout)  # Armazenamento da figura e de seus rectivos dados em fig0         
fig0.update_layout(plot_bgcolor="#242423")                 # Definição de fundo 
fig0.update_layout(paper_bgcolor="#242423")  
fig0.update_layout(font_color="white")            

''' Gráfico categorias '''

# Relacionando categorias por valor
categorias_faturamento=[]                                     # Criação lista categoria por faturamento
name = 14                                                     # Classificando variavel name com 14 "respectiva coluna com os nomes de produtos"
for linha in range (len(aux_data)):                           # Percorrendo aux_data   
    categorias=aux_data[linha][name]                          # Selecionando os nomes das categorias
    faturamento=aux_data[linha][valor]*aux_data[linha][qtd]   # Selecionando valor*qnt de cada categoria
    categorias_faturamento.append([categorias,faturamento])   # Relacionando cada categoria com seu faturamento faturamento 
categorias_faturamento[0:5]

#Laço que inclui apenas as categorias dentro da lista
categorias = []                                                     # Criando lista categoria
produto = 0                                                         # Classificando variavel produto com 0 "respectiva coluna com os nomes de produtos"
for linha in range (len(categorias_faturamento)):                   # Percorrendo as linhas de categorias_faturamento  
    if categorias_faturamento [linha][produto] not in categorias:   # Condição para inclusão na lista categoria, ainda nn estar na mesma        
        categorias.append(categorias_faturamento[linha][produto])   # Adição definitiva a lista    

# Laço que soma valor de cada categoria por mês
faturamento_total_por_categoria=[]                                    # Criando lista faturamento_total_por_categoria                                        
soma=0                                                                # Iniciando contador do 0
for linha in range(len(categorias)):                                  # Percorrer numero de linhas de categorias  
    for x in range (len(categorias_faturamento)):                     # Percorrendo numero de linhas de categorias_faturamento
        if (categorias_faturamento[x][0]==categorias[linha]):         # Condição pra soma do faturamento_total_por_categoria, terem a mesma categoria
            soma+=categorias_faturamento[x][1]                        # Adição a lista soma o valor da categoria satisfeita acima      
    faturamento_total_por_categoria.append(soma)                      # Adição da soma a lista faturamento_total_por_categoria
    soma=0                                                            # zerando soma                                             

trace1 = go.Bar(y=faturamento_total_por_categoria,   # trace1 Armazena informações a respeito do gráfico, bem tipo "go.bar"
                x=categorias,                        # A correspondenciado dos eixos, "x=categorias" e "y=faturamento_total_por_categoria"    
                marker = {'color': '#13D6C0',        # maker=recebe caracterísca de layout da barra, sendo color sua cor, line sendo linha, com sua respectivas
                          'line': {'color': 'black', # Caracteristicas como cor e espessura "width"
                                   'width': 3}
                        }         
              )

data1 = [trace1]   # Armazenando dados do trace1 em data1 

# Criando Layout
configuracoes_layout = go.Layout(title='Vendas por categoria de Produtos',             # Definição da legenda das linhas como título            
                   xaxis=dict(titlefont=dict(size=50,color='black'),tickangle=50),     # Definição da legenda do eixo y e x
                   yaxis={'title': 'Quantidade vendida'},
                   
                   )

# Objeto figura

fig1 = go.Figure(data=data1, layout=configuracoes_layout)    # Armazenamento da figura e de seus rectivos dados em fig0
fig1.update_layout(plot_bgcolor="#242423")                   # Definição de fundo 
fig1.update_layout(paper_bgcolor="#242423")                  
fig1.update_layout(font_color="white")                       # Cor da legenda 





'''Gráfico satisfação'''
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
fig2.update_layout(font_color="white")                       # Cor da legenda 


'''Gráfico Frete_Produto'''
# valor_produto
valor1=[]
for c in range (len(aux_data)):
    valor1.append(aux_data[c][3])


# valor frete
frete=[]
for c in range (len(aux_data)):
    frete.append(aux_data[c][4])
len(frete)


#relação_valor_frete_produto
frete_produto=[]
for c in range (len(aux_data)):
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
fig3.update_layout(font_color="white")                       # Cor da legenda 



app = dash.Dash(__name__)

opcoes = {
    'Barras': ['Média', 'Trimestre', 'Semestre'],
    'Linhas': []
}

app.layout = html.Div(children=[
    html.H1(children= 'DASH ECCOMERCE', style = {"text-align":"center"}),
    

    html.Div([
        dcc.Dropdown(
            id='drop',
            options=[
                {'label': x, 'value': x} for x in opcoes.keys()],
            value = 'Barras'
        ),dcc.RadioItems(id='valores' )],style ={'width':'30%'}),
      

    html.Hr(),

    html.Div([
        dcc.Graph(id='g0'), #grafico0   
        
        dcc.Graph(id= 'g1')],style={'display':'flex'}),   #grafico1    

    html.Hr(),#Linha de divisão

    html.Div([
        dcc.Graph(figure=fig2),

        dcc.Graph(figure=fig3)],style={'display':'flex','width':'100%'})


    
], style={'background':'#242423', 'color':'white'})
    

# função linhas barras
@app.callback(
    [Output('valores', 'options'),  #saida para id = valores no dash (média, trimestre e semestre)
    Output('g0', 'figure'), # saida para id = g0 (grafico0)
    Output('g1', 'figure')],    #saida para id = g1 (graafico1)
    [Input('drop', 'value'),    #entrada valores do id=drop (Barras ou Linhas)
    Input ('valores','value')]) #entrada valores do id=valores (Média, Trimestre e Semestre)
def funcao (variavel, filtro):  #funçao que atribui o nome variavel ao 1º input (Barras ou Linhas) e filtro ao 2ºinput(Média, Trimestre e Semestre)
    if variavel == 'Barras':
        if filtro == 'Média':
            #laço soma valores 
            total = 0
            for y in range(len(vendas_periodo)):
                total += aux_data[y][3]*aux_data[y][5]
            #print(total)
            media_periodo = total/len(tempo)
            media_cate= total/len(categorias)

            cor=[]
            for x in preço:
                if x < media_periodo:
                    cor.append('red')
                else: 
                    cor.append('#13D6C0')
        

            trace00 = [go.Bar(x=tempo,
            y=preço,
            marker = {'color': cor, 
                        'line': {'color': 'black',
                                'width': 3}
                        },
            )]

            media1=[]
            for x in range(len(tempo)):
                media1.append(media_periodo)

            media2=[]
            for x in range(len(categorias)):
                media2.append(media_cate)
            data00 = trace00
            configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                    yaxis={'title':'Valores em Vendas'},
                                    xaxis={'title':'Periodo'})
            
            fig00 = go.Figure(data=data00, layout=configuracoes_layout)
            fig00.add_trace(go.Scatter(y=media1,x= tempo, mode='lines', marker={'color':'red', 'line':{'color': 'black','width': 3}}))  #Adiciona a linha de media no grafico

            fig00.update_layout(plot_bgcolor="#242423") #background grafico
            fig00.update_layout(paper_bgcolor="#242423") #background grafico
            fig00.update_layout(font_color="white")                       # Cor da legenda 


            '''--------'''
            a = 0
            for x in range(len(faturamento_total_por_categoria)):
                a += faturamento_total_por_categoria[x]

            cor1=[]
            for x in faturamento_total_por_categoria:
                if x < media_cate:
                    cor1.append('red')
                else: 
                    cor1.append('#13D6C0')


            trace1 = go.Bar(y=faturamento_total_por_categoria,
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
            fig11.update_layout(font_color="white")                       # Cor da legenda 

            fig11.add_trace(go.Scatter(y=media2,x= categorias, mode='lines', marker={'color':'red', 'line':{'color': 'black','width': 3}})) #Adiciona a linha de media no grafico

            return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig11   #Retorna conforme os outputs nos id's (valores, g0, g1)

    
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
                        soma+=preço[x]
                        
                    y=soma
            
                    

            valor_trimestre.append(y)

            ''' Valor Segundo Trimestre '''

            soma=0

            for c in range (len(segundo_trimestre)):
                for x in range (len(tempo)):
                    if segundo_trimestre[c]==tempo[x]:
                        soma+=preço[x]
                        
                    y=soma
                    

            valor_trimestre.append(y)

            ''' Valor Terceiro Trimestre '''

            soma=0

            for c in range (len(terceiro_trimestre)):
                for x in range (len(tempo)):
                    if terceiro_trimestre[c]==tempo[x]:
                        soma+=preço[x]
                        
                    y=soma
                    

            valor_trimestre.append(y)


            ''' Valor Quarto Trimestre '''

            soma=0

            for c in range (len(quarto_trimestre)):
                for x in range (len(tempo)):
                    if quarto_trimestre[c]==tempo[x]:
                        soma+=preço[x]
                        
                    y=soma
                    

            valor_trimestre.append(y)


            ''' Valor Quinto Trimestre '''

            soma=0

            for c in range (len(quinto_trimestre)):
                for x in range (len(tempo)):
                    if quinto_trimestre[c]==tempo[x]:
                        soma+=preço[x]
                        
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
            fig00.update_layout(font_color="white")                       # Cor da legenda 


            return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig1    #Retorna conforme os outputs nos id's (valores, g0, g1)

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
                        soma+=preço[x]
                        
                    y=soma
                    

            valor_semestre.append(y)

            ''' Valor Segundo Semestre '''

            soma=0

            for c in range (len(primeiro_semestre)):
                for x in range (len(tempo)):
                    if segundo_semestre[c]==tempo[x]:
                        soma+=preço[x]
                        
                    y=soma
                    

            valor_semestre.append(y)

            ''' Valor Terceiro Semestre '''

            soma=0

            for c in range (len(terceiro_semestre)):
                for x in range (len(tempo)):
                    if terceiro_semestre[c]==tempo[x]:
                        soma+=preço[x]
                        
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
            fig00.update_layout(font_color="white")                       # Cor da legenda 

            return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig1    #Retorna conforme os outputs nos id's (valores, g0, g1)

        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig0, fig1   #Retorna conforme os outputs nos id's (valores, g0, g1)
    if variavel == 'Linhas':

        data00 = [go.Line(x=tempo,
           y=preço,
           marker = {'color': '#13D6C0',
                     'line': {'color': 'black',
                              'width': 3}
                    },
          )]
        configuracoes_layout = go.Layout(title='Vendas no Periodo',
                                 yaxis={'title':'Valores em Vendas'},
                                 xaxis={'title':'Periodo'})

        fig00 = go.Figure(data=data00, layout=configuracoes_layout)
        fig00.update_layout(plot_bgcolor="#242423") #background grafico
        fig00.update_layout(paper_bgcolor="#242423") #background grafico
        fig00.update_layout(font_color="white")                       # Cor da legenda 



        trace1 = go.Line(y=faturamento_total_por_categoria,
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
        fig11.update_layout(font_color="white")                       # Cor da legenda 

        
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig00, fig11   #Retorna conforme os outputs nos id's (valores, g0, g1)

    
    
    else:
        return [{'label': i, 'value': i} for i in opcoes[variavel]], fig0, fig1     #Retorna conforme os outputs nos id's (valores, g0, g1)



if __name__== '__main__':
    app.run_server(debug=True)