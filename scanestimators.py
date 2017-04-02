import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import datetime

def union_set(a, b):
    for j in range(len(b)):
        if b[j] not in set(a):
            a.append(b[j])
    return a

def return_k_nn(source,G,k):

    read_index = 0
    my_set = []
    my_set = union_set(my_set,[source])
    
    
    while len(my_set) < k :
        
        x = my_set[read_index]
        #global G
        old_len = len(my_set)
        new_set = []
        for p in range(len(G.neighbors(x))):
            new_set = union_set(my_set,[G.neighbors(x)[p]])
            if len( new_set ) >k:
                my_set = new_set
                break
            else:
                continue
                
        read_index += 1
        if read_index >= len(my_set):
            break
    
    return my_set

def graph_scan(G,k,weights,print_time):
    N = np.max(G.nodes())+1 #nx.number_of_nodes(G)
    my_set = []
    avg_ngbd = np.zeros(N)
    
    start = datetime.datetime.now()
    every_ngbd = [None]*(N)
    for v in G.nodes():
        if print_time:
            
            if v == 10000:
                
                end = datetime.datetime.now()
                duration = (end - start).total_seconds()
            
                print(v)
                print("Total execution time till 10000th node = {t:.3f} seconds".format(t=duration))
                
        my_set = return_k_nn(v,G,k)
        every_ngbd[v] = my_set
        avg_ngbd[v] = np.mean(weights[my_set])
    #print("Estimated value of a for the given input:",min(avg_ngbd))
    return np.min(avg_ngbd),np.argmin(avg_ngbd), every_ngbd, avg_ngbd


"""
def union_set(a, b):
    for j in range(len(b)):
        if b[j] not in set(a):
            a.append(b[j])
    return a

def return_k_nn(source,k):

    read_index = 0
    my_set = []
    my_set = union_set(my_set,[source])

    while len(my_set) < k :
        
        x = my_set[read_index]
        global G
        old_len = len(my_set)
        my_set = union_set(my_set,G.neighbors(x))
        new_len = len(my_set)
        if old_len == new_len:
            break
        read_index += 1
    
    return my_set 

def graph_scan(G,k,weights):
    my_set = []
    avg_ngbd = np.zeros(N)
    for v in G.nodes():
        my_set = return_k_nn(v,k)
        avg_ngbd[v] = np.mean(weights[my_set])
    print("Estimated value of a for the given input:",min(avg_ngbd))
    return np.min(avg_ngbd)
"""