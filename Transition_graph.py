#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import networkx as nx
import numpy as np
import pandas as pd
from PIL import Image
from bokeh.embed import components
from bokeh.io import output_file, show, output_notebook, reset_output
from bokeh.models import MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, TapTool, BoxSelectTool, PointDrawTool, SaveTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4
from bokeh.plotting import figure


# In[3]:


data_file = pd.read_csv('../all_fixation_data_cleaned_up.csv', encoding='latin1', delim_whitespace=True)


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
    # iterate through the graph nodes to gather all the weights
    for (node1,node2,data) in G.edges(data=True):
        all_weights.append(data['weight']) #we'll use this when determining edge thickness
 
    # get unique weights
    unique_weights = list(set(all_weights))
 
    # plot the edges - one by one
    for weight in unique_weights:
        # form a filtered list with just the weight you want to draw
        weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
        # multiplying by [num_nodes/sum(all_weights)] makes the graphs edges look cleaner
        width = weight*len(node_list)*3.0/sum(all_weights)
        nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=width)
   
    graph_renderer = from_networkx(G, pos, scale=2, center=(0,0))
    
    graph_renderer.node_renderer.data_source.data['imgs'] = [
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg',
    'https://cdn.discordapp.com/attachments/411252758918856715/713308484787241011/cropped.jpg']
    
    
    TOOLTIPS = """
    <div>
        <div>
            <img
                src="@imgs" height="100" alt="@imgs" width="100"
            ></img>
        </div>
    </div>
    """
    
    plot = figure(title="Transition Graph Demonstration", x_range=(-1.1,1.1), y_range=(-1.1,1.1), 
                  tools=[ HoverTool(tooltips=[("AOI", "@index")]), BoxZoomTool(), ResetTool(),
                         TapTool(), BoxSelectTool(), PointDrawTool(), SaveTool() ],
                  tooltips = TOOLTIPS,
                  toolbar_location="below",  toolbar_sticky=False)
    
#     node_hover_tool = HoverTool(tooltips=[("AOI", "@index")])
#     plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
    
    # customise nodes
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    
    # customise edges
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)
    
    # customise edge width
    graph_renderer.edge_renderer.data_source.data["line_width"] = [G.get_edge_data(a,b)['weight'] for a, b in G.edges()]
    graph_renderer.edge_renderer.glyph.line_width = {'field': 'line_width'}
    
    graph_renderer.selection_policy = NodesAndLinkedEdges()
#     graph_renderer.inspection_policy = EdgesAndLinkedNodes()

    plot.renderers.append(graph_renderer)
 
#     output_file("transition_graph.html")
#     show(plot)
    
    # BOKEH CODE
    script, div = components(plot)
    return [script, div]

