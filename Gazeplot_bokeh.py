#import libraries
import pandas as pd
import random
from bokeh.models import LabelSet
from bokeh.plotting import ColumnDataSource, figure
from bokeh.embed import components
import PIL

data_file = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding = 'latin1', sep='\t')

ListUser = data_file.user.unique()

#get data of one test (user, picture, color):
def get_data_user(user_name, name_map):
    data_user = data_file.loc[data_file['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user


#get array of all fixations with fixation duration in order from one experiment:
def get_array_fixations(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = get_x_fixation(user_name, name_map)
    array_fixations_y = get_y_fixation(user_name, name_map)
    array_fixation_duration = get_duration_fixation(user_name, name_map)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l],array_fixations_y[l], array_fixation_duration[l]])
    return array_fixations


#get array of all x_coordinate fixations from one experiment:
def get_x_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = []
    for i in data_user['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x


#get array of all y_coordinate fixations from one experiment:
def get_y_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_y = []
    for i in data_user['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y


#get array of all fixation durations from one experiment:
def get_duration_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixation_duration = []
    for i in data_user['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration

def random_color():
    rgbl=[255, 0, 0]
    random.shuffle(rgbl)
    return tuple(rgbl)


# draw a figure showing the gazeplot of one experiment:
def draw_gazeplot(user_name, name_map):
    fixation_array = get_array_fixations(user_name, name_map)
    df = pd.DataFrame(fixation_array, columns=['x_cor','y_cor','fix_time'])
    df['fix_time_scaled']=df['fix_time']/12
    source = ColumnDataSource(df)
    
    TOOLS="tap,box_zoom,box_select,reset,save"
    TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "(@x_cor, @y_cor)"),
    ("fixation time", "@fix_time"),
]
    img_path = 'static/stimuli/' + name_map
    with PIL.Image.open(img_path) as image:
        IMG_width, IMG_height = image.size

    ax = figure(tools=TOOLS, plot_width=710, plot_height=450, x_axis_location=None, y_axis_location=None,
           title="Gazeplot user "+user_name[1:], tooltips=TOOLTIPS)

    ax.image_url([img_path], 0, IMG_height)

    if user_name == 'ALL':
        for i in ListUser:
            if i != 'ALL':
                # draw saccades
                ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)

                # draw each fixation
                fixation_array = get_array_fixations(i, name_map)
                df = pd.DataFrame(fixation_array, columns=['x_cor','y_cor','fix_time'])
                df['fix_time_scaled']=df['fix_time']/12
                source = ColumnDataSource(df)
                ax.circle('x_cor', 'y_cor', color=random_color(), size='fix_time_scaled', source=source, alpha=0.6)
                label = LabelSet(x='x_cor', y='y_cor', text='index', source=source, level="image", render_mode='canvas')
                ax.add_layout(label)
    else:
        # draw saccades
        ax.line('x_cor', 'y_cor', color='black', source=source, alpha=1)

        # draw each fixation
        ax.circle('x_cor', 'y_cor', color='navy', size='fix_time_scaled', source=source, alpha=0.6)
        label = LabelSet(x='x_cor', y='y_cor', text='index', source=source, level="image", render_mode='canvas')
        ax.add_layout(label)

    script, div = components(ax)
    return [script, div]

