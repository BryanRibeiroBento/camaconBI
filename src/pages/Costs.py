import dash
from dash import html,dcc,Input,Output,callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas_datareader.data as web
import dash_bootstrap_components as dbc
import datetime



dash.register_page(__name__,
                   path='/dash',  # '/' is home page and it represents the url
                   name='dash',  # name of page, commonly used as name of link
                   title='Costs',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
)

#====================DATA FRAME====================
df_costs = pd.read_excel('/Users/bryanribeiro/Desktop/python/multipage_project/data/base_custos.xlsx')

df_costs['Data'] = pd.to_datetime(df_costs['Data'])
df_costs['MES'] = df_costs['Data'].dt.month

df_costs = df_costs.dropna(axis = 0, how='all') 
df_costs['MES'] = df_costs['MES'].astype(int)
pd.set_option('display.max_rows',None)



# print(df_costs)




#==================================================


#====================VARIABLES + STYLE=============
months = {"abril":4,"maio":5,"junho":6,"julho":7}
month_options = [{"label": month, "value": value} for month, value in months.items()]

def format_cost(cost):
    return f'R${cost:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def calculate_percentage_change(values):
    percentages = []
    for i in range(1, len(values)):
        change = (values[i] - values[i-1]) / values[i-1] * 100
        percentages.append(change)
    return percentages

colors = [
    '#F0E7D8',  # Background color
    '#4D2D61',  # Primary color
    '#8D8D8D',  # Secondary color
    '#4D5B6F',  # Success color
    '#D9534F',  # Danger color
    '#F0AD4E',  # Warning color
    '#4D2D61',  # Info color
    '#F7F7F7',  # Light color
    '#333333',  # Dark color
    '#F0A202',  # Danger color (repeated, but often used for emphasis)
    '#F0E7D8',   # Background color (repeated, used for various elements)
    '#14213D',
    '#124E78',
    '#353535',
    '#A8DADC',
    '#2D4739',
]


#==================================================


#====================LAYOUT=======================
layout = dbc.Container([
    #Row 1
    dbc.Row([

         dbc.Col([
            html.H2("Centro de Custos - Camacon Terraplenagem",className="text-light text-center mx-2"),
           
        ],xs=11, sm=11, md=11, lg=8, xl=8,),

       dbc.Col([
           dbc.Card([
               dbc.CardBody([
                   html.H5('Escolha o Mês'),
                    dbc.RadioItems(
                        id="radio-month",
                            options=month_options,
                            value=4,
                            inline=True,
                            labelCheckedClassName="text-success",
                            inputCheckedClassName="border border-success bg-success",
                            className="bg-primary"                 
                    ),
                    
               ],className="bg-primary text-light")
           ],style={"margin-top":"2vh"})
       ],xs=12, sm=12, md=12, lg=4, xl=4,className="align-items-center bg-primary"),

    ],align="center"), 
    #Row 2
    dbc.Row([
        dbc.Col([
            #Card Investimento Maquinario
            dbc.Card([
                dbc.CardBody([
                    html.H6('TOTAL:',className="fs-4"),
                    html.H5(className="text-success fs-2",id = 'total-card'),
                    

                ],className="text-center")
            ],className="rounded")
            
        ],xs=12, sm=12, md=12, lg=4, xl=4,className = "mb-2"),
        dbc.Col([
            #Card Investimento Maquinario
            dbc.Card([
                dbc.CardBody([
                    html.H6('Invest.Maquinário'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'invest-maq-card'),
                    

                ],className="text-center")
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2),
        #Card Investimento Imobiliario
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Invest.Imobiliarios'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'invest-imob-card'),
                ],className="text-center")
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2),
        #Card Diesel
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Diesel'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'diesel-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Impostos
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Impostos'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'impostos-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
         #Card Funcionarios
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Funcionarios'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'funcionarios-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
         #Card Escritorio
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Escritorio'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'escritorio-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
         #Card IPVA
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('IPVA'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'ipva-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
         #Card Frota ADM
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Frota Administrativa'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'frota-adm-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
         #Card Manut.Maquinas
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Manut.Maquinas'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'manut-maquinas-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Caminhoes
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Caminhoes'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'caminhoes-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Multas
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Multas'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'multas-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Femacon
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Femacon'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'femacon-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Despesas Rodolfo
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Despesas Rodolfo'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'rodolfo-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Despesas Rodolfinho
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Despesas Rodolfinho'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'rodolfinho-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Diversos
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Diversos'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'diversos-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
        #Card Davi
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Davi'),
                    html.H5('R$ 1.000.000,00',className="text-success",id = 'davi-card'),
                ],)
            ],className="rounded")
            
        ],xs=6, sm=6, md=6, lg=2, xl=2,className = "mb-2"),
    ],className="text-center my-1"),

    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # html.H4("Distribuição Por Tipo", className="text-center"),
                    dcc.Graph(id='pie-graph', style = {"height":"100%", "width":"100%"})
                    

                ])
            ],className="rounded")

        ],xs=12, sm=12, md=12, lg=5, xl=5,className = "mb-2"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # html.H4("Distribuição Por Tipo", className="text-center"),
                    dcc.Graph(id='line-graph', style = {"height":"100%", "width":"100%"})
                    

                ])
            ],className="rounded")

        ],xs=12, sm=12, md=12, lg=7, xl=7,className = "mb-2"),

    ]),

    #Row 4
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Col([
                    
                    dcc.Dropdown(
                        id = 'dp-types',
                        multi=True,
                        options=df_costs['TIPO'].unique(),
                        className="text-dark"
                    )
                     ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2"),

                    dbc.Col([
                    html.H4("Categorias x Mês",className="text-center fw-bold text-primary")
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 mt-3"),

                    dbc.Col([
                        dcc.Graph(id = "types-graph",style = {"height":"100%", "width":"100%"})
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 text-dark")

            ])
        ],className="text-light rounded")
    ])
])

    


],fluid=True, className="bg-primary text-light")
#==================================================

