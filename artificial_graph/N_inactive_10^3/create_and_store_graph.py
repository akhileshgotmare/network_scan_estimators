# Script to create a Graph with N_active = 10^6, N_inactive = 10^3
# Each node in the small subgraph connected to 3 random nodes in the same subgraph
# Each node in the bigger subgraph connected to 3 random nodes in the same subgraph

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import time

import sys
sys.path.insert(0,'/Users/akhileshgotmare/Desktop/Git_Junta/network_scan_estimators')

from scanestimators import *

"""
[0:N_active] - active group resides here
[N_active:N] - inactive group here! 

"""

""" Build the graph with N_active and N_inactive number of nodes"""

G = nx.Graph()
N_active = 1000000
N_inactive = 1000
N = N_active + N_inactive
L = list(np.arange(N))
G.add_nodes_from(L)
print('all nodes added')

c = list(np.random.randint(0,N_active,3*N_active))
d = np.arange(0,N_active)
d1 = list(np.hstack((d,d,d)))

G.add_edges_from(list(zip(c,d1))) #adding edges within bigger group (subgraph with million nodes)

b = list(np.random.randint(N_active, (N), 3*N_inactive))
a = np.arange(N_active, (N))
a1 = list(np.hstack((a,a,a)))

G.add_edges_from(list(zip(a1,b))) #adding edges within smaller group (subgraph with thousand nodes)

print('all edges added')

L1 = list(np.arange(0,N_active))
L2 = list(np.arange(N_active,N))
for j in np.random.choice(L2,20):
    v = np.random.choice(L1)
    G.add_edge(j,v)
    
date_string = time.strftime("%Y-%m-%d-%H:%M")

nx.write_graphml(G,'G_10_power_3' + date_string + ".graphml")