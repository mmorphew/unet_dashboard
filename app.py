import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.express as px
import glob
import os
import cv2
import json
import pandas as pd
from skimage.transform import resize
import numpy as np
import datetime as dt
from flask_caching import Cache
from dash_canvas import DashCanvas
import dash_daq as daq
from dash_canvas.utils import array_to_data_url

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

top_list = glob.glob(r'./assets/top*')

#top_list = top_list[:5]

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

    
image_library = np.zeros((len(top_list),256,256,3))

for i in range(len(top_list)):
    image = plt.imread(top_list[i])
    image = resize(image, (256, 256, 3)) # resize it
    image_library[i] = image

#flattened_library = []
#for i in range(len(top_list)):
#    flattened_library.append(image_library[i].flatten())

#df = pd.DataFrame(flattened_library).transpose()

app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Graph(
                    id='image'),
                dcc.Slider(
                id='my-slider',
                min=0, max=len(top_list)-1, step=1, value=int(len(top_list)/2),
                updatemode='mouseup'),
                ]),
            html.Div([
                dcc.Graph(
                    id='image-filtered'),
                dcc.Slider(id='filter-slider',
                    min=1, max=50, step=1, value=5, updatemode='mouseup'),
                ])
#    html.Div(children=list_string, id='stored-data', style={'display':'none'})
            ], style={'columnCount':2}),
        html.Div([
            DashCanvas(id='canvas-color'),
            dcc.Slider(
                id='bg-width-slider',
                min=2,
                max=40,
                step=1,
                value=5
            ),
            daq.ColorPicker(
                id='color-picker',
                label='Brush color',
                value=dict(hex='#119DFF'))
            ])
        ])


@app.callback(Output('image', 'figure'),
              [Input('my-slider', 'value')])
def update_figure(slider_value):
    #dff = df[slider_value]
    #image = dff.values.reshape(256,256,3)
    displayed_image = image_library[slider_value]
    fig = px.imshow(displayed_image)
    fig.update_layout(clickmode='event+select', coloraxis_showscale=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

@app.callback(Output('image-filtered', 'figure'),
        [Input('image', 'figure'), Input('my-slider', 'value'), Input('filter-slider', 'value')])
def update_filter(original_image, slider_value, filter_choice):
    #dff = df[slider_value]
    #image = dff.values.reshape(256,256,3)
    displayed_image = image_library[slider_value]
    filterSize = filter_choice
    filterSize = (filterSize, filterSize)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,  
                                   filterSize) 
  
    # Applying the Top-Hat operation 
    tophat_img = cv2.morphologyEx(np.float32(displayed_image),  
                              cv2.MORPH_TOPHAT, 
                              kernel) 
    fig = px.imshow(tophat_img)
    fig.update_layout(clickmode='event+select', coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig

@app.callback(Output('canvas-color', 'image_content'),
        [Input('my-slider', 'value'), Input('image', 'figure')])
def update_background_image(slider_value, image_figure):
    displayed_image = image_library[slider_value]
    return array_to_data_url((displayed_image*255).astype(np.uint8))

@app.callback(Output('canvas-color', 'lineColor'),
            [Input('color-picker', 'value')])
def update_canvas_linewidth(value):
    if isinstance(value, dict):
        return value['hex']
    else:
        return value


@app.callback(Output('canvas-color', 'lineWidth'),
            [Input('bg-width-slider', 'value')])
def update_canvas_linewidth(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)
