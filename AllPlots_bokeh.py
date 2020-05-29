# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import gc
from PIL import Image
from bokeh.models import LabelSet
from bokeh.plotting import ColumnDataSource, figure, show
from bokeh.layouts import gridplot
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_array_fixations, get_x_fixation, random_color
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes

def draw_all_plots(user_name: str, name_map: str):
    gc.collect()
    X_dat = get_x_fixation(user_name, name_map)
    if X_dat == []:
            return ["No user data found",""]
    else:
        gazeplot = draw_gazeplot(user_name, name_map, True)
        heatmap = draw_heatmap(user_name, name_map, True)
        transition = draw_transition_graph(user_name, name_map, True)
        gazestripes = draw_gaze_stripes(user_name, name_map, True)

        grid = gridplot([gazeplot,heatmap,transition,gazestripes], ncols=1)
        print('works')

        script, div = components(grid)
        return [script, div]
