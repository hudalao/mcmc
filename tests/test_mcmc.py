#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_mcmc
----------------------------------

Tests for `mcmc` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner
import numpy as np
import math as mt
import networkx as nx
import copy

sys.path.append('../mcmc')
from posi_assign import posi_assign
from edge_oper import edge_oper
from theta import theta
from graph import connec_graph
from mcmc import mcmc
from Metripolis_Hastings import Metripolis_Hastings 
from plot_graph import plot_graph


class TestMcmc(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass
    
    def prohibited_cutedges_check(self):
        posi = posi_assign(5, 5, 5, 1, 1)
        N = 5
        G = nx.Graph()
        graph = connec_graph(N, G)
        graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        edge_oper = edge_oper(N, posi, G)
        weight = edge_oper.weight_calc()
        r = 5

        edges_keep_num, edges_keep_list = graph.edges_keep()
        edges_keep_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        edges_keep_num_expected = 4
        self.assertEqual(edges_keep_num, edges_keep_num_expected)
        self.assertEqual(edges_keep_list, edges_keep_list_expected)

    def edge_delet(self):
        posi = posi_assign(5, 5, 5, 1, 1)
        N = 5
        G = nx.Graph()
        graph = connec_graph(N, G)
        graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        edge_oper = edge_oper(N, posi, G)
        weight = edge_oper.weight_calc()
        r = 5
        
        R = copy.deepcopy(self.G)
        graph = connec_graph(N, R)
        edge_oper = edge_oper(N, posi, R)
        
        R.add_edge(1, 3)
        edges_keep_num, edges_keep_list = graph.edges_keep()
        edge_gene = (1,3)
        edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(R.edges(), edges_list_expected)

    def edge_add(self):
        posi = posi_assign(5, 5, 5, 1, 1)
        N = 5
        G = nx.Graph()
        graph = connec_graph(N, G)
        graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        edge_oper = edge_oper(N, posi, G)
        weight = edge_oper.weight_calc()
        r = 5
        
        S = copy.deepcopy(G)
        graph = connec_graph(N, S)
        edge_oper = edge_oper(N, posi, S)
        
        edges_keep_num, edges_keep_list = graph.edges_keep()
        edge_gene = (1,3)
        edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3)]
        self.assertEqual(S.edges(), edges_list_expected)

    def no_edge_change(self):
        posi = posi_assign(5, 5, 5, 1, 1)
        N = 5
        G = nx.Graph()
        graph = connec_graph(N, G)
        graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        edge_oper = edge_oper(N, posi, G)
        weight = edge_oper.weight_calc()
        r = 5
        
        edges_keep_num, edges_keep_list = graph.edges_keep()
        edge_gene = (0,3)
        edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(self.G.edges(), edges_list_expected)
        
    def theta_check(self):
        posi = posi_assign(5, 5, 5, 1, 1)
        N = 5
        G = nx.Graph()
        graph = connec_graph(N, G)
        graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        edge_oper = edge_oper(N, posi, G)
        weight = edge_oper.weight_calc()
        r = 5
        
        edges_list_weighted = edge_oper.edges_weighted(weight)
        theta_calc = theta(r, N, G, edges_list_weighted, weight)
        theta_expect = (r + 1) * (weight[0][1] + weight[0][2] + weight[0][3] + weight[0][4]) 
        self.assertEqual(theta_expect, theta_calc)
