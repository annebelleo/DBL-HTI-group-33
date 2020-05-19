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


data_file = pd.read_csv("all_fixation_data_cleaned_up.csv",
                        encoding='latin1', sep='\t')


def get_data_user(user_name, name_map):
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

    im = Image.open('01b_Antwerpen_S2.jpg')
    x_dim = im.size[0]
    y_dim = im.size[1]
    
    X, Y, Z, = np.array([]), np.array([]), np.array([])
    for i in range(len(X_dat)):
        X = np.append(X, X_dat[i])
        Y = np.append(Y, Y_dat[i])
        Z = np.append(Z, (Z_dat[i]))
    
    # create x-y points to be used in heatmap
    xi = np.linspace(0, 1850)
    yi = np.linspace(0,1200)
    zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

    mapper = LogColorMapper(palette="Turbo256", low=0, high=max(Z_dat))

    #ax.rect(x="x_cor", y="y_cor", source=source, width=5,height=5,fill_color=transform("z_val", mapper))

    p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
    p.x_range.range_padding = p.y_range.range_padding = 0
    
    color_bar = ColorBar(color_mapper=mapper,ticker=LogTicker(),
                         formatter=PrintfTickFormatter(),location=(50,50),background_fill_alpha=0.5)
        
    p.add_layout(color_bar, 'right')

    p.image(image=[zi], x=0, y=0, dw=x_dim, dh=y_dim, palette="Turbo256", level="image")
    p.grid.grid_line_width = 0
    
    script, div = components(p)
    return [script, div]


draw_heatmap('p9', '01b_Antwerpen_S2.jpg')
