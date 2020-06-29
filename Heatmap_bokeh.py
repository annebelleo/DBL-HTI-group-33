import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from bokeh.plotting import figure, show
from bokeh.models import ColorBar, LinearAxis, LinearColorMapper, PrintfTickFormatter, Label
from bokeh.embed import components
from bokeh.layouts import gridplot
# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_x_fixation, get_source, get_y_fixation, get_duration_fixation, get_data_map

np.set_printoptions(threshold=sys.maxsize)

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


def draw_heatmap(user_name: str, name_map: str, data_set: pd.DataFrame, image_source: str, multiple=False):
    """
    This function creates a heatmap, based on the input data, from either one or all users and from one map.
    :param multiple:
    :param data_set:
    :param image_source:
    :param user_name:
    :param name_map:
    :return:
    """

    # separately get the data from the fixation coordinates and duration
    X_dat = get_x_fixation(user_name, name_map, data_set)
    Y_dat = get_y_fixation(user_name, name_map, data_set)
    Z_dat = get_duration_fixation(user_name, name_map, data_set)

    # if there is no data from the user of that map, return a message informing the user
    if not X_dat:
        return ["No user data found", ""]

    # import the image the user has chosen
    img = plt.imread(image_source)
    im = Image.fromarray((img * 255).astype(np.uint8))
    x_dim = im.size[0]
    y_dim = im.size[1]

    if user_name == 'ALL':
        xi = np.linspace(0, x_dim,300)
        yi = np.linspace(y_dim, 0,300)

    else:
        xi = np.linspace(0, x_dim,200)
        yi = np.linspace(y_dim, 0,200)
    
    grid = np.array([[0]*len(xi)]*len(yi))

    for x in range(len(X_dat)):
        Y = int(Y_dat[x]//(y_dim/len(yi)))
        X = int(X_dat[x]//(x_dim/len(xi)))
        if not (X >= len(xi) or Y >= len(yi)):
            grid[Y][X] = Z_dat[x]

    zi_old=grid

    # apply a gaussian filter from the scipy library, the sigma is based on if all users are selected or just one
    if user_name == 'ALL':
        zi = gaussian_filter(zi_old, sigma=6)
    else:
        zi = gaussian_filter(zi_old, sigma=3)

    max_zi = 0
    for i in range(len(zi)):
        for j in range(len(zi[0])):
            max_zi = max(max_zi, zi[i][j])

    zi = np.flip(zi,0)

    # define a mapper that can assign colors from a certain palette to a range of integers
    mapper = LinearColorMapper(palette="Turbo256", low=0, high=max_zi)

    # Tools and tooltips that define the extra interactions
    TOOLS = "hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"

    # create a figure in which the heatmap can be displayed
    p = figure(plot_width=int(x_dim / 1.8), plot_height=int(y_dim / 1.8), x_range=[0, x_dim],
               y_range=[0, y_dim], tools=TOOLS,
               sizing_mode='scale_both')
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.grid_line_width = 0

    # add a color bar which shows the user which color is mapped to which fixation duration
    color_bar = ColorBar(color_mapper=mapper, formatter=PrintfTickFormatter(),
                         major_tick_line_color = None, major_label_text_color = None,
                         location=(0, 0), background_fill_alpha=0.5)

    p.add_layout(color_bar, 'right')
    
    color_bar_label= Label(text="Relative Fixation Duration (<- high - low ->)", x=-10, y= int(y_dim / 1.8)/2,
                           angle=270, render_mode='canvas', text_align = 'center',
                           angle_units='deg', x_units='screen', y_units='screen', text_font_size='14pt')

    p_dummy = figure(plot_height=int(y_dim / 1.8), width=50, toolbar_location=None, min_border=0, outline_line_color=None)
    p_dummy.add_layout(color_bar_label, 'right')
    
    # map the original map and the data grid using the color mapper, turning it into a heatmap
    p.image_url([image_source], 0, y_dim, x_dim, y_dim)
    p.image(image=[zi], x=0, y=0, dw=x_dim, dh=y_dim, color_mapper=mapper, global_alpha=0.7)

    grid_plot = gridplot([p, p_dummy], ncols=2, toolbar_location=None)
    
    p.title.text = 'Heatmap'
    
    if not multiple:
        script, div = components(grid_plot)
        return [script, div]
    else:
        return grid_plot