#====================CallBacks====================

@callback(
    Output("total-card","children"),    
    Output("invest-maq-card","children"),
    Output("invest-imob-card","children"),
    Output("diesel-card","children"),
    Output("impostos-card","children"),
    Output("funcionarios-card","children"),
    Output("escritorio-card","children"),
    Output("ipva-card","children"),
    Output("frota-adm-card","children"),
    Output("manut-maquinas-card","children"),
    Output("caminhoes-card","children"),
    Output("multas-card","children"),
    Output("femacon-card","children"),
    Output("rodolfo-card","children"),
    Output("rodolfinho-card","children"),
    Output("diversos-card","children"),
    Output("davi-card","children"),

   
    Input("radio-month","value"),
    

)
def setCosts(month):
    #Filtrando do df_costs o valor total de cada tipo no mes selecionado
    df_total = df_costs.groupby(['MES', 'TIPO'])['VALOR'].sum().reset_index()


    # Filtrando para o mês 4
    df_mes = df_total[df_total['MES'] == month]

    #df para dicionario
    total_tipo = df_mes.set_index('TIPO')['VALOR'].to_dict()
    
     #Filtrando por Tipo
    total = format_cost(df_mes['VALOR'].sum())
    investMaq = format_cost(total_tipo.get('INVESTIMENTO MAQUINARIO', 0))
    investImob = format_cost(total_tipo.get('INVESTIMENTOS IMOBILIARIOS', 0))
    diesel = format_cost(total_tipo.get('DIESEL', 0))
    impostos = format_cost(total_tipo.get('IMPOSTOS', 0))
    funcionarios = format_cost(total_tipo.get('FUNCIONARIOS', 0))
    escritorio = format_cost(total_tipo.get('ESCRITORIO', 0))
    ipva = format_cost(total_tipo.get('IPVA', 0))
    fadm = format_cost(total_tipo.get('FROTA ADMNISTRATIVA', 0))
    manutMaq = format_cost(total_tipo.get('MANUTENCAO MAQUINAS', 0))
    caminhoes = format_cost(total_tipo.get('CAMINHOES', 0))
    multas = format_cost(total_tipo.get('MULTAS', 0))
    femacon = format_cost(total_tipo.get('FEMACON', 0))
    rodolfo = format_cost(total_tipo.get('DESPESAS RODOLFO', 0))
    finho = format_cost(total_tipo.get('DESPESAS RODOLFINHO', 0))
    diversos = format_cost(total_tipo.get('DIVERSOS', 0))
    davi = format_cost(total_tipo.get('DAVI', 0))
        
    return total,investMaq,investImob,diesel,impostos,funcionarios,escritorio,ipva,fadm,manutMaq,caminhoes,multas,femacon,rodolfo,finho,diversos,davi


@callback(
    Output("pie-graph","figure"),
    Input("radio-month","value"),
)
def pieGraph(month):
    #Filtrando do df o valor total de cada tipo no mes selecionado
    df_total = df_costs.groupby(['MES', 'TIPO'])['VALOR'].sum().reset_index()
    # Filtrando para o mês 4
    df_mes = df_total[df_total['MES'] == month]
    fig1 = go.Figure()
    fig1.add_trace(go.Pie(
       
        labels=df_mes['TIPO'],
        values=df_mes['VALOR'],
        textinfo='label+percent',
        
        textfont=dict(family='Georgia'),
        marker=dict(colors=colors),
        
        
        
        rotation=90,
        ))

    fig1.update_layout( 
        showlegend=False, 
        margin=dict(t=0, b=0, l=0, r=0),
        
        )
    return fig1

@callback(
    Output("line-graph","figure"),
    Input("radio-month","value"),
    
)
def lineGraph(month):
    #Filtrando do df o valor total de cada tipo no mes selecionado
    df_total = df_costs.groupby(['MES'])['VALOR'].sum().reset_index()
    months_list = list(months.keys())
    variacao = calculate_percentage_change(df_total['VALOR'])
    
    # Filtrando para o mês 4
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=months_list,
        y=df_total['VALOR'],
        mode='lines+markers+text',  # Exibir linhas e marcadores
        marker=dict(
            color='#FFFFFF',  # Cor dos marcadores
            size=10,  # Tamanho dos marcadores
            line=dict(width=1.5, color='#000000')  # Borda dos marcadores
        ),
        line=dict(
            color='rgba(31, 119, 180, 0.8)',  # Cor da linha
            width=5  # Largura da linha
        ),
        text=[format_cost(value) for value in df_total['VALOR']],  # Valores formatados com R$
        textposition='top right',
        textfont=dict(color='black'),
        name='Valor'
    )),
    for i in range(1, len(months_list)):
        fig2.add_annotation(
            x=months_list[i],
            y=df_total['VALOR'][i],
            text=f'{variacao[i-1]:.1f}%',  # Variação percentual formatada
            # showarrow=True,
            # arrowhead=2,
            ax=0,
            ay=+20,
            font=dict(size=15, color='black')
        )
        

    fig2.update_layout(
        title='Custo Total X Meses',
        title_font_size=20,
        yaxis_title='Valor',
        xaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12),
            
        ),
        yaxis=dict(
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Remover cor de fundo do gráfico
        paper_bgcolor='rgba(0,0,0,0)',  
        margin=dict(t=40, b=40, l=40, r=40),
        autosize = True, # Ajustar margens
    )

    return fig2

@callback(
    Output('types-graph','figure'),
    Input("dp-types","value"),
    
)

def typesGraph(types):
    df_types = df_costs.groupby(['MES','TIPO'])['VALOR'].sum().reset_index()
    if types is None or len(types) == 0:
        return px.line(title = 'Selecione Uma Categoria Para Visualizar o Gráfico') 
    df_selected = df_types[df_types['TIPO'].isin(list(types))]
    print(df_selected)
    fig3 = px.line(df_selected, x='MES', y='VALOR', color='TIPO', markers=True)
    return fig3

#==================================================















# #====================RUN SERVER====================
# if __name__ == '__main__':
#     run_server(debug = True)
# #==================================================








