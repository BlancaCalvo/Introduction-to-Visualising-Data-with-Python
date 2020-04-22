
import pandas as pd
import datetime as dt
from bokeh.models import LinearColorMapper, ColorBar, ColumnDataSource, BasicTicker
from bokeh.plotting import figure, show, output_file
import seaborn as sns

# STEP 1: import the data
w_temperature_data = pd.read_csv('data/GlobalTemperatures.csv', sep=',', index_col = False, parse_dates=['dt'])

w_temperature_data.rename(columns={'dt':'date'}, inplace=True) # we do this because we have a package called dt and it could make things confusing

# the dt package allows us to extract the month and the year from a full date
w_temperature_data['year'] = w_temperature_data.date.dt.year
w_temperature_data['month'] = w_temperature_data.date.dt.month

# creating a range for the figure, we will need this later!
years = list(w_temperature_data.year)
months = list(w_temperature_data.month)
years_range =(years[0], years[-1])
months_range = (months[0], months[-1])

# STEP 2: map the colors to our data
pal = sns.color_palette("coolwarm", 8) # we get a palette with 8 different colors, seborn palettes: https://seaborn.pydata.org/tutorial/color_palettes.html
colors = pal.as_hex() # we get the values of those colors
colormap = LinearColorMapper(palette=colors, low=w_temperature_data.LandAverageTemperature.min(), 
										high=w_temperature_data.LandAverageTemperature.max()) # note that we are working with linear data here

# STEP 3: create the data source for the interactive graph
source = ColumnDataSource(data={ 
	'x' : w_temperature_data.year,
	'y' : w_temperature_data.month,
	'value' : w_temperature_data.LandAverageTemperature
	})

# STEP 4: create the base figure
p = figure(title="World temperature",
			x_range=years_range, y_range=months_range, # stablished the limits of the plot axes
           plot_width=900, plot_height=400,
           tools="hover,save,pan,box_zoom,reset,wheel_zoom", # the hover tool adds the label to each data point when the mouse is on it
           tooltips=[('Year', '@x'), ('Temperature', '@value')]) # this tells what's going to be displayed by hover

# STEP 5: fill it with rectanbles
p.rect(x="x", y="y", width=1, height=1, # height and width of the rectangles
       source=source,
       fill_color={'field': 'value', 'transform': colormap},
       line_color=None)

# STEP 6: add elements to the interactive graph --> NEXT WEEK MATERIAL
# add a color bar that serves as legend
color_bar = ColorBar(color_mapper=colormap, 
                     ticker=BasicTicker(desired_num_ticks=len(colors)))

# add_layout is an important function in bokeh, as dropup menus, timelines and other interactive functions are done here --> NEXT WEEK MATERIAL
p.add_layout(color_bar, 'right')

# save the plot as html output
output_file("Lab3_heatmap.html", title="Heatmap example")

show(p)