#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import needed libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# import geojson data with polish regions
# https://github.com/ppatrzyk/polska-geojson
import json
with open('Data/map.geojson', encoding='UTF-8') as f:
    data = json.load(f)

# Clean data
df = pd.read_csv('Data/matura_region_ratio.csv')
df['region_pl'] = df['region_pl'].apply(lambda x: x.lower())
df['ratio'] = df['ratio'].apply(lambda x: float("{:.2f}".format(x)))

# App layout
app.layout = html.Div([
    # Title on the page
    html.H1('Polish National Exam Passing Rate By Region', style={'text-align': 'center', 'margin': 0}),
    
    # Dropdown for choosing the year
    dcc.Dropdown(id='year', options=[
        {'label': '2010', 'value': 2010},
        {'label': '2011', 'value': 2011},
        {'label': '2012', 'value': 2012},
        {'label': '2013', 'value': 2013},
        {'label': '2014', 'value': 2014},
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019},
        {'label': '2020', 'value': 2020},
        {'label': '2021', 'value': 2021}],
        multi=False,
        value=2021,
        style={'width': '40%'}
        ),
    # Info about what percent passed this year
     html.Div(id='container', children='', style={'text-align': 'center', 'margin': 0}),

    # Dropdown for choosing the level
    dcc.Dropdown(id='gender', options=[
        {'label': 'Men', 'value': 'Men'},
        {'label': 'Women', 'value': 'Women'}],
        multi=False,
        value='Men',
        style={'width': '40%'}
        ),
    # The actual graph
    dcc.Graph(id='map_plot', figure = {})
])

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='container', component_property='children'),
    Output(component_id='map_plot', component_property='figure')],
    [Input(component_id='year', component_property='value'),
    Input(component_id='gender', component_property='value')]
)
def update_graph(year, gender):

    dff = df.copy()
    dff = dff[dff['year'] == year]
    dff = dff[dff['gender'] == gender]

    rate = dff[dff['region_pl'] == 'ogółem']['ratio'].values[0]

    
    
    container = "{}% of students passed the exam in {}.".format(rate * 100, year)
    
    
    fig = px.choropleth(dff, geojson=data, color='ratio',
                        locations="region_pl", featureidkey="properties.nazwa",
                        projection="mercator",
                        color_continuous_scale='Viridis',
                        labels = {'region_pl': 'Region', 'ratio': 'Passing Rate'},
                         height=480)
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return container, fig

if __name__ == '__main__':
    app.run_server(debug=False)


# In[179]:


# Trying the graph
dff = df.copy()
dff = dff[dff['year'] == 2010]
dff = dff[dff['gender'] == 'Men']



fig = px.choropleth(dff, geojson=data, color='ratio',
                    locations="region_pl", featureidkey="properties.nazwa",
                    projection="mercator",
                    color_continuous_scale='Viridis',
                    labels = {'region_pl': 'Region', 'ratio': 'Passing Rate'},)
    
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(plot_bgcolor= 'rgb(158, 137, 141, 0.2)')
fig.update_layout(paper_bgcolor="rgb(158, 137, 141, 0.2)")


# In[ ]:




