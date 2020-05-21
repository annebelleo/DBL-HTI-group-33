import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.interpolate import griddata
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from bokeh.plotting import figure, output_file, show
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter, )
from bokeh.transform import transform
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import HoverTool
from PIL import Image
from bokeh.models import ColorBar, LogColorMapper, LogTicker, LinearColorMapper


data_file = pd.read_csv('static/all_fixation_data_cleaned_up.csv',
                        encoding='latin1', sep='\t')


def get_data_user(user_name, name_map):
    if user_name == 'ALL':
        data_user = data_file.loc[data_file['StimuliName'] == name_map]
    else:
        data_user = data_file.loc[data_file['user'] == user_name]
        data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user


def get_array_fixations(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = get_x_fixation(user_name, name_map)
    array_fixations_y = get_y_fixation(user_name, name_map)
    array_fixation_duration = get_duration_fixation(user_name, name_map)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l], array_fixations_y[l], array_fixation_duration[l]])
    return array_fixations


def get_x_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = []
    for i in data_user['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x


def get_y_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_y = []
    for i in data_user['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y


def get_duration_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixation_duration = []
    for i in data_user['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration


def draw_heatmap(user_name, name_map):
    X_dat=get_x_fixation(user_name, name_map)
    Y_dat=get_y_fixation(user_name, name_map)
    Z_dat=get_duration_fixation(user_name,name_map)

    string_folder='static/stimuli/'
    image_source = string_folder+name_map
    img = plt.imread(image_source)
    im = Image.fromarray(img)
    x_dim = im.size[0]
    y_dim = im.size[1]
    
    X, Y, Z, = np.array([]), np.array([]), np.array([])
    for i in range(len(X_dat)):
        X = np.append(X, X_dat[i])
        Y = np.append(Y, Y_dat[i])
        Z = np.append(Z, (Z_dat[i]))
    
    # create x-y points to be used in heatmap
    xi = np.linspace(0,x_dim)
    yi = np.linspace(0,y_dim)
    zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

    mapper = LogColorMapper(palette="Turbo11", low=0, high=max(Z_dat))
    
    TOOLS="hover,crosshair,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select"
    p = figure(plot_width=825, plot_height=600,x_range=[0, x_dim], y_range=[0, y_dim], tools=TOOLS, title='Heatmap Test')
    color_bar = ColorBar(color_mapper=mapper,ticker=LogTicker(),
                         formatter=PrintfTickFormatter(),location=(50,50),background_fill_alpha=0.5)
    
    p.add_layout(color_bar, 'right')
   
    p.image(image=[zi], x=0, y=0, dw=x_dim, dh=y_dim, palette="Turbo11",global_alpha=0.9)
    p.image_url([image_source], 0, y_dim, x_dim, y_dim, global_alpha = 0.4)
    p.grid.grid_line_width = 0
    script, div = components(p)
    return [script, div]
