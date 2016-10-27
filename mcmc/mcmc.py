import sys
import os
#make sure the program can be executable from test file
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(dir_root)

import numpy as np
import math as mt
import networkx as nx
import copy
import operator
import ast
import matplotlib.pyplot as plt
from edge_oper import edge_oper
from posi_assign import posi_assign
from theta import theta
from graph import connec_graph
from Metripolis_Hastings import Metripolis_Hastings
from plot_graph import plot_graph




###the main program: Metripolis Hastings Algorithm
# parameters:
# Time_points : the total time points
# T : constant
# r : constant
# N : the number of vertexs
# Dx: the dimension of the 2D grid along x direction
# Dy: the dimension of the 2D grid along y direction
# Lx: the length of 2D grid along x direction
# Ly: the length of 2D grid along y direction
# Req1: N is equal or smaller than D^2
Time_points = 20000
T = 10
r = 5
N = 5
Dx = 5
Dy = 5
Lx = 1
Ly = 1

#create a list storing every graphs at every time points

G = [None] * Time_points

#initialize the first graph at time=0

G[0] = nx.Graph()
connec_graph(N, G[0]).init_graph()

#the parameters being keep constant throught the whole project
posi = posi_assign(N, Dx, Dy, Lx, Ly)  # unifromly distributed random posi array
#or you can use a stationary position array 
posi = np.array([[ 0. ,   0.25],[ 0.15 , 0.  ],[ 0.25 , 0.75],[ 0.75 , 1.  ],[ 0.5 ,  0.5 ]])

weight = edge_oper(N, posi, G[0]).weight_calc()

#the theta value at time = 0
edge_weighted_list_o = edge_oper(N, posi, G[0]).edges_weighted(weight)
Xi = copy.deepcopy(G[0])
theta_o = theta(r, N, Xi, edge_weighted_list_o, weight)
edges_keep_num_o, edges_keep_list_o = connec_graph(N, Xi).edges_keep()


#need to store the attribution of current graph to the reference graph
R = copy.deepcopy(Xi)

#calculate the transition probability from X(i) to potential X(j), here, from X(0) to potential X(1)
qij = 1 / (N * (N - 1) / 2 - edges_keep_num_o)


#create a dic storing the string of edges list of the graph as the key and the appearance time in the time sequence  as the corresponding value
num_appearance_dic = {}
#create a numpy array storing all the number of edges connected to vertex 0 
num_edges_tozero_arry = np.empty(Time_points)
#create a numpy array storing all the number of edges in the entire graph
num_edges_arry = np.empty(Time_points)
#create a numpy array storing all the maximum distance of the shortest path in a graph that connects vertex 0 to another vertex
shortest_path_max_arry = np.empty(Time_points)

#put the G[0] edges list into the dic
G_str = ','.join(str(e) for e in G[0].edges())
return_value = num_appearance_dic.setdefault(G_str, 1)

#the numer of edges connected to vertex 0 for G[0]
num_edges_tozero_arry[0] = G[0].degree(0)

#the number of edges in the entire graph for G[0]
num_edges_arry[0] = G[0].number_of_edges()

#the maximum distance of the shortest path in a graph that connects vertex 0 to another vertex for G[0]
length = nx.shortest_path_length(G[0], 0, weight='weight')
length_sort = sorted(length.items(), key=operator.itemgetter(1), reverse = True)
shortest_path_max_arry[0] = length_sort[0][1]


#applying Metripolis-Hastings Algorithm

edges_keep_list_i = edges_keep_list_o
theta_i = theta_o

for ii in range(1, Time_points):

    G[ii], accept_j, edges_keep_update_j, edge_gene_j, edges_keep_list_j, qji, theta_j = Metripolis_Hastings(r, T, N, posi, weight, Xi, R, edges_keep_list_i, qij, theta_i)
    # reassign the parameters for the next run
    Xi = copy.deepcopy(G[ii])
    R = copy.deepcopy(Xi)
    edges_keep_list_i = edges_keep_list_j
    qij = qji
    theta_i = theta_j
    edge_oper(N, posi, G[ii]).edges_weighted(weight)

    #add the graph edges as a new key into dic if it is not exist in the dictionary
    G_str = ','.join(str(e) for e in G[ii].edges())
    return_value = num_appearance_dic.setdefault(G_str)
    if return_value != None:
        num_appearance_dic[G_str] = num_appearance_dic[G_str] + 1
    else:
        num_appearance_dic[G_str] = 1
    #the numer of edges connected to vertex 0
    num_edges_tozero_arry[ii] = G[ii].degree(0)

    #the number of edges in the entire graph
    num_edges_arry[ii] = G[ii].number_of_edges()
    
    #the maximum distance of the shortest path in a graph that connects vertex 0 to another vertex
    length = nx.shortest_path_length(G[ii], 0, weight='weight')
    length_sort = sorted(length.items(), key=operator.itemgetter(1), reverse = True)
    shortest_path_max_arry[ii] = length_sort[0][1]


#ploting the first num graphs
#num = 1
#for ii in range(num):
#    plot_graph(G, N, ii, posi)


#answering the questions mentioned in the note
#because we are under the ergodic condition, the expectation value can be calculate by 
#E(h(x)) = 1/N*Sum(h(xi)) *summing over the time sequece

#Problem 1: we can pick the key corresponding to the maximum value in the dic which is the most possible graph during the whole simulation
num_appearance_dic_sort = sorted(num_appearance_dic.items(), key=operator.itemgetter(1), reverse = True)
##most_possible_graph_edges 
A1 = num_appearance_dic_sort[0][0]
##convert it to the standard edges list which can be used to plot graph later
A1 = ast.literal_eval(A1)
A1 = list(A1)
##plot it out
### create a graph named A
A = [None] * 1
A[0] = nx.Graph()
A[0].add_edges_from(A1)
###weight it first
edge_oper(N, posi, A[0]).edges_weighted(weight)
###plot it
plot_graph(A, N, 0, posi)

#Problem2 : the expected number of edges connected to vertex 0
E2 = np.sum(num_edges_tozero_arry)/Time_points

#Problem3 : the expected number of edges in the entire graph
E3 = np.sum(num_edges_arry)/Time_points

#Problem4 : the expected maximum distance of the shortest path in a graph that connects vertex 0 to another vertex
E4 = np.sum(shortest_path_max_arry)/Time_points

print('problem1:',A1,'\n','problem2:',E2,'\n','problem3:',E3,'\n','problem4:', E4)

#plt.axis('on') #for displaying using
#plt.show() # display
