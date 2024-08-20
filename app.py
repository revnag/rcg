# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 21:24:03 2024

@author: HP
"""

import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output
import plotly.express as px
import dash_bootstrap_components as dbc

def title_pram(dropdown_value: str):
    value=['MP1','MP2','MP5','OSMP1','OSMP2','OSMP5','OSGF','OSMW','OSIOD' ,
           'S1','S2','S5X']  
    label=['Multipath12','Multipath21','Multipath15','Obs per Slip:MP12',
    'Obs per Slip:MP21','Obs per Slip:MP15','Obs per Slip:GF','Obs per Slip:MW',
    'Obs per Slip:IOD','Signal to Noise Ration on L1',
    'Signal to Noise Ration on L2',
    'Signal to Noise Ration on L5']
    for i in range(len(value)):
       if dropdown_value==value[i]:
           return label[i]
def title_site(dropdown_value: str):
    value=['IITK','BOMB','MANI','ROPA','TRIV','DHAN']
    label=['IIT Kanpur','IIT Bombay','MANIT','IIT Ropar','IIST','IIT(IISM]']
    for i in range(len(value)):
       if dropdown_value==value[i]:
           return label[i]
def SetColor(value):
    if(value==2):
        return " red"
    elif(value ==3 ):
        return "blue"
    elif(value == 4):
        return "green"
    elif(value==1):
        return 
pio.renderers.default='browser'

# Plotly and Dash Reading RINGO output 
ringo24 = pd.read_csv('rcgPram.csv')
ind = pd.read_csv('rcgMet.csv')
obs=pd.read_csv('rcgObs.csv')



app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                            'content': "width=device-width, initial-scale=1"}]
                            )
server=app.server
# Layout section : Bootstrap               
app.layout = dbc.Container([
# First Row
    dbc.Row([
        dbc.Col([
             dbc.Card(
                  [
                  dbc.CardImg(src="assets/NCG.png" , 
                              className = 'align-self-right',top=True)
                   ],style = {'width':"6rem"}),
                 ],className="g0",align='center'),
        
        dbc.Col([html.H1("RCG's Quality Parameters  ",
                         className="text-left text-primary")],
                width={'size':7,'offset':0},className="p-1" "g0",align='center'),
        dbc.Col([
           dbc.Card(
              [
              dbc.CardImg(src="assets/Layout.jpg" , 
                          className = 'align-self-right',top=True)
               ],style = {'width':"6rem"}),
             ],className="go" ,align='center'),
       ],justify='around',style={"height": "13%"}),
    html.Br(), 
#First Row A
html.Div([
      html.Span('The graphed parameters include multipath,cycleslip,SNR and % valid observations. Sites having met sensors:',
             style=dict(textAlign='Left',color='DarkRed',fontStyle='italic')),
      
      html.Span('  BOMB,MANI,ROPA and TRIV ',
                style=dict(textAlign='Left',color='DarkRed',fontStyle='italic',) )
   
   ],style={'marginBottom': 10,'marginTop': 30,'font-size':'21px'}),

#First Row B
dbc.Row([
      dbc.Col([
          html.Span('Year'
                     ,style={'font-size':'20px','color':'blue','text-decoration': 'underline','justify':'center'}), 
                ],width=1,style={"text-align": "center"}),
      dbc.Col([
         html.H3('Site'
              ,style={'font-size':'20px','color':'blue','text-decoration': 'underline'}),
         ],width=2,style={"text-align": "center"}),
      dbc.Col([
          html.H3('Parameter  (single)   Constellation  (single/multi)'
               ,style={'font-size':'20px','color':'blue','text-decoration': 'underline'}),
          ],width=6,style={"text-align": "center"}),
     
      dbc.Col([
          html.H3('Check/Uncheck'
               ,style={'font-size':'20px','color':'blue', 'text-decoration': 'underline'}),
          ],width=3,style={"text-align": "left"},className="pr-2"),  
    ],className="pt-2"),           
 
# Second Row
  dbc.Row([
      dbc.Col([
          dcc.Dropdown(
              id="year-dropdown",options={'rcgPram.csv':'2024'},
                  value='rcgPram.csv',clearable=False, )
          ],width={"size": 1, "offset": 0}),
      
      dbc.Col([
          dcc.Dropdown(id='site-dropdown',options={'IITK':'IIT Kanpur',
                      'BOMB':'IIT Bombay','MANI':'MANIT','ROPA':'IIT Ropar',                        
                      'TRIV':'IIST','DHAN':'IIT(IISM)'},value='MANI') 
          ],width={'size':2}),
      
      dbc.Col([
          html.Div([
          dcc.Dropdown(id='quality-dropdown',options={'MP1':'Multipath12','MP2':
                          'Multipath21','MP5':'Multipath15','OSMP1':'Slip:MP12',
                          'OSMP2':'Slip:MP21','OSMP5':'Slip:MP15','OSGF':'Slip:GF',
                          'OSMW':'Slip:MW','OSIOD':'Slip:IOD','S1':'SNR(L1)','S2':'SNR(L2)'
                          ,'S5X':'SNR(L5)'},value='MP1'),
              ],style={"width": "25%"},),
                 
          dcc.Checklist(
              id="const-check",
              options=[
                  {"label": "GPS", "value": "G"},
                  {"label": "GLONASS", "value": "R"},
                  {"label": "GALILEO", "value": "E"},
                  {"label": "BEIDOU", "value": "C"},
                  {"label": "QZSS", "value": "J"},
                  
                    ],
              value=["G"],style={'accent-color': '#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
                    
                ],style=dict(display='flex',),width=6,),
     dbc.Col([
          dcc.Checklist(
                  id="site-check",
                  options=[
                      {"label": "OBS", "value": "OBS"},
                      {"label": "TEMP", "value": "TD"},
                      {"label": "PRES", "value": "PR"},
                        ],value=['OBS'],style={'accent-color': '#A6192E'},
                  inline=True ,inputStyle={"margin-right": "10px","margin-left": "10px"}),
                   ],width={"size": 3}),   
                              
              ], style={'width': '100%'}),
html.Br(),       
#Third Row        
    dbc.Row([
            dcc.Graph(id='quality-graph',responsive=True)
            ],style={"height": "50%"}),
      ],style={"height": "100vh"})
   
    
# Connect the Plotly graph with Dash COmponents    
@app.callback(
    Output('quality-graph','figure'),
    Input('year-dropdown','value'),
    Input('site-dropdown','value'),
    Input('quality-dropdown','value'),
    Input('const-check','value'),
    Input('site-check','value')
)

def graph(yr_sel,site_sel,quality_sel,const_sel,ind_sel):
         ringo= pd.read_csv(yr_sel)
         selection=ringo[ringo['SITE']==site_sel]
         if len(ind_sel) == 0:
             selection= selection[selection['CONST'].isin(const_sel)]
             df=selection
             myy=quality_sel
             pram=title_pram(quality_sel) 
             site=title_site(site_sel)
             value=1
             mycolorVal=SetColor(value)
             legend=True
             fig=select_graph(df,myy,value,pram,site,site_sel,legend,mycolorVal)
         elif 'OBS' in ind_sel:
            selection=obs[obs['SITE']==site_sel]
            df=selection
            myy='OBS'
            pram="% Observations > 10 deg (independent of constellation)"
            site=title_site(site_sel)
            legend=False
            value=2
            mycolorVal=SetColor(value)
            fig=select_graph(df,myy,value,pram,site,site_sel,legend,mycolorVal)
         elif 'TD' in ind_sel:
             selection=ind[ind['SITE']==site_sel]
             df=selection
             myy='TD'
             pram="Dry temperature in deg Celsius"
             site=title_site(site_sel)
             legend=False
             value=3
             mycolorVal=SetColor(value)
             fig=select_graph(df,myy,value,pram,site,site_sel,legend,mycolorVal)
         else:
            selection=ind[ind['SITE']==site_sel]
            df=selection
            myy='PR'
            pram="Pressure in mbar "
            site=title_site(site_sel)
            legend=False
            value=4
            mycolorVal=SetColor(value)
            fig=select_graph(df,myy,value,pram,site,site_sel,legend,mycolorVal)
     
         return fig
def select_graph(df,myy,value,pram,site,site_sel,legend,colorVal):
    if value == 1:
        # Plotly Express
             line_fig=px.line(df,template="plotly_dark",
                          x='DOY',y=myy,
                          color='CONST',
                          color_discrete_map={
                         "G": "#FF6347",
                         "R": "#F0E68C",
                         "E":"#1E90FF",#006400" ,
                          "C":"#9ACD32",#FF1493" ,#000080" ,
                          "J":"#BA55D3",#8B008B "
                          },
                          labels={
                         "CONST": "Satellite Constellation",
                         "DOY": 'Day of year 2024',
                         'MP1':'Multipath12 (m)','MP2':'Multipath21 (m)','MP5':'Multipath15 (m)',
                         'OSMP1':'Obs per Slip:MP12','OSMP2':'Obs per Slip:MP21',
                         'OSMP5':'Obs per Slip:MP15','OSGF':'Obs per Slip:GF',
                          'OSMW':'Obs per Slip:MW','OSIOD':'Obs per Slip:IOD',
                          'S1':'Signal to Noise Ratio (dB)',
                          'S2':'Signal to Noise Ratio (dB)',
                          'S5X':'Signal to Noise Ratio (dB)'
                          },
                          title=f'{pram} in {site}',
                          )             
             line_fig.update_layout(showlegend=legend)
             line_fig.update_traces(mode="markers+lines",marker=dict(size=3))
             line_fig.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
             line_fig.update(layout=dict(title=dict(
                 x=0.5,
                 y=0.9,
                 )))
             return line_fig
        
    else:
       
        line_fig1=px.line(df,template="ggplot2",color_discrete_sequence=[colorVal],
                     x='DOY',y=myy, 
                     labels={"DOY": 'Day of year 2024','PR':'Pressure (mbar)',
                     'TD':'Dry temperature (deg Celsius)'},
                     title=f'{pram} in {site}',)
        line_fig1.update_layout(showlegend=legend,)
        line_fig1.update_traces(mode="markers+lines",marker=dict(size=3))
        line_fig1.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
        line_fig1.update(layout=dict(title=dict(
             x=0.5,
             y=0.9,
             )))
        return line_fig1
   
if __name__=='__main__':
    app.run_server(debug=True)
    
