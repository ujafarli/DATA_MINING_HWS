import networkx as nx


def get_data():

	path1 = input("Insert path to USA-road-d.CAL.co: ")
	path2 = input("Insert path to USA-road-d.CAL.gr: ")
	path3 = input("Insert path to USA-road-t.CAL.gr: ")

	with open(path1,'r',newline = '\n') as file:
	    nodes = file.readlines()
	with open(path2,'r',newline = '\n') as file:
	    dis_m = file.readlines()
	with open(path3,'r',newline = '\n') as file:
	    dis_t = file.readlines()


	# data cleaning

	# the first 6 lines are descriptions of the data
	nodes = nodes[7:]
	dis_m = dis_m[7:]
	dis_t = dis_t[7:]

	# From the nodes file, we keep only the latitude and longitude of each node.


	for i in range(len(nodes)):
	    nodes[i] = nodes[i][:-1]
	    nodes[i] = list(nodes[i].split())[2:]

	# Latitude and longitude of each node are strings without float point (e.g ''-114318765''). 
	# Since we know that longitude and latitude of California and Nevada go from 32.5-42.0 and 114.0 - 125.0 respectively, 
	# we want to convert that string into a float number in the format : -114.318765. 

	for i in range(len(nodes)):
	    # just add the comma after the third or second digit
	    nodes[i][0] = float(nodes[i][0][0:4]+'.'+nodes[i][0][4:])
	    nodes[i][1] = float(nodes[i][1][0:2]+'.'+nodes[i][1][2:])

	# Clean data in the same way but for edges

	# every row is in the format, 'starting node' \t 'ending node' \t ' distance'
	for i in range(len(dis_m)):
	    dis_m[i] = dis_m[i][1:]
	    dis_t[i] = dis_t[i][1:]
	    dis_m[i] = dis_m[i][:-1]
	    dis_t[i] = dis_t[i][:-1]    
	    dis_m[i] = dis_m[i].split()
	    dis_t[i] = dis_t[i].split()

	g = nx.DiGraph()
	# add nodes
	for i in range(len(nodes)):
	    # add latitude and longitude as an attribute to each node, in the format of a tuple
	    g.add_node(i+1, pos = (nodes[i][0], nodes[i][1]) )
	# add edges with spatial distance only, if you want with time distance then just change to dis_t
	for i in range(len(dis_m)):
	    # not every row of dis_m has numbers as entries, there can also be missing values or just
	    # wrong values. For this reason we use 'try'
	    try:
	        if (int(dis_m[i][0]) in g.nodes() and int(dis_m[i][1]) in g.nodes()): 
	            # add as attribute to every edge the distance
	            g.add_edge(int(dis_m[i][0]), int(dis_m[i][1]), distance = float(dis_m[i][2]),
	                                                                        time = float(dis_t[i][2]))
	    except Exception as e:
	        print(i, e)
	        continue


	nodes = []
	dis_m = []
	dis_t = []

	nx.write_gpickle(g, "complete_graph_di.gpickle.gz")

