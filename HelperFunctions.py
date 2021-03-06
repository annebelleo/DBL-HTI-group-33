import pandas as pd
import numpy as np
import os
import re
import datetime
import matplotlib.pyplot as plt
from PIL import Image
import random
import math
from bokeh.plotting import ColumnDataSource
from sklearn.cluster import KMeans
import shutil


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def drop_down_info(vis_methode: list, df: pd.DataFrame) -> list:
    """
    Gives all items to de displayed on the dropdown menus.
    :param vis_methode:
    :param df:
    :return:
    """
    all_maps = np.sort(df.StimuliName.unique())
    all_users = np.sort(df.user.unique())
    if type(all_users[0]) is str:
        all_users = sorted(all_users, key=natural_key)
    all_users = np.insert(all_users, 0, "ALL")
    max_AOI = 20
    all_AOIs = list(range(1, max_AOI + 1))

    return [all_users, all_maps, vis_methode, all_AOIs]


def get_source(user_name: str, name_map: str, data_set: pd.DataFrame) -> ColumnDataSource:
    df = get_data_user(user_name, name_map, data_set)
    df['fix_time_scaled'] = df['FixationDuration'] / 12
    source = ColumnDataSource(df)
    return source


def get_data_user_all_maps(user_name: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    When given a pd.dataframe it will return all rows were the user_name & map_name match.
    :param user_name: expected to be a sting string
    :param map_name: expected to be a sting string
    :param df: pd.dataframe to filter
    :return: pd.dataframegit
    """
    if user_name == 'ALL':
        user_data = df
    else:
        user_data = df.loc[df['user'] == user_name]
    return user_data


def get_data_user(user_name: str, map_name: str, df: pd.DataFrame) -> pd.DataFrame:
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


def get_data_map(map_name, df: pd.DataFrame) -> pd.DataFrame:
    """
    When given a pd.dataframe it will return all rows were the map_name match.
    :param map_name: expected to be string
    :param df: pd.dataframe to filter
    :return:
    """
    map_data = df.loc[df['StimuliName'] == map_name]
    return map_data


def get_x_fixation(user_name: str, map_name: str, df: pd.DataFrame) -> list:
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


def get_y_fixation(user_name: str, map_name: str, df: pd.DataFrame) -> list:
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


def get_duration_fixation(user_name: str, map_name: str, df: pd.DataFrame) -> list:
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


def get_array_fixations(user_name: str, map_name: str, df: pd.DataFrame):
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
    image_source = string_folder + name_map
    im = plt.imread(image_source)
    img = Image.fromarray(im)
    width, height = img.size

    images = []
    for i in get_array_fixations(user_name, name_map):
        x = i[0] - 100
        y = i[1] - 100
        w = i[0] + 100
        h = i[1] + 100
        area = (x, y, width, height)
        cropped_img = img.crop(area)
        images.append(cropped_img)
    return images, len(images)


def get_cropped_images_gazestripe(user_name, name_map, data_set, image_source):
    img = Image.open(image_source)

    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    width, height = img.size
    list_fixations = get_array_fixations(user_name, name_map, data_set)
    images = Image.new('RGB', (200 * len(list_fixations), 200))

    for n, i in enumerate(list_fixations):
        i[1] = height - i[1]
        x = i[0] - 100
        y = i[1] - 100
        w = i[0] + 100
        h = i[1] + 100
        area = (x, y, w, h)
        cropped_img = img.crop(area)
        images.paste(cropped_img, (n * 200, 0))

    return images


# Returns dataframe with coordinates put in clusters
def findClusters(map_name, num_clusters, data_set):
    df = get_data_map(map_name, data_set)
    X_km = df[['MappedFixationPointX', 'MappedFixationPointY']].copy()
    km = KMeans(n_clusters=num_clusters)
    km.fit(X_km)
    X_km['cluster'] = km.labels_
    return X_km


# Returns dataframe with column identifying specific AOI for each fixation 
def find_AOIs(map_name, num_AOIs, data_set):
    df_map = get_data_map(map_name, data_set)
    df_fixation = df_map[['FixationDuration', 'Timestamp', 'user', 'StimuliName', ]]
    num_clusters = math.ceil(num_AOIs * 1.5)
    X_km = findClusters(map_name, num_clusters, data_set)
    df_clusters = X_km.join(df_fixation)

    grouped_cluster = df_clusters.groupby('cluster')
    grouped_sum = grouped_cluster[['FixationDuration']].sum()
    nlargest = grouped_sum.nlargest(num_AOIs, ['FixationDuration'])
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
    data = data.sort_values(['user', 'Timestamp'], ascending=[1, 1]).reset_index()

    # Initializing the matrix
    gridline = []
    for i in range(num_AOIs + 1):
        gridline.append(0)
    grid = []
    for i in range(num_AOIs + 1):
        grid.append(list(gridline))

    # Calculating number of transitions between AOIs and adding them to matrix
    for i in range(len(data) - 1):
        current_AOI = data.loc[i, 'AOI']
        next_AOI = data.loc[i + 1, 'AOI']
        if data.loc[i, 'user'] == data.loc[i + 1, 'user']:
            if current_AOI != next_AOI:
                grid[current_AOI][next_AOI] += 1
            else:
                i += 1
        else:
            i += 1

    return grid


def get_cropped_image_AOI(data, AOI, name_map, image_source):
    data = data[data["AOI"] == AOI]


    im = plt.imread(image_source)
    
    if (not isinstance(im[0][0][0], np.uint8)):
        img = Image.fromarray((im * 255).astype(np.uint8))
    else:
        img = Image.fromarray(im)
        
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    sum_x = 0
    sum_y = 0
    count = 0
    for j in data['MappedFixationPointX']:
        count += 1
        sum_x += j

    for k in data['MappedFixationPointY']:
        sum_y += k

    x = sum_x/count
    y = sum_y/count

    img_size = 100
   
    minX = x - img_size 
    minY = y - img_size
    maxX = x + img_size
    maxY = y + img_size

    area = (minX, minY, maxX, maxY)
    cropped_img = img.crop(area)
    return cropped_img


def normalize_time(map_name, num_AOIs, data_set):
    df_AOI = find_AOIs(map_name, num_AOIs, data_set)
    df_AOI = df_AOI.sort_values('Timestamp')
    users = df_AOI['user'].unique()
    grouped_user = df_AOI.groupby('user')

    df_norm = pd.DataFrame(columns=['Time', 'user', 'AOI'])

    for i in range(len(users)):
        df_temp = grouped_user.get_group(users[i]).reset_index().drop('index', 1)
        initial_time_in = df_temp.loc[0, 'Timestamp']
        initial_time_out = df_temp.loc[0, 'Timestamp'] + df_temp.loc[0, 'FixationDuration']
        total_time = df_temp['FixationDuration'].sum()

        for j in range(len(df_temp)):
            current_time = df_temp.loc[j, 'Timestamp']
            AOI = df_temp.loc[j, 'AOI']
            fix_time = df_temp.loc[j, 'FixationDuration']
            time_in = int(1000 * ((current_time - initial_time_in) / total_time))
            time_out = int(1000 * ((current_time + fix_time - initial_time_out) / total_time))
            df_norm = df_norm.append({'Time': time_in, 'user': users[i], 'AOI': AOI}, ignore_index=True)
            df_norm = df_norm.append({'Time': time_out, 'user': users[i], 'AOI': AOI}, ignore_index=True)

            df_norm = df_norm.sort_values('Time').reset_index().drop('index', 1)

    return df_norm


def aggregate_time(map_name, num_AOIs, data_set):
    df_norm = normalize_time(map_name, num_AOIs, data_set)

    df = pd.DataFrame(0, index = range(len(df_norm)), columns = ['Time']+['AOI_{0}'.format(i) for i in range(1, num_AOIs + 1)])

    for i in range(len(df)):
        AOI = df_norm.loc[i, 'AOI']
        df.loc[i, 'AOI_{0}'.format(AOI)] = 1

    df['Time'] = df_norm['Time']

    step = 50
    max_norm = df_norm['Time'].max()
    min_norm = df_norm['Time'].min()
    s = math.ceil((max_norm - min_norm) / step)
    df_agg = pd.DataFrame(columns=df.columns.to_list())

    df_agg.loc[0, 'Time'] = 0
    for i in range(1, s + 1):
        df_agg.loc[i, 'Time'] = int(df_agg.loc[i - 1, 'Time'] + step)

    count = 0
    i = 0

    while i < ((len(df_norm)) - 1):
        norm = df_agg.loc[count, 'Time']
        time = df_norm.loc[i, 'Time']
        prev = i
        while (norm >= time) and (i < (len(df_norm)) - 1):
            i = i + 1
            norm = df_agg.loc[count, 'Time']
            time = df_norm.loc[i, 'Time']
        for j in range(1, num_AOIs + 1):
            df_temp = df.loc[prev:i, 'AOI_{0}'.format(j)].to_frame()
            df_agg.loc[count, 'AOI_{0}'.format(j)] = df_temp.sum()[0]
        count += 1

    df_agg.drop(df_agg[df_agg['Time'] > 1000].index, inplace=True)

    return df_agg


def cleanup_temp_files(path, t: int = 7200,) -> None:
    """ removes all files older tahn
    """
    files = []
    format_str = "%Y-%m-%d-%H-%M"  # The format
    # r=root, d=directories, f = files

    for r, d, f in os.walk(path):
        files = f
        directories = d
        break

    try:
        for i in files:
            a = datetime.datetime.strptime(i[:16], format_str)
            b = datetime.datetime.now()
            if t < (b - a).total_seconds():
                os.remove(path + i)
                print("removed file:", i)
    except:
        print("no files found")
    try:
        for i in directories:
            a = datetime.datetime.strptime(i[:16], format_str)
            b = datetime.datetime.now()
            if t < (b - a).total_seconds():
                shutil.rmtree(path + i)
                print("removed folder:", i)
    except:
        print("no folders found")
