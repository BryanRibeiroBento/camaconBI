import dash
from dash import html,dcc,Input,Output,callback
import dash_bootstrap_components as dbc



dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Home',  # name of page, commonly used as name of link
                   title='Home',  # title that appears on browser's tab
                   image='assets/camacon.png',  # image in the assets folder
                   description='Histograms are the new bar charts.'
)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Home Page')
        ])
    ])

])