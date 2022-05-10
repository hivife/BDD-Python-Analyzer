# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:09:26 2022

@author: Tim
"""

import matplotlib.pyplot as plt
import csv




def return_list_attribute(attribute,csvFile):
	  result = []
	  counter = 0
	  for lines in csvFile:
		    counter +=1
		    if(len(lines) != 0):
			    if(lines[0] == attribute):
				    value = lines[1].split(" ",2)
				    
				    result.append(float(value[0]))
				    
	  print(counter)
	  result.sort()
	  return result


# code data
with open('results/code_data_incomplete - Kopie.csv', 'r')as file:
   
  # reading the CSV file
  csvFile = csv.reader(file)

  edge_list = return_list_attribute("Number of reachable states",csvFile)


file.close()
  

# bdd data
with open('results/output.csv', 'r')as file:
  csvFile = csv.reader(file)
  clustering_list = return_list_attribute("Characteristic path length",csvFile)
  print(edge_list)
  print(clustering_list)
  
  
plt.plot(edge_list, clustering_list)
plt.xlabel('Number of reachable states')
plt.ylabel('Characteristic path length')
#plt.xlim(1000,10000)
plt.xscale('log')

