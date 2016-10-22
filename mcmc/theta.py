#r: constant
#N: the number of vertexs
#edges_list: should be sorted in advance
#G: the graph

import networkx as nx

def theta(r, N, G, edges_list_weighted, weight):
    first_term = 0
    for ii in range(G.number_of_edges()):
        row_ind = edges_list_weighted[ii][0] 
        col_ind = edges_list_weighted[ii][1]
        add = weight[row_ind][col_ind]
        first_term = first_term + add
    first_term = r * first_term
    
    #only count the shortest path for each nodes pair
    second_term = 0
    length = nx.shortest_path_length(G, 0, weight='weight')
    for ii in range(N):
        second_term = second_term + float(length[ii])
    theta = first_term + second_term

    return theta
