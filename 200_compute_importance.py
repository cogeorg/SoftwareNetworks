#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import datetime
import random

import networkx as nx
from tqdm import tqdm

# ###########################################################################
# METHODS
# ###########################################################################

def infect_nodes(G, infected_nodes, node, e):
    for _node in G.predecessors(node):
        if random.uniform(0.0,1.0) > e:
            infect_nodes(G, infected_nodes, _node, e)
    if node not in infected_nodes: # only append nodes that haven't been infected before
        infected_nodes.append(node)


# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier, e):
    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "importance_" + identifier + ".csv"
    # ensure file is empty
    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    infected_nodes = []

    print("<<<<<< WORKING ON: " + input_filename)

    G = nx.read_gexf(input_filename)

    num_nodes = G.number_of_nodes()
    print(str(datetime.datetime.now()) + "    << NETWORK WITH " + str(num_nodes) + " NODES AND " + str(G.number_of_edges()) + " EDGES FOUND" )

    if False:
        print(type(G))
        print(G.nodes())
        print(G.edges())

    #
    # COMPUTE IMPORTANCE
    #
    _count = 0
    for node in tqdm(G.nodes()):
        infect_nodes(G, infected_nodes, node, e)

        # append text to output file while code is running        
        out_text = str(node) + ";" + str(len(infected_nodes)) + "\n"
        out_file = open(output_filename, "a")
        out_file.write(out_text)
        out_file.close()
        
        infected_nodes = []

    
    print("  >> OUTPUT WRITTEN TO:" + base_directory + output_filename)

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
    e = float(args[3])
    
#
# CODE
#
    do_run(base_directory, identifier, e)
