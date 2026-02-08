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
_LAM = None


def init_worker(adj, depth, lam):
    global _ADJ, _DEPTH, _LAM
    _ADJ = adj
    _DEPTH = depth
    _LAM = lam


def kstep_counts(args):
    """BFS contagion from a single seed node.

    *args* is a tuple ``(seed_node, run_seed)`` where *run_seed* is used
    to initialise a per-run RNG for probabilistic transmission (lam < 1).
    When lam >= 1.0 the RNG is never consulted and transmission is
    deterministic.
    """
    seed_node, run_seed = args
    adj = _ADJ
    depth = _DEPTH
    lam = _LAM

    visited = {seed_node}
    frontier = [seed_node]
    counts = []

    if lam >= 1.0:
        # Fast deterministic path (original behaviour)
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
    else:
        rng = random.Random(run_seed)
        for _ in range(depth):
            counts.append(len(visited))
            if not frontier:
                continue
            next_frontier = []
            for node in frontier:
                for nbr in adj.get(node, ()):
                    if nbr not in visited and rng.random() < lam:
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


def load_seed_file(path: Path):
    """Read seed node IDs from a file (one per line)."""
    seeds = []
    with path.open("r") as handle:
        for line in handle:
            node = line.strip()
            if node:
                seeds.append(node)
    return seeds


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
    parser.add_argument(
        "--seed-file",
        default=None,
        help="File with pre-generated seed node IDs (one per line). "
        "Seeds not present in the (possibly protected) graph are skipped.",
    )
    parser.add_argument(
        "--lam",
        type=float,
        default=1.0,
        help="Transmission probability per edge (default: 1.0 = deterministic).",
    )
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
        graph.remove_nodes_from(protected)

    nodes = list(graph.nodes())
    if not nodes:
        raise RuntimeError("Graph has no nodes after protection.")
    node_set = set(nodes)

    # Build seed list -------------------------------------------------
    if args.seed_file:
        seed_file_path = (
            Path(args.seed_file)
            if os.path.isabs(args.seed_file)
            else base_directory / args.seed_file
        )
        all_seeds = load_seed_file(seed_file_path)
        # Keep only seeds that are present in the (possibly protected) graph
        seeds = [s for s in all_seeds if s in node_set]
        if not seeds:
            raise RuntimeError(
                f"No seeds from {seed_file_path} are present in the graph "
                f"(after protection). Check that node IDs match."
            )
        print(f"Loaded {len(seeds)} seeds from {seed_file_path} "
              f"({len(all_seeds) - len(seeds)} skipped as absent/protected)")
    else:
        rng = random.Random(args.seed)
        seeds = [rng.choice(nodes) for _ in range(args.runs)]

    # Per-run RNG seeds for probabilistic transmission ----------------
    master_rng = random.Random(args.seed)
    run_seeds = [master_rng.randint(0, 2**63) for _ in range(len(seeds))]
    work_items = list(zip(seeds, run_seeds))

    adj = {node: list(graph.successors(node)) for node in nodes}

    methods = mp.get_all_start_methods()
    ctx = mp.get_context("fork" if "fork" in methods else "spawn")

    with ProcessPoolExecutor(
        max_workers=args.workers,
        mp_context=ctx,
        initializer=init_worker,
        initargs=(adj, args.depth, args.lam),
    ) as executor:
        with output_path.open("w") as handle:
            for run_id, counts in enumerate(
                tqdm(executor.map(kstep_counts, work_items), total=len(work_items), desc="runs", mininterval=1.0)
            ):
                handle.write(str(run_id))
                for value in counts:
                    handle.write(f";{value}")
                handle.write("\n")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
