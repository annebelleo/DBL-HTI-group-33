import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.interpolate import griddata
from bokeh.plotting import figure, show
from bokeh.models import PrintfTickFormatter
from bokeh.embed import components
from bokeh.models import ColorBar, LinearColorMapper

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_x_fixation, get_y_fixation, get_duration_fixation


FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


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
    yi = np.linspace(y_dim,0)
    zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')
    for x in range(len(zi)):
        for y in range(len(zi[0])):
            if np.isnan(zi[x][y]):
                zi[x][y] = 0

    mapper = LinearColorMapper(palette="Turbo256", low=0, high=max(Z_dat)+50)
    
    TOOLS="hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"
    TOOLTIPS = [
    ("(x,y)", "($x, $y)")
    ]
    
    p = figure(plot_width=int(x_dim/1.8), plot_height=int(y_dim/1.8),x_range=[0, x_dim],
               y_range=[0, y_dim], tools=TOOLS, tooltips=TOOLTIPS,
               title='Heatmap ' + user_name + " map " + name_map)
    
    color_bar = ColorBar(color_mapper=mapper, formatter=PrintfTickFormatter(),
                         location=(0,0),background_fill_alpha=0.5)
    
    p.add_layout(color_bar, 'right')
   
    p.image_url([image_source], 0, y_dim, x_dim, y_dim)
    p.image(image=[zi], x=0, y=0, dw=x_dim, dh=y_dim, color_mapper=mapper, global_alpha=0.7)
    p.grid.grid_line_width = 0


    script, div = components(p)
    return [script, div]
