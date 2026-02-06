#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import argparse
import datetime
import os
import sys

import networkx as nx
import numpy as np


def compute_ef(graph, node):
    ef_value = 0.0
    for neighbor in list(nx.neighbors(graph, node)):
        try:
            ef_value += 1.0 / len(list(nx.neighbors(graph, neighbor)))
        except ZeroDivisionError:
            pass
    return ef_value


def build_output_path(output_dir, output_name):
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_name)


def do_run(base_directory, identifier, output_dir, output_name):
    np.set_printoptions(threshold=sys.maxsize)

    input_filename = os.path.join(base_directory, f"{identifier}.gexf")
    output_filename = build_output_path(output_dir, output_name)

    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print(str(datetime.datetime.now()) + " <<<<< WORKING ON: " + input_filename)

    graph = nx.read_gexf(input_filename).reverse()

    num_nodes = graph.number_of_nodes()
    print(
        str(datetime.datetime.now())
        + "    << NETWORK WITH "
        + str(num_nodes)
        + " NODES AND "
        + str(graph.number_of_edges())
        + " EDGES FOUND"
    )

    out_file = open(output_filename, "a")

    centralities = nx.betweenness_centrality(graph, normalized=False)
    for node in graph.nodes():
        expected_fatality = compute_ef(graph, node)
        out_text = (
            str(node)
            + ";"
            + str(centralities[node])
            + ";"
            + str(expected_fatality)
            + ";"
            + str(graph.out_degree(node))
        )
        out_file.write(out_text + "\n")

    out_file.close()
    print(str(datetime.datetime.now()) + "    >> OUTPUT WRITTEN TO:" + output_filename)

    print(str(datetime.datetime.now()) + " >>>>> FINISHED")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute centrality and expected fatality measures."
    )
    parser.add_argument("base_directory")
    parser.add_argument("identifier")
    parser.add_argument("--out-dir", dest="output_dir", default=None)
    parser.add_argument("--out-name", dest="output_name", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = args.output_dir if args.output_dir else args.base_directory
    output_name = (
        args.output_name
        if args.output_name
        else f"centrality_{args.identifier}.csv"
    )
    do_run(args.base_directory, args.identifier, output_dir, output_name)
