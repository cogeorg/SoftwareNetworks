#!/usr/bin/env python3
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
    input_filename = base_directory + identifier + ".dat"
    output_filename = base_directory + "analysis_" + identifier + ".csv"

    print("<<<<<< WORKING ON: " + input_filename)
    
    print(str(datetime.datetime.now()) + "  << START READING .dat FILE")
    G = nx.read_edgelist(input_filename)  # this is an undirected graph
    print(str(datetime.datetime.now()) + "  >> COMPLETE READING .dat FILE")

    # nodes, edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING NODES + EDGES")

    # components
    # num_weakly_connected_components = nx.number_weakly_connected_components(G)
    num_connected_components = nx.number_connected_components(G)
    largest_cc = G.subgraph(max(nx.connected_components(G), key=len))
    size_largest_cc = len(largest_cc)
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING COMPONENTS")

    # degree (distributions)
    deghist = nx.degree_histogram(G)
    deghist_lcc = nx.degree_histogram(largest_cc)

    # entire network
    deg_text = ""
    for deg in deghist:
        deg_text += str(deg) + ";"

    deg_file = open(base_directory + "deghist_" + identifier + ".csv", "w")
    deg_file.write(deg_text)
    deg_file.close()

    # largest connected component
    deg_text = ""
    for deg in deghist_lcc:
        deg_text += str(deg) + ";"

    deg_file = open(base_directory + "deghist_" + identifier + "-lcc.csv", "w")
    deg_file.write(deg_text)
    deg_file.close()

    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING DEGREE DISTRIBUTIONS")
    
    # CLUSTERING, PATH LENGTH
    avg_shortest_path_length = nx.average_shortest_path_length(largest_cc)
    avg_clustering = nx.average_clustering(largest_cc)
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING CLUSTERING + PATH LENGTH")

    # CENTRALITIES FOR EACH NODE
    degree_centrality = nx.degree_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING CENTRALITIES")

    
    # DONE
    print(str(datetime.datetime.now()) + "  << COMPLETED NETWORK ANALYSIS")

    out_text = "num_nodes;num_edges;num_conn_comp;size_largest_cc;avg_shortest_path_length-lcc;average_clustering-lcc\n"
    out_text += str(num_nodes) + ";" + str(num_edges) + ";" \
        + str(num_connected_components) + ";" + str(size_largest_cc) \
        + str(avg_shortest_path_length) + ";" + str(avg_clustering) \
        + "\n"

    out_file = open(output_filename, "w")
    out_file.write(out_text)
    out_file.close()
    
    if False:
        print(out_text)

    print("  >> FILES WRITTEN TO:" + base_directory + output_filename)

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
