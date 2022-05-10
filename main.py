# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:25:03 2022

@author: Tim
"""

import networkx as nx
import re
import os
import csv




# functions

def read_gv_file(file_path):
	print("reading file")
	bdd = nx.DiGraph()
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
			first_node = nodes[0].replace("\"","")
			bdd.output_node_true = first_node
		if(line_is_label_false):
			nodes = line.split(" ")
			first_node = nodes[0].replace(" ","")
			first_node = nodes[0].replace("\"","")
			bdd.output_node_false = first_node
	
	
	file.close()
	bdd.root_node = "Trans"
	return bdd



def print_results(result , output_file , path):
	file = open(output_file , "a")
	#file.write(path + "\n")
	#for entry in result:
	#	file.write(str(entry))
	#	file.write("\n")
	csv.writer(file).writerow(("file",path))
	for entry in result:
		csv.writer(file).writerow(entry)
		#file.write("\n")
	
	
	
	
	
	file.close()
	#print(result)



def analyze_bdd(bdd):
	result = []
	
	
	# General Information
	
	print("processing general information")
	result.append(("Number of edges",bdd.number_of_edges()))
	result.append(("Number of nodes",bdd.number_of_nodes()))
	#result.append(("Root node",bdd.root_node))
	#result.append(("Output node false",bdd.output_node_false))
	#result.append(("Output node true",bdd.output_node_true))
	
	
	# Clustering
	print("processing cluster information")
	result.append(("Average clustering",nx.average_clustering(bdd)))
	#result.append(("Maximal Cliques",nx.graph_number_of_cliques(bdd)))
	#result.append(("Gerneralized Degree",nx.generalized_degree(bdd)))
	

	temp = centrality_helper_function(nx.betweenness_centrality(bdd))
	max_value = temp[0]
	avg_value = temp[1]
	result.append(("Betweenness centrality max. value",max_value))
	result.append(("Betweenness centrality avg. value",avg_value))
	
	temp = centrality_helper_function(nx.closeness_centrality(bdd))
	max_value = temp[0]
	avg_value = temp[1]
	result.append(("Closeness centrality max. value",max_value))
	result.append(("Closeness centrality avg. value",avg_value))
	
	temp = centrality_helper_function(nx.degree_centrality(bdd))
	max_value = temp[0]
	avg_value = temp[1]
	result.append(("Degree centrality max. value",max_value))
	result.append(("Degree centrality avg. value",avg_value))
	
	#print(nx.betweenness_centrality(bdd))
	#print(nx.closeness_centrality(bdd))
	#print(nx.degree_centrality(bdd))
	
	
	

	#print(nx.k_core(bdd,3).size())
	
	

	#paths
	print("processing path information")
# 	all_paths_false = nx.all_simple_edge_paths(bdd, bdd.root_node, bdd.output_node_false)
# 	false_counter = 0
# 	sum_false = 0
# 	longest_path_false = 0
# 	for path in all_paths_false:
#  			path_length = len(path)
#  			sum_false += path_length
#  			false_counter += 1
#  			if(longest_path_false < path_length): longest_path_false = path_length
 			
# 	all_paths_true = nx.all_simple_edge_paths(bdd, bdd.root_node , bdd.output_node_true)
# 	true_counter = 0
# 	sum_true = 0
# 	longest_path_true = 0
# 	for path in all_paths_true:
#  			path_length = len(path)
#  			sum_true += path_length
#  			true_counter += 1
#  			if(longest_path_true < path_length): longest_path_true = path_length
 			
# 	characteristic_path_length = (sum_false + sum_true) / (true_counter + false_counter)
# 	characteristic_path_length_false = sum_true / true_counter
# 	characteristic_path_length_true = sum_false  /  false_counter
	tf= {bdd.output_node_false,bdd.output_node_true}
	visited=set()
	all_paths = return_all_path_length(bdd,visited, "Trans", [], tf, 0)
	true_counter = 0
	sum_true = 0
	false_counter = 0
	sum_false = 0
	longest_path_false = 0
	longest_path_true = 0

	for value in all_paths:
		if value[1]== bdd.output_node_true:
			sum_true+=value[0]
			true_counter+=1
			if(longest_path_true < value[0]): longest_path_true = value[0]
		else:
			sum_false+=value[0]
			false_counter+=1
			if(longest_path_false < value[0]): longest_path_false = value[0]
	
	characteristic_path_length = (sum_false + sum_true) / (true_counter + false_counter)
	characteristic_path_length_false = sum_true / true_counter
	characteristic_path_length_true = sum_false  /  false_counter
	
	result.append(("Characteristic path length",characteristic_path_length))	
	result.append(("Characteristic path length for output false",characteristic_path_length_false))
	result.append(("Characteristic path length for output true",characteristic_path_length_true))
	result.append(("Number of paths from root to output true",true_counter))	
	result.append(("Number of paths from root to output false",false_counter))	
	result.append(("Number of paths from root to any output",true_counter + false_counter))	
	result.append(("Longest path from root to true",longest_path_true))	
	result.append(("Longest path from root to false",longest_path_false))	
 	 	
	#result.append(("Small-world coefficient",nx.omega(bdd)))
 
	return result



def centrality_helper_function(input_list):
	values = input_list
	max_value = 0
	avg_value = 0
	sum = 0
	
	for node in values:
		current_value = values[node]
		if(current_value > max_value):
			max_value =  current_value
		sum += current_value
		
	avg_value = sum / len(values)
	
	return (max_value,avg_value)

def return_all_path_length(bdd,visited,node,path_length,tf,depth):
	
	if node not in visited :
	        #print ("Node: " + node + " Depth: " + str(depth))
	        if node in tf:
	        	path_length.append((depth,node))
	        if node not in tf:
	        	visited.add(node)
	        depth+=1
	        for neighbour in bdd.edges(node):
	            
	            return_all_path_length(bdd,visited, neighbour[1],path_length,tf,depth)

	        return path_length
	




#main

input_folder = "data/"
output_file = "output.csv"
#path = "bmc_tutorial.gv
#path = "data/brp/brp.gv"


# clear file
f = open("output.csv","w")
f.close()

for folder in os.listdir(input_folder):
	for file in os.listdir(input_folder + folder):
		print("starting:" + input_folder + folder + "/" + file)
		path = input_folder + folder + "/" + file
		current_bdd = read_gv_file(path)
		result_list = analyze_bdd(current_bdd)
		print_results(result_list,output_file,path) 
		print("completed:" + input_folder + folder + "/" + file)
		pass
	
# visited = list()
# tf = {"5","6"}
#bdd= read_gv_file("data/smv-dist/periodic.gv")
# print(bdd.edges)
# print(return_all_path_length(bdd, "Trans", visited,tf,0))
#print(analyze_bdd(bdd))

#print(list(current_bdd.edges))