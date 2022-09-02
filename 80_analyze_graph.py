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
def do_run(base_directory, identifier, output_filename, task):
    input_filename = base_directory + identifier + "-merged.gexf"
    print("<<<<<< WORKING ON: " + input_filename)
    
    print(str(datetime.datetime.now()) + "  << START READING .gexf FILE")
    G = nx.read_gexf(input_filename)
    print(str(datetime.datetime.now()) + "  >> COMPLETE READING .gexf FILE")

    if task == "sample_graph":
        sample_graph_filename = base_directory + identifier + "-sampled.gexf"
        H = nx.DiGraph()
        for u,v in G.edges():
            if random.random() < 0.01:  # we add only one percent of all edges
                H.add_edge(u,v)
        nx.write_gexf(H, sample_graph_filename)
        print("  >>> SAMPLED GRAPH WRITTEN TO:" + sample_graph_filename)

    # print("  >>> FILES WRITTEN TO:" + base_directory + output_filename)
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
    output_filename = args[3]
    task = args[4]


#
# CODE
#
    do_run(base_directory, identifier, output_filename, task)
