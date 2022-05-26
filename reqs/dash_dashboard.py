#!/usr/bin/env python
# coding: utf-8

# In[99]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Clean data
df = pd.read_csv('Data/matura_results.csv')
df['subject'] = df['subject'].apply(lambda x: x.strip())
df = df.groupby(['level', 'subject', 'gender', 'year'])[['value_perc']].mean()
df.reset_index(inplace=True)
df = df[ (df['gender'] == 'Men') | (df['gender'] =='Women')]

# App layout
app.layout = html.Div([
    # Title on the page
    html.H1('Polish National Exam Subjects By Year', style={'text-align': 'center'}),
    
    # Dropdown for choosing the year
    dcc.Dropdown(id='year', options=[
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019},
        {'label': '2020', 'value': 2020},
        {'label': '2021', 'value': 2021}],
        multi=False,
        value=2015,
        style={'width': '40%', 'display': 'inline-block'}
        ),
    
    # Dropdown for choosing the level
    dcc.Dropdown(id='level', options=[
        {'label': 'Advanced', 'value': 'Advanced'},
        {'label': 'Basic', 'value': 'Basic'}],
        multi=False,
        value='Basic',
        style={'width': '40%', 'display': 'inline-block'}
        ),
    # Some space 
    html.Br(),
    html.Br(),
    # The actual graph
    dcc.Graph(id='bar-chart', figure = {})
])

# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    [Input(component_id='year', component_property='value'),
     Input(component_id='level', component_property='value')]
)
def update_graph(year, level):

    df_cleared = df.copy()
    df_cleared = df_cleared[df_cleared['year'] == year]
    df_cleared = df_cleared[df_cleared['level'] == level]
    df_cleared = df_cleared.sort_values('value_perc', ascending=False)

    # Plotly Express
    fig = px.bar(df_cleared, x='subject', y='value_perc', color='gender', 
                labels = {'value_perc': 'Average Score (%)', 'subject': 'Subject'})
    fig.update_layout(barmode='group')
    fig.update_layout(yaxis_range=[0,100])
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)


# In[97]:


df_cleared = df.copy()
df_cleared = df_cleared[df_cleared['year'] == 2017]
df_cleared = df_cleared[df_cleared['level'] == 'Basic']
df_cleared = df_cleared.sort_values('value_perc', ascending=False)

# Plotly Express
fig = px.bar(df_cleared, x='subject', y='value_perc', color='gender', 
            labels = {'value_perc': 'Average Score (%)', 'subject': 'Subject'})
fig.update_layout(barmode='group')
fig.update_layout(yaxis_range=[0,100])


# In[ ]:




