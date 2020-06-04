# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet, CDSView, GroupFilter
from bokeh.plotting import ColumnDataSource, figure, show
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_array_fixations, random_color, get_source, get_data_user

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)

ListUser = df_data.user.unique()

def draw_gazeplot(user_name: str, name_map: str, multiple = False):
    """
    Draw a gazeplot using the given data and parameters
    :param user_name:
    :param name_map:
    :return:
    """
    #import source for plot
    source = get_source(user_name, name_map)

    #import the image of the map, which will be displayed later
    string_folder = 'static/stimuli/'
    image_source = string_folder + name_map
    img = plt.imread(image_source)
    im = Image.fromarray(img)
    x_dim, y_dim = im.size

    #define tools and tooltips to add interactions to the plot
    TOOLS = "hover,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,save,box_select"
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "(@MappedFixationPointX, @MappedFixationPointY)"),
        ("fixation time", "@FixationDuration"),
        ("user", "@user")
    ]

    #create a figure, in which the gazeplot is plotted
    ax = figure(tools=TOOLS, plot_width=int(x_dim / 1.5), plot_height=int(y_dim / 1.5),
                x_range=[0, x_dim], y_range=[y_dim, 0],
                x_axis_location=None, y_axis_location=None,
                tooltips=TOOLTIPS, sizing_mode='scale_both')

    #add the image to the figure
    ax.image_url([image_source], 0, 0, x_dim, y_dim)

    #define if there is data for the user and map
    output_info = df_data.loc[(df_data['user'] == user_name) & (df_data['StimuliName'] == name_map), 'MappedFixationPointX']
    if output_info.empty:
        return ("There is no data available for this user and map.")

    #define if all users are selected or only one
    if user_name == 'ALL':
        view1=CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map)])
        ax.line('MappedFixationPointX', 'MappedFixationPointY', color='black', source=source, view=view1, alpha=1)
        for i in ListUser:
            if i != 'ALL':
                view2=CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map),GroupFilter(column_name='user', group=str(i))])

                #plot the saccades and fixations based on the source file of that user
                ax.circle('MappedFixationPointX', 'MappedFixationPointY', color=random_color(), size='fix_time_scaled', source=source, view=view2, alpha=0.6)

    else:
        view3 = CDSView(source=source, filters=[GroupFilter(column_name='StimuliName', group=name_map),GroupFilter(column_name='user', group=user_name)])

        # draw the saccades
        ax.line('MappedFixationPointX', 'MappedFixationPointY', color='black', source=source, view=view3, alpha=1)

        # draw each fixation
        ax.circle('MappedFixationPointX', 'MappedFixationPointY', color='magenta', size='fix_time_scaled', source=source, view=view3, alpha=0.6)

        new_source=get_data_user(user_name, name_map)
        new_source = ColumnDataSource(new_source)
        label = LabelSet(x='MappedFixationPointX', y='MappedFixationPointY', text='index', source=new_source, text_color='black', render_mode='canvas')
        ax.add_layout(label)

    if not multiple:
        script, div = components(ax)
        return [script, div]
    else:
        return ax
