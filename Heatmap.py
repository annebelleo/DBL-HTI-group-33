import pandas as pd
import csv
import matplotlib.pyplot as plt, mpld3
import numpy as np
from scipy import ndimage
#from skimage import io
#from skimage import transform
from scipy.interpolate import griddata
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


#import data
# data_file = pd.read_csv('all_fixation_data_cleaned_up.csv', encoding ='latin1', sep='\t')


def get_data_user(user_name, name_map, data_file):
    data_user = data_file.loc[data_file['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user


def get_x_fixation(user_name, name_map, data_file):
    data_user = get_data_user(user_name, name_map, data_file)
    array_fixations_x = []
    for i in data_user['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x


def get_y_fixation(user_name, name_map, data_file):
    data_user = get_data_user(user_name, name_map, data_file)
    array_fixations_y = []
    for i in data_user['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y


def get_duration_fixation(user_name, name_map, data_file):
    data_user = get_data_user(user_name, name_map, data_file)
    array_fixation_duration = []
    for i in data_user['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration


def draw_heatmap(user_name, name_map, data_file ):
    #string_folder = 'datasets/stimuli/'
    #image_source = string_folder + name_map
    #img = plt.imread(image_source)
    fig, ax = plt.subplots()
    # Comment out next line to see the plot if it's not visible
    #ax.imshow(img)

    X_dat = get_x_fixation(user_name, name_map, data_file)
    Y_dat = get_y_fixation(user_name, name_map, data_file)
    Z_dat = get_duration_fixation(user_name, name_map, data_file)

    # scale data from -0.1 to 0.1 (instead of 0 to largest fixation duration)
    # Z_max = max(Z_dat)
    # for j in range(len(Z_dat)):
    # Z_dat[j]= (Z_dat[j]/(Z_max))*0.2 -0.1

    X, Y, Z, = np.array([]), np.array([]), np.array([])
    for i in range(len(X_dat)):
        X = np.append(X, X_dat[i])
        Y = np.append(Y, Y_dat[i])
        Z = np.append(Z, (Z_dat[i]))

    # create x-y points to be used in heatmap
    xi = np.linspace(0, 1650)
    yi = np.linspace(0, 1200)

    levels = MaxNLocator(nbins=25).tick_values(0, Z.max())
    cmap = plt.get_cmap('rainbow')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    # Z is a matrix of x-y values
    zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='cubic')

    # Create the heatmap
    CS = plt.pcolormesh(xi, yi, zi, cmap=cmap, norm=norm, alpha=0.7)
    a = plt.gcf()

    plt.colorbar()
    #plt.show()
    #output = mpld3.fig_to_html(plt)
    #print (output)
    output = "test"
    return output


#draw_heatmap('p9', '01b_Antwerpen_S2.jpg')