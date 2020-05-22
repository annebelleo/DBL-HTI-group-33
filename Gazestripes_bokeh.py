import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.embed import components
#from bokeh.io import hplot

df = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding = 'latin1', sep='\t')

def get_data_user(user_name, name_map):
    data_user = df.loc[df['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user

def get_data_map(name_map):
    data_map = df.loc[df['StimuliName'] == name_map]
    return data_map

def get_array_fixations(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = get_x_fixation(user_name, name_map)
    array_fixations_y = get_y_fixation(user_name, name_map)
    array_fixation_duration = get_duration_fixation(user_name, name_map)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l],array_fixations_y[l], array_fixation_duration[l]])
    #print(array_fixations)
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
    string_folder='static/stimuli/'
    image_source = string_folder+name_map
    im = plt.imread(image_source)
    img = Image.fromarray(im)
    width, height = img.size

    images=[]
    for i in get_array_fixations(user_name, name_map):
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        #cropped_img.save("{0}.jpg".format(type))
        images.append(cropped_img)
    return images, len(images)
    #return(cropped_img)

def draw_gaze_stripes(user_name, name_map):

    if user_name == 'ALL':
        max_amount_images = 0
        ListUser = get_data_map(name_map).user.unique()

        for i in range(len(ListUser)):
            images, amount_images = get_cropped_images(ListUser[i], name_map)
            max_amount_images = max(max_amount_images, amount_images)
        
        fig = figure(plot_width = 25*max_amount_images, plot_height = 25*len(ListUser), x_range=(0,max_amount_images-1), y_range=(-1,len(ListUser)-1), x_axis_location=None, y_axis_location=None, title = 'Gaze stripes all users')
        for i in range(len(ListUser)):
            images, amount_images = get_cropped_images(ListUser[i], name_map)
            amount_images -= 1
            for j in range(amount_images):
                #This must be changed
                fig.image_url(['1.jpg'], j, i, 1, 1)
        
    else:
        images, amount_images = get_cropped_images(user_name, name_map)
        #we need to work on the x axis (duration scale)
        fig = figure(plot_width=75*amount_images, plot_height=75, x_range=(0,amount_images), y_range=(0,1), x_axis_location=None, y_axis_location=None, title = 'Gaze stripes user '+ str(user_name[1:]))
        for i in range(amount_images):
            im = images[i].convert("RGBA")
            imarray = np.array(im)
            fig.image_rgba(image=[imarray], x=i, y=0, dw=1, dh=1)

    script, div = components(fig)
    return [script, div]

#get_cropped_images('p1', '01_Antwerpen_S1.jpg')
