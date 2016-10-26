#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mcmc
----------------------------------

Tests for `mcmc` module.
"""

import sys
import unittest
import numpy as np
import math as mt
import networkx as nx
import copy

from mcmc.posi_assign import posi_assign
from mcmc.edge_oper import edge_oper
from mcmc.theta import theta
from mcmc.graph import connec_graph
from mcmc.Metripolis_Hastings import Metripolis_Hastings 
from mcmc.plot_graph import plot_graph
import mcmc.mcmc

class TestMcmc(unittest.TestCase):

    def setUp(self):
        self.posi = posi_assign(5, 5, 5, 1, 1)
        self.N = 5
        self.G = nx.Graph()
        self.graph = connec_graph(self.N, self.G)
        self.graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        self.edge_oper_1 = edge_oper(self.N, self.posi, self.G)
        self.weight = self.edge_oper_1.weight_calc()
        self.r = 5
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_prohibited_cutedges(self):
        edges_keep_num, edges_keep_list = self.graph.edges_keep()
        edges_keep_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        edges_keep_num_expected = 4
        self.assertEqual(edges_keep_num, edges_keep_num_expected)
        self.assertEqual(edges_keep_list, edges_keep_list_expected)

    def test_edge_delet(self):
        #creating a graph with a deletable edge
        R = nx.Graph()
        R.add_edges_from([(0,1),(0,2),(0,3),(0,4),(1,3)])
        graph_2 = connec_graph(self.N, R)
        edge_oper_2 = edge_oper(self.N, self.posi, R)

        edges_keep_num, edges_keep_list = graph_2.edges_keep()
        edge_gene = (1,3)
        edge_oper_2.update_edges_list(edge_gene, edges_keep_list)
        
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(R.edges(), edges_list_expected)

    def test_edge_add(self):
        S = nx.Graph()
        S.add_edges_from([(0,1),(0,2),(0,3),(0,4)])
        graph_3 = connec_graph(self.N, S)
        edge_oper_3 = edge_oper(self.N, self.posi, S)
        
        edges_keep_num, edges_keep_list = graph_3.edges_keep()
        edge_gene = (1,3)
        edge_oper_3.update_edges_list(edge_gene, edges_keep_list)
        
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3)]
        self.assertEqual(S.edges(), edges_list_expected)

    def test_no_edge_change(self):
        edges_keep_num, edges_keep_list = self.graph.edges_keep()
        edge_gene = (0,3)
        self.edge_oper_1.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(self.G.edges(), edges_list_expected)
        
    def test_theta(self):
        edges_list_weighted = self.edge_oper_1.edges_weighted(self.weight)
        theta_calc = theta(self.r, self.N, self.G, edges_list_weighted, self.weight)
        theta_expect = (self.r + 1) * (self.weight[0][1] + self.weight[0][2] + self.weight[0][3] + self.weight[0][4]) 
        #only keep the seven digts after the point
        theta_expect = round(theta_expect, 7)
        theta_calc = round(theta_calc, 7)
        self.assertEqual(theta_expect, theta_calc)



