import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import random
import math
from sklearn.cluster import KMeans


def drop_down_info(vis_methode: list, df: pd.DataFrame = df_data) -> list:
    """
    Gives all items to de displayed on the dropdown menus.
    :param vis_methode:
    :param df:
    :return:
    """
    all_maps = np.sort(df.StimuliName.unique())
    all_users = np.sort(df.user.unique())
    all_users = np.insert(all_users, 0, "ALL")
    return [all_users, all_maps, vis_methode]


def get_data_user(user_name: str, map_name: str, df: pd.DataFrame = df_data) -> pd.DataFrame:
    """
    When given a pd.dataframe it will return all rows were the user_name & map_name match.
    :param user_name: expected to be a sting string
    :param map_name: expected to be a sting string
    :param df: pd.dataframe to filter
    :return: pd.dataframe
    """
    if user_name == 'ALL':
        user_data = df.loc[df['StimuliName'] == map_name]
    else:
        user_data = df.loc[df['user'] == user_name]
        user_data = user_data.loc[user_data['StimuliName'] == map_name]
    return user_data


def get_data_map(map_name, df: pd.DataFrame = df_data) -> pd.DataFrame:
    """
    When given a pd.dataframe it will return all rows were the map_name match.
    :param map_name: expected to be string
    :param df: pd.dataframe to filter
    :return:
    """
    map_data = df.loc[df['StimuliName'] == map_name]
    return map_data


def get_x_fixation(user_name: str, map_name: str, df: pd.DataFrame = df_data) -> list:
    """
    get array of all x_coordinate fixations from one experiment:
    :param user_name: expected to be a string
    :param map_name: expected to be a string
    :param df: pd.dataframe to filter
    :return:
    """
    user_data = get_data_user(user_name, map_name, df)
    array_fixations_x = []
    for i in user_data['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x


def get_y_fixation(user_name: str, map_name: str, df: pd.DataFrame = df_data) -> list:
    """
    get array of all y_coordinate fixations from one experiment:
    :param user_name: expected to be a string
    :param map_name: expected to be a string
    :param df: pd.dataframe to filter
    :return:
    """
    user_data = get_data_user(user_name, map_name, df)
    array_fixations_y = []
    for i in user_data['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y


def get_duration_fixation(user_name: str, map_name: str, df: pd.DataFrame = df_data) -> list:
    """
    Get array of all fixation durations from one experiment
    :param user_name:
    :param map_name:
    :param df:
    :return:
    """

    user_data = get_data_user(user_name, map_name, df)
    array_fixation_duration = []
    for i in user_data['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration


def get_array_fixations(user_name: str, map_name: str, df: pd.DataFrame = df_data):
    """
    get array of all fixations with fixation duration in order from one experiment
    :param user_name:
    :param map_name:
    :param df:
    :return:
    """
    array_fixations_x = get_x_fixation(user_name, map_name, df)
    array_fixations_y = get_y_fixation(user_name, map_name, df)
    array_fixation_duration = get_duration_fixation(user_name, map_name, df)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l], array_fixations_y[l], array_fixation_duration[l]])
    return array_fixations


def random_color() -> list:
    """
    Generates a random RGB color and returns it in a tuple.
    >>> type(random_color()) == tuple
    True
    >>> type(random_color()[1]) == int
    True
    """
    r = random.randrange(0, 255, 16)
    g = random.randrange(0, 255, 16)
    b = random.randrange(0, 255, 16)
    return r, g, b

def get_cropped_images(user_name, name_map):
    string_folder = 'static/stimuli/'
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
        area = (x, y, width, height)
        cropped_img = img.crop(area)
        images.append(cropped_img)
    return images, len(images)

def get_cropped_images_gazestripe(user_name, name_map):
    string_folder = 'static/stimuli/'
    image_source = string_folder+name_map
    img = Image.open(image_source)
    ImageOps.flip(img)
    img.save("image_cropped_function.jpg")
    width, height = img.size

    list_fixations = get_array_fixations(user_name, name_map)
    images=Image.new('RGB', (200*len(list_fixations), 200))
    count = 0
    for i in list_fixations:
        x = i[0]-100
        y = i[1]-100
        w = i[0]+100
        h = i[1]+100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        images.paste(cropped_img, (count*200,0))
        count+=1
    return images

# Returns dataframe with coordinates put in clusters
def findClusters(map_name, num_clusters):
	
    df = get_data_map(map_name)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    X_km['cluster'] = km.labels_
    return X_km   

# Returns dataframe with column identifying specific AOI for each fixation 
def find_AOIs(map_name, num_AOIs):

    df_map = get_data_map(map_name)
    df_fixation = df_map[['FixationDuration', 'Timestamp', 'user', 'StimuliName',]]
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

# Returns adjacency matrix representing frequencies of shifts in AOIs 
def get_adjacency_matrix(data, num_AOIs):

	data = data.sort_values(['user','Timestamp'], ascending = [1,1]).reset_index()
	
	#Initializing the matrix
	gridline = []
	for i in range(num_AOIs + 1):
		gridline.append(0)
	grid = []
	for i in range(num_AOIs + 1):
		grid.append(list(gridline))

	#Calculating number of transitions between AOIs and adding them to matrix
	for i in range (len(data) - 1):
		current_AOI = data.loc[i,'AOI']
		next_AOI = data.loc[i+1,'AOI']
		if data.loc[i,'user'] == data.loc[i+1,'user']:
			if current_AOI != next_AOI:
				grid[current_AOI][next_AOI] += 1
			else: i+=1
		else:i+=1

	return grid
