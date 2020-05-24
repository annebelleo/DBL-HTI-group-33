import pandas as pd
import random

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


def get_data_user(user_name, name_map):
    if user_name == 'ALL':
        data_user = df_data.loc[df_data['StimuliName'] == name_map]
    else:
        data_user = df_data.loc[df_data['user'] == user_name]
        data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user

def get_data_map(name_map):
    data_map = df_data.loc[df_data['StimuliName'] == name_map]
    return data_map


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
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)