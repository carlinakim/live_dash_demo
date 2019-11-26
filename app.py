import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

#theme for altair chair 
def make_plot(x_axis='Displacement',
             y_axis= 'Cylinders'): #Add in a default value to start with

    # Create a plot of the Displacement and the Horsepower of the cars dataset
    
    #add theme there
    
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    #alt.themes.enable('none') # to return to default

    chart = alt.Chart(vega_datasets.data.cars.url).mark_point(size=90).encode(
                alt.X(f'{x_axis}:Q', title = f'{x_axis}'),
                alt.Y(f'{y_axis}:Q', title = f'{y_axis}'),
                tooltip = ['Horsepower:Q', 'Displacement:Q']
            ).properties(title= f'Horsepower vs. {x_axis}',
                        width=500, height=350).interactive()

    return chart
    

#LAYOUT    
app.layout = html.Div([


    ### ADD CONTENT HERE like: html.H1('text'),
    html.H1("This is my first dashboard"),
    html.H2("This is a subtitle"),
    html.H5("This is an actual plot"),

    html.Img(src = "https://www.incimages.com/uploaded_files/image/970x450/getty_938993594_401542.jpg"),

    dcc.Markdown('''

    ## Add markdown text here (copy this entire cell and paste it in your app
    * my list 
    '''
    ),
    
    #ADDING DROPDOWN FOR THE DIFFERENT PLOTS 
    dcc.Dropdown(
id='dd-chart',
options=[
    {'label': 'Fuel efficiency', 'value': 'Miles_per_Gallon'},
    {'label': 'Cylinders', 'value': 'Cylinders'},
    {'label': 'Engine Displacement', 'value': 'Displacement'},
    # Missing option here
],
value='Displacement', #DEFAULT VALUE
style=dict(width='45%',
           verticalAlign="middle")
          ),
    
    dcc.Dropdown(
id='dd-chart-y',
options=[
    {'label': 'Fuel efficiency', 'value': 'Miles_per_Gallon'},
    {'label': 'Cylinders', 'value': 'Cylinders'},
    {'label': 'Engine Displacement', 'value': 'Displacement'},
    # Missing option here
],
value='Displacement', #DEFAULT VALUE
style=dict(width='45%',
           verticalAlign="middle")
          ),

    #ADDING IN SLIDER
    dcc.Slider(
    min=0,
    max=9,
    marks={i: 'Label {}'.format(i) for i in range(10)},
    value=5,
    ),

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='2000',
        width='1500',
        style={'border-width': '5px'},

        ################ The magic happens here
        #srcDoc=open('complex_chart.html').read()
        srcDoc = make_plot().to_html()
        ################ The magic happens here
        ),

])

@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart', 'value'),
    dash.dependencies.Input('dd-chart-y', 'value')])
def update_plot(xaxis_column_name, yaxis_column_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(xaxis_column_name,
                            yaxis_column_name).to_html()
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True) 
