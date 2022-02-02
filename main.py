# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:25:03 2022

@author: Tim
"""

import networkx as nx
import re
import os




# functions

def read_gv_file(file_path):
	bdd = nx.Graph()
	file = open(file_path)
	for line in file:
		line_is_edge = re.search("^\".+\" -> \".+\"(;| \[style = dashed\];| \[style = solid\];)$",line)
		line_is_label_true = re.search("^\".+\" \[label = \"TRUE\"\];$",line)
		line_is_label_false = re.search("^\".+\" \[label = \"FALSE\"\];$",line)
		if(line_is_edge):
			#print(line)
			first_node = 0
			second_node = 0
			edge_weight = 1
			nodes = line.split("->")
			first_node = nodes[0].replace(" ","")
			first_node = first_node.replace("\"","")
			second_node = nodes[1]
			if("style = dashed" in second_node):
				edge_weight = 0
			second_node = second_node.replace("[style = dashed];","")
			second_node = second_node.replace("[style = solid];","")
			second_node = second_node.replace(" ","")
			second_node = second_node.replace("\"","")
			second_node = second_node.replace(";","")
			second_node = second_node.strip()
			#print(first_node)
			#print(second_node)
			#print(edge_weight)
			bdd.add_edge(first_node,second_node,weight = edge_weight)
			
		if(line_is_label_true):
			nodes = line.split(" ")
			first_node = nodes[0].replace(" ","")
			bdd.output_node_true = first_node
		if(line_is_label_false):
			nodes = line.split(" ")
			first_node = nodes[0].replace(" ","")
			bdd.output_node_false = first_node
	
	
	file.close()
	bdd.root_node = "Trans"
	return bdd



def print_results(result , output_file , path):
	file = open(output_file , "w")
	file.write(path + "\n")
	for entry in result:
		file.write(str(entry))
		file.write("\n")
	
	
	file.close()
	print(result)



def analyze_bdd(bdd):
	result = []
	result.append(("Number of edges:",bdd.number_of_edges()))
	result.append(("Number of nodes:",bdd.number_of_nodes()))
	result.append(("root:",bdd.root_node))
	result.append(("Output node false:",bdd.output_node_false))
	result.append(("Output node true:",bdd.output_node_true))
	result.append(("Average clustering:",nx.average_clustering(bdd)))
	result.append(("Maximal Cliques:",nx.graph_number_of_cliques(bdd)))
	#result.append(("Small-world coefficient:",nx.omega(bdd)))
	#result.append(("Gerneralized Degree:",nx.generalized_degree(bdd)))
	return result




#main

input_folder = "data/"
output_file = "output.txt"

#for folder in os.listdir(input_folder):
	#print(os.listdir(input_folder + folder))
	

path = "bmc_tutorial.gv"
#path = "data/brp/brp.gv"

current_bdd = read_gv_file(path)


result_list = analyze_bdd(current_bdd)


print_results(result_list,output_file,path) 

print(list(current_bdd.nodes))












