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

    print("<<<<<< WORKING ON: " + input_filename)
    
    G = nx.read_gexf(input_filename)  # this is an undirected graph and had to be manually changed to directed
    # print(nx.adjacency_spectrum(G))

    # nodes, edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    print(str(datetime.datetime.now()) + "    << # NODES: " + str(num_nodes) + " # EDGES: " + str(num_edges))
    if nx.is_directed_acyclic_graph(G):
        print("    << WARNING: GRAPH IS A DAG")

    out_text = "id_node;in_degree;out_degree;katz_centrality;ev_centrality;indeg_centrality\n"
    katz_centralities = nx.katz_centrality(G, max_iter=1000, tol=1e-06) # 
    ev_centralities = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
    indeg_centralities = nx.in_degree_centrality(G)

    for node in G.nodes():
        out_text += str(node) + ";" + str(G.in_degree(node)) + ";" + str(G.out_degree(node))
        out_text += ";" + str(katz_centralities[node]) + ";" + str(ev_centralities[node]) + ";" + str(indeg_centralities[node])
        out_text += "\n"

    out_file = open(output_filename, "w")
    out_file.write(out_text)
    out_file.close()
    print("  >> FILES WRITTEN TO:" + output_filename)

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
    
#
# CODE
#
    do_run(base_directory, identifier)
