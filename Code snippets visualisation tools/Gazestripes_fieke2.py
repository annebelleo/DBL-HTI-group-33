import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
#from bokeh.io import hplot

df = pd.read_csv(r"C:\Users\20182483\OneDrive - TU Eindhoven\Documents\Jaar 2\Q4\2IOA0\MetroMapsEyeTracking\MetroMapsEyeTracking\all_fixation_data_cleaned_up.csv", encoding='latin1', delim_whitespace=True)
#df

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
    string_folder= r'C:\Users\20182483\OneDrive - TU Eindhoven\Documents\Jaar 2\Q4\2IOA0\MetroMapsEyeTracking\MetroMapsEyeTracking\\stimuli\\'
    image_source = string_folder+name_map
    im = plt.imread(image_source)
    img = Image.fromarray(im)
    width, height = img.size
#     print(width, height)

    images=[]
    n = 1
    for i in get_array_fixations(user_name, name_map):
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        type = n
        cropped_img.save("{0}.jpg".format(type))
        n+= 1
        images.append(cropped_img)
    return(images)
    #return(cropped_img)

def draw_gaze_stripes(user_name, name_map):


    fig1 = figure(plot_width = 710, plot_height = 450)
    fig1.image_url(['1.jpg'], 0, 100, 100, 100)
    fig2 = figure(plot_width = 710, plot_height = 450)    
    fig2.image_url(['1.jpg'], 0, 100, 100, 100)
    p = gridplot([[fig1, fig2]])
    show(p)

    fig1 = figure(plot_width = 100, plot_height = 100)
    fig1.image_url(['1.jpg'], 0, 80, 80, 80)
    fig2 = figure(plot_width = 100, plot_height = 100)
    fig2.image_url(['2.jpg'], 0, 80, 80, 80)
    fig3 = figure(plot_width = 100, plot_height = 100)
    fig3.image_url(['3.jpg'], 0, 80, 80, 80)
    fig4 = figure(plot_width = 100, plot_height = 100)
    fig4.image_url(['4.jpg'], 0, 80, 80, 80)
    fig5 = figure(plot_width = 100, plot_height = 100)
    fig5.image_url(['5.jpg'], 0, 80, 80, 80)
    fig6 = figure(plot_width = 100, plot_height = 100)
    fig6.image_url(['6.jpg'], 0, 80, 80, 80)
    fig7 = figure(plot_width = 100, plot_height = 100)
    fig7.image_url(['7.jpg'], 0, 80, 80, 80)
    p = gridplot([[fig1, fig2, fig3, fig4, fig5, fig6, fig7]])
    show(p)
    
##    n = 1
##    for i in get_array_fixations(user_name, name_map):
##        figure_name = 'fig{}'.format(n)
##        #print(figure_name)
##        figure_name = figure(plot_width = 710, plot_height = 450)
##        figure_name.image_url(['{0}.jpg'.format(n)], 0, 80, 80, 80)
##        p = gridplot([[fig1, fig2]])
##        n+=1
##
##    show(p)

    #show(fig)
    #fig.savefig('gaze stripe' + name_map)

#get_array_fixations('p1','01_Antwerpen_S1.jpg')
#get_cropped_images('p1', '01_Antwerpen_S1.jpg')

draw_gaze_stripes('p1', '01_Antwerpen_S1.jpg')
