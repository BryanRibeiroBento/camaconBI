import dash
from dash import html, dcc,Output,Input
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX], 
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

 

navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src = "assets/camacon.png", height="50px"),
                 dbc.NavbarBrand('Camacon',className='ms-2'),

            ],width='auto'),


            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home",href="/")),
                    dbc.NavItem(dbc.NavLink("C.Custos",href="/dash")),
                    dbc.NavItem(dbc.NavLink("Faturamento",href="/income")),
                    dbc.NavItem(dbc.NavLink("Equipamentos",href="/dash")),
                    dbc.NavItem(dbc.NavLink("Patrimônio",href="/dash")),
                    dbc.NavItem(dbc.NavLink("Diesel",href="/dash")),
                    
                ],navbar = True)

            ],width='auto'),

        ]),

        

    ]),
    color="primary",
    dark=True,
)

app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col([
                    navbar
            ], width=12, className='bg-primary'),
        ], className="bg-primary"),
    dbc.Row([
        dbc.Col(
                [
                    dash.page_container
                ], width=12)
    ])
], fluid=True)


@app.callback(
    Output("dash-link", "active"),
    [Input("url", "pathname")]
)
def update_active_link(pathname):
    return pathname == "/dash"


if __name__ == "__main__":
    app.run_server(debug=False)
