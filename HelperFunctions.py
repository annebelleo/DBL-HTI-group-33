import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

FIXATION_DATA = 'static/all_fixation_data_cleaned_up.csv'
df_data = pd.read_csv(FIXATION_DATA, encoding='latin1', delim_whitespace=True)


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
