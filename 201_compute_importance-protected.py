#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import datetime
import random

import networkx as nx
import numpy as np
import pandas as pd

from tqdm import tqdm

# ###########################################################################
# METHODS
# ###########################################################################
def nodes_to_protect(protect_filename,k):
    df = pd.read_csv(protect_filename, delimiter=';', header=None)
    nodes_to_protect = df.iloc[:k, 0].values.astype(str)
    return nodes_to_protect

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier, protect_filename, depth, k, protection):
    np.set_printoptions(threshold=sys.maxsize)

    debug = False

    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "importance_" + identifier + "-" + str(k) + "-" + str(depth) + "_" + protection + ".csv"
    
    # ensure file is empty
    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print("<<<<<< WORKING ON: " + input_filename)

    G = nx.read_gexf(input_filename).reverse()
    print(str(datetime.datetime.now()) + "    << NETWORK WITH " + str(G.number_of_nodes()) + " NODES AND " + str(G.number_of_edges()) + " EDGES FOUND" )

    if False:
        print(type(G))
        # for node in G.nodes():
        #     print(node)
        print(G.nodes())
        print(G.edges())

    # remove nodes that are protected from contagion
    protected_nodes = nodes_to_protect(base_directory + protect_filename, k)
    G.remove_nodes_from(protected_nodes)

    print(str(datetime.datetime.now()) + "    << NETWORK WITH " + str(G.number_of_nodes()) + " NODES AND " + str(G.number_of_edges()) + " EDGES CONSTRUCTED" )

    # appending results continuously for large networks
    out_file = open(output_filename, "a")

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
    protect_filename = args[3]
    depth = int(args[4])
    k = int(args[5])
    protection = args[6]

#
# CODE
#
    do_run(base_directory, identifier, protect_filename, depth, k, protection)
