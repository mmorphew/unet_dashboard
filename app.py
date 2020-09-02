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

top_list = glob.glob(r'./assets/top*')
dsm_list = glob.glob(r'./assets/dsm*')
image_library = np.zeros((len(top_list), 256, 256, 3))

for i in range(len(file_list)):
    image = plt.imread(file_list[i])
    image = resize(image, (256, 256, 3)) # resize it
    image_library[i] = image
# Getting the kernel to be used in Top-Hat
filterSize = 400
filterSize =(filterSize, filterSize) 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,  
                                   filterSize) 
  
# Applying the Top-Hat operation 
tophat_img = cv2.morphologyEx(image,  
                              cv2.MORPH_TOPHAT, 
                              kernel) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    dcc.Graph(
        id='image'),
    dcc.Slider(
        id='my-slider',
        min=0, max=len(file_list)-1, step=1, value=int(len(file_list)/2),
        updatemode='drag'),
    html.Div(id='slider-output-container'),
    dcc.Graph(
        id='image-filtered'),
    dcc.Slider(id='filter-slider',
        min=1, max=50, step=1, value=5, updatemode='drag')
])

@app.callback(Output('image', 'figure'),
              [Input('my-slider', 'value')])
def update_figure(image_choice):
    image = image_library[image_choice]
    fig = px.imshow(image)
    fig.update_layout(clickmode='event+select')
    return fig
@app.callback(Output('image-filtered', 'figure'),
        [Input('filter-slider', 'value'), Input('my-slider', 'value')])
def update_filter(filter_choice, image_choice):
    image = image_library[image_choice]
    filterSize = filter_choice
    filterSize = (filterSize, filterSize)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,  
                                   filterSize) 
  
    # Applying the Top-Hat operation 
    tophat_img = cv2.morphologyEx(image,  
                              cv2.MORPH_TOPHAT, 
                              kernel) 
    fig = px.imshow(tophat_img)
    fig.update_layout(clickmode='event+select')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
