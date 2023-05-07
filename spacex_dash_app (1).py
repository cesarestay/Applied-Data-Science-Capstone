# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},

                                             ],
                                             value='ALL',
                                             placeholder="place holder here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                 dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',  100: '100'},
                                    value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[['Launch Site','class']].groupby('Launch Site').sum('class').reset_index()
        fig = px.pie(data , values='class',
                     names='Launch Site',
                     title='Total Success By Site')
        return fig
    else:
        data =pd.DataFrame(spacex_df[spacex_df['Launch Site']==entered_site].groupby('class')['Launch Site'].count()).reset_index().rename(columns={'Launch Site': "count"})
        fig = px.pie( data , values = 'count',
        names = 'class',
        title = 'Success Rate: ' + entered_site)
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value')
             ,Input(component_id="payload-slider", component_property="value")]
             )
def get_sccatterplot(entered_site,minmax):
    if entered_site == 'ALL':
        data=spacex_df[(spacex_df['Payload Mass (kg)']>minmax[0]) & (spacex_df['Payload Mass (kg)']<minmax[1]) ]
        fig =  px.scatter(data, x="Payload Mass (kg)", y='class',color="Booster Version Category")
        return fig
    else:
        data =spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>minmax[0]) & (spacex_df['Payload Mass (kg)']<minmax[1]) ]
        fig =  px.scatter(data, x="Payload Mass (kg)", y='class',color="Booster Version Category")
        return fig

    # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
        app.run_server()