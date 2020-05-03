#import libraries

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

data_file = pd.read_csv('Test data/data.csv', encoding='latin1', delim_whitespace=True)

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
    string_folder = 'Test data/stimuli/'
    image_source = string_folder + name_map
    img = plt.imread(image_source)
    fig, ax = plt.subplots()
    ax.imshow(img)

    # draw saccades
    x = get_x_fixation(user_name, name_map)
    y = get_y_fixation(user_name, name_map)
    ax.plot(x, y, linewidth=1, color='black', alpha=1, zorder=1)
    count = 1

    # draw each fixation
    fixation_array = get_array_fixations(user_name, name_map)
    for i in fixation_array:
        ax.scatter(i[0], i[1], marker='o', color='cyan', s=i[2], edgecolors='black', alpha=0.6, zorder=2)
        # can't get the numbers to look pretty :(
        ax.annotate(str(count), (i[0], i[1]), size=6, color='black', alpha=1, horizontalalignment='center',
                    verticalalignment='center', multialignment='center')
        count = count + 1

    # y axis must be reversed to match with original images
    plt.show()


draw_gazeplot('p1', '04_Köln_S1.jpg')