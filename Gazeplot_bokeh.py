#import libraries
import pandas as pd
from bokeh.models import Label
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

data_file = pd.read_csv("D:/User/Documenten/GitHub/DBL-HTI-group-33/all_fixation_data_cleaned_up.csv", encoding = 'latin1', sep='\t')

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


# draw a figure showing the gazeplot of one experiment:
def draw_gazeplot(user_name, name_map):
    ax=figure()
    ax.image_url([name_map], 0, 1200, 1894, 1200)

    # draw saccades
    x = get_x_fixation(user_name, name_map)
    y = get_y_fixation(user_name, name_map)
    ax.line(x, y, color='black', alpha=1)
    count = 1

    # draw each fixation
    fixation_array = get_array_fixations(user_name, name_map)
    for i in fixation_array:
        ax.circle(i[0], i[1], color='navy', size=i[2]/10, alpha=0.6)
        label = Label(x=i[0], y=i[1], text=str(count), level="image", render_mode='canvas')
        count = count + 1
        ax.add_layout(label)

    script, div = components(ax)
    return [script, div]


draw_gazeplot('p1', '04_Köln_S1.jpg')
