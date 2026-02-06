#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import argparse
import datetime
import os
import sys

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm


def nodes_to_protect(protect_path, num_protected):
    df = pd.read_csv(protect_path, delimiter=";", header=None)
    nodes = df.iloc[:num_protected, 0].values.astype(str)
    return nodes


def resolve_protect_path(base_directory, protect_filename):
    if os.path.isabs(protect_filename):
        return protect_filename
    return os.path.join(base_directory, protect_filename)


def build_output_path(output_dir, output_name):
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, output_name)


def do_run(
    base_directory,
    identifier,
    protect_filename,
    depth,
    num_protected,
    protection,
    output_dir,
    output_name,
):
    np.set_printoptions(threshold=sys.maxsize)

    input_filename = os.path.join(base_directory, f"{identifier}.gexf")
    output_filename = build_output_path(output_dir, output_name)

    out_file = open(output_filename, "w")
    out_file.write("")
    out_file.close()

    print("<<<<<< WORKING ON: " + input_filename)

    graph = nx.read_gexf(input_filename).reverse()
    print(
        str(datetime.datetime.now())
        + "    << NETWORK WITH "
        + str(graph.number_of_nodes())
        + " NODES AND "
        + str(graph.number_of_edges())
        + " EDGES FOUND"
    )

    protect_path = resolve_protect_path(base_directory, protect_filename)
    protected_nodes = nodes_to_protect(protect_path, num_protected)
    graph.remove_nodes_from(protected_nodes)

    print(
        str(datetime.datetime.now())
        + "    << NETWORK WITH "
        + str(graph.number_of_nodes())
        + " NODES AND "
        + str(graph.number_of_edges())
        + " EDGES CONSTRUCTED"
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
        description="Compute k-step contagion after protecting nodes."
    )
    parser.add_argument("base_directory")
    parser.add_argument("identifier")
    parser.add_argument("protect_filename")
    parser.add_argument("depth", type=int)
    parser.add_argument("num_protected", type=int)
    parser.add_argument("protection")
    parser.add_argument("--out-dir", dest="output_dir", default=None)
    parser.add_argument("--out-name", dest="output_name", default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = args.output_dir if args.output_dir else args.base_directory
    output_name = (
        args.output_name
        if args.output_name
        else f"importance_{args.identifier}-{args.num_protected}-{args.depth}_{args.protection}.csv"
    )
    do_run(
        args.base_directory,
        args.identifier,
        args.protect_filename,
        args.depth,
        args.num_protected,
        args.protection,
        output_dir,
        output_name,
    )
