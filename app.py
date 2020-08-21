import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import glob
import os

app = dash.Dash()
server = app.server
file_list = glob.glob(r'.\assets\*')
for i in range(len(file_list)):
    file_list[i] = os.path.basename(file_list[i])
app.layout = html.Div([
    html.Section(id="slideshow", children=[
        html.Div(id="slideshow-container", children=[
            html.Div(id="image"),
            dcc.Interval(id='interval', interval=3000)
        ]),
    dcc.Slider(
        id='my-slider',
        min=0, max=len(file_list)-1, step=1, value=10),
    html.Div(id='slider-output-container'),
    ])

])
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return '{}'.format(file_list[value])
@app.callback(Output('image', 'children'),
              [Input('my-slider', 'value')])
def display_image(value):
    img = html.Img(src= app.get_asset_url(file_list[value]), height=512, width=512)
    return img

if __name__ == '__main__':
    app.run_server(debug=True)
