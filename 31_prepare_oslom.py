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
    input_filename = base_directory + identifier + "-merged.dat"
    node_dict = {}

    print(str(datetime.datetime.now()) + " <<<<<< START WORKING ON: " + input_filename)

    G = nx.read_edgelist(input_filename)
    _i = 0
    for node in G.nodes():
        try:
            node_dict[node] = _i
            _i += 1 
        except:
            pass

    key_filename = base_directory + "key_" + identifier + "-merged.dat"
    key_text = "key;node_id\n"
    for key in node_dict.keys():
        key_text += key + ";" + str(node_dict[key]) + "\n"
    key_file = open(key_filename, "w")
    key_file.write(key_text)
    key_file.close()

    out_text = ""
    for u,v in G.edges():
        out_text += str(node_dict[u]) + " " + str(node_dict[v]) + "\n"

    output_filename = base_directory + "enc_" + identifier + "-merged.dat"
    output_file = open(output_filename, "w")
    output_file.write(out_text)
    output_file.close()

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
