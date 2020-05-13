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

data_file = pd.read_csv("D:/User/Documenten/GitHub/DBL-HTI-group-33/all_fixation_data_cleaned_up.csv",
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
    # string_folder='C:\\Users\\20182504\\Documents\\Uni\\Year 2\\Q4\\2IOA0 DBL HTI + Webtech\\Data Visualization\\MetroMapsEyeTracking\\stimuli\\'
    # image_source = string_folder+name_map
    # img = plt.imread(image_source)
    # fig, ax = plt.subplots()
    # Comment out next line to see the plot if it's not visible
    # ax.imshow(img)

    X_dat = get_x_fixation(user_name, name_map)
    Y_dat = get_y_fixation(user_name, name_map)
    Z_dat = get_duration_fixation(user_name, name_map)

    X, Y, Z, = np.array([]), np.array([]), np.array([])
    for i in range(len(X_dat)):
        X = np.append(X, X_dat[i])
        Y = np.append(Y, Y_dat[i])
        Z = np.append(Z, (Z_dat[i]))

    # create x-y points to be used in heatmap
    xi = np.linspace(0, 1850)
    yi = np.linspace(0, 1200)

    ax = figure()
    ax.image_url([name_map], 50, 50, 0, 0)

    # Z is a matrix of x-y values
    zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='cubic')
    Z_zero = zi.tolist()
    z_list = []
    for i in range(len(Z_zero)):
        for j in range(len(Z_zero[i])):
            if np.isnan(Z_zero[i][j]):
                z_list.append(0)
            else:
                z_list.append(Z_zero[i][j])

    y_list = list(range(50)) * 50
    x_list = []
    for i in range(50):
        for j in range(50):
            x_list.append(i)
    data = {'x_cor': x_list, 'y_cor': y_list, 'z_val': z_list}
    df = pd.DataFrame(data)
    source = ColumnDataSource(df)

    colors = ["#0055ff", "#00bbff", "#00ffd9", "#00ff77", "#00ff22", "#a2ff00", "#eeff00", "#ffdd00", "#ff9900",
              "#ff5500", "#ff0000"]

    mapper = LinearColorMapper(palette=colors, low=0, high=max(Z_dat))

    ax.rect(x="x_cor", y="y_cor", source=source, width=5, height=5, fill_color=transform("z_val", mapper))
    color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(), location=(50, 50), background_fill_alpha=0.5)
    ax.add_layout(color_bar, 'right')

    script, div = components(ax)
    return [script, div]


draw_heatmap('p9', '01b_Antwerpen_S2.jpg')
