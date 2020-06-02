import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.palettes import d3
from bokeh.plotting import figure, output_file, show

from HelperFunctions import find_AOIs, findClusters, normalize_time, aggregate_time, get_data_map

def draw_AOI_rivers(user_name, map_name, num_AOIs, multiple = False):
    
    if user_name != "ALL":
        return ["AOI rivers only displays data for all users",""]
    
    df_agg = aggregate_time(map_name, num_AOIs)
    df_plot = df_agg.set_index('Time')
    highest_stack = df_plot[1:].sum(axis = 1).max()
    p = figure(x_range=(int(df_plot.head(1).index.to_list()[0]), int(df_plot.tail(1).index.to_list()[0])), y_range=(0, highest_stack))
    p.grid.minor_grid_line_color = '#eeeeee'

    names = df_plot.columns.to_list()
    p.varea_stack(stackers=names, x='Time',color=d3['Category20'][num_AOIs], legend_label=names, source=df_plot)

    # reverse the legend entries to match the stacked order
    p.legend.items.reverse()

    if not multiple:
        script, div = components(p)
        return [script, div]
    else:
        return p