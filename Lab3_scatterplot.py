
import pandas as pd
import datetime as dt
from bokeh.plotting import figure, show, output_file
from bokeh.models import CategoricalColorMapper, ColumnDataSource
import seaborn as sns

# STEP 1: import the data
w_temperature_data = pd.read_csv('data/GlobalLandTemperatures/GlobalLandTemperaturesByCountry.csv', sep=',', index_col = False, parse_dates=['dt'])
w_temperature_data.rename(columns={'dt':'date'}, inplace=True) # we do this because we have a package called dt and it could make things confusing

# the dt package allows us to extract the month and the year from a full date
w_temperature_data['year'] = w_temperature_data.date.dt.year
w_temperature_data['month'] = w_temperature_data.date.dt.month

# filter the data to make it a bit less complicated
countries = ["Albania", "Austria", "Netherlands (Europe)"]
w_temperature_data = w_temperature_data[w_temperature_data.Country.isin(countries)]
w_temperature_data = w_temperature_data[w_temperature_data.month == 1]

# STEP 2: map the colors to our data
pal = sns.color_palette("hls", 3) # 3 is the number of colors to extract from the palette
colors = pal.as_hex() # get the values of those colors. We could also have written the name/numbers of some colors
#print(colors) # you can observe that this is just a string of color values
colormap = CategoricalColorMapper(palette=colors, 
				factors=w_temperature_data['Country'].unique()) # note that we are working with categorical data here, so we need one color per category
				#factors=list(set(w_temperature_data['Country']))) # set() is similar to unique(), but makes the data of type 'set'

# STEP 3: create the data source for the interactive graph
source = ColumnDataSource(data=dict( 
	x = w_temperature_data.year,
	y = w_temperature_data.AverageTemperature,
	country = w_temperature_data.Country,
	))

# STEP 4: create the base figure
p = figure(title = "Country Land Temperture",
	plot_width=900, plot_height=400,
	tools="hover, save, pan, box_zoom, reset, wheel_zoom", # here we add the interactive tools that we want our plot to have (these are the simple ones)
	tooltips = [('Year', '@x'), ('Temperature', '@y'), ('Country', '@country')]) # here we can assign which values to show on the hover tool

p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Temperature'

# STEP 5: fill it with circles
p.circle(x = 'x', y = 'y', source = source, # here we assign the data
         color={'field': 'country', 'transform': colormap}, # assign the colors: this is a dictionary with the keys field and transform, transform has to be a mapper object
         fill_alpha=0.2, size=10) # transparency and size of the circles

# we save it as html
output_file("Lab3_scatterplot.html", title="Scatterplot example")

# and display
show(p)