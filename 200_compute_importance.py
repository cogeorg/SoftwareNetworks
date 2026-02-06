#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import argparse
import datetime
import os
import random
import sys

import networkx as nx
import numpy as np
from tqdm import tqdm


def random_shock(num_nodes):
    arr = np.zeros(num_nodes, dtype=int)
    random_index = random.randint(0, num_nodes - 1)
    random_index = 1
    arr[random_index] = 1
    return [random_index, arr.reshape(num_nodes, 1)]


def build_output_path(output_dir, output_name):
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_name)


def do_run(base_directory, identifier, depth, output_dir, output_name):
    np.set_printoptions(threshold=sys.maxsize)

    input_filename = os.path.join(base_directory, f"{identifier}.gexf")
    output_filename = build_output_path(output_dir, output_name)

    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print("<<<<<< WORKING ON: " + input_filename)

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

    for node in tqdm(graph.nodes()):
        infected_nodes = nx.descendants_at_distance(graph, node, 0)
        out_text = str(node) + ";" + str(len(infected_nodes)) + ";"

        for distance in range(1, depth):
            infected_nodes.update(nx.descendants_at_distance(graph, node, distance))
            out_text += str(len(infected_nodes)) + ";"

        out_file.write(out_text + "\n")

    out_file.close()
    print("  >> OUTPUT WRITTEN TO:" + output_filename)

    print(">>>>>> FINISHED")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute k-step contagion (systemicness) for each node."
    )
    parser.add_argument("base_directory")
    parser.add_argument("identifier")
    parser.add_argument("depth", type=int)
    parser.add_argument("--out-dir", dest="output_dir", default=None)
    parser.add_argument("--out-name", dest="output_name", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = args.output_dir if args.output_dir else args.base_directory
    output_name = (
        args.output_name
        if args.output_name
        else f"importance_{args.identifier}-{args.depth}.csv"
    )
    do_run(args.base_directory, args.identifier, args.depth, output_dir, output_name)
