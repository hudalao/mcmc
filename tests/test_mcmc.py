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

from mcmc.posi_assign import posi_assign
from mcmc.edge_oper import edge_oper
from mcmc.theta import theta
from mcmc.graph import connec_graph
from mcmc.mcmc import mcmc
from mcmc.cli import cli
from mcmc.Metripolis_Hastings import Metripolis_Hastings 
from mcmc.plot_graph import plot_graph

class TestMcmc(unittest.TestCase):
    
    def __init__(self):
        posi = posi_assign.posi_assign(5, 5, 5, 1, 1)
        self.N = 5
        self.G = nx.Graph()
        self.graph = graph.connec_graph(self.N, self.G)
        self.graph.init_graph()  #start with the graph with edges([(0,1),(0,2),(0,3),(0,4)])
        self.edge_oper = edge_oper.edge_oper(self.N, posi, self.G)
        self.weight = self.edge_oper.weight_calc()
        self.r = 5

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'mcmc.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def prohibited_cutedges_check(self):
        edges_keep_num, edges_keep_list = self.graph.edges_keep()
        edges_keep_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        edges_keep_num_expected = 4
        self.assertEqual(edges_keep_num, edges_keep_num_expected)
        self.assertEqual(edges_keep_list, edges_keep_list_expected)

    def edge_delet(self):
        R = copy.deepcopy(self.G)
        graph = graph.connec_graph(self.N, R)
        edge_oper = edge_oper.edge_oper(self.N, posi, R)
        
        R.add_edge(1, 3)
        edges_keep_num, edges_keep_list = graph.edges_keep()
        edge_gene = (1,3)
        edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(R.edges(), edges_list_expected)

    def edge_add(self):
        S = copy.deepcopy(self.G)
        graph = graph.connec_graph(self.N, S)
        edge_oper = edge_oper.edge_oper(self.N, posi, S)
        
        edges_keep_num, edges_keep_list = graph.edges_keep()
        edge_gene = (1,3)
        edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3)]
        self.assertEqual(S.edges(), edges_list_expected)

    def no_edge_change(self):
        edges_keep_num, edges_keep_list = self.graph.edges_keep()
        edge_gene = (0,3)
        self.edge_oper.update_edges_list(edge_gene, edges_keep_list)
        edges_list_expected = [(0, 1), (0, 2), (0, 3), (0, 4)]
        self.assertEqual(self.G.edges(), edges_list_expected)
        
    def theta_check(self):
        edges_list_weighted = self.edge_oper.edges_weighted(self.weight)
        theta_calc = theta.theta(self.r, self.N, self.G, edges_list_weighted, self.weight)
        theta_expect = (self.r + 1) * (self.weight[0][1] + self.weight[0][2] + self.weight[0][3] + self.weight[0][4]) 
        self.assertEqual(theta_expect, theta_calc)
