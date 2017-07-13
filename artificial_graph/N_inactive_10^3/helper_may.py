import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import networkx as nx
import time
import sys


def dfs(graph, start):
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited and labels[vertex] == 0:
                #print(vertex)
                color[vertex] = 'gray'
                visited.add(vertex)
                stack.extend(set(graph.neighbors(vertex)) - visited)
                color[vertex] = 'black'
        return visited

def give_max_cluster_size(G,p):
    
    N = 1000000 + 1000 #len(G.nodes()) #10^6 + 10^3
    global labels
    labels_r = np.random.random((N))
    labels = np.ones(labels_r.shape) 
    labels[labels_r <= p] = 0 
    
    
    nodes_list = np.array(G.nodes())
    zeros_list = (nodes_list[labels[G.nodes()] == 0])
    global color
    global community
    community = [set() for _ in range(N)]
    color = ['white']*len(nodes_list)
    
    for x in zeros_list:
        visited = dfs(G,x)
        community[x] = visited
    
    size_list = [len(cluster) for cluster in community]
    max_cluster_size = np.max(size_list)
    
    return max_cluster_size
    

    

    
    
