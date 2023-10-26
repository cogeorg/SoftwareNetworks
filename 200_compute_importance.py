#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import datetime
import random

import networkx as nx
import numpy as np

from tqdm import tqdm

# ###########################################################################
# METHODS
# ###########################################################################

def random_shock(n):
    # Create an array of zeros with length n
    arr = np.zeros(n, dtype=int)    
    # Generate a random index to place the '1'
    random_index = random.randint(0, n - 1)
    random_index = 1
    # Place the '1' at the random index
    arr[random_index] = 1
    
    
    return [random_index, arr.reshape(n,1)]

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier, depth):
    np.set_printoptions(threshold=sys.maxsize)

    debug = False

    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "importance_" + identifier + ".csv"
    
    # ensure file is empty
    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print("<<<<<< WORKING ON: " + input_filename)

    G = nx.read_gexf(input_filename).reverse()
    # H = G.subgraph(max(nx.weakly_connected_components(G), key=len))
    
    num_nodes = G.number_of_nodes()
    print(str(datetime.datetime.now()) + "    << NETWORK WITH " + str(num_nodes) + " NODES AND " + str(G.number_of_edges()) + " EDGES FOUND" )

    if False:
        print(type(G))
        print(G.nodes())
        print(G.edges())

    # appending results continuously for large networks
    out_file = open(output_filename, "a")

    # [current_node, p] = random_shock(num_nodes)
    for i in tqdm(G.nodes()):
        infected_nodes = nx.descendants_at_distance(G,i,0)
        out_text = str(i) + ";" + str(len(infected_nodes)) + ";"

        for k in range(1,depth):
            infected_nodes.update(nx.descendants_at_distance(G,i,k))
            out_text += str(len(infected_nodes)) + ";"

        if False:
            print(i, "->", infected_nodes, "\n")
        out_file.write(out_text + "\n") # + ";" + str(infected_nodes) + 
    
    out_file.close()
    print("  >> OUTPUT WRITTEN TO:" + output_filename)

    print(">>>>>> FINISHED")
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
#
#  MAIN
#
# -------------------------------------------------------------------------
if __name__ == '__main__':
#
# VARIABLES
#
    args = sys.argv
    base_directory = args[1]
    identifier = args[2]
    depth = int(args[3])
#
# CODE
#
    do_run(base_directory, identifier, depth)




        # # create adjacency matrix (columns = from, rows = to)
        # # must be reconstructed each run as infected nodes are removed below
        # M = np.matrix(nx.adjacency_matrix(H).toarray())
        # # reset infected nodes
        # infected_nodes = np.array([])

        # # Create an array of zeros with length n
        # p = np.zeros(num_nodes, dtype=int)    
        # # Place the '1' at the random index
        # p[i] = 1
        # p = p.reshape(num_nodes,1)

        # if False:
        #     print("  << i =", i, "------------------------------------------------------------------------")
        #     print("  << M = \n", M)
        #     print("  << p.T = ", p.T, "\n" )

        # _count = 0
        # while np.any( p != 0):
        #     if debug:
        #         print("  << _count =", _count)
        #         # print("  << p.T = ", p.T)
        #         print("  << M_start = \n", M)
            
        #     # find the index of all affected nodes in p and remember them for later
        #     q = np.where( p == 1)
        #     if debug:
        #         print(  "q = ", q[0])
        #     infected_nodes = np.concatenate((infected_nodes, q[0]))

        #     # then infect neighbors of all nodes in p
        #     p = np.dot(M,p)
        #     if debug:
        #         print("  << p_", _count, ".T = ", p.T )

        #     # since nodes can only be removed once, set the corresponding colums of M
        #     # to zero for each remembered node
        #     for _q in q[0]:
        #         M[:,_q] = 0

        #     if _count > num_nodes:  # should never happen
        #         if True:
        #             print("  << ERROR: NUMBER OF ALGORITHM STEPS (" + str(_count) + ") EXCEEDS NUM_NODES (" +str(num_nodes) + ")")
        #             # print(M)
        #             # print(p.T)
        #             print(len(infected_nodes), infected_nodes)
            
        #     _count += 1
