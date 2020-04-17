import numpy as np
import math
from func_3 import dijkstra
import networkx as nx
import folium

def adj_matrix_task2(g, l):
    adj_mat = np.zeros((len(l), len(l)))
    i = 0
    for elem in l:
        for j in range(len(l)):
            x1 = g.nodes[elem]['pos'][::-1][0]
            y1 = g.nodes[elem]['pos'][::-1][1]
            x2 = g.nodes[l[j]]['pos'][::-1][0]
            y2 = g.nodes[l[j]]['pos'][::-1][1]
            adj_mat[i][j] = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        i = i + 1
    return adj_mat


# return a sub graf
# every edge have weights: path = list of nodes(shortest path), dist : distance/time/network(depends on the given mode)
def graph_task2(g, l_nodes, mode):
    new_g = nx.Graph()
    # add nodes
    for j in range(len(l_nodes)):
        # add latitude and longitude as an attribute to each node, in the format of a tuple
        new_g.add_node(l_nodes[j], pos = g.nodes[l_nodes[j]]['pos'][::-1] )
            
    for i in range(len(l_nodes)):
        adj_mat = adj_matrix_task2(g, l_nodes)
        current_node = i
        path = [l_nodes[current_node]]

        for _ in range(len(l_nodes) - 1):

            adj_mat[:, current_node] = float('inf')

            next_node = np.where(adj_mat[current_node] == min(adj_mat[current_node]))[0][0]

            current_node = next_node
            path.append(l_nodes[current_node])
            
        c_node = path[0]
        for n_node in path[1:]:
            if not new_g.get_edge_data(c_node, n_node):
                weight = dijkstra(g, c_node, n_node, mode)
                new_g.add_edge(c_node, n_node, path = weight[0], dist = weight[1])
            c_node = n_node
    return new_g

def func_2(g, v, typ):
    s = graph_task2(g,v,typ)
    
    edges = list(s.edges())
    we = [s.edges[d]['dist'] for d in s.edges()]
    
    nodes = []
    for e in edges:
        nodes.append(e[0])
        nodes.append(e[1])
    nodes = list(set(nodes))   
    
    # for the Kruskal algorithm we need to sort the weights and according that also the list of edges
    n_we = sorted(we)
    n_edges = [None]*len(we)
    for i in range(len(n_we)):
        for j in range(len(we)):
            if n_we[i] == we[j]:
                n_edges[i] = edges[j]
    edges = n_edges    
    
    # Kruskal algorithm
    # list that will contain the mst edges
    mste = []
    # the trees dictionary
    f = {}
    j = 0
    # at the beginning every node is a tree
    for i in v:
        f[j] = [i]
        j += 1
    mod_v = len(v)
    # a mst has |V| - 1 edges, so we loop until this condition is verified
    while len(mste) != mod_v - 1:
        # at every loop we pick one edge from the sorted edges list and delete it, if that edge
        # connects 2 different trees then we add it in mste, otherwise just delete it
        e = edges[0]
        edges.pop(0)
        # to check if an edge connects 2 different trees we need to find the trees that contains
        # that edge's nodes

        # here we check the tree i and j, that contain the vertices of the edge
        for key in f:
            if e[0] in f[key]:
                i = key
        for key in f:
            if e[1] in f[key]:
                j = key  
        # if the trees are different then we join them
        if i!=j:
            f[i] = f[i] + f[j]
            mste.append(e)
            del f[j]
            
    edges = []
    for e in mste:
        tmp = s.edges[e]['path']
        for i in range(len(tmp)-1):
            edges.append((tmp[i],tmp[i+1]))   

    p = g.nodes[v[0]]['pos']
    m = folium.Map(location = [p[1], p[0]], zoom_start = 12 )
    for n in v:
        p = g.nodes[n]['pos']
        folium.CircleMarker(location = [p[1], p[0]], radius = 10,color = "red",
                            popup = "Input Node", fill = True).add_to(m)
     

    for e in edges:
        folium.PolyLine(locations = [(g.nodes[e[0]]['pos'][1],g.nodes[e[0]]['pos'][0]),
                                     (g.nodes[e[1]]['pos'][1],g.nodes[e[1]]['pos'][0])], 
                    line_opacity = 0.5, color = 'red').add_to(m)



    return(m)
