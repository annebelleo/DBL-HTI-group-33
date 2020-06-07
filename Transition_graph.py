#!/usr/bin/env python
# coding: utf-8

# In[2]:

import networkx as nx
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, TapTool, BoxSelectTool, PointDrawTool,     SaveTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges
from bokeh.models import Arrow, VeeHead, Circle, MultiLine
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from HelperFunctions import get_adjacency_matrix, find_AOIs, get_cropped_image_AOI

df_data = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', sep='\t')


# In[12]:


# draw a figure showing the transition graph for one map:
def draw_transition_graph(user_name: str, name_map: str, multiple = False):

    # read in user input of desired top AOI's to be displayed in transition graph
    num_AOIs = 5 # num_AOIs is defined for now

    # run AOI algorithm
    df_AOI = find_AOIs(name_map, num_AOIs)

    # filter out all data that belongs to the chosen user(s)
    data = df_AOI[df_AOI['StimuliName'] == name_map]
    if user_name != "ALL":
        data = data[data['user'] == user_name]

    if data.size == 0:
        return ["No user data found",""]

    # create empty matrix
    dimension = num_AOIs + 1 # dimensions are +1 in size, so AOIs correspond with index
    A = np.zeros(shape=(dimension, dimension))

    # create adjacency matrix by finding out frequencies of shifts between AOI's over the data
    A = np.matrix(get_adjacency_matrix(data, num_AOIs))

    #scale matrix
    if user_name !="ALL":
        A = 5*A

    # convert matrix to representation of graph
    G = nx.from_numpy_matrix(np.matrix(A), create_using=nx.DiGraph)

    # remove nodes without neigbours, including node 0
    iso_nodes = list(nx.isolates(G))
    for n in iso_nodes:
            G.remove_node(n)  # removes node 0, which does not have any edges

    # define list of existing nodes and edges
    node_list = list(G.nodes)
    edge_list = list(G.edges(data=True))

    # define positions of nodes
    try:
        pos = nx.planar_layout(G) # apply planar positioning
    except nx.exception.NetworkXException: # in case the adjacency matrix is not planar
        pos=nx.circular_layout(G) # apply circular positioning
        pass

    # convert networkx graph representation to bokeh graph renderer
    graph_renderer = from_networkx(G, pos, scale=2, center=(0, 0))
    
#     # store AOI thumnails in list (not working)
#     image = get_cropped_image_AOI(df_AOI, 1, name_map)
    
#     graph_renderer.node_renderer.data_source.data['imgs'] = [image,image,image,image,image]
    
    graph_renderer.node_renderer.data_source.data['imgs'] = [
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg']

    # define custom tooltips behaviour when hovering over nodes
    TOOLTIPS = """
    <div>
        <div>
            <p> AOI: @index </p>
            <img
                src="@imgs" height="100" alt="@imgs" width="100"
            ></img>
        </div>
    </div>
    """

    # define plot features
    plot = figure(title="Transition Graph Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                      tools=[HoverTool(tooltips=[("AOI", "@index")]), BoxZoomTool(), ResetTool(),
                             TapTool(), BoxSelectTool(), PointDrawTool(), SaveTool()],
                              tooltips = TOOLTIPS, # custom defined html code
                              toolbar_location="below", toolbar_sticky=False, sizing_mode='scale_both')

    # customise nodes
    circleSize = 40
    graph_renderer.node_renderer.glyph = Circle(size=circleSize, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=circleSize, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=circleSize, fill_color=Spectral4[1])

    # customise edges
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=10)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=10)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=10)

    # customise edge width
    graph_renderer.edge_renderer.data_source.data["line_width"] = [G.get_edge_data(a,b)['weight'] for a, b in G.edges()]
    graph_renderer.edge_renderer.glyph.line_width = {'field': 'line_width'}

    graph_renderer.selection_policy = NodesAndLinkedEdges()

    # draw an arrow for each edge
    for S, E, W in edge_list:
        plot.add_layout(Arrow(line_alpha=0, end=VeeHead(fill_color = "#CCCCCC", line_color="#CCCCCC", line_width=W['weight']),
                                  x_start=pos[S][0], y_start=pos[S][1], x_end=pos[E][0], y_end=pos[E][1]))
        
    plot.axis.visible = False
    plot.renderers.append(graph_renderer) # append graph renderer to the plot
    
     ## BOKEH END CODE
     # display graph on web page
     if not multiple:
         script, div = components(plot)
         return [script, div]
     else:
         return plot
