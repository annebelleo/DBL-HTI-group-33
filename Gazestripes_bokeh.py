import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bokeh.plotting import figure,show
from bokeh.embed import components
from bokeh.models.tickers import FixedTicker

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_data_map, get_array_fixations

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


def get_cropped_images(user_name, name_map):
    string_folder='static/stimuli/'
    image_source = string_folder+name_map
    im = plt.imread(image_source)
    img = Image.fromarray(im)
    width, height = img.size

    images=[]
    for i in get_array_fixations(user_name, name_map):
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, width, height)
        cropped_img = img.crop(area)
        images.append(cropped_img)
    return images, len(images)

def draw_gaze_stripes(user_name, name_map):
    TOOLS = "hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"

    if user_name == 'ALL':
        max_amount_images = 0
        ListUser = get_data_map(name_map).user.unique()
        ListUser = list(ListUser)

        for i in range(len(ListUser)):
            images, amount_images = get_cropped_images(ListUser[i], name_map)
            max_amount_images = max(max_amount_images, amount_images)
        
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
            images, amount_images = get_cropped_images(ListUser[j], name_map)
            for k in range(amount_images):
                im = images[k].convert("RGBA")
                imarray = np.array(im)
                fig.image_rgba(image=[imarray], x=k, y=j, dw=1, dh=0.9)
            
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
