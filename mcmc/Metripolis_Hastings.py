from theta import theta
from edge_oper import edge_oper
from graph import connec_graph
import math as mt
import numpy as np
import copy


def Metripolis_Hastings(r, T, N, posi, weight, Xi, R, edges_keep_list_i, qij, theta_i):

    #create randomly a edge
    edge_oper_j = edge_oper(N, posi, R)
    edge_gene = edge_oper_j.ran_edge()
    #Be Careful here!!!must copy all the attributions to the reference graph object in case the created graph be rejected
    edge_list_update_j = edge_oper_j.update_edges_list(edge_gene, edges_keep_list_i)
    edges_keep_num_j, edges_keep_list_j = connec_graph(N, R).edges_keep()
    edge_weighted_list_j = edge_oper_j.edges_weighted(weight)
    theta_j = theta(r, N, R, edge_weighted_list_j, weight)


    #transition probability from potential X(j) to X(i)
    qji = 1 / (N * (N - 1) / 2 - edges_keep_num_j)

    #calculate the acceptance probability
    relative_pi = mt.exp(-(theta_j - theta_i) / T)
    relative_transi = float(qji) / float(qij)
    relative = relative_pi * relative_transi
    accept_prob = min(relative, 1)
    U = np.random.uniform(0, 1)
    #if accept the proposel state, the output would be updated, otherwise, using the values of the last graph
    if U <= accept_prob:
        Xj = copy.deepcopy(R)
        accept = True
    elif U > accept_prob:
        Xj = copy.deepcopy(Xi)
        accept = False
        qji = qij
        theta_j = theta_i
    edges_keep_num_j, edges_keep_list_j = connec_graph(N, Xj).edges_keep()

    return Xj, accept, edge_list_update_j, edge_gene, edges_keep_list_j, qji, theta_j
