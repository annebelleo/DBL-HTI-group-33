import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

df = pd.read_csv("all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace=True)
df

def get_data_user(user_name, name_map):
    data_user = df.loc[df['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user

def get_array_fixations(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = get_x_fixation(user_name, name_map)
    array_fixations_y = get_y_fixation(user_name, name_map)
    array_fixation_duration = get_duration_fixation(user_name, name_map)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l],array_fixations_y[l], array_fixation_duration[l]])
    return array_fixations

def get_x_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = []
    for i in data_user['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x

def get_y_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_y = []
    for i in data_user['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y

def get_duration_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixation_duration = []
    for i in data_user['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration

def get_cropped_images(user_name, name_map):
    my_file = os.path.join('stimuli', name_map)
    img = plt.imread(my_file)
    img = Image.fromarray(img)
    width, height = img.size
#     print(width, height)

    images=[]
    for i in get_array_fixations(user_name, name_map):
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        images.append(cropped_img)
    return(images)

def draw_gaze_stripes(user_name, name_map):

    fig = plt.figure()
    fig.set_figwidth(80)
    plt.xlim(0, sum(get_duration_fixation(user_name, name_map)))
    plt.yticks([])
    plt.ylabel(user_name)
    plt.subplots_adjust(hspace=0,wspace=0)
    n=1
    for i in get_cropped_images(user_name, name_map):
        fig.add_subplot(1, len(get_cropped_images(user_name, name_map)), n)
        plt.yticks([])
        plt.xticks([])
        plt.imshow(i)
        n+=1
    fig.subplots_adjust(bottom=0.5)
    plt.show()
    fig.savefig('gaze stripe' + name_map)

# get_cropped_images('p3', '17_Krakau_S2.jpg')

# draw_gaze_stripes('p3', '17_Krakau_S2.jpg')
