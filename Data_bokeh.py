# import libraries
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bokeh.models import LabelSet, Select
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import column
from bokeh.embed import components

# 'library' created by the team to help with he processing of the data
from HelperFunctions import get_data_user, get_data_user_all_maps

def draw_dataframe(user_name, name_map, sortby = ['StimuliName'], ascending=False):
    if name_map == 'ALL':
        df = get_data_user_all_maps(user_name)
    else:
        df = get_data_user(user_name, name_map)

    df.sort_values(by=sortby, inplace=True, ascending=ascending)

    source = ColumnDataSource(df)
    columns = [
        TableColumn(field="Timestamp", title="Time Stamp"),
        TableColumn(field="StimuliName", title="Map"),
        TableColumn(field="FixationIndex", title="Fixation Index"),
        TableColumn(field="FixationDuration", title="Fixation Duration"),
        TableColumn(field="MappedFixationPointX", title="X Coordinate Fixation"),
        TableColumn(field="MappedFixationPointY", title="Y Coordinate Fixation"),
        TableColumn(field="user", title="Participant"),
        TableColumn(field="description", title="description"),
    ]
    
    data_table = DataTable(source=source, columns=columns, width = 750, height=1500)

    script, div = components(data_table)
    return [script, div]
