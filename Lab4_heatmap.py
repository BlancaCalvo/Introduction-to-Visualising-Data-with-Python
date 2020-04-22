
# run the script like: bokeh serve --show Lab4_heatmap.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.models import HoverTool, Slider, ColumnDataSource, Select, CDSView, GroupFilter
from bokeh.io import curdoc
import seaborn as sns

def get_dataset(path):
  data = pd.read_csv(path, sep=',', index_col = False, parse_dates=['dt'])
  data.rename(columns={'dt':'date'}, inplace=True) # we do this because we have a package called dt and it could make things confusing
  # the dt package allows us to extract the month and the year from a full date
  data['year'] = data.date.dt.year
  data['month'] = data.date.dt.month
  return data

def map_colors(data, sns_palette, n_colors):
  pal = sns.color_palette(sns_palette, n_colors) # we get a palette with 8 different colors, seborn palettes: https://seaborn.pydata.org/tutorial/color_palettes.html
  colors = pal.as_hex() # we get the values of those colors
  colormap = LinearColorMapper(palette=colors, low=data.LandAverageTemperature.min(), 
                    high=data.LandAverageTemperature.max()) # note that we are working with linear data here
  return colormap, colors

def range_data(data):
  # creating a range for the figure, we will need this later!
  years = list(data.year)
  months = list(data.month)
  years_range =(years[0], years[-1])
  months_range = (months[0], months[-1])
  return years_range, months_range

# STEP 1: import the data
data = get_dataset('data/GlobalTemperatures.csv')
# STEP 2: map the colors to our data
colormap, colors = map_colors(data, "coolwarm", 8)
# creating a range for the figure, we will need this later!
years_range, months_range = range_data(data)
# STEP 3: create the data source for the interactive graph
source = ColumnDataSource(data={ 
    'x' : data.year,
    'y' : data.month,
    'value' : data.LandAverageTemperature
})

# STEP 4: create the base figure
p = figure(title="World temperature",
      x_range=years_range, y_range=months_range, # stablished the limits of the plot axes
           plot_width=900, plot_height=400,
           tools="hover,save,pan,box_zoom,reset,wheel_zoom", # the hover tool adds the label to each data point when the mouse is on it
           tooltips=[('Year', '@x'), ('Value', '@value')]) # this tells what's going to be displayed by hover

# STEP 5: fill it with rectanbles
p.rect(x="x", y="y", width=1, height=1, # height and width of the rectangles
       source=source,
       fill_color={'field': 'value', 'transform': colormap},
       line_color=None)

# STEP 6: add elements to the interactive graph 
# add a color bar that serves as legend
color_bar = ColorBar(color_mapper=colormap, major_label_text_font_size="10pt",
	ticker=BasicTicker(desired_num_ticks=len(colors)),
	border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

# ADD AN INTERACTIVE SELECT!!!
# we create the dropdown to be able to choose between variables
menu = Select(options=['Land Average Temperature', 'Land Average Temperature Uncertainty'],
	value='Land Average Temperatures', title='Variable')


def update_plot(attr, old, new): # we define the function to upload the plot when the factor is changed
  if new == 'Land Average Temperature': 
    source.data = {
        'x' : data.year,
        'y' : data.month,
        'value': data.LandAverageTemperature
      }
  elif new == 'Land Average Temperature Uncertainty':
    source.data = {
        'x' : data.year,
        'y' : data.month,
        'value': data.LandAverageTemperatureUncertainty
      }

menu.on_change('value', update_plot) # we link the function to the dropdown menu

# STEP 7: design our layout
layout = column (p, menu) # we create the layout in a column shape

output_file = ('heatmap.html') # we output the html file

# STEP 8: run the server behind the visualisation!
curdoc().add_root(layout) 
