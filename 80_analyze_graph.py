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
def do_run(base_directory, identifier, task):
    input_filename = base_directory + identifier + "-merged.dat"
    output_filename = base_directory + identifier + "_analysis.csv"

    print("<<<<<< WORKING ON: " + input_filename)
    
    print(str(datetime.datetime.now()) + "  << START READING .dat FILE")
    G = nx.read_edgelist(input_filename)  # this is an undirected graph
    print(str(datetime.datetime.now()) + "  >> COMPLETE READING .dat FILE")

    # if task == "sample_graph":
    #     sample_graph_filename = base_directory + identifier + "-sampled.gexf"
    #     H = nx.DiGraph()
    #     for u,v in G.edges():
    #         if random.random() < 0.01:  # we add only one percent of all edges
    #             H.add_edge(u,v)
    #     nx.write_gexf(H, sample_graph_filename)
    #     print(str(datetime.datetime.now()) + "  >> SAMPLED GRAPH WRITTEN TO:" + sample_graph_filename)

    if task == "analyze_graph":
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

        # largest weakly connected component
        deg_text = ""
        for deg in deghist_lcc:
            deg_text += str(deg) + ";"

        deg_file = open(base_directory + "deghist_" + identifier + "-lcc.csv", "w")
        deg_file.write(deg_text)
        deg_file.close()

        print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING DEGREE DISTRIBUTIONS")
        
        # DONE
        print(str(datetime.datetime.now()) + "  << COMPLETED NETWORK ANALYSIS")

    if task == "analyze_graph":
        out_text = "num_nodes;num_edges;num_conn_comp;size_largest_cc\n"
        out_text += str(num_nodes) + ";" + str(num_edges) + ";" \
            + str(num_connected_components) + ";" + str(size_largest_cc) \
            + "\n"

        out_file = open(output_filename, "w")
        out_file.write(out_text)
        out_file.close()
        
        if True:
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
    task = args[3]
    
#
# CODE
#
    do_run(base_directory, identifier, task)
