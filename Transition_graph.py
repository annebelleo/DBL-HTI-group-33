import io
import base64
import networkx as nx
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, TapTool, BoxSelectTool, PointDrawTool, \
    SaveTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges
from bokeh.models import Arrow, VeeHead, Circle, MultiLine
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from HelperFunctions import get_adjacency_matrix, find_AOIs, get_cropped_image_AOI
import sympy.geometry as sp


# draw a figure showing the transition graph for one map:
def draw_transition_graph(user_name: str, name_map: str, data_set: pd.DataFrame, image_source: str, NUM_AOIS, multiple=False):
    # read in user input of desired top AOI's to be displayed in transition graph
    NUM_AOIS = int(NUM_AOIS)  # num_AOIs is defined for now

    # run AOI algorithm
    df_AOI = find_AOIs(name_map, NUM_AOIS, data_set)

    # filter out all data that belongs to the chosen user(s)
    data = df_AOI[df_AOI['StimuliName'] == name_map]
    if user_name != "ALL":
        data = data[data['user'] == user_name]

    if data.size == 0:
        return ["No user data found", ""]

    # create empty matrix
    dimension = NUM_AOIS + 1  # dimensions are +1 in size, so AOIs correspond with index
    A = np.zeros(shape=(dimension, dimension))

    # create adjacency matrix by finding out frequencies of shifts between AOI's over the data
    A = np.matrix(get_adjacency_matrix(data, NUM_AOIS))

    # scale matrix
    if user_name != "ALL":
        A = 5 * A
    else:
        A = 0.2 * A

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
        pos = nx.planar_layout(G)  # apply planar positioning
    except nx.exception.NetworkXException:  # in case the adjacency matrix is not planar
        pos = nx.circular_layout(G)  # apply circular positioning
        pass

    # convert networkx graph representation to bokeh graph renderer
    graph_renderer = from_networkx(G, pos, scale=2, center=(0, 0))

    # save AOI thumbnails in memory and encode to base64 strings
    graph_renderer.node_renderer.data_source.data['imgs'] = []
    for AOI in node_list:
        # get AOI thumbnail
        AOI_thumbnail = get_cropped_image_AOI(df_AOI, AOI, name_map)
        # save image in memory
        in_mem_file = io.BytesIO()
        AOI_thumbnail.save(in_mem_file, format="JPEG")

        # reset file pointer to start
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()

        # encode image to base64 string
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        AOI_image_b64 = base64_encoded_result_bytes.decode('latin1')
        graph_renderer.node_renderer.data_source.data['imgs'].append(
            AOI_image_b64)  # save base64-encoded strings to nodes

    # define custom tooltips behaviour when hovering over nodes
    TOOLTIPS = """
        <div>
            <div>
                <p><b> AOI: @index </b></p>
                <img
                    src="data:image/jpeg;base64, @imgs" height="100" alt="@imgs" width="100"
                ></img>
            </div>
        </div>
        """

    # define plot features
    plot = figure(title="Transition Graph " + name_map, x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                  tools=[HoverTool(tooltips=[("AOI", "@index")]), BoxZoomTool(), ResetTool(),
                         TapTool(), BoxSelectTool(), PointDrawTool(), SaveTool()],
                  tooltips=TOOLTIPS,  # custom defined html code
                  toolbar_location="below", toolbar_sticky=False, sizing_mode='scale_both')

    # customise nodes
    circleRadius = 0.075
    graph_renderer.node_renderer.glyph = Circle(radius=circleRadius, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=circleRadius, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=circleRadius, fill_color=Spectral4[1])

    # customise edges
    graph_renderer.edge_renderer.data_source.data["line_width"] = [G.get_edge_data(a, b)['weight'] for a, b in
                                                                   G.edges()]
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8,
                                                   line_width={'field': 'line_width'})
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2],
                                                             line_width={'field': 'line_width'})

    graph_renderer.selection_policy = NodesAndLinkedEdges()

    # draw an arrow for each edge
    for S, E, W in edge_list:
        x1 = pos[S][0]
        y1 = pos[S][1]
        x2 = pos[E][0]
        y2 = pos[E][1]
        p1 = sp.Point(x1, y1)
        p2 = sp.Point(x2, y2)

        c = sp.Circle(p2, circleRadius)

        l = sp.Line(p1, p2)

        intersections = sp.intersection(l, c)
        intersection1 = [float(intersections[0][0]), float(intersections[0][1])]
        intersection2 = [float(intersections[1][0]), float(intersections[1][1])]

        if x1 <= intersection1[0] <= x2:
            intersectX = intersection1[0]
            intersectY = intersection1[1]
        else:
            intersectX = intersection2[0]
            intersectY = intersection2[1]

        plot.add_layout(
            Arrow(line_alpha=0, end=VeeHead(fill_color="#b3b3b3", line_color="#b3b3b3", line_width=W['weight']),
                  x_start=pos[S][0], y_start=pos[S][1], x_end=intersectX, y_end=intersectY))

    # remove axis and gridlines
    plot.axis.visible = False
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    
    plot.renderers.append(graph_renderer)  # append graph renderer to the plot
    
    # display graph on web page
    if not multiple:
        script, div = components(plot)
        return [script, div]
    else:
        return plot
