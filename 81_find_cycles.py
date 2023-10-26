#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
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
    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "analysis_" + identifier + ".csv"
    out_text = ""

    print("<<<<<< WORKING ON: " + input_filename)
    
    G = nx.read_gexf(input_filename)  # this is an undirected graph and had to be manually changed to directed
    # print(nx.adjacency_spectrum(G))

    # nodes, edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    print(str(datetime.datetime.now()) + "    << # NODES: " + str(num_nodes) + " # EDGES: " + str(num_edges))
    # if nx.is_directed_acyclic_graph(G):
    #     print(str(datetime.datetime.now()) + "    << WARNING: GRAPH IS A DAG")
    if False:
        print(G.edges())
    cycles = nx.simple_cycles(G)
    for entry in cycles:
        out_text += str(entry) + "\n"

    out_file = open(output_filename, "w")
    out_file.write(out_text)
    out_file.close()
    
    print(str(datetime.datetime.now())+ "  >>>>>> FINISHED: ")
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
