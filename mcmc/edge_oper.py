#the class edge_oper including all the possible operations about the edges in the project
#N:the number of the vertex
#posi: the positions of every vertex
#G: the graph G = networkx.graph()

import numpy as np
import math as mt
import networkx as nx

class edge_oper():

    def __init__(self,N, posi, G):
        self.N = N
        self.posi = posi
        self.G = G
        self.edges_num = G.number_of_edges()
        self.edges_list = G.edges()
        self.vertex_list = G.nodes()
        #sorting the every edge in the edges_list making sure the start point is smaller than the end point


    def weight_calc(self):
        #create a 2D array for potential edge between different vertexs
        weight = np.empty([self.N,self.N])
        for ii in range(self.N):
            for jj in range(self.N):
                diffsqx = (self.posi[ii][0] - self.posi[jj][0]) ** 2
                diffsqy = (self.posi[ii][1] - self.posi[jj][1]) ** 2
                weight[ii][jj] = mt.sqrt(diffsqx + diffsqy)
        
        return weight
    
    def ran_edge(self):
        vertex_start_index = np.random.randint(0, self.N)
        vertex_start = self.vertex_list[vertex_start_index]

        vertex_ref = self.vertex_list.remove(self.vertex_list[vertex_start_index])
        vertex_end_index = np.random.randint(0, self.N - 1)
        vertex_end = self.vertex_list[vertex_end_index]

        #reverse the order if vertex_end is smaller than vertex_start
        edge_ref_unsort = (vertex_start, vertex_end)
        edge_gene = tuple(sorted(edge_ref_unsort))
        return edge_gene


####unidentified function: to estimate whether keeping the created edge or not
    def update_edges_list(self, edge_gene,edges_keep_list):
        edges_list_sorted = [None] * self.G.number_of_edges()
        for ii in range(self.G.number_of_edges()):
            edges_list_sorted[ii] = tuple(sorted(self.G.edges()[ii])) 
        keep = edge_gene in edges_keep_list
        exist = edge_gene in edges_list_sorted
        if exist ==True and keep == False:
            #if the edge created already existed and it is not in spanning tree, delet it
            self.G.remove_edge(edge_gene[0], edge_gene[1])
        elif exist == False:
            #if it is not existed, create it
            self.G.add_edge(edge_gene[0], edge_gene[1])
        return not keep

    def edges_weighted(self, weight):
        for ii in range(self.G.number_of_edges()):
            edges_item = self.G.edges()[ii]
            self.G[edges_item[0]][edges_item[1]]['weight'] = weight[edges_item[0]][edges_item[1]]

        return self.G.edges()
       





