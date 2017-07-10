import networkx as nx
import numpy as np
import datetime
import pickle
import sys

G = nx.read_graphml('G_10_power_3_2017-03-29-21:24.graphml')
print('graph loaded')
mapping = {str(x):x for x in range(len(G.nodes()))}
nx.relabel_nodes(G, mapping, copy=False)

every_ngbd = np.load('every_ngbd_G_10_power_3_2017-03-29-21:24.npy')
print('ngbd data loaded')

def fast_graph_scan(G,every_ngbd,k,weights,print_time):
    
    N = nx.number_of_nodes(G) 
    my_set = []
    avg_ngbd = np.zeros(N)
    
    start = datetime.datetime.now()
    
    for v in G.nodes():
        
        my_set = every_ngbd[v][0:(k+1)]
        avg_ngbd[v] = np.mean(weights[my_set])
    
    return np.min(avg_ngbd),np.argmin(avg_ngbd)

N = nx.number_of_nodes(G)
N_big = pow(10,6)
N_small = pow(10,3)
m = 100 # no of experiments
store = [None]*m

t1 = datetime.datetime.now()

for exp_no in range(m):

    t1 = datetime.datetime.now()
    print('currently running exp',exp_no)

    L_ic = np.random.choice(range(0,N_big), int(N_big/2), replace=False) 
                                                         # list of indices of inactive nodes in the 
                                                         # bigger group (of million nodes)
    weights = 10*np.ones(N) + np.random.normal(0,1,N)
    weights[N_big:N] -= 8
    weights[L_ic] -= 8
    k = 1000
    [a,a_ind] = fast_graph_scan(G,every_ngbd,k,weights,False) #without the adversary
    print('without adversary done')
    t3 = datetime.datetime.now()
    execution_time_iter = (t3 - t1).total_seconds()
    print("time for this version = {t:.3f} seconds".format(t=execution_time_iter))

    
    
    all_inactive = set(L_ic).union((set(np.arange(N_big,N))))
    all_active = set(np.arange(0,N)) - all_inactive
    active_in_best_ngbd = set(every_ngbd[a_ind][0:k+1]) - all_inactive
    a_new = 9999
    a_new_ind = 9999
    
    if active_in_best_ngbd:
        altered_weights = weights
        altered_weights[np.array(list(active_in_best_ngbd))] = pow(10,6) #set weights for the active guys in the best ngbd to 1mn
        [a_new,a_new_ind] = fast_graph_scan(G,every_ngbd,k,altered_weights,False)
        print('with adversary version 1 done')
        t3 = datetime.datetime.now()
        execution_time_iter = (t3 - t1).total_seconds()
        print("time for this version = {t:.3f} seconds".format(t=execution_time_iter))

    

    altered_2_weights = weights
    altered_2_weights[np.array(list(all_active))] = 1000000 #adversary setting all active guys to 1 mn
    [a_2_new,a_2_new_ind] = fast_graph_scan(G,every_ngbd,500,altered_2_weights,False)
    print('with adversary version 2 done')
    t3 = datetime.datetime.now()
    execution_time_iter = (t3 - t1).total_seconds()
    print("time for this version = {t:.3f} seconds".format(t=execution_time_iter))

    
    store[exp_no] = np.array([a,a_ind,a_new,a_new_ind,a_2_new,a_2_new_ind])
    t2 = datetime.datetime.now()
    execution_time_iter = (t2 - t1).total_seconds()
    print("execution time for this iteration = {t:.3f} seconds".format(t=execution_time_iter))
    
with open('adversary_results/a_k_1000_estimate_data_', 'wb') as fp:
    pickle.dump(store, fp)
