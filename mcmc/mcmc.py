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
Time_points = 200
T = 10
r = 5
N = 5
Dx = 5
Dy = 5
Lx = 1
Ly = 1
import sys
sys.path.append('../mcmc')

import numpy as np
import math as mt
import networkx as nx
import copy
import matplotlib.pyplot as plt
from mcmc.edge_oper import edge_oper
from mcmc.posi_assign import posi_assign
from mcmc.theta import theta
from mcmc.graph import connec_graph
from mcmc.Metripolis_Hastings import Metripolis_Hastings
from mcmc.plot_graph import plot_graph



#create a list storing every graphs at every time points

G = [None] * Time_points

#initialize the first graph at time=0

G[0] = nx.Graph()
connec_graph(N, G[0]).init_graph()

#the parameters being keep constant throught the whole project
posi = posi_assign(N, Dx, Dy, Lx, Ly)
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

#applying Metripolis-Hastings Algorithm

edges_keep_list_i = edges_keep_list_o
theta_i = theta_o

for ii in range(1, Time_points):
    G[ii], accept_j, edges_keep_update_j, edge_gene_j, edges_keep_list_j, qji, theta_j = Metripolis_Hastings(r, T, N, posi, weight, Xi, R, edges_keep_list_i, qij, theta_i)
    Xi = copy.deepcopy(G[ii])
    R = copy.deepcopy(Xi)
    edges_keep_list_i = edges_keep_list_j
    qij = qji
    theta_i = theta_j
    edge_oper(N, posi, G[ii]).edges_weighted(weight)

#ploting the first num graphs
num = 1
for ii in range(num):
    plot_graph(G, N, ii, posi)
plt.axis('on')
#plt.show() # display
