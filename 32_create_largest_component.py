#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import os
import re
import datetime
import random

import networkx as nx

# ###########################################################################
# METHODS
# ###########################################################################



# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier):
    input_filename = base_directory + identifier + ".dat"
    node_dict = {}

    print(str(datetime.datetime.now()) + " <<<<<< START WORKING ON: " + input_filename)

    G = nx.read_edgelist(input_filename)  # networkx.Graph()

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    largest_cc = G.subgraph(max(nx.connected_components(G), key=len))
    num_nodes_cc = largest_cc.number_of_nodes()
    num_edges_cc = largest_cc.number_of_edges()

    print(str(datetime.datetime.now()) + "  << FULL GRAPH -- N=" + str(num_nodes) + " E=" + str(num_edges) + " -- LARGEST CC -- N=" + str(num_nodes_cc) + " E=" + str(num_edges_cc))

    nx.write_edgelist(largest_cc, base_directory + identifier + "-lcc.dat", data=False)

    print(str(datetime.datetime.now()) + " >>>>>> FINISHED WORKING ON " + input_filename)
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

#
# CODE
#
    do_run(base_directory, identifier)
