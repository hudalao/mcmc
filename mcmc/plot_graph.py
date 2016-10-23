import sys
sys.path.append('../mcmc')

# commend the lines for plotting using
#import matplotlib.pyplot as plt 
import networkx as nx

def plot_graph(G, N, time_point, posi):
    #setting up for graph plotting
    #setting the positions for all nodes
    pos = {}
    for ii in range(N):
        pos[ii] = posi[ii]
 #   plt.figure(time_point + 1)
    elarge=[(u,v) for (u,v,d) in G[time_point].edges(data=True) if d['weight'] >0.5]
    esmall=[(u,v) for (u,v,d) in G[time_point].edges(data=True) if d['weight'] <=0.5]

    # nodes
 #   nx.draw_networkx_nodes(G[time_point],pos,node_size=200)

    # edges
 #   nx.draw_networkx_edges(G[time_point],pos,edgelist=elarge,width=3)
 #   nx.draw_networkx_edges(G[time_point],pos,edgelist=esmall,width=3,alpha=0.5,edge_color='b',style='dashed')

    # labels
 #   nx.draw_networkx_labels(G[time_point],pos,font_size=10,font_family='sans-serif')

