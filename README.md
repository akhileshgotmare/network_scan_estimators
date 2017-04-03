# Description

This repository contains two kinds of experiments to verify the claims of the scanning algorithm proposed in the paper. The first type contained in the directory <artifical_graph> is a simulated example of a network containing about million nodes, whereas the second example contained in the <blog_graph> directory is a network of political blogs obtained from http://moreno.ss.uci.edu/data.html.  

# Directory Structure

scanestimators.py: defines functions for finding the K_hat neighborhood of a node in the network and running the scanning algorithm.

artificial_graph: this directory contains two subdirectories: N_inactive_10^3 and N_inactive_10^4 each of the two correspond to slightly different settings of the experiment on the simulated network.

N_inactive_10^3: contains scripts create_and_store_graph.py, compute_every_ngbd.py, combine_all_ngbd.py and run_M_expmnts.py (further details explained inside the scripts as comments) and analysis.ipynb that is used to analyze the results and obtain the final plots
(similar structure for N_inactive_10^4)

blog_graph: contains analysis.ipynb that does all the processing and analysis for this case. run_M_expmnts_blog.py creates M estimates for the same network with our algorithm 

# Appendix:

Stack-overflow suggestions for other libraries to play with graphs: 
http://stackoverflow.com/questions/606516/python-graph-library

Other toy examples tried include: atlas, cirular tree, fb snap data

# Notes:

https://docs.google.com/document/d/1CN0KhdYcq445ABN2K-VbGVVdq-LNf5kJAPLwtN_t_0o/edit?usp=sharing
