#!/usr/bin/env python3

import argparse
import csv
import multiprocessing as mp
import os
import random
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm

_ADJ = None
_DEPTH = None


def init_worker(adj, depth):
    global _ADJ, _DEPTH
    _ADJ = adj
    _DEPTH = depth


def kstep_counts(seed):
    adj = _ADJ
    depth = _DEPTH
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


def load_manifest(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"policy", "multiplier", "sim_id", "n_nodes", "file"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Manifest missing columns: {', '.join(sorted(missing))}")
    return df


def read_edgelist(path: Path, n_nodes: int):
    edges = []
    with path.open("r") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if len(row) < 2:
                continue
            edges.append((str(row[0]).strip(), str(row[1]).strip()))
    graph = nx.DiGraph()
    graph.add_nodes_from(str(i) for i in range(1, n_nodes + 1))
    graph.add_edges_from(edges)
    return graph


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute contagion on AI simulated edgelists."
    )
    parser.add_argument("ai_data_dir", help="Directory with manifest.csv and edgelists/")
    parser.add_argument("--depth", type=int, default=6)
    parser.add_argument("--runs", type=int, default=256)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", dest="output_dir", default=None)
    parser.add_argument(
        "--policies",
        default=None,
        help="Comma-separated policy labels to run (default: all in manifest).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ai_data_dir = Path(args.ai_data_dir)
    manifest_path = ai_data_dir / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(manifest_path)

    output_dir = Path(args.output_dir) if args.output_dir else ai_data_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_manifest(manifest_path)
    if args.policies:
        policies = {p.strip() for p in args.policies.split(",") if p.strip()}
        df = df[df["policy"].isin(policies)]
    if df.empty:
        raise ValueError("No simulations found for requested policies.")

    methods = mp.get_all_start_methods()
    ctx = mp.get_context("fork" if "fork" in methods else "spawn")

    for policy, group in df.groupby("policy"):
        group = group.sort_values("sim_id")
        out_path = output_dir / f"ai_c2_{policy}.csv"
        with out_path.open("w") as handle:
            for _, row in tqdm(group.iterrows(), total=group.shape[0], desc=f"{policy}", mininterval=1.0):
                sim_id = int(row["sim_id"])
                n_nodes = int(row["n_nodes"])
                rel_path = str(row["file"])
                edgelist_path = ai_data_dir / rel_path
                if not edgelist_path.exists():
                    raise FileNotFoundError(edgelist_path)

                graph = read_edgelist(edgelist_path, n_nodes).reverse()
                nodes = list(graph.nodes())
                if not nodes:
                    raise RuntimeError(f"Graph has no nodes for {edgelist_path}")

                rng = random.Random(args.seed + sim_id)
                seeds = [rng.choice(nodes) for _ in range(args.runs)]

                adj = {node: list(graph.successors(node)) for node in nodes}

                sums = np.zeros(args.depth, dtype=float)
                with ProcessPoolExecutor(
                    max_workers=args.workers,
                    mp_context=ctx,
                    initializer=init_worker,
                    initargs=(adj, args.depth),
                ) as executor:
                    for counts in tqdm(
                        executor.map(kstep_counts, seeds),
                        total=len(seeds),
                        desc="runs",
                        mininterval=1.0,
                        leave=False,
                    ):
                        sums += np.asarray(counts, dtype=float)

                means = sums / float(args.runs)
                handle.write(str(sim_id))
                for value in means:
                    handle.write(f";{value}")
                handle.write("\n")

        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
