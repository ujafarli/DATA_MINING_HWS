import networkx as nx
import folium

def func_1(g, v, d, typ):
    '''
    "v" is the initial node and d is the distance threshold and type is the distance type: distance,
    temporal and network. The function returns a folium object.
    g is the graph
    '''

    # we are going to use a BFS algorithm with a distance

    # the visited list: if v[i] = True it means that the i-th node was visited by the algorithm
    vis = [False]*(len(g.nodes)+1)
    # this array will contain the distances of all visited nodes from the initial node "v"
    dist = [0]*(len(g.nodes)+1)

    # "q" is a queue
    q = []
    q.append(v)
    vis[v] = True

    '''
    Just standard BFS algorithm
    '''

    while q:
        s = q.pop()
        # neighbours of s
        n = [node for node in g[s]]
        for i in n:
            if vis[i] == False:
                if typ == "distance":
                    tmp = int(g.edges[(s,i)]['distance']) + dist[s]
                elif typ == "time":
                    tmp = int(g.edges[(s,i)]['time']) + dist[s]
                elif typ == "network":
                    tmp = 1 + dist[s]
                if tmp <= d:
                    q.append(i)
                    vis[i]=True
                    dist[i]=tmp 

    '''
    subgraph making
    '''                        
    neigh = []
    # check the vis array and when the value is True add it in the list
    for i in range(len(vis)):
        if vis[i]==True:
            neigh.append(i)
    # given the subset of nodes from neigh, here we get all edges that contain those nodes
    edges =  []
    for n in neigh:
        for m in neigh:
            if m in g[n] and (m,n) not in edges:
                edges.append((n,m))
                
    # subgraph making 
    subg = nx.Graph()
    # add nodes
    for x in neigh:
        subg.add_node(x)
    # add edges
    for x in edges:
        subg.add_edge(x[0], x[1]) 

    # visualization with folium
    p = g.nodes[v]['pos']
    m = folium.Map(location = [p[1], p[0]], zoom_start = 12 ) 
    folium.CircleMarker(location = [p[1], p[0]], radius = 10,color = "red",popup = "Starting Node", fill = True).add_to(m)
    for node in subg.nodes():
        if node != v:
            p = g.nodes[node]['pos']
            folium.CircleMarker(location = [p[1], p[0]], radius = 5,popup = "Node {}; distance from starting node {}".format(node,dist[node]) ,fill = True).add_to(m)

    for e in subg.edges():
        folium.PolyLine(locations = [(g.nodes[e[0]]['pos'][1],g.nodes[e[0]]['pos'][0]), (g.nodes[e[1]]['pos'][1],g.nodes[e[1]]['pos'][0])], 
                    line_opacity = 0.5).add_to(m)    
    
    return(m)