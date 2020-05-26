# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet
from bokeh.plotting import ColumnDataSource, figure, show, curdoc
from bokeh.layouts import gridplot
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_array_fixations, random_color
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes

def draw_all_plots(user_name: str, name_map: str):
    gazeplot = draw_gazeplot(user_name, name_map, True)
    heatmap = draw_heatmap(user_name, name_map, True)
    transition = draw_transition_graph(user_name, name_map, True)
    gazestripes = draw_gaze_stripes(user_name, name_map, True)

    gazeplot.plot_width=20
    gazeplot.plot_height=20
    

    grid = gridplot([[gazeplot, heatmap],[transition, gazestripes]], plot_width=200, plot_height=200)
    show(grid)

draw_all_plots('p1', '01_Antwerpen_S1.jpg')
