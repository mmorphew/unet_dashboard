''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Image
from bokeh.plotting import figure
import glob
import matplotlib.pyplot as plt
from skimage.transform import resize
import os

# Set up data
top_list = glob.glob(r'unet_dashboard/static/top*')
print(top_list)
for i in range(len(top_list)):
    top_list[i] = os.path.basename(top_list[i])
    top_list[i] = os.path.join("unet_dashboard", "static", top_list[i])

image_library = np.zeros((len(top_list),256,256,3))

for i in range(len(top_list)):
    image = plt.imread(top_list[i])
    image = resize(image, (256, 256, 3)) # resize it
    image_library[i] = image

# Set up plot
plot = figure(plot_height=800, plot_width=800, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.image_url(url=[top_list[0]], x=1, y=1, anchor="bottom_left")


# Set up widgets
text = TextInput(title="title", value='my sine wave')
img_num = Slider(title="image number", value=0, start=0, end=len(top_list)-1, step=1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a = img_num.value

    # Generate the new curve
    plot = figure(plot_height=3000, plot_width=3000, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom")

    plot.image_url(url=[top_list[a]])

img_num.on_change('value', update_data)


# Set up layouts and add to document
inputs = column(text, img_num)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
