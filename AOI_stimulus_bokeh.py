import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bokeh.models import Label
from bokeh.plotting import figure, show

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
DF_DATA = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)
TRANSLATE = {'KÃ¶ln': 'Köln', 'BrÃ¼ssel': 'Brüssel', 'DÃ¼sseldorf': 'Düsseldorf', 'GÃ¶teborg': 'Göteborg',
             'ZÃ¼rich': 'Zürich'}
DF_DATA.replace(TRANSLATE, regex=True, inplace=True)


from HelperFunctions import find_AOIs


def draw_AOI_stimulus(user_name, map_name, num_AOIs, data_set: pd.DataFrame, image_source, multiple: False):
    num_AOIs = int(num_AOIs)

    df_AOI = find_AOIs(map_name, num_AOIs, data_set)

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

        minX = data["MappedFixationPointX"].min()
        maxX = data["MappedFixationPointX"].max()
        minY = data["MappedFixationPointY"].min()
        maxY = data["MappedFixationPointY"].max()

        x = ((maxX-minX)/ 2)+minX
        y = ((maxY-minY)/ 2)+minY

        minX = x - 60
        maxX= x + 60
        minY = y - 60
        maxY = y + 60

        ax.line([minX, minX, maxX, maxX, minX],[minY, maxY, maxY, minY, minY], line_width = 4, line_color = 'black') 
        label = Label(x=x-15, y=y+23, text = str(i), text_color='black', text_font_size = '17pt')
        ax.add_layout(label)

    if not multiple:
        script, div = components(ax)
        return [script, div]
    else:
        return ax
