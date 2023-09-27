#!/usr/local/bin/python3
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
# ##########################################################################

# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, input_file_name, output_identifier, sample_size):
    G = nx.DiGraph()
    # H = nx.DiGraph()

    print(str(datetime.datetime.now()) + " <<<<<< START WORKING ON: " + base_directory + input_file_name + " USING _NO_ SAMPLE SIZE: " + str(sample_size))
    G = nx.read_edgelist(base_directory + input_file_name, delimiter=";")

    if True:  # debugging
        print("    << " + str(datetime.datetime.now()) + " G: # Nodes: " + str(len(G.nodes())) + " # Edges: " + str(len(G.edges())))
    
    if sample_size != 0.0:
        print("    << " + str(datetime.datetime.now()) + " H: # Nodes: " + str(len(H.nodes())) + " # Edges: " + str(len(H.edges())))
    #     nx.write_gexf(H, base_directory + "sampled-" + str(sample_size) + "_" + output_identifier + ".gexf")
    else:
        nx.write_gexf(G, base_directory + output_identifier + ".gexf")

    print(str(datetime.datetime.now()) + " >>>>>> FINISHED")
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
    input_file_name = args[2]
    output_identifier = args[3]
    sample_size = float(args[4])

#
# CODE
#
    do_run(base_directory, input_file_name, output_identifier, sample_size)
