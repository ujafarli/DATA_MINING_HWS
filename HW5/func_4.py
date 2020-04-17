import numpy as np
import math



# create an adjacency matrix used to calculate the shortest path
def adj_matrix(graph, l):
    adj_mat = np.zeros((len(l), len(l)))
    i = 0
    for elem in l:
        for j in range(len(l)):
            x1 = graph.node[elem]['pos'][::-1][0]
            y1 = graph.node[elem]['pos'][::-1][1]
            x2 = graph.node[l[j]]['pos'][::-1][0]
            y2 = graph.node[l[j]]['pos'][::-1][1]
            if j == len(l) - 1:
                adj_mat[i][j] = 9999999999999999
            else:
                adj_mat[i][j] = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        i = i + 1
    return adj_mat



# heuristic function
# Function that compute the 
def app_short(graph, l_nodes):
    
    adj_mat = adj_matrix(graph, l_nodes)

    current_node = 0
    path = [l_nodes[current_node]]
    
    for _ in range(len(l_nodes) - 1):
        
        adj_mat[:, current_node] = float('inf')
        
        next_node = np.where(adj_mat[current_node] == min(adj_mat[current_node]))[0][0]
        
        current_node = next_node
        path.append(l_nodes[current_node])
        
    return path