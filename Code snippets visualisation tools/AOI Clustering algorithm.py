#Copied libraries from Data Analytics DMM Programming exercises

import numpy as np  # import auxiliary library, typical idiom
import pandas as pd  # import the Pandas library, typical idiom
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans  # for clustering

data_file = pd.read_csv('datasets/all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace=True)

def get_data_map(name_map):
    data_map = data_file.loc[data_file['StimuliName'] == name_map]
    return data_map


def FindClusters(name_map, num_clusters):
    df = get_data_map(name_map)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    X_km['cluster'] = km.labels_
    return X_km   


def Find_AOIs(name_map, num_total_AOIs):
    df_map = get_data_map(name_map)
    df_fixation = df_map[['FixationDuration']]
    num_clusters = math.ceil(num_total_AOIs*1.5)
    X_km = FindClusters(name_map, num_clusters)
    df_clusters = X_km.join(df_fixation)
    grouped_cluster = df_clusters.groupby('cluster')
    grouped_sum = grouped_cluster[['FixationDuration']].sum()
    nlargest = grouped_sum.nlargest(num_total_AOIs,['FixationDuration'])
    nlargest = nlargest.reset_index()
    df_AOI = pd.DataFrame()
    count = 1
    for i in nlargest['cluster']:
        df_AOI = df_AOI.append(grouped_cluster.get_group(i))
        df_AOI.loc[df_AOI['cluster'] == i, 'AOI'] = count
        count += 1
    df_AOI = df_AOI.astype({'AOI': int})
    return df_AOI     


def Find_Specific_AOI(name_map, num_total_AOIs, num_AOI):
    df_AOI = Find_AOIs(name_map, num_total_AOIs)
    grouped_AOI = df_AOI.groupby('AOI') 
    return grouped_AOI.get_group(num_AOI)
