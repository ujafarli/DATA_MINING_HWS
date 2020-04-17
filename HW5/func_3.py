# modified Fibonacci_Heap_Mod
# We modified it to keep track of the  nodes
from fibonacci_heap import Fibonacci_heap
import folium
import webbrowser



# get the weight from the graph
# with a given modality
def get_weight(graph, node, next_node, mode):
    if mode == 'network':
        return 1
    elif mode == 'time':
        return graph.get_edge_data(node, next_node)['time']
    elif mode == 'distance':
        return graph.get_edge_data(node, next_node)['distance']


# Calculates the shortest path between two nodes
def dijkstra(graph, start, dest, mode):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    # initialize it with the initial node and set it with wight 0
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()
    
    # create a fibonacci heap and store the nodes
    # ordered by currend wight
    heap = Fibonacci_heap()
    
    while current_node != dest:
        # Add current node to the set of visited nodes
        visited.add(current_node)
        # adjacency list, take all edges from the current node
        destinations = [elem[1] for elem in graph.edges(current_node)]
        # take the total weight
        weight_to_current_node = shortest_paths[current_node][1]

        # visit all nodes connected to the current node
        for next_node in destinations:
            # calculate the weight of the current edge
            # weight of the edge + weight of edges previously visited in the path
            weight = get_weight(graph, current_node, next_node, mode) + weight_to_current_node
            
            # add nodes to the heap
            if next_node not in visited and next_node not in heap.nodes:
                heap.enqueue(next_node, weight)
            
            # add new node in shortest path
            # or update it if current path is shorter of previous path
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        # if heap is empty we cannot continue
        # and we cannot reach the destination
        
        if not heap.__bool__():
            return "Not Possible"
        
        # update current_node
        # next node is the destination with the lowest weight
        current_node = heap.dequeue_min().m_elem
    
    # Work back through destinations in shortest path
    # create path and reverse it
    path = []
    while current_node is not None:
        path.append(current_node)
        # take previous node from the dict
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return (path, shortest_paths[path[-1]][1])



# takes in input the starting node
# and then visit in order the list route
def shortest_ordered_route(graph, start, route, mode):
    if len(route) < 1:
        print("Insert at least 1 node")
        return

    all_route = []
    all_route.extend([start])
    all_route.extend(route)

    total = 0
    path = [start]
    for elem in route:
        tmp = dijkstra(graph, start, elem, mode)
        total += tmp[1]
        path.extend(tmp[0][1:])
        start = elem
    return (path, all_route, total)



