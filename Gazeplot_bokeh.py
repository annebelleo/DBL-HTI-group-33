# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet, CDSView, GroupFilter
from bokeh.plotting import ColumnDataSource, figure, show
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_array_fixations, random_color, get_source, get_data_user


def draw_gazeplot(user_name, name_map: str, data_set: pd.DataFrame, image_source: str, multiple=False):
    """
    Draw a gazeplot using the given data and parameters
    :param image_source:
    :param multiple:
    :param data_set:
    :param user_name:
    :param name_map:
    :return:
    """
    # import source for plot
    source = get_source(user_name, name_map, data_set)

    # import the image of the map, which will be displayed later
    img = plt.imread(image_source)
    im = Image.fromarray((img * 255).astype(np.uint8))
    x_dim, y_dim = im.size

    # define tools and tooltips to add interactions to the plot
    TOOLS = "hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "(@MappedFixationPointX, @MappedFixationPointY)"),
        ("fixation time", "@FixationDuration"),
        ("user", "@user")
    ]

    # create a figure, in which the gazeplot is plotted
    ax = figure(tools=TOOLS, plot_width=int(x_dim / 1.5), plot_height=int(y_dim / 1.5),
                x_range=[0, x_dim], y_range=[y_dim, 0],
                x_axis_location=None, y_axis_location=None,
                tooltips=TOOLTIPS, sizing_mode='scale_both')

    # add the image to the figure
    ax.image_url([image_source], 0, 0, x_dim, y_dim)

    view1 = CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map)])
    ax.line('MappedFixationPointX', 'MappedFixationPointY',color='black', source=source, view=view1, alpha=1)

    # define if all users are selected or only one
    if user_name == 'ALL':
        for i in data_set.user.unique():
            if i != 'ALL':
                view2 = CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map),
                                                        GroupFilter(column_name='user', group=str(i))])

                # plot the saccades and fixations based on the source file of that user
                ax.circle('MappedFixationPointX', 'MappedFixationPointY', color=random_color(), size='fix_time_scaled',
                          source=source, view=view2, alpha=0.6)

    else:
        for i in user_name:
            view3 = CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map),
                                                GroupFilter(column_name='user', group=i)])

            # draw each fixation
            ax.circle('MappedFixationPointX', 'MappedFixationPointY', color=random_color(), size='fix_time_scaled',
                       source=source, view=view3, alpha=0.6)

            if len(user_name) < 2:
                new_source = get_data_user(user_name, name_map, data_set)
                indexing = []
                for i in range(len(new_source)):
                    indexing.append(str(i))
                new_source['index_num'] = indexing
                new_source = ColumnDataSource(new_source)
                label = LabelSet(x='MappedFixationPointX', y='MappedFixationPointY',
                                 text='index_num', source=new_source, text_color='black', render_mode='canvas')
                ax.add_layout(label)

    if not multiple:
        script, div = components(ax)
        return [script, div]
    else:
        return ax
