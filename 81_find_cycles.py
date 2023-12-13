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
def find_cycles_length_1(graph):
    cycles_length_1 = []
    for node in graph.nodes():
        if node in graph.successors(node):
            cycles_length_1.append([node])
    return cycles_length_1

def find_cycles_length_2(graph):
    cycles_length_2 = []
    for node in graph.nodes():
        for neighbor1 in graph.successors(node):
            if node in graph.successors(neighbor1):
                cycles_length_2.append([node, neighbor1, node])
    return cycles_length_2

def find_cycles_length_3(graph):
    cycles_length_3 = []
    for node in graph.nodes():
        for neighbor1 in graph.successors(node):
            for neighbor2 in graph.successors(neighbor1):
                if node in graph.successors(neighbor2):
                    cycles_length_3.append([node, neighbor1, neighbor2, node])
    return cycles_length_3

def find_cycles_length_4(graph):
    cycles_length_4 = []
    for node in graph.nodes():
        for neighbor1 in graph.successors(node):
            for neighbor2 in graph.successors(neighbor1):
                for neighbor3 in graph.successors(neighbor2):
                    if node in graph.successors(neighbor3):
                        cycles_length_4.append([node, neighbor1, neighbor2, neighbor3, node])
    return cycles_length_4

def find_cycles_length_5(graph):
    cycles_length_5 = []

    for node in graph.nodes():
        for neighbor1 in graph.successors(node):
            for neighbor2 in graph.successors(neighbor1):
                for neighbor3 in graph.successors(neighbor2):
                    for neighbor4 in graph.successors(neighbor3):
                        if node in graph.successors(neighbor4):
                            cycles_length_5.append([node, neighbor1, neighbor2, neighbor3, neighbor4, node])

    return cycles_length_5

def find_cycles_length_6(graph):
    cycles_length_6 = []

    for node in graph.nodes():
        for neighbor1 in graph.successors(node):
            for neighbor2 in graph.successors(neighbor1):
                for neighbor3 in graph.successors(neighbor2):
                    for neighbor4 in graph.successors(neighbor3):
                        for neighbor5 in graph.successors(neighbor4):
                            if node in graph.successors(neighbor5):
                                cycles_length_6.append([node, neighbor1, neighbor2, neighbor3, neighbor4, neighbor5, node])

    return cycles_length_6
# -------------------------------------------------------------------------
# do_run(file_name)
# -------------------------------------------------------------------------
def do_run(base_directory, identifier):
    input_filename = base_directory + identifier + ".gexf"
    output_filename = base_directory + "cycles_" + identifier + ".csv"
    out_text = "1;2;3;4;5;6\n"

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
    # cycles = nx.simple_cycles(G)
    # for entry in cycles:
    #     out_text += str(entry) + "\n"

    cycles_length_1 = find_cycles_length_1(G)
    cycles_length_2 = find_cycles_length_2(G)
    cycles_length_3 = find_cycles_length_3(G)
    print(str(datetime.datetime.now()) + "      << FINISHED WORKING ON CYCLES LENGTH 3")
    cycles_length_4 = find_cycles_length_4(G)
    print(str(datetime.datetime.now()) + "      << FINISHED WORKING ON CYCLES LENGTH 4")
    cycles_length_5 = find_cycles_length_5(G)
    print(str(datetime.datetime.now()) + "      << FINISHED WORKING ON CYCLES LENGTH 5")
    cycles_length_6 = find_cycles_length_6(G)
    print(str(datetime.datetime.now()) + "      << FINISHED WORKING ON CYCLES LENGTH 6")

    out_text += str(len(cycles_length_1)) + ";" + str(len(cycles_length_2)) + ";" + str(len(cycles_length_3)) + ";" + str(len(cycles_length_4)) + ";" + str(len(cycles_length_5)) + ";" + str(len(cycles_length_6))

    out_file = open(output_filename, "w")
    out_file.write(out_text)
    out_file.close()
    print(out_text)
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
