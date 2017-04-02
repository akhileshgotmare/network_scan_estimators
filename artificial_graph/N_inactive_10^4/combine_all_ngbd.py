# Script to combine all the neighborhoods

import numpy as np
import networkx as nx


N = pow(10,6) + pow(10,4) 
every_ngbd = [None]*N

for x in range(0,30):
    
    print(x)
    
    chunk_ngbd = np.load('/home/gotmare/network_scan_estimators/mar28_new/N_inactive_10^4/neighborhood_data/ngbd_part_'
                         +str(x)+'_of_40.npy')
   
    for j in range(len(chunk_ngbd)):
        every_ngbd[chunk_ngbd[j][0]] = chunk_ngbd[j]
        
np.save('every_ngbd_G_10_power_4_2017-03-29-18:48.npy', every_ngbd)