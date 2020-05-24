import networkx as nx
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, TapTool, BoxSelectTool, PointDrawTool, \
    SaveTool
from bokeh.models.graphs import from_networkx
from bokeh.plotting import figure
from bokeh.models import ImageURL
from bokeh.models import Arrow, VeeHead

df_data = pd.read_csv('static/all_fixation_data_cleaned_up.csv', encoding='latin1', sep='\t')


# draw a figure showing the transition graph for one map:
def draw_transition_graph(user_name, name_map):
    # filter out all data that belongs to name_map

    data = df_data[df_data['StimuliName'] == name_map]

    # read in user input of desired top AOI's to be displayed in transition graph
    # run AOI algorithm (with a high AOI number?? gives more accurate cropped images)
    # or find a way to resize the cropped images depending on size of AOI.
    # or AOI algorithm creates equally big clusters?
    numberOfAOIs = 7

    # define AOI's (create classes?)
    # define centre coordinates of AOI

    # create adjacency matrix with size being the number of AOI's
    A = np.zeros(shape=(numberOfAOIs + 1, numberOfAOIs + 1))  # +1 in size, so AOIs correspond with index

    # find out frequencies of shifts between AOI's over all data
    # loop over all participants
    # attribute weights to the the different AOI shifts in the adjacency matrix
    # weight is the amount of times the path is taken from one AOI to another
    A = np.matrix([[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 10, 0, 0, 0, 0, 0],
                   [0, 0, 0, 7, 5, 0, 0, 0],
                   [0, 0, 0, 0, 0, 4, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 7],
                   [0, 0, 0, 0, 0, 0, 0, 4],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 4, 0, 0, 0, 0, 0, 0]])

    # convert matrix to representation of graph    
    G = nx.from_numpy_matrix(np.matrix(A), create_using=nx.DiGraph)

    G.remove_node(0)  # removes node 0, which does not have any edges
    node_list = list(G.nodes)
    edge_list = list(G.edges(data=True))

    pos = nx.planar_layout(G)  # needs to be changed to a hierarchical algorithm


    graph_renderer = from_networkx(G, pos, scale=2, center=(0, 0))

    TOOLTIPS = """
    <div>
        <div>
            <img
                src="@imgs" height="100" alt="@imgs" width="100"
            ></img>
        </div>
    </div>
    """

    plot = figure(title="Transition Graph Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                  tools=[HoverTool(tooltips=[("AOI", "@index")]), BoxZoomTool(), ResetTool(),
                         TapTool(), BoxSelectTool(), PointDrawTool(), SaveTool()],
                  tooltips=TOOLTIPS,
                  toolbar_location="below", toolbar_sticky=False)

    #     node_hover_tool = HoverTool(tooltips=[("AOI", "@index")])
    #     plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    # customise nodes

    string_folder = 'static/stimuli/'
    image_source = string_folder+name_map

    graph_renderer.node_renderer.glyph = ImageURL(url=[image_source], w=0.1, h=0.1)
    graph_renderer.node_renderer.selection_glyph = ImageURL(url=[image_source], w=0.15, h=0.15)
    graph_renderer.node_renderer.hover_glyph = ImageURL(url=[image_source], w=0.2, h=0.2)

    # Draw a arrow for each edge
    for S, E, W in edge_list:
        plot.add_layout(Arrow(end=VeeHead(line_color="firebrick", line_width=W['weight']), x_start=pos[S][0], y_start=pos[S][1], x_end=pos[E][0], y_end=pos[E][1]))

    #     graph_renderer.inspection_policy = EdgesAndLinkedNodes()

    plot.renderers.append(graph_renderer)

    #     output_file("transition_graph.html")
    #     show(plot)

    # BOKEH CODE
    script, div = components(plot)
    return [script, div]
