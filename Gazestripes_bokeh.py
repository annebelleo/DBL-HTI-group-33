import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.models.tickers import FixedTicker

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_data_map, get_array_fixations, get_cropped_images, get_cropped_images_gazestripe

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)

def draw_gaze_stripes(user_name, name_map):
    TOOLS = "hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"

    if user_name == 'ALL':
        ListUser = get_data_map(name_map).user.unique()
        ListUser = list(ListUser)

        amount_fixations = []
        for i in ListUser:
            fixations = get_array_fixations(i, name_map)
            amount_fixations.append(len(fixations))

        max_amount_images = max(amount_fixations)
        
        
        fig = figure(plot_width = 25*max_amount_images, plot_height = 25*len(ListUser),
                     x_range=(0,max_amount_images), y_range=(0,len(ListUser)),
                     x_axis_label = "Time (order of fixations)", y_axis_label = "User",
                     title = 'Gaze stripes all users map '+ name_map, tools=TOOLS)
        fig.xgrid.visible = False
        fig.ygrid.visible = False
        
        ticks = [g/2 for g in range(len(ListUser)*2)]
        ticks_labels = {h+0.5:ListUser[h] for h in range(len(ListUser))}
        fig.yaxis.ticker = ticks
        fig.yaxis.major_label_overrides = ticks_labels
        fig.yaxis.major_label_orientation = 3.14/4
        
        for j in range(len(ListUser)):
            gazestripe = get_cropped_images_gazestripe(ListUser[j], name_map)
            im = gazestripe.convert("RGBA")
            imarray = np.array(im)
            np.flip(imarray)
            fig.image_rgba(image=[imarray], x=0, y=j, dw=amount_fixations[j], dh=0.9)
            
    else:
        images, amount_images = get_cropped_images(user_name, name_map)
        fig = figure(plot_width=75*amount_images, plot_height=75, x_range=(0,amount_images),
                     y_range=(0,1), x_axis_label = "Time (order of fixations)",
                     y_axis_label = "User", title = 'Gaze stripes user '+ user_name + ' map ' + name_map,
                     tools=TOOLS)
        for i in range(amount_images):
            im = images[i].convert("RGBA")
            imarray = np.array(im)
            fig.image_rgba(image=[imarray], x=i, y=0, dw=1, dh=1)
            
    script, div = components(fig)
    return [script, div]