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
from Data_bokeh import draw_dataframe
from Gazeplot_bokeh import draw_gazeplot
from Heatmap_bokeh import draw_heatmap
from Transition_graph import draw_transition_graph
from Gazestripes_bokeh import draw_gaze_stripes
from AOI_rivers_bokeh import draw_AOI_rivers

def draw_all_plots(user_name: str, name_map: str, check_vis, num_AOIs):
    vis = []
    gc.collect()
    X_dat = get_x_fixation(user_name, name_map)
    
    string_folder = 'static/stimuli/'
    image_source = string_folder + name_map
    img = plt.imread(image_source)
    im = Image.fromarray(img)
    x_dim, y_dim = im.size
    
    if X_dat == []:
            return ["No user data found",""]
    else:
        if "Data Table" in check_vis:
            datatable = draw_dataframe(user_name, name_map)
            script, div = components(datatable)
            return [script, div]
        if "Gaze Plot" in check_vis:
            gazeplot = draw_gazeplot(user_name, name_map, True)
            vis.append(gazeplot)
        if "Heatmap" in check_vis:
            heatmap = draw_heatmap(user_name, name_map, True)
            vis.append(heatmap)
        if "Transition Graph" in check_vis: 
            transition = draw_transition_graph(user_name, name_map, True)
            vis.append(transition)
        if "Gaze Stripes" in check_vis:    
            gazestripes = draw_gaze_stripes(user_name, name_map, True)
            vis.append(gazestripes)
        if "AOI Rivers" in check_vis:
                if user_name != "ALL":
                    return ["AOI rivers only displays data for all users",""]
                else: 
                    aoiriv = draw_AOI_rivers(user_name, name_map, num_AOIs, True)
                    vis.append(aoiriv)
                    
        grid = gridplot(vis, ncols=1, plot_width=int(x_dim / 2.5), plot_height=int(y_dim / 2.5))
        print('works')

        script, div = components(grid)
        return [script, div]
