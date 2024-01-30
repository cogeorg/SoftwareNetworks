#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import datetime

import networkx as nx
import numpy as np
from tqdm import tqdm

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier):
    np.set_printoptions(threshold=sys.maxsize)

    debug = False

    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "centrality_" + identifier + ".csv"
    
    # ensure file is empty
    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print(str(datetime.datetime.now()) + " <<<<< WORKING ON: " + input_filename)

    G = nx.read_gexf(input_filename).reverse()  # TODO: CHECK THAT THIS IS THE RIGHT DIRECTION OF LINKS; LOOKS CORRECT FOR REAL GRAPH, THOUGH
    # H = G.subgraph(max(nx.weakly_connected_components(G), key=len))
    
    num_nodes = G.number_of_nodes()
    print(str(datetime.datetime.now()) + "    << NETWORK WITH " + str(num_nodes) + " NODES AND " + str(G.number_of_edges()) + " EDGES FOUND" )

    if False:
        print(type(G))
        print(G.nodes())
        print(G.edges())

    # appending results continuously for large networks
    out_file = open(output_filename, "a")

    centralities = nx.betweenness_centrality(G, normalized=False)
    # [current_node, p] = random_shock(num_nodes)
    for i in G.nodes():
        out_text = str(i) + ";" + str(centralities[i])

        if False:
            print(i, ":", str(centralities[i]))

        out_file.write(out_text + "\n") # + ";" + str(infected_nodes) + 
    
    out_file.close()
    print(str(datetime.datetime.now()) + "    >> OUTPUT WRITTEN TO:" + output_filename)

    # for from_node in G.nodes():
    #     for to_node in G.nodes():
    #         try:
    #             paths = [p for p in nx.all_shortest_paths(G, source=from_node, target=to_node)]
    #         except nx.NetworkXNoPath:
    #             paths = []
    #         print(from_node, to_node, paths)
    print(str(datetime.datetime.now()) + " >>>>> FINISHED")
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
