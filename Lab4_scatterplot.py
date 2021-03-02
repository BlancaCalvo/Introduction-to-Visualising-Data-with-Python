
# run the script like: bokeh serve --show Lab4_scatterplot.py

import pandas as pd
import datetime as dt
from bokeh.plotting import figure, show, output_file
from bokeh.models import CategoricalColorMapper, ColumnDataSource, Slider, Select, CDSView, GroupFilter, RangeSlider, CheckboxGroup
import seaborn as sns
from bokeh.layouts import column, row
from bokeh.io import curdoc


def get_dataset(path):
  data = pd.read_csv(path, sep=',', index_col = False, parse_dates=['dt'])
  data.rename(columns={'dt':'date'}, inplace=True) # we do this because we have a package called dt and it could make things confusing
  # the dt package allows us to extract the month and the year from a full date
  data['year'] = data.date.dt.year
  data['month'] = data.date.dt.month
  countries = ["China", "Australia", "Netherlands (Europe)", "Austria", 'Colombia', 'Comoros']
  data = data[data.Country.isin(countries)]
  #data = data[data.month == 1]
  return data

def map_colors(data, sns_palette, n_colors):
	pal = sns.color_palette(sns_palette, n_colors) # 3 is the number of colors to extract from the palette
	colors = pal.as_hex() # get the values of those colors. We could also have written the name/numbers of some colors
	#print(colors) # you can observe that this is just a string of color values
	colormap = CategoricalColorMapper(palette=colors, factors=data['Country'].unique())
	return colormap, colors

# STEP 1: import the data
data = get_dataset('data/GlobalLandTemperatures/GlobalLandTemperaturesByCountry.csv')
# STEP 2: map the colors to our data
colormap, colors = map_colors(data, "hls", len(list(data.Country.unique())))
# STEP 3: create the data source for the interactive graph
source = ColumnDataSource(data={ 
    'year' : data.year,
    'month' : data.month,
    'temperature' : data.AverageTemperature,
    'country' : data.Country
})

# STEP 4: create the base figure
p = figure(title = "Country Land Temperture",
	plot_width=900, plot_height=400,
	tools="hover, save, pan, box_zoom, reset, wheel_zoom", # here we add the interactive tools that we want our plot to have (these are the simple ones)
	tooltips = [('Year', '@year'), ('Temperature', '@temperature'), ('Country', '@country')]) # here we can assign which values to show on the hover tool

p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Temperature'

# STEP 5: fill it with circles
p.circle(x = 'year', y = 'temperature', source = source, # here we assign the data
         color={'field': 'country', 'transform': colormap}, # assign the colors: this is a dictionary with the keys field and transform, transform has to be a mapper object
         fill_alpha=0.2, size=10) # transparency and size of the circles


# STEP 6: add elements to the interactive graph 
# SLIDER ELEMENT
slider_month = Slider(start = 1, end = 12, 
                     step = 1, value = 1, title = 'Month to plot')
# CHECKBOX ELEMENT
checkbox_selection = CheckboxGroup(labels=list(data.Country.unique()), 
                                  active = [0, 1, 2, 3, 4, 5]) # default checkboxes to be active when opening the plot, right now: the 6 countries will be
                                  #active = [0, 3, 5]) # default checkboxes to be active when opening the plot, right now: the 6 countries will be

def update(attrname, old, new):
    # Get the current slider value
    print(slider_month.value) # this line should be commented, it's jut here to show the behaviour of the slider
    k = slider_month.value

    # Get the current checkbox slections
    print(checkbox_selection.active) # this line should be commented, it's jut here to show the behaviour of the checkbox
    checkbox_to_plot = [checkbox_selection.labels[i] for i in checkbox_selection.active]

    # Generate the new curve
    source.data = {
    	'year' : data[(data.month == k) & (data.Country.isin(checkbox_to_plot))].year,
    	'month' : data[(data.month == k) & (data.Country.isin(checkbox_to_plot))].month,
    	'temperature' : data[(data.month == k) & (data.Country.isin(checkbox_to_plot))].AverageTemperature,
    	'country' : data[(data.month == k) & (data.Country.isin(checkbox_to_plot))].Country
	}

slider_month.on_change('value', update)
checkbox_selection.on_change('active', update)

# STEP 7: design our layout
layout = column (p, row(checkbox_selection, slider_month)) # we create the layout in a column and row shape

output_file = ('scatter.html') # we output the html file

# STEP 8: run the server behind the visualisation!
curdoc().add_root(layout) 




