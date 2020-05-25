import networkx as nx
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, TapTool, BoxSelectTool, PointDrawTool, \
    SaveTool
from bokeh.models.graphs import from_networkx
from bokeh.models import Arrow, VeeHead, Circle
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from HelperFunctions import get_adjacency_matrix, find_AOIs, get_cropped_image_AOI

df_data = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', sep='\t')


# draw a figure showing the transition graph for one map:
def draw_transition_graph(user_name, name_map):

    # read in user input of desired top AOI's to be displayed in transition graph
    num_AOIs = 5 # num_AOIs is defined for now
    
    # run AOI algorithm  
    df_AOI = find_AOIs(name_map, num_AOIs)

    # filter out all data that belongs to the chosen user(s) 
    data = df_AOI[df_AOI['StimuliName'] == name_map]
    if user_name != "ALL":
        data = data[data['user'] == user_name]
        
    if data.size != 0:

        # create empty matrix
        dimension = num_AOIs + 1 # dimensions are +1 in size, so AOIs correspond with index
        A = np.zeros(shape=(dimension, dimension))  
        
        # create adjacency matrix by finding out frequencies of shifts between AOI's over the data
        A = np.matrix(get_adjacency_matrix(data, num_AOIs))

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


        # define plot features
        plot = figure(title="Transition Graph Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                      tools=[HoverTool(tooltips=[("AOI", "@index")]), BoxZoomTool(), ResetTool(),
                             TapTool(), BoxSelectTool(), PointDrawTool(), SaveTool()],
                              toolbar_location="below", toolbar_sticky=False)

        # customise nodes
        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
        graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

##        graph_renderer.node_renderer.glyph = ImageURL(url=[image_source], w=0.1, h=0.1)
##        graph_renderer.node_renderer.selection_glyph = ImageURL(url=[image_source], w=0.15, h=0.15)
        
        # draw an arrow for each edge
        for S, E, W in edge_list:
            plot.add_layout(Arrow(end=VeeHead(line_color="firebrick", line_width=W['weight']),
                                  x_start=pos[S][0], y_start=pos[S][1], x_end=pos[E][0], y_end=pos[E][1]))

        plot.axis.visible = False
        plot.renderers.append(graph_renderer) # append graph renderer to the plot

        # display graph on web page
        script, div = components(plot)
        return [script, div]
