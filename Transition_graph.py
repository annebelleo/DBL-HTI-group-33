#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import networkx as nx
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from bokeh.embed import components
from bokeh.models import HoverTool, BoxZoomTool, ResetTool


# In[2]:


data_file = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', sep='\t')

#get data of one test (user, picture, color):
def get_data_user(user_name, name_map):
    data_user = data_file.loc[data_file['user'] == user_name]
    data_user = data_user.loc[data_user['StimuliName'] == name_map]
    return data_user


#get array of all fixations with fixation duration in order from one experiment:
def get_array_fixations(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = get_x_fixation(user_name, name_map)
    array_fixations_y = get_y_fixation(user_name, name_map)
    array_fixation_duration = get_duration_fixation(user_name, name_map)
    array_fixations = []
    for l in range(len(array_fixations_x)):
        array_fixations.append([array_fixations_x[l],array_fixations_y[l], array_fixation_duration[l]])
    return array_fixations


#get array of all x_coordinate fixations from one experiment:
def get_x_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_x = []
    for i in data_user['MappedFixationPointX']:
        array_fixations_x.append(i)
    return array_fixations_x


#get array of all y_coordinate fixations from one experiment:
def get_y_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixations_y = []
    for i in data_user['MappedFixationPointY']:
        array_fixations_y.append(i)
    return array_fixations_y


#get array of all fixation durations from one experiment:
def get_duration_fixation(user_name, name_map):
    data_user = get_data_user(user_name, name_map)
    array_fixation_duration = []
    for i in data_user['FixationDuration']:
        array_fixation_duration.append(i)
    return array_fixation_duration

def get_cropped_image(x, y, name_map):
    # (security check: check that crop range does not go outside the image size)
    # use coordinates and set crop range
    # crop image and save it as a new image in a transition_graph_images folder
    
    
    my_file = os.path.join('stimuli', name_map)
    img = plt.imread(my_file)
    img = Image.fromarray(img)
    width, height = img.size
#     print(width, height)


# In[3]:


# commands to explore data
# name_map = '01_Antwerpen_S1.jpg'
# data = data_file[data_file['StimuliName'] == name_map]
# test = data_file.sort_values('Timestamp')
# test.mode()
# test = data_file[data_file['Timestamp'] == 223463]
# test
# test = data_file[data_file["user"] == 'p2']
# test = test[test['StimuliName'] == '01_Antwerpen_S2.jpg']
# test
# CTRL + / comments


# In[11]:




# draw a figure showing the transition graph for one map:
def draw_transition_graph(name_map):
    # filter out all data that belongs to name_map
    name_map = '04_Köln_S1.jpg' # remove later
    data = data_file[data_file['StimuliName'] == name_map]
    
    # read in user input of desired top AOI's to be displayed in transition graph
        # run AOI algorithm (with a high AOI number?? gives more accurate cropped images)
        # or find a way to resize the cropped images depending on size of AOI.
        # or AOI algorithm creates equally big clusters?
    numberOfAOIs = 7
    
    # define AOI's (create classes?)
        # define centre coordinates of AOI
    
    # create adjacency matrix with size being the number of AOI's
    A = np.zeros(shape=(numberOfAOIs + 1,numberOfAOIs + 1)) # +1 in size, so AOIs correspond with index
    
    # find out frequencies of shifts between AOI's over all data
        # loop over all participants
        # attribute weights to the the different AOI shifts in the adjacency matrix
        # weight is the amount of times the path is taken from one AOI to another
    A = np.matrix([[0,0,0,0,0,0,0,0],
                   [0,0,10,0,0,0,0,0],
                   [0,0,0,7,5,0,0,0],
                   [0,0,0,0,0,4,1,0],
                   [0,0,0,0,0,0,0,7],
                   [0,0,0,0,0,0,0,4],
                   [0,0,0,0,0,0,0,0],
                   [0,4,0,0,0,0,0,0]])
    
    # convert matrix to representation of graph    
    G = nx.from_numpy_matrix(np.matrix(A), create_using=nx.DiGraph)
    
    G.remove_node(0) #removes node 0, which does not have any edges
    node_list = list(G.nodes)
    edge_list = list(G.edges(data=True)) 
    
    pos=nx.planar_layout(G) # needs to be changed to a hierarchical algorithm
    nx.draw_networkx_nodes(G,pos,node_color='blue')
 
    all_weights = []
    # Iterate through the graph nodes to gather all the weights
    for (node1,node2,data) in G.edges(data=True):
        all_weights.append(data['weight']) #we'll use this when determining edge thickness
 
    # Get unique weights
    unique_weights = list(set(all_weights))
 
    # Plot the edges - one by one
    for weight in unique_weights:
        # Form a filtered list with just the weight you want to draw
        weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
        # Multiplying by [num_nodes/sum(all_weights)] makes the graphs edges look cleaner
        width = weight*len(node_list)*3.0/sum(all_weights)
        nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)
 
    #Plot the graph
#     plt.axis('off')
    plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.title('Transition graph')
    plt.savefig("TransitionGraph.png")
    
    
    plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1),
                  tools="", toolbar_location=None)

    graph = from_networkx(G, pos, scale=2, center=(0,0))
    plot.renderers.append(graph)
    
    node_hover_tool = HoverTool(tooltips=[("AOI", "@index")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    #output_file("networkx_graph.html")
    script, div = components(plot)
    return [script, div]

#     return nx.planar_layout(G), edge_list
    

