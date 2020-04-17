import sys
from func_3 import shortest_ordered_route, viz_map
from func_4 import app_short
import networkx as nx
import folium
import webbrowser
from func_1 import func_1
from func_2 import func_2
import time
from get_data import get_data


def main(argv):
	functionality = argv[1]

	if functionality == '1':
		start = int(input("Chose the starting node: "))

		methods = ['distance', 'time', 'network']
		print("Choose a measure metod between: distance, time, network")
		mode = input("Insert measure method: ")

		while mode not in methods:
			print("Invalid measure method")
			print("It should be one of: distance, time, network")
			mode = input("Insert measure method: ")

		distance = float(input("Insert the distance threshold (float or int): "))

		t = time.time()

		G = nx.read_gpickle("complete_graph_di.gpickle.gz")

		m = func_1(G, start, distance, mode)

		m.save(outfile = "func_1_map.html")
		webbrowser.open("func_1_map.html", new = 2)

		print("Elapsed time: ", time.time() - t)

	elif functionality == '2':

		print("Now you will give a set of nodes one by one")
		print("The last will be the destination")
		print("The nodes should be between 1 and 1890815")

		path = set()

		n = input("Insert a node (type STOP when done): ")

		while(n != "STOP"):

			if int(n) < 1 or int(n) > 1890815:
				print("Invalid node, it should be between 1 and 1890815")
				continue

			path.add(int(n))

			n = input("Insert a node (type STOP when done): ")

		methods = ['distance', 'time', 'network']
		print("Choose a measure metod between: distance, time, network")

		mode = input("Insert measure method: ")

		while mode not in methods:
			print("Invalid measure method")
			print("It should be one of: distance, time, network")
			mode = input("Insert measure method: ")

		t = time.time()

		G = nx.read_gpickle("complete_graph_di.gpickle.gz")

		m = func_2(G, list(path), mode)

		m.save(outfile = "func_2_map.html")
		webbrowser.open("func_2_map.html", new = 2)

		print("Elapsed time: ", time.time() - t)





	elif functionality == '3':
		start = int(input("Chose the starting node: "))

		print("Now you will give a list of nodes one by one")
		print("The last will be the destination")
		print("The nodes should be between 1 and 1890815")

		path = []

		n = input("Insert a node (type STOP when done): ")

		while(n != "STOP"):

			if int(n) < 1 or int(n) > 1890815:
				print("Invalid node, it should be between 1 and 1890815")

			path.append(int(n))

			n = input("Insert a node (type STOP when done): ")

		if len(path) == 0:
			print("No destination")
			return

		methods = ['distance', 'time', 'network']
		print("Choose a measure metod between: distance, time, network")

		mode = input("Insert measure method: ")

		while mode not in methods:
			print("Invalid measure method")
			print("It should be one of: distance, time, network")
			mode = input("Insert measure method: ")

		t = time.time()

		G = nx.read_gpickle("complete_graph_di.gpickle.gz")

		shortest_path = shortest_ordered_route(G, start, path, mode)

		print("Total distance:", shortest_path[2])

		m = viz_map(G, shortest_path[1], shortest_path[0])

		m.save(outfile = "func_3_map.html")
		webbrowser.open("func_3_map.html", new = 2)

		print("Elapsed time: ", time.time() - t)

	elif functionality == '4':
		start = int(input("Chose the starting node: "))

		print("Now you will give a list of nodes one by one")
		print("The last will be the destination")
		print("The nodes should be between 1 and 1890815")

		path = set()

		n = input("Insert a node (type STOP when done): ")

		while(n != "STOP"):

			if int(n) < 1 or int(n) > 1890815:
				print("Invalid node, it should be between 1 and 1890815")
				continue

			path.add(int(n))

			n = input("Insert a node (type STOP when done): ")

		if len(path) == 0:
			print("No destination")
			return

		methods = ['distance', 'time', 'network']
		print("Choose a measure metod between: distance, time, network")

		mode = input("Insert measure method: ")

		while mode not in methods:
			print("Invalid measure method")
			print("It should be one of: distance, time, network")
			mode = input("Insert measure method: ")

		t = time.time()

		G = nx.read_gpickle("complete_graph_di.gpickle.gz")

		all_nodes = [start]
		all_nodes.extend(list(path))

		s_path = app_short(G, all_nodes)

		shortest_path = shortest_ordered_route(G, s_path[0], s_path[1:], mode)

		print("Total distance:", shortest_path[2])

		m = viz_map(G, shortest_path[1], shortest_path[0])

		m.save(outfile = "func_4_map.html")
		webbrowser.open("func_4_map.html", new = 2)

		print("Elapsed time: ", time.time() - t)



if __name__ == "__main__":

	d = input("Do you already have the data? (yes or no): ")
	if d == 'no':
		get_data()



	main(sys.argv)
