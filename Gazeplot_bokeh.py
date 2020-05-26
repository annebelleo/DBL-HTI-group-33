# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet
from bokeh.plotting import ColumnDataSource, figure
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_array_fixations, random_color

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
        ("(x,y)", "(@x_cor, @y_cor)"),
        ("fixation time", "@fix_time"),
        ("user", "@user")
    ]

    #create a figure, in which the gazeplot is plotted
    ax = figure(tools=TOOLS, frame_width=int(x_dim / 1.8), frame_height=int(y_dim / 1.8),
                x_range=[0, x_dim], y_range=[y_dim, 0],
                x_axis_location=None, y_axis_location=None,
                title="Gazeplot user " + user_name, tooltips=TOOLTIPS)

    #add the image to the figure
    ax.image_url([image_source], 0, 0, x_dim, y_dim)

    #define if all users are selected or only one
    if user_name == 'ALL':
        for i in ListUser:
            if i != 'ALL':
                #create a source for one particular user
                fixation_array = get_array_fixations(i, name_map)
                df = pd.DataFrame(fixation_array, columns=['x_cor', 'y_cor', 'fix_time'])
                df['fix_time_scaled'] = df['fix_time'] / 12
                df['user'] = i
                source = ColumnDataSource(df)

                #plot the saccades and fixations based on the source file of that user
                ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)
                ax.circle('x_cor', 'y_cor', color=random_color(), size='fix_time_scaled', source=source, alpha=0.6)

    else:
            
        #make a source file based on the data from the user
        fixation_array = get_array_fixations(user_name, name_map)
        df = pd.DataFrame(fixation_array, columns=['x_cor', 'y_cor', 'fix_time'])
        df['fix_time_scaled'] = df['fix_time'] / 12
        df['user'] = user_name
        source = ColumnDataSource(df)
        
        # draw the saccades
        ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)

        # draw each fixation
        ax.circle('x_cor', 'y_cor', color='magenta', size='fix_time_scaled', source=source, alpha=0.6)
        label = LabelSet(x='x_cor', y='y_cor', text='index', source=source, text_color='black', render_mode='canvas')
        ax.add_layout(label)

    if not multiple:
        script, div = components(ax)
        return [script, div]
    else:
        return ax