def viz_map(graph, route, steps):
    m = folium.Map(location=(graph.node[1]['pos'][::-1]), zoom_start=13,tiles='openstreetmap')
    
    #add lines
    folium.PolyLine([graph.node[elem]['pos'][::-1] for elem in steps], color="red", weight=2.5, opacity=1).add_to(m)
    
    for loc in steps:
        if loc in route:
            folium.CircleMarker(location=graph.node[loc]['pos'][::-1], radius=10, line_color='#3186cc',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
        else:
            folium.CircleMarker(location=graph.node[loc]['pos'][::-1], radius=1, line_color='#3186cc',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
    
    return m







# Just for fun

def bi_dijkstra(graph, start, dest, mode):
    m = folium.Map(location=(G.node[1]['pos'][::-1]), zoom_start=13,tiles='openstreetmap')
    
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    # initialize it with the initial node and set it with wight 0
    shortest_paths_start = {start: (None, 0)}
    current_node_start = start
    visited_start = set()
    
    shortest_paths_dest = {dest: (None, 0)}
    current_node_dest = dest
    visited_dest = set()
    
    # create a heap and store the nodes
    # ordered by currend wight
    # heap = []
    heap_start = Fibonacci_heap()
    
    heap_dest = Fibonacci_heap()
    
    folium.CircleMarker(location=G.node[current_node_start]['pos'][::-1], radius=10, line_color='#3186cc',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
    folium.CircleMarker(location=G.node[current_node_dest]['pos'][::-1], radius=10, line_color='#3186cc',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
    
    
    try:
        while True:
            
            # Add current node to the set of visited nodes
            visited_start.add(current_node_start)
            visited_dest.add(current_node_dest)
            #folium.CircleMarker(location=G.node[current_node_start]['pos'][::-1], radius=1, line_color='#3186cc',
             #       fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)
            folium.CircleMarker(location=G.node[current_node_dest]['pos'][::-1], radius=1, line_color='#3186cc',
                    fill_color='#000000',fill_opacity=0.7, fill=True).add_to(m)

            # adjacency list, take all edges from the current node
            destinations_start = [elem[1] for elem in graph.edges(current_node_start)]
            destinations_dest = [elem[1] for elem in graph.edges(current_node_dest)]
            # take the total weight
            weight_to_current_node_start = shortest_paths_start[current_node_start][1]
            weight_to_current_node_dest = shortest_paths_dest[current_node_dest][1]

            # visit all nodes connected to the current node
            for next_node in destinations_start:
                # test for bidirectional
                if next_node in visited_dest:
                    current_node_dest = next_node
                    raise StopIteration

                # calculate the weight of the current edge
                # weight of the edge + weight of edges previously visited in the path
                weight = get_weight(graph, current_node_start, next_node, mode) + weight_to_current_node_start

                # add nodes to the heap
                if next_node not in visited_start and next_node not in heap_start.nodes:
                    #heappush(heap, (weight, next_node))
                    heap_start.enqueue(next_node, weight)

                # add new node in shortest path
                # or update it if current path is shorter of previous path
                if next_node not in shortest_paths_start:
                    shortest_paths_start[next_node] = (current_node_start, weight)
                else:
                    current_shortest_weight = shortest_paths_start[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths_start[next_node] = (current_node_start, weight)

            # visit all nodes connected to the current node
            for next_node in destinations_dest:
                # test for bidirectional
                if next_node in visited_start:
                    current_node_start = next_node
                    raise StopIteration

                # calculate the weight of the current edge
                # weight of the edge + weight of edges previously visited in the path
                weight = get_weight(graph, current_node_dest, next_node, mode) + weight_to_current_node_dest

                # add nodes to the heap
                if next_node not in visited_dest and next_node not in heap_dest.nodes:
                    #heappush(heap, (weight, next_node))
                    heap_dest.enqueue(next_node, weight)

                # add new node in shortest path
                # or update it if current path is shorter of previous path
                if next_node not in shortest_paths_dest:
                    shortest_paths_dest[next_node] = (current_node_dest, weight)
                else:
                    current_shortest_weight = shortest_paths_dest[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths_dest[next_node] = (current_node_dest, weight)
        
            # if heap is empty we cannot continue
            # and we cannot reach the destination
            #if len(heap) == 0:
             #   return "Not Possible"

            if not heap_start.__bool__():
                return "Not Possible"
            if not heap_dest.__bool__():
                return "Not Possible"

            # update current_node
            # next node is the destination with the lowest weight
            #current_node = heappop(heap)[1]
            current_node_start = heap_start.dequeue_min().m_elem
            current_node_dest = heap_dest.dequeue_min().m_elem
    
    except StopIteration:
        pass
    
    supp_weight = get_weight(graph, current_node_start, current_node_dest, mode)
    start_weight = shortest_paths_start[current_node_start][1]
    dest_weight = shortest_paths_dest[current_node_dest][1]
    # Work back through destinations in shortest path
    # create path and reverse it
    path = []
    while current_node_start is not None:
        path.append(current_node_start)
        # take previous node from the dict
        next_node = shortest_paths_start[current_node_start][0]
        current_node_start = next_node
    # Reverse path
    path = path[::-1]
    
    print(len(path))
    
    while current_node_dest is not None:
        path.append(current_node_dest)
        # take previous node from the dict
        next_node = shortest_paths_dest[current_node_dest][0]
        current_node_dest = next_node
    
    display(m)
    
    return (path, supp_weight + start_weight + dest_weight)