import dash
from dash import html,dcc,Input,Output,callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

#======TO DO========
#mudar ids dos componentes para ids unicos de cada pagina (Costs e income)
#===================




dash.register_page(__name__,
                   path='/income',  # '/' is home page and it represents the url
                   name='Faturamento',  # name of page, commonly used as name of link
                   title='Faturamento',  # title that appears on browser's tab
                   image='assets/camacon.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
)

#====================DATA FRAME====================
df = pd.read_excel('./data/base_faturamento.xlsx')
df_total_costs = pd.read_excel('./data/base_custos_totais.xlsx')


#==================================================



#===================VARIABLES + STYLE==============
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
#====================LAYOUT=======================
layout = dbc.Container([
    #Row 1
    dbc.Row([

         dbc.Col([
            html.H2("Faturamento - Camacon Terraplenagem",className="text-light text-center mx-2"),
           
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
        # Coluna esquerda com Faturamento e Lucro
        dbc.Col([
            dbc.Row([
                # Card Faturamento
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('FATURAMENTO:', className="fs-4"),
                            html.H5(className="text-success fs-2", id='income-card'),
                        ], className="text-center")
                    ], className="rounded mb-2")
                ], width=12),
            ]),
            dbc.Row([
                # Card Lucro
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Lucro:', className="fs-4"),
                            html.H5(className="text-success fs-2", id='profit-card'),
                        ], className="text-center")
                    ], className="rounded mb-2")
                ], width=12),
            ]),
        ], xs=12, sm=12, md=12, lg=4, xl=4),

        # Coluna direita com outros cards
        dbc.Col([
            dbc.Row([
                # Card Obras Diarias
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Obras Diarias'),
                            html.H5('R$ 1.000.000,00', className="text-success", id='daily-card'),
                        ], className="text-center fs-1")
                    ], className="rounded mb-2")
                ], xs=6, sm=6, md=6, lg=6, xl=6),

                # Card Locacao
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Locacao'),
                            html.H5('R$ 1.000.000,00', className="text-success", id='rental-card'),
                        ], className="text-center fs-1")
                    ], className="rounded mb-2")
                ], xs=6, sm=6, md=6, lg=6, xl=6),
            ]),
            dbc.Row([
                # Card Perfuracao
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Perfuracao'),
                            html.H5('R$ 1.000.000,00', className="text-success", id='drilling-card'),
                        ], className="text-center fs-1")
                    ], className="rounded mb-2 mt-4")
                ], xs=6, sm=6, md=6, lg=6, xl=6),

                # Card Venda de Equipamentos
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6('Venda de Maquinas'),
                            html.H5('R$ 1.000.000,00', className="text-success", id='machine-sales-card'),
                        ], className="text-center fs-2")
                    ], className="rounded mb-2 mt-4")
                ], xs=6, sm=6, md=6, lg=6, xl=6),
            ]),
        ], xs=12, sm=12, md=12, lg=8, xl=8),
    ], className="text-center my-1"),

    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Distribuição Por Fonte", className="text-center"),
                    dcc.Graph(id='income-pie-graph')
                    

                ])
            ],className="rounded h-100")

        ],xs=12, sm=12, md=12, lg=4, xl=4,className = "mb-2"),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Col([
                    
                    dcc.Dropdown(
                        id = 'dp-types',
                        multi=True,
                        options=df['TIPO'].unique(),
                        className="text-dark"
                    )
                     ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2"),

                    dbc.Col([
                    html.H4("Categorias x Mês",className="text-center fw-bold text-primary")
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 mt-3"),

                    dbc.Col([
                        dcc.Graph(id = "income-types-graph",style = {"height":"100%", "width":"100%"})
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 text-dark")

            ]),
        ],className='rounded mb-2'),

        ]),

       
    ]),

    #Row 4
    dbc.Row([
         dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # html.H4("Distribuição Por Tipo", className="text-center"),
                    dcc.Graph(id='income-line-graph', )
                    

                ])
            ],className="rounded")

        ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2"),
        
    ]),
    #Row 5
    dbc.Row([
       dbc.Col([
           dbc.Card([
               dbc.CardBody([
                   dbc.Col([
                    html.H4("Faturamento x Lucro",className="text-center fw-bold text-primary")
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 mt-3"),

                    dbc.Col([
                        dcc.Graph(id = "income-profit-graph")
                    ],xs=12, sm=12, md=12, lg=12, xl=12,className = "mb-2 text-dark")
               ])
           ])
       ])
    ]),


    

],fluid=True, className="bg-primary text-light")

#==================================================

#====================CallBacks====================

@callback(
    Output("income-card","children"),    
    Output("profit-card","children"),
    Output("daily-card","children"),    
    Output("rental-card","children"),
    Output("drilling-card","children"),    
    Output("machine-sales-card","children"),
   
    Input("radio-month","value"),
    

)
def setCosts(month):
    #Filtrando do df o valor total de cada tipo no mes selecionado
    df_total = df.groupby(['MES', 'TIPO'])['TOTAL'].sum().reset_index()


    # Filtrando para o mês 4
    df_mes = df_total[df_total['MES'] == month]

    #df para dicionario
    total_tipo = df_mes.set_index('TIPO')['TOTAL'].to_dict()
    
     #Filtrando por Tipo
    income = format_cost(df_mes['TOTAL'].sum())
    
    profit = format_cost(df_mes['TOTAL'].sum() - df_total_costs.loc[df_total_costs['MES'] == month, 'TOTAL'].sum())
    daily = format_cost(total_tipo.get('DIARIA', 0))
    rental = format_cost(total_tipo.get('LOCACAO', 0))
    drilling= format_cost(total_tipo.get('PERFURACAO', 0))
    sales = format_cost(total_tipo.get('VENDA', 0))

    # diesel = format_cost(total_tipo.get('DIESEL', 0))
   
        
    return income,profit,daily,rental,drilling,sales


@callback(
    Output("income-pie-graph","figure"),
    Input("radio-month","value"),
)
def pieGraph(month):
    #Filtrando do df o valor total de cada tipo no mes selecionado
    df_total = df.groupby(['MES', 'TIPO'])['TOTAL'].sum().reset_index()
    # Filtrando para o mês 4
    df_mes = df_total[df_total['MES'] == month]
    fig1 = go.Figure()
    fig1.add_trace(go.Pie(
       
        labels=df_mes['TIPO'],
        values=df_mes['TOTAL'],
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
    Output('income-types-graph','figure'),
    Input("dp-types","value"),
    
)

def typesGraph(types):
    df_types = df.groupby(['MES','TIPO'])['TOTAL'].sum().reset_index()
    if types is None or len(types) == 0:
        return px.line(title = 'Selecione Uma Categoria Para Visualizar o Gráfico') 
    df_selected = df_types[df_types['TIPO'].isin(list(types))]
    fig2 = px.line(df_selected, x='MES', y='TOTAL', color='TIPO', markers=True)
    return fig2


@callback(
    Output("income-line-graph","figure"),
    Input("radio-month","value"),
    
)
def lineGraph(month):
    #Filtrando do df o valor total de cada tipo no mes selecionado
    df_total = df.groupby(['MES'])['TOTAL'].sum().reset_index()
    months_list = list(months.keys())
    variacao = calculate_percentage_change(df_total['TOTAL'])
    
    # Filtrando para o mês 4
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=months_list,
        y=df_total['TOTAL'],
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
        text=[format_cost(value) for value in df_total['TOTAL']],  # Valores formatados com R$
        textposition='top right',
        textfont=dict(color='black'),
        name='Valor'
    )),
    for i in range(0, len(variacao)):
        fig3.add_annotation(
            x=months_list[i+1],
            y=df_total['TOTAL'][i+1],
            text=f'{variacao[i]:.1f}%',  # Variação percentual formatada
            # showarrow=True,
            # arrowhead=2,
            ax=0,
            ay=+20,
            font=dict(size=15, color='black')
        )
        

    fig3.update_layout(
        title='Faturamento X Meses',
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

    return fig3

@callback(
    Output('income-profit-graph','figure'),
    Input("dp-types","value"),
    
)

def profitIncomeGraph(types):
    df_income = df.groupby(['MES'])['TOTAL'].sum().reset_index()
    df_profit = df_income.copy()
    df_profit['TOTAL'] = df_income['TOTAL'] - df_total_costs['TOTAL']

    df_income['TIPO'] = 'Faturamento'
    df_profit['TIPO'] = 'Lucro'

    df_combined = pd.concat([df_income, df_profit])

    fig4 = px.line(df_combined, x='MES', y='TOTAL', color='TIPO', markers=True)
    
    
    return fig4

    
   
    

#=================================================


