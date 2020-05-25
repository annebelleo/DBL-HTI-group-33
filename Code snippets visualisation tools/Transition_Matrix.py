import numpy as np
import pandas as pd 
import math
from sklearn.cluster import KMeans

data_file = pd.read_csv('static/all_fixation_data_cleaned_up.csv',
                        encoding='latin1', sep='\t')

def get_data_map(map_name):
    data_map = data_file.loc[data_file['StimuliName'] == map_name]
    return data_map


#Returns dataframe with coordinates put in clusters
def FindClusters(map_name, num_clusters):
	
    df = get_data_map(map_name)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    X_km['cluster'] = km.labels_
    return X_km   

#Returns dataframe with column identifying specific AOI for each fixation 
def Find_AOIs(map_name, num_AOIs):

    df_map = get_data_map(map_name)
    df_fixation = df_map[['FixationDuration', 'Timestamp', 'user']]
    num_clusters = math.ceil(num_AOIs*1.5)
    X_km = FindClusters(map_name, num_clusters)
    df_clusters = X_km.join(df_fixation)
	
    grouped_cluster = df_clusters.groupby('cluster')
    grouped_sum = grouped_cluster[['FixationDuration']].sum()
    nlargest = grouped_sum.nlargest(num_AOIs,['FixationDuration'])
    nlargest = nlargest.reset_index()
	
    df_AOI = pd.DataFrame()
    count = 1
    for i in nlargest['cluster']:
        df_AOI = df_AOI.append(grouped_cluster.get_group(i))
        df_AOI.loc[df_AOI['cluster'] == i, 'AOI'] = count
        count += 1
    df_AOI = df_AOI.astype({'AOI': int})
    return df_AOI


def get_transition_matrix(map_name, num_AOIs):
	
	df_AOI = Find_AOIs(map_name, num_AOIs)
	groupuser = df_AOI.sort_values(['user','Timestamp'], ascending = [1,1]).reset_index()
	
	#Initializing the matrix
	gridline = []
	for i in range(num_AOIs + 1):
		gridline.append(0)
	grid = []
	for i in range(num_AOIs + 1):
		grid.append(list(gridline))

	#Calculating number of transitions between AOIs and adding them to matrix
	for i in range (len(groupuser) - 1):
		current_AOI = groupuser.loc[i,'AOI']
		next_AOI = groupuser.loc[i+1,'AOI']
		if groupuser.loc[i,'user'] == groupuser.loc[i+1,'user']:
			if current_AOI != next_AOI:
				grid[current_AOI][next_AOI] += 1
			else: i+=1
		else:i+=1

	return grid		