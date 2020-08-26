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

file_list = glob.glob(r'.\assets\*')
image = plt.imread(file_list[0])
image = resize(image, (256, 256, 3)) # resize it
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


fig = px.imshow(image)

fig.update_layout(clickmode='event+select')

app.layout = html.Div([
    dcc.Graph(
        id='image'),
    dcc.Slider(
        id='my-slider',
        min=0, max=len(file_list)-1, step=1, value=int(len(file_list)/2),
        updatemode='drag'),
    html.Div(id='slider-output-container')
])

@app.callback(Output('image', 'figure'),
              [Input('my-slider', 'value')])
def update_figure(image_choice):
    image = plt.imread(file_list[image_choice])
    image = resize(image, (256, 256, 3))
    fig = px.imshow(image)
    fig.update_layout(clickmode='event+select')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
