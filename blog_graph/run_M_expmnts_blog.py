def run_exp_M_times_blog(ind):
    
    import numpy as np
    import networkx as nx
    import matplotlib.pyplot as plt
    import random
    
    from scanestimators import graph_scan
    
    K_list = [50,100,150,200,300]
    M = 400
    
    path = 'blog_data/blogs_data_edge_list.txt'
    edges_data = np.loadtxt(path, dtype = int)

    edges_data[:,0] -= 1
    edges_data[:,1] -= 1

    N = np.max(edges_data)

    G = nx.Graph()
    G.add_nodes_from([n for n in range(N+1)])
    G.add_edges_from(edges_data[edges_data[:,2] == 1] [:,0:2])
    N = np.max(G.nodes()) + 1 

    connected_comp_sub = nx.connected_component_subgraphs(G)
    remove_list = list([])
    for g in connected_comp_sub:
        if len(list(nx.nodes(g))) <= 2:
            remove_list = remove_list + (list(nx.nodes(g)))
    for r in remove_list:
        G.remove_node(r)

    output_a = np.zeros((M,len(K_list)))
    
    
    for n_expmnt in range(M):
        
        if n_expmnt%100 == 0:
            print('proc on ind = ',ind,'completed upto: ',n_expmnt,'/400')
        
        weights = 10*np.ones(N+1) + np.random.normal(0,1,(N+1))
        weights[758:1490] -= 8 

        for k_ind,k in enumerate(K_list):
            
            [a,b,c,d] = graph_scan(G,k,weights,False)
            if n_expmnt%50 == 0:
                print(a)
            
            
            output_a[n_expmnt,k_ind] = a
            
            
        print('proc working on ind: ',ind,'reached: ',n_expmnt,' out of 400')
    
    np.save('output_a_for_ind_=_'+str(ind)+'_.npy',output_a)
    
#run_exp_M_times_blog(4)

list_ind = [1,2,3]       
no_of_rep = len(list_ind)   #2
no_of_cores = len(list_ind) #2 #40  
from multiprocessing import Pool
p = Pool(no_of_cores)

results = p.map(run_exp_M_times_blog, list_ind)