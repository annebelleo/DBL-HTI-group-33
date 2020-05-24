#import libraries
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet
from bokeh.plotting import ColumnDataSource, figure
from bokeh.embed import components


from HelperFunctions import get_data_user, get_data_map, get_array_fixations, get_x_fixation, get_y_fixation, get_duration_fixation, random_color

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)

ListUser = df_data.user.unique()


# draw a figure showing the gazeplot of one experiment:
def draw_gazeplot(user_name, name_map):
    fixation_array = get_array_fixations(user_name, name_map)
    df = pd.DataFrame(fixation_array, columns=['x_cor','y_cor','fix_time'])
    df['fix_time_scaled']=df['fix_time']/12
    df['user']=user_name
    source = ColumnDataSource(df)
    
    string_folder='static/stimuli/'
    image_source = string_folder+name_map
    img = plt.imread(image_source)
    im = Image.fromarray(img)
    x_dim, y_dim = im.size
    
    TOOLS="hover,crosshair,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select"
    TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "(@x_cor, @y_cor)"),
    ("fixation time", "@fix_time"),
    ("user", "@user")
    ]

    ax = figure(tools=TOOLS, frame_width=int(x_dim/1.8), frame_height=int(y_dim/1.8),
                x_range=[0, x_dim], y_range=[y_dim,0],
                x_axis_location=None, y_axis_location=None,
                title="Gazeplot user "+user_name[1:], tooltips=TOOLTIPS)

    ax.image_url([image_source], 0, 0, x_dim, y_dim)

    if user_name == 'ALL':
        for i in ListUser:
            if i != 'ALL':
                # draw saccades
                ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)

                # draw each fixation
                fixation_array = get_array_fixations(i, name_map)
                df = pd.DataFrame(fixation_array, columns=['x_cor','y_cor','fix_time'])
                df['fix_time_scaled']=df['fix_time']/12
                df['user']= i
                source = ColumnDataSource(df)
                ax.circle('x_cor', 'y_cor', color=random_color(), size='fix_time_scaled', source=source, alpha=0.6)
                
    else:
        # draw saccades
        ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)

        # draw each fixation
        ax.circle('x_cor', 'y_cor', color='magenta', size='fix_time_scaled', source=source, alpha=0.6)
        label = LabelSet(x='x_cor', y='y_cor', text='index', source=source, text_color='black', render_mode='canvas')
        ax.add_layout(label)

    script, div = components(ax)
    return [script, div]
