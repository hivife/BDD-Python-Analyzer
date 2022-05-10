# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:29:55 2022

@author: Tim
"""

import os
import main

def parse_file(filename):
	
	
	result = []
	
	
	file = open(filename)
	line_counter = 0
	module_counter = 0
	var_counter = 0
	trans_counter = 0
	state_counter = 0
	process_counter = 0
	var_mode = False
	trans_mode = False

	#print(file.read())
	#print(file.split("MODULE"))
	for l in file.readlines():
		if(not (l[0] == "-"  and l[1] == "-")):
			#print(l)
			line_counter = line_counter +1
			if(l.startswith(" ") and var_mode):
				var_counter = var_counter +1
			else:
				var_mode = False
			if(l.startswith(" ") and trans_mode):
				if(l.__contains__("->")):
					trans_counter = trans_counter +1
			else:
				trans_mode = False
			
			if(l.startswith('MODULE')):
				module_counter = module_counter +1
			if(l.startswith('TRANS')):
				trans_mode = True
			if(l.startswith('VAR')):
				var_mode = True
			
		
	result.append(("Number of lines of codes",line_counter))
	result.append(("Number of Modules",module_counter))
	result.append(("Number of processes",process_counter))
	result.append(("Number of transitions",trans_counter))
	result.append(("Number of variables",var_counter))
	result.append(("Number of states",state_counter))
	
	
	return result


input_folder = "example source codes/"
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
		result_list = parse_file(path)
		main.print_results(result_list,output_file,path) 
		print("completed:" + input_folder + folder + "/" + file)
		
		
		
		
		
		