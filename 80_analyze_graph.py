#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import datetime
import random

import networkx as nx

compute_clustering = True
compute_centralities = True

# ###########################################################################
# METHODS
# ###########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier):
    input_filename = base_directory + identifier + ".dat"
    output_filename = base_directory + "analysis_" + identifier + ".csv"
    cent_filename = base_directory + "centrality-" + identifier + ".csv"

    print("<<<<<< WORKING ON: " + input_filename)
    
    print(str(datetime.datetime.now()) + "  << START READING .dat FILE")
    G = nx.read_edgelist(input_filename)  # this is an undirected graph
    print(str(datetime.datetime.now()) + "  >> COMPLETE READING .dat FILE")
    nx.write_gexf(G, base_directory + identifier + ".gexf")
    
    # nodes, edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING NODES + EDGES")

    # components
    # num_weakly_connected_components = nx.number_weakly_connected_components(G)
    num_connected_components = nx.number_connected_components(G)
    largest_cc = G.subgraph(max(nx.connected_components(G), key=len))
    size_largest_cc = len(largest_cc)
    nx.write_gexf(largest_cc, base_directory + identifier + "-lcc.gexf")
    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING COMPONENTS")

    # degree (distributions)
    deghist = nx.degree_histogram(G)
    deghist_lcc = nx.degree_histogram(largest_cc)
    # average degree
    _avg_degree = 0
    for node in G.nodes():
        _avg_degree += nx.degree(G, node)
    avg_degree = float(_avg_degree) / num_nodes 

    _avg_degree = 0
    for node in G.nodes():
        _avg_degree += nx.degree(G, node)
    avg_degree_lcc = float(_avg_degree) / size_largest_cc 

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
    
    # assortativity
    assort = nx.degree_assortativity_coefficient(G)
    assort_lcc = nx.degree_assortativity_coefficient(largest_cc)

    print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING ASSORTATIVITY")

    # CLUSTERING, PATH LENGTH
    if compute_clustering:
        avg_shortest_path_length = nx.average_shortest_path_length(largest_cc)
        avg_clustering = nx.average_clustering(largest_cc)
        print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING CLUSTERING + PATH LENGTH")

    # CENTRALITIES FOR EACH NODE
    if compute_centralities:
        degree_centrality = nx.degree_centrality(G)  # returns dict of centralities
        mean_degree_centrality = 0.0
        for node in degree_centrality.keys():
            mean_degree_centrality += degree_centrality[node]
        try:
            mean_degree_centrality = mean_degree_centrality / len(degree_centrality)
        except:
            mean_degree_centrality = 0.0

        print(str(datetime.datetime.now()) + "      << FINISHED COMPUTING DEGREE CENTRALITY")
        
        eigenvector_centrality = nx.eigenvector_centrality(G)
        mean_eigenvector_centrality = 0.0
        for node in eigenvector_centrality.keys():
            mean_eigenvector_centrality += eigenvector_centrality[node]
        try:
            mean_eigenvector_centrality = mean_eigenvector_centrality / len(eigenvector_centrality)
        except:
            mean_eigenvector_centrality = 0.0

        print(str(datetime.datetime.now()) + "      << FINISHED COMPUTING EIGENVECTOR CENTRALITY")
        # closeness_centrality = nx.closeness_centrality(G)
        # betweenness_centrality = nx.betweenness_centrality(G)
        print(str(datetime.datetime.now()) + "    << FINISHED COMPUTING CENTRALITIES")

    
    # DONE
    print(str(datetime.datetime.now()) + "  << COMPLETED NETWORK ANALYSIS")

    out_text = "num_nodes;num_edges;num_conn_comp;size_largest_cc;avg_degree;avg_degree-lcc;assort;assort-lcc"
    if compute_clustering:
        out_text += ";avg_shortest_path_length-lcc;average_clustering-lcc"
    if compute_centralities:
        out_text += ";deg_cent-lcc;ev_cent-lcc"
    out_text += "\n"

    out_text += str(num_nodes) + ";" + str(num_edges) + ";" \
        + str(num_connected_components) + ";" + str(size_largest_cc) + ";" + str(round(avg_degree,2)) + ";" + str(round(avg_degree_lcc,2)) + ";" \
        + str(assort) + ";" + str(assort_lcc)
    if compute_clustering:
        out_text += ";" + str(avg_shortest_path_length) + ";" + str(avg_clustering)
    if compute_centralities:
        out_text += ";" + str(mean_degree_centrality) + ";" + str(mean_eigenvector_centrality)
    out_text += "\n"

    out_file = open(output_filename, "w")
    out_file.write(out_text)
    out_file.close()
    

    out_text = "node;ev_centrality;deg_centrality\n"
    for node in degree_centrality.keys():
        out_text += str(node) + ";" + str(eigenvector_centrality[node]) + ";" + str(degree_centrality[node]) + "\n"
    
    cent_file = open(cent_filename, "w")
    cent_file.write(out_text)
    cent_file.close()

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
