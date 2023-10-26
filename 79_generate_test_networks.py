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
def do_run(base_directory, identifier, num_nodes, network_type, net_param1):
    output_filename = base_directory + "/" + identifier + "_" + network_type + "_" + str(num_nodes) + "_"  + str(net_param1) + ".gexf"
    
    if network_type == "fast_gnp":
        G = nx.fast_gnp_random_graph(num_nodes, net_param1, directed=True)
        nx.write_gexf(G, output_filename)
        print("  >> FILE WRITTEN TO:" + output_filename)

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
    num_nodes = int(args[3])
    network_type = args[4]
    net_param1 = float(args[5])

#
# CODE
#
    do_run(base_directory, identifier, num_nodes, network_type, net_param1)
