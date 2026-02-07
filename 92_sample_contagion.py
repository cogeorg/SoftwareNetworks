#!/usr/bin/env python3

import argparse
import multiprocessing as mp
import os
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import networkx as nx
from tqdm import tqdm

_ADJ = None
_DEPTH = None
_PROTECTED = None


def init_worker(adj, depth, protected):
    global _ADJ, _DEPTH, _PROTECTED
    _ADJ = adj
    _DEPTH = depth
    _PROTECTED = protected


def kstep_counts(seed):
    adj = _ADJ
    depth = _DEPTH
    if _PROTECTED and seed in _PROTECTED:
        return [0] * depth
    visited = {seed}
    frontier = [seed]
    counts = []
    for _ in range(depth):
        counts.append(len(visited))
        if not frontier:
            continue
        next_frontier = []
        for node in frontier:
            for nbr in adj.get(node, ()):
                if nbr not in visited:
                    visited.add(nbr)
                    next_frontier.append(nbr)
        frontier = next_frontier
    return counts


def load_protected(path: Path, num_protected: int):
    protected = []
    with path.open("r") as handle:
        for line in handle:
            if len(protected) >= num_protected:
                break
            node = line.strip().split(";")[0]
            if node:
                protected.append(node)
    return set(protected)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sample contagion runs and write importance-style CSV."
    )
    parser.add_argument("base_directory")
    parser.add_argument("identifier")
    parser.add_argument("depth", type=int)
    parser.add_argument("--runs", type=int, default=1024)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--protect-file", default=None)
    parser.add_argument("--num-protected", type=int, default=None)
    parser.add_argument("--protect-label", default=None)
    parser.add_argument("--out-dir", dest="output_dir", default=None)
    parser.add_argument("--out-name", dest="output_name", default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    base_directory = Path(args.base_directory)
    graph_path = base_directory / f"{args.identifier}.gexf"
    output_dir = Path(args.output_dir) if args.output_dir else base_directory
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.output_name:
        output_name = args.output_name
    else:
        if args.protect_file and args.num_protected and args.protect_label:
            output_name = (
                f"importance_{args.identifier}-{args.num_protected}-{args.depth}_{args.protect_label}.csv"
            )
        else:
            output_name = f"importance_{args.identifier}-{args.depth}.csv"
    output_path = output_dir / output_name

    graph = nx.read_gexf(graph_path).reverse()

    protected = set()
    if args.protect_file and args.num_protected:
        protect_path = (
            Path(args.protect_file)
            if os.path.isabs(args.protect_file)
            else base_directory / args.protect_file
        )
        protected = load_protected(protect_path, args.num_protected)

    nodes = list(graph.nodes())
    if not nodes:
        raise RuntimeError("Graph has no nodes after protection.")

    rng = random.Random(args.seed)
    seeds = [rng.choice(nodes) for _ in range(args.runs)]

    adj = {node: list(graph.successors(node)) for node in nodes}

    methods = mp.get_all_start_methods()
    ctx = mp.get_context("fork" if "fork" in methods else "spawn")

    with ProcessPoolExecutor(
        max_workers=args.workers,
        mp_context=ctx,
        initializer=init_worker,
        initargs=(adj, args.depth, protected),
    ) as executor:
        with output_path.open("w") as handle:
            for run_id, counts in enumerate(
                tqdm(executor.map(kstep_counts, seeds), total=len(seeds), desc="runs", mininterval=1.0)
            ):
                handle.write(str(run_id))
                for value in counts:
                    handle.write(f";{value}")
                handle.write("\n")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
