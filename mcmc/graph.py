#this class including all the function needed for the graph
#N: the number of the vertexs
#G: the graph

import networkx as nx
import numpy as np

class connec_graph():

    def __init__(self,N, G):
        self.N = N
        self.G = G

    def init_graph(self):
        #connect vertex 0 to all the other vertex
        for ii in range(1,self.N):
            self.G.add_edge(0, ii)    
            

    ######finding all the spanning trees for the graph to figure out the edges necessary to keep the graph connected
    def edges_keep(self):
        #tring to cut every edges in the graph to see if the graph is still connected
        edges_keep_num = 0
        edges_keep_list = []
        cout = 0
        for ii in range(self.G.number_of_edges()):
            edges_list_sorted = [None] * self.G.number_of_edges()
            for jj in range(self.G.number_of_edges()):
                edges_list_sorted[jj] = tuple(sorted(self.G.edges()[ii])) 
            edges_pick = edges_list_sorted[ii]
            self.G.remove_edge(edges_pick[0],edges_pick[1])
            if nx.is_connected(self.G) == False:
                edges_keep_num = edges_keep_num + 1
                edges_keep_list.append(edges_pick)
            self.G.add_edge(edges_pick[0],edges_pick[1])
            cout = cout + 1
        return edges_keep_num, edges_keep_list
