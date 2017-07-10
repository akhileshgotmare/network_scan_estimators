import networkx as nx
import numpy as np
import datetime
import pickle
import matplotlib.pyplot as plt

G = nx.read_graphml('G_10_power_3_2017-03-29-21:24.graphml')
mapping = {str(x):x for x in range(len(G.nodes()))}
nx.relabel_nodes(G, mapping, copy=False)
every_ngbd = np.load('every_ngbd_G_10_power_3_2017-03-29-21:24.npy')

exp_estimate_list = [None]*10

N = nx.number_of_nodes(G)
N_big = pow(10,6)
N_small = pow(10,3)

def fast_graph_scan(G,every_ngbd,k,weights,print_time):
    
    N = nx.number_of_nodes(G) 
    my_set = []
    avg_ngbd = np.zeros(N)
    
    start = datetime.datetime.now()
    
    for v in G.nodes():
        
        my_set = every_ngbd[v][0:(k+1)]
        avg_ngbd[v] = np.mean(weights[my_set])
    
    return np.min(avg_ngbd),np.argmin(avg_ngbd)



for exp_no in range(1):
    print('exp_no = ',exp_no)
    
    exp_estimate_list[exp_no] = [None]*100
    
    L_ic = np.random.choice(range(0,N_big), int(N_big/2), replace=False) 
                                                 # list of indices of inactive nodes in the 
                                                 # bigger group (of million nodes)
    weights = 10*np.ones(N) + np.random.normal(0,1,N)
    weights[N_big:N] -= 8
    weights[L_ic] -= 8
    k = 1000
    [a,a_ind] = fast_graph_scan(G,every_ngbd,k,weights,False) #without the adversary
    print('without adversary done')


    all_inactive = set(L_ic).union((set(np.arange(N_big,N))))
    all_active = set(np.arange(0,N)) - all_inactive
    active_in_best_ngbd = set(every_ngbd[a_ind][0:k+1]) - all_inactive
    a_new = 9999
    a_new_ind = 9999
    print(a)
    
    
    
    for step_no in range(50):

        if active_in_best_ngbd:

            altered_weights = weights

            #set weights for the active guys in the best ngbd to 1mn
            altered_weights[np.array(list(active_in_best_ngbd))] = pow(10,6) 

            [a_new,a_new_ind] = fast_graph_scan(G,every_ngbd,k,altered_weights,False)
            print('with weak but multi-step adversary done')
            print(a_new)
        else:
            print('Game Over! We won!')
            [a_new,a_new_ind] = [9999,9999]
            

        active_in_best_ngbd = set(every_ngbd[a_new_ind][0:k+1]) - all_inactive
        
        exp_estimate_list[exp_no][step_no] = a_new
        
with open('adversary_results/a_k_1000_estimate_data_50_steps', 'wb') as fp:
    pickle.dump(store, fp)

        
    
        