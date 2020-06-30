import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bokeh.models import Label
from bokeh.plotting import figure

from HelperFunctions import find_AOIs, get_data_user


def draw_AOI_stimulus(user_name, map_name, num_AOIs, data_set: pd.DataFrame, image_source, multiple: False):
    num_AOIs = int(num_AOIs)
    
    df_AOI = find_AOIs(map_name, num_AOIs, get_data_user(user_name, map_name, data_set))

    # filter out all data that belongs to the chosen user(s)
    data = df_AOI[df_AOI['StimuliName'] == map_name]
    if user_name != "ALL":
        data = data[data['user'] == user_name]

    if data.size == 0:
        return ["No user data found", ""]

    # import the image of the map, which will be displayed later
    img = plt.imread(image_source)
    im = Image.fromarray((img * 255).astype(np.uint8))
    x_dim, y_dim = im.size

    # create a figure, in which the gazeplot is plotted
    ax = figure(plot_width=int(x_dim / 1.5), plot_height=int(y_dim / 1.5),
                x_range=[0, x_dim], y_range=[y_dim, 0],
                x_axis_location=None, y_axis_location=None,
                sizing_mode='scale_both')

    # add the image to the figure
    ax.image_url([image_source], 0, 0, x_dim, y_dim)

    AOIs = df_AOI.AOI.unique()
    for i in AOIs:
        data = df_AOI[df_AOI['AOI'] == i]

        sum_x = 0
        sum_y = 0
        count = 0
        for j in data['MappedFixationPointX']:
            count += 1
            sum_x += j

        for k in data['MappedFixationPointY']:
            sum_y += k

        x = sum_x/count
        y = sum_y/count

        img_size = 100
        
        minX = x - img_size 
        minY = y - img_size
        maxX = x + img_size
        maxY = y + img_size

        ax.line([minX, minX, maxX, maxX, minX],[minY, maxY, maxY, minY, minY], line_width = 4, line_color = 'black') 
        label = Label(x=x-15, y=y+23, text = str(i), text_color='black', text_font_size = '17pt')
        ax.add_layout(label)

    
    ax.title.text = 'AOI Locations'
    
    if not multiple:
        script, div = components(ax)
        return [script, div]
    else:
        return ax
