#Copied libraries from Data Analytics DMM Programming exercises

import numpy as np  # import auxiliary library, typical idiom
import pandas as pd  # import the Pandas library, typical idiom
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans  # for clustering

data_file = pd.read_csv('datasets/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace=True)

def get_data_user(user_name, name_map):
    data_user = data_file.loc[data_file['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user


def GetNumClusters(num_AOIs):
    num_clusters = math.ceil(num_AOIs*1.5)
    return num_clusters


def FindClusters(user_name, name_map, num_clusters):
    df = get_data_user(user_name, name_map)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    centers = pd.DataFrame(km.cluster_centers_, columns=X_km.columns)
    X_km['cluster'] = km.labels_
    return X_km


def FindCenters(user_name, name_map, num_clusters):
    df = get_data_user(user_name, name_map)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    centers = pd.DataFrame(km.cluster_centers_, columns=X_km.columns)
    X_km['cluster'] = km.labels_
    return centers


def DrawClusters(user_name, name_map, num_clusters):
    X_km = FindClusters(user_name, name_map, num_clusters)
    centers = FindCenters(user_name, name_map, num_clusters)

    # NRest of code in this cell is just for visualizing clusters, not needed
    # Colors will not always be in same order so centers not always same color as clusters
    ax = X_km[X_km['cluster'] == 0].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='green')
    X_km[X_km['cluster'] == 1].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='orange', ax=ax)
    X_km[X_km['cluster'] == 2].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='purple', ax=ax)
    X_km[X_km['cluster'] == 3].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='blue', ax=ax)
    X_km[X_km['cluster'] == 4].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='red', ax=ax)
    X_km[X_km['cluster'] == 5].plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', s=50, c='yellow', ax=ax)

    centers.plot(kind='scatter', x='MappedFixationPointX', y='MappedFixationPointY', c=['green', 'orange', 'purple', 'blue', 'red', 'yellow'], s=50, marker='x', ax=ax);

    string_folder = 'datasets/stimuli/'
    image_source = string_folder + name_map
    img = plt.imread(image_source)
    ax.imshow(img, alpha=0.5)

    # y axis must be reversed to match with original images
    ax.invert_yaxis()
    plt.show()

#Number of AOIs user want to display
#The number of clusters will be 1.5*num_AOIs (rounded up to nearest int)
#Then pick a num_AOIs number of clusters that have longest fixation duration
#1.5*num_AOIs is just my evaluation for it, could be higher or lower
num_AOIs = 4

DrawClusters('p1', '04_Köln_S1.jpg', 6)