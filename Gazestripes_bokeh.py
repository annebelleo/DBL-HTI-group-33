import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Range1d


# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_data_map, get_array_fixations, get_cropped_images_gazestripe


def draw_gaze_stripes(user_name: str, name_map: str, data_set: pd.DataFrame, image_source: str, multiple=False):
    TOOLS = "hover, wheel_zoom, zoom_in, zoom_out, box_zoom, reset, save, box_select, pan"

    if user_name == 'ALL':
        ListUser = get_data_map(name_map, data_set).user.unique()
        ListUser = list(ListUser)

        amount_fixations = []
        for i in ListUser:
            fixations = get_array_fixations(i, name_map, data_set)
            amount_fixations.append(len(fixations))

        max_amount_images = max(amount_fixations)

        fig = figure(plot_width=25 * max_amount_images, plot_height=25 * len(ListUser),
                     x_range=Range1d(0, max_amount_images, bounds="auto"), y_range=Range1d(0, len(ListUser), bounds="auto"),
                     x_axis_label="Time (order of fixations)", y_axis_label="User",
                     title='Gaze stripes all users map ' + name_map, tools=TOOLS,
                     sizing_mode='scale_both')
        fig.xgrid.visible = False
        fig.ygrid.visible = False

        ticks = [g / 2 for g in range(len(ListUser) * 2)]
        ticks_labels = {h + 0.5: ListUser[h] for h in range(len(ListUser))}
        fig.yaxis.ticker = ticks
        fig.yaxis.major_label_overrides = ticks_labels
        fig.yaxis.major_label_orientation = 3.14 / 4

        for j in range(len(ListUser)):
            gazestripe = get_cropped_images_gazestripe(ListUser[j], name_map, data_set, image_source)
            im = gazestripe.convert("RGBA")
            imarray = np.array(im)
            np.flip(imarray)
            fig.image_rgba(image=[imarray], x=0, y=j, dw=amount_fixations[j], dh=0.9)

    else:
        images = get_cropped_images_gazestripe(user_name, name_map, data_set, image_source)
        fixations = get_array_fixations(user_name, name_map, data_set)
        amount_images = len(fixations)

        if amount_images == 0:
            return ["No user data found", ""]

        fig = figure(plot_width=25 * amount_images, plot_height=25,
                    x_range=Range1d(0, amount_images, bounds="auto"), y_range=Range1d(0, amount_images, bounds="auto"),
                    x_axis_label="Time (order of fixations)", y_axis_label="User",
                    tools=TOOLS)

        im = images.convert("RGBA")
        imarray = np.array(im)
        fig.image_rgba(image=[imarray], x=0, y=0, dw=amount_images, dh=1)

    fig.title.text = 'Gaze Stripes'
    
    if not multiple:
        script, div = components(fig)
        return [script, div]
    else:
        return fig
