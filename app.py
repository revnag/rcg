# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 14:08:04 2024

@author: HP
"""

import pandas as pd
import plotly.io as pio
from dash import Dash,html,dcc,Input,Output,callback
import plotly.express as px
import dash_bootstrap_components as dbc
import sidefunc as s

pio.renderers.default='browser'

# Plotly and Dash Reading RINGO output 
ringo = pd.read_csv('rcgPram.csv')
met = pd.read_csv('rcgMet.csv')
obs=pd.read_csv('rcgObs.csv')
pos=pd.read_csv('gamPos.csv')

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                            'content': "width=device-width, initial-scale=1"}] )
SIDEBAR_STYLE = {
    "margin": "1rem 0rem 2rem ",
    "padding": "1rem 1rem 4rem ","background-color": "#f8f9fa"}
GRAPH_STYLE = {
    "margin": "1rem 0rem 2rem ",
    "padding": "2rem 1rem ",
    "background-color": "#f8f9fa"}
sidebar = html.Div([
   html.H3("GPS Position Time Series",style={'font-size':'18px','color':'green','text-decoration': 'underline','justify':'left'}),
   html.H3("GAMIT",style={'font-size':'15px','color':'red','justify':'center'}),
   dcc.Checklist(
       id="g-pos",options=['dN','dE','dU'],
       value=["dN"],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
   html.Br(),
   html.H3("BERNESE",style={'font-size':'15px','color':'red','justify':'center'}),
   dcc.Checklist(
     id="b-pos",options=[{'label':'dN','value':'dN','disabled': True},
    {'label':'dE','value':'dE','disabled': True},{'label':'dU','value':'dU','disabled': True},],
       value=[ ],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
   html.Br(),            
   html.H3("TBC",style={'font-size':'15px','color':'red','justify':'center'}),
   dcc.Checklist(
       id="tbc-pos",options=[{'label':'dN','value':'dN','disabled': True},
      {'label':'dE','value':'dE','disabled': True},{'label':'dU','value':'dU','disabled': True},],
         value=[ ],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
   html.Br(),
   html.H3("Site Map",style={'font-size':'20px','color':'red','justify':'center'}),
   dcc.Checklist(
       id="rcgloc",options=[{"label":"Site Map","value":"loc"}],
       value= ['loc'],style={'accent-color':'#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"},),
    ],style=SIDEBAR_STYLE,)
server=app.server
# Layout section : Bootstrap               
app.layout = dbc.Container([
# First Row
dbc.Row([
  dbc.Col([dbc.Card([
    dbc.CardImg(src="assets/NCG.png",className = 'align-self-right',top=True)
      ],style = {'width':"6rem",'border':0}),],className="g0",align='center'),
  dbc.Col([html.H1("RCG's Quality Parameters",className=" text-align: justify text-primary")],
        width={'size':7,'offset':0},className="p-1" "g0",align='center'),
  dbc.Col([dbc.Card([
    dbc.CardImg(src="assets/bluelog.jpg",className = 'align-self-left',top=True)
      ],style = {'width':"6rem",'border':0})],className="go" ,align='center'),
       ],justify='around',style={'marginTop': 30,"height": "7vh"}),
# html.Br(), 
#First Row A
html.Div([html.Span('The graphed parameters include multipath,cycleslip,SNR and % valid observations. Sites having met sensors:',
         style=dict(textAlign='Left',color='DarkRed',fontStyle='italic')),
         html.Span('  BOMB, MANI, ROPA and TRIV      ',style=dict(textAlign='Left',color='DarkRed',fontStyle='italic') ),
         html.Span('Note : Checkboxes need to be unchecked to view selected options',style=dict(textAlign='Left',color='Red',fontStyle='italic',) )
      ],style={'marginBottom': 10,'marginTop': 30,'font-size':'21px',"height": "4vh"}),
html.Br(),
#First Row B
dbc.Row([
  dbc.Col([html.H3('Year',style={'font-size':'20px','color':'blue','text-decoration': 'underline','justify':'center'}), 
          ],width=1,style={"text-align": "center"}),
  dbc.Col([html.H3('Site',style={'font-size':'20px','color':'blue','text-decoration': 'underline'}),
          ],width=2,style={"text-align": "center"}),
  dbc.Col([html.H3('Parameter (single) Constellation (single/multi)',style={'font-size':'20px','color':'blue','text-decoration': 'underline'}),
          ],width=6,style={"text-align": "center"}),
  dbc.Col([html.H3('Check/Uncheck',style={'font-size':'20px','color':'blue', 'text-decoration': 'underline'}),
          ],width=3,style={"text-align": "left"}),  
    ],style={"height": "4vh"}),           
# Second Row
dbc.Row([
  dbc.Col([dcc.Dropdown(id="year-dropdown",options={'ringo':'2024'},value='ringo',clearable=False, )
          ],width={"size": 1, "offset": 0}),
  dbc.Col([dcc.Dropdown(id='site-dropdown',options={'IITK':'IIT Kanpur','BOMB':'IIT Bombay',
                       'MANI':'MANIT','ROPA':'IIT Ropar','TRIV':'IIST','DHAN':'IIT(IISM)'},value='IITK') 
          ],width={'size':2}),
  dbc.Col([html.Div([
    dcc.Dropdown(id='quality-dropdown',options={'MP1':'Multipath12','MP2':'Multipath21','MP5':'Multipath15',
                  'OSMP1':'Slip:MP12','OSMP2':'Slip:MP21','OSMP5':'Slip:MP15','OSGF':'Slip:GF','OSMW':'Slip:MW',
                  'OSIOD':'Slip:IOD','S1':'SNR(L1)','S2':'SNR(L2)','S5X':'SNR(L5)'},value='MP1'),
                    ],style={"width": "25%"},),
    dcc.Checklist(id="const-check",options=[{"label":"GPS","value":"G"},{"label":"GLONASS","value":"R"},
                  {"label":"GALILEO","value":"E"},{"label":"BEIDOU","value":"C"},{"label":"QZSS","value":"J"}],
                  value=[''],style={'accent-color': '#A6192E'},inline=True,inputStyle={"margin-right": "10px","margin-left": "10px"}),
            ],style=dict(display='flex',),width=6,),
  dbc.Col([dcc.Checklist(id="ind-check",options=[{"label":"OBS","value":"OBS"},{"label":"TEMP","value":"TD"},{"label":"PRES","value":"PR"}],
                  value=[''],style={'accent-color': '#A6192E'},inline=True ,inputStyle={"margin-right": "10px","margin-left": "10px"}),
                   ],width={"size": 3}),   
       ], style={"height": "4vh"}),

#Third Row        
dbc.Row([
  dbc.Col([sidebar],width=2),
  dbc.Col([dcc.Graph(id='quality-graph',responsive=True)],width='10'),
       ],style={"height": "80vh"}),
# End Container
],class_name='m-auto' 'p-auto')
  #style={'margin': '5px' '10px' '0px' '20px'})
@callback(
    Output('quality-graph','figure'),
    Input('year-dropdown','value'),
    Input('site-dropdown','value'),
    Input('quality-dropdown','value'),
    Input('const-check','value'),
    Input('ind-check','value'), 
    Input('g-pos','value'),
    Input('b-pos','value'),
    Input('tbc-pos','value'),
    Input('rcgloc','value')
    )

def graph(yr_sel,site_sel,quality_sel,const_sel,ind_sel,g,b,tbc,loc):
       selection=ringo[ringo['SITE']==site_sel]
       fig=mymap('rcgloc.csv')
# Creating Graph conditions 
       if loc!= []:
          fig=mymap('rcgloc.csv')
       elif g != []:
          possel=pos[pos['SITE']==site_sel]
          if 'dN' in g:
            yax='dN'
            ery='Sn'
            rangey=[-10,10]
            mycolorVal='red'
          elif 'dE' in g:
            yax='dE'
            ery='Se'
            rangey=[-15,15]
            mycolorVal='yellow'
          else:
            yax='dU'
            ery='Su'
            rangey=[-30,30]
            mycolorVal='deepskyblue'
          pram='GPS Position Time Series '
          sitel=s.label_site(site_sel)
          legend=True
          fig=pos_graph(possel,yax,ery,rangey,pram,sitel,legend,mycolorVal)
          
       elif len(const_sel) > 1:
          consel= selection[selection['CONST'].isin(const_sel)]
          yax=quality_sel
          pram=s.label_pram(quality_sel) 
          sitel=s.label_site(site_sel)
          legend=True
          fig=const_graph(consel,yax,pram,sitel,site_sel,legend)
          
       elif ind_sel != []:
         if ('OBS' in ind_sel):
          obssel=obs[obs['SITE']==site_sel]
          df=obssel
          yax='OBS'
          pram="% Observations > 10 deg (independent of constellation)"
          sitel=s.label_site(site_sel)
          legend=True
          mycolorVal='red'
          fig=ind_graph(df,yax,pram,sitel,legend,mycolorVal) 
         elif ('TD' in ind_sel):
          metsel=met[met['SITE']==site_sel]
          yax='TD'
          pram="Dry temperature in deg Celsius"
          sitel=s.label_site(site_sel)
          legend=True
          mycolorVal='blue'
          fig=ind_graph(metsel,yax,pram,sitel,legend,mycolorVal)
         elif ('PR' in ind_sel):
          metsel=met[met['SITE']==site_sel]
          sitel=s.label_site(site_sel)
          yax='PR'
          pram="Pressure in mbar "
          legend=True
          mycolorVal='green'
          fig=ind_graph(metsel,yax,pram,sitel,legend,mycolorVal)
       # else:
       #    fig=mymap('rcgloc.csv')
       return fig
     
       
# Function to plot graph  
def pos_graph(possel,yax,ery,rangey,pram,sitel,legend,mycolorVal):
  fig = px.scatter(possel,template="plotly_dark",y=yax, x="DOY", error_y=ery,
        labels={"DOY": 'Day of year 2024'},title=f'{pram} in {sitel}',)
  fig.update_layout(yaxis_title='Component in mm',legend_title=f' {yax}')
  fig.update_traces(error_y=dict(color='#00FFFF',thickness=0.4))
  fig.update_traces(showlegend=legend)
  fig.update_traces(marker=dict(size=5,color=mycolorVal))
  fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='LightPink')
  fig.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
  fig.update(layout=dict(title=dict(x=0.5,y=0.9,))) 
  fig.update_layout(legend=dict(orientation='h',bordercolor="White",y=1,x=1,borderwidth=1))
  fig.update_layout(yaxis_range=rangey)
  return fig 

def const_graph(df,yax,pram,sitel,site_sel,legend):
# Constellation  based parameters
  line_fig=px.line(df,template="plotly_dark",
      x='DOY',y=yax,color='CONST',color_discrete_map={"G": "#FF6347",
         "R": "#F0E68C","E":"#1E90FF","C":"#9ACD32","J":"#BA55D3"},
        labels={"CONST": "Satellite Constellation","DOY": 'Day of year 2024',
        'MP1':'Multipath12 (m)','MP2':'Multipath21 (m)','MP5':'Multipath15 (m)',
        'OSMP1':'Obs per Slip:MP12','OSMP2':'Obs per Slip:MP21','OSMP5':'Obs per Slip:MP15','OSGF':'Obs per Slip:GF',
        'OSMW':'Obs per Slip:MW','OSIOD':'Obs per Slip:IOD','S1':'Signal to Noise Ratio (dB)',
        'S2':'Signal to Noise Ratio (dB)','S5X':'Signal to Noise Ratio (dB)'},
        title=f'{pram} in {sitel}')             
  line_fig.update_layout(showlegend=legend)
  line_fig.update_traces(mode="markers+lines",marker=dict(size=3))
  line_fig.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
  line_fig.update(layout=dict(title=dict(x=0.5,y=0.9,)))
  return line_fig

def ind_graph(df,yax,pram,sitel,legend,mycolorVal):   
# Constellation independent Information
  line_fig1=px.line(df,template="ggplot2",color_discrete_sequence=[mycolorVal],
      x='DOY',y=yax,labels={"DOY": 'Day of year 2024','PR':'Pressure (mbar)',
      'TD':'Dry temperature (deg Celsius)'},
      title=f'{pram} in {sitel}',)
  line_fig1.update_layout(showlegend=legend,)
  line_fig1.update_traces(mode="markers+lines",marker=dict(size=3))
  line_fig1.update_layout(hoverlabel=dict(bgcolor="white",font_size=16,font_family="Rockwell"))
  line_fig1.update(layout=dict(title=dict(x=0.5,y=0.9, )))
  return line_fig1  

def mymap(file):
# Creating Location map
  df = pd.read_csv(file)
  mycolorVal='red'
  rcgloc = px.scatter_mapbox(df, lat="Lat", lon="Lon",zoom=3, mapbox_style='open-street-map',text= df['SITE'],)
  rcgloc.update_layout(hoverlabel=dict(bgcolor="white",font_size=10,font_family="Rockwell"))
  rcgloc.update_traces(marker=dict(size=8,color=mycolorVal))
  rcgloc.update_traces(textposition='top right',textfont=dict(color='blue',size=11),
                  mode='markers+text',)
  rcgloc.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
)
  return rcgloc
 
if __name__=='__main__':
    app.run_server(debug=True)
    
