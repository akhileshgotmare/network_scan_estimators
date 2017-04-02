# Script to run M experiments for the following setting - 
# Given: every_ngbd and G
# Return 200 outputs for the scanning algorithm using this data

from multiprocessing import Pool
import networkx as nx
import numpy as np
import datetime

def fast_graph_scan(G,every_ngbd,k,weights,print_time):
    
    N = nx.number_of_nodes(G) #np.max(G.nodes())+1 #nx.number_of_nodes(G)
    my_set = []
    avg_ngbd = np.zeros(N)
    
    start = datetime.datetime.now()
    
    for v in G.nodes():
        
        my_set = every_ngbd[v][0:(k+1)]
        avg_ngbd[v] = np.mean(weights[my_set])
    
    return np.min(avg_ngbd),np.argmin(avg_ngbd)

def run_exp_M_times(ind):
    
       
    dictn =  {1:100 ,2:500,3:1000,4:2000}
    M_dict = {1:100 ,2:100,3:100, 4:100 }
    
    k = dictn[ind]
              
    M = M_dict[ind]
    
    G = nx.read_graphml('G_10_power_4_2017-03-29-21:24.graphml')
    mapping = {str(x):x for x in range(len(G.nodes()))}

    nx.relabel_nodes(G, mapping, copy=False)
    print('processor working on ind = ',ind,' just loaded the graph')
    
    every_ngbd = np.load('every_ngbd_G_10_power_3_2017-03-29-21:24.npy')
    print('processor working on ind = ',ind,' just loaded the every_ngbd')
    
    N = nx.number_of_nodes(G)
    N_active = pow(10,6)
    N_inactive = pow(10,4)
    
    L_ic = np.random.randint(0,N_active,int(N_active/2)) # list of indices of inactive nodes in the active group
    
    
    a = [None]*M
    b = [None]*M
    
    start = datetime.datetime.now()
    
    for n_expmnt in range(M):
        
        weights = 10*np.ones(N) + np.random.normal(0,1,N)
        weights[N_active:N] -= 8
        weights[L_ic] -= 8

        print('ind = ',ind,' reached experiment: ',n_expmnt,'/200')
        
        [a_s,b_s] = fast_graph_scan(G,every_ngbd,k,weights,True)
        a[n_expmnt] = a_s
        b[n_expmnt] = b_s
    np.save('scan_results/output_a_for_ind_=_'+str(ind)+'.npy',a)
    np.save('scan_results/output_b_for_ind_=_'+str(ind)+'.npy',b)
       
list_ind = [1,2,3,4]

#list(set(np.arange(17,247,10)) - set([147,127,67,157,27,97,77,217,227,197,107,167,137,87])) 

no_of_rep = len(list_ind)   #2
no_of_cores = len(list_ind) #2 #40  

p = Pool(no_of_cores)
results = p.map(run_exp_M_times, list_ind)

#from joblib import Parallel, delayed
#Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
#Parallel(n_jobs = 2)(delayed(run_exp_M_times)(i) for i in [1,2])