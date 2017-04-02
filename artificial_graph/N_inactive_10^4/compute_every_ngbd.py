import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import datetime
import time
import sys

sys.path.insert(0, '/home/gotmare/network_scan_estimators/')

from multiprocessing import Pool
from scanestimators import *

def find_one_ngbd(x):
    
    G = nx.read_graphml('G_10_power_4_2017-03-29-18:48.graphml') #because reading the graph causes num2str operation on nodes, 
    mapping = {str(x):x for x in range(len(G.nodes()))}
    nx.relabel_nodes(G, mapping, copy=False)
    print('processor working on x = ',x,'/30 just loaded the graph G')
    N = nx.number_of_nodes(G)
    k = 1000
    chunk = np.int(N/30)
    partial_ngbd = [None]*chunk
    
    for source in range( (x*chunk) , ((x+1)*chunk) ):
        #print(source)
        partial_ngbd[source - x*chunk] = return_k_nn((source),G,k)
        
    np.save('/home/gotmare/network_scan_estimators/mar28_new/N_inactive_10^4/neighborhood_data/ngbd_part_'+str(x)+'_of_40.npy',
            partial_ngbd)
    
    
no_of_rep = 30
no_of_cores = 30  

p = Pool(no_of_cores)
list_ind = np.arange(no_of_rep)
#list_ind = np.array([12,18,26])

results = p.map(find_one_ngbd, list_ind)

#np.save('/home/gotmare/network_scan_estimators/mar28_new/neighborhood_data/all_ngbd_results.npy',results)