# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 05:49:46 2024

@author: revna
"""
import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output
import plotly.express as px

pio.renderers.default='browser'

#Plotly and Dash
ringo = pd.read_csv('ringo.csv')


# Create Dash object named app
app=Dash()
server=app.server

site_dropdown = dcc.Dropdown(id='site-dropdown',options=ringo['SITE'].unique(),
                            value='BART')

app.layout = html.Div([
    html.H1('Quality Parameters of CORS stations based on RINGO software'),
    html.Br(),    
    site_dropdown,
    dcc.RadioItems(id='quality-radio',options={'MP1':'Multipath12','MP2':
                                               'Multipath21'},
                   value='MP1',inline=True),
    dcc.Graph(id='quality-graph')
    ])

@app.callback(
    Output('quality-graph','figure'),
    Input('site-dropdown','value'),
    Input('quality-radio','value')
)

def update_graph(selected_site,selected_quality):
     filtered_site=ringo[ringo['SITE']==selected_site]
     line_fig=px.line(filtered_site,
                      x='DOY',y=selected_quality,
                      color='CONST',
                      labels={
                     "CONST": "Satellite Constellation",
                     "DOY": "Day Of Year",
                     "MP1": "Multipath12"
                 },
                      title=f'{selected_quality} in {selected_site}'
                      )
     return line_fig
    
if __name__ == "__main__":
    app.run_server(debug=True)