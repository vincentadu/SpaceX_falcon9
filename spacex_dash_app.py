# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
site_dropdown = spacex_df["Launch Site"].value_counts()
site_dropdown = list(site_dropdown.index)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site_dropdown',options=[{'label': 'All Sites', 'value': 'ALL'},
                                                                         {'label': site_dropdown [0], 'value': site_dropdown [0]},
                                                                         {'label': site_dropdown [1], 'value': site_dropdown [1]},
                                                                         {'label': site_dropdown [2], 'value': site_dropdown [2]},
                                                                         {'label': site_dropdown [3], 'value': site_dropdown [3]},
                                                                         ],
                                                                        value='ALL',
                                                                        placeholder="Select a Launch Site here",
                                                                        searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload_slider',
                                    min=0,max=10000,step=1000,
                                    marks = {
                                            0: '0',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500',
                                            10000: '10000'
                                    },

                                    value=[min_payload,max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id='success-pie-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value')]
)
def get_pie_chart(entered_site):
    filtered_df  = spacex_df[spacex_df['class'] == 1]
    filter = spacex_df['Launch Site'] == entered_site
    filter_launchSite  = spacex_df.loc[filter]
    if entered_site == "ALL":
        fig = px.pie(filtered_df , names = 'Launch Site',title = 'All Site Success Launches')
    else:
        fig = px.pie(filter_launchSite, names = 'class',title = f"{entered_site} Sucess and Failed Launches")
    return fig
 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id='success-payload-scatter-chart',component_property='figure'),
     [Input(component_id='site_dropdown',component_property='value'),Input(component_id="payload_slider", component_property="value")]
)
def update_scattergraph(entered_site,payloadslider):
    filtered_df  = spacex_df
    filt = spacex_df['Launch Site'] == entered_site
    df1  = spacex_df.loc[filt]

    if entered_site == 'ALL':
        min, max = payloadslider
        filt1 = (filtered_df['Payload Mass (kg)'] > min) & (filtered_df['Payload Mass (kg)'] < max)
        fig = px.scatter(
            filtered_df[filt1], x="Payload Mass (kg)", y="class",
            color="Booster Version", title = 'Correlation Between Payload and Sucess for All Sites')
    else:
        min, max = payloadslider
        filt2 = (df1['Payload Mass (kg)'] > min) & (df1['Payload Mass (kg)'] < max)
        fig = px.scatter(
            df1[filt2], x="Payload Mass (kg)", y="class",
            color="Booster Version", title = f"Correlation Between Payload and Sucess for {entered_site} ")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
