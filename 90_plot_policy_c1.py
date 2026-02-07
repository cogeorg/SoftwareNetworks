#!/usr/bin/env python3

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def load_means(path: Path) -> np.ndarray:
    df = pd.read_csv(path, sep=";", header=None, dtype=str)
    if df.shape[1] > 1 and df.iloc[:, -1].isna().all():
        df = df.iloc[:, :-1]
    counts = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    return counts.mean(axis=0, skipna=True).to_numpy()


def percent_to_k(n_nodes: int, pct: int) -> int:
    return max(1, math.ceil(n_nodes * (pct / 100.0)))


def plot_policy(
    steps: np.ndarray,
    series: dict,
    out_path: Path,
    title: str,
    legend_title: str,
):
    styles = {
        "model": ("black", "solid", "o", "Model"),
        "indeg": ("red", (0, (5, 3)), "o", "Indegree"),
        "ef": ("blue", (0, (3, 2, 1, 2)), "o", "Exp. Fatality"),
        "betef": ("magenta", (0, (1, 2)), "o", "Betweenness + Exp. Fatality"),
    }

    plt.figure(figsize=(8, 4.5))
    for key, values in series.items():
        color, linestyle, marker, label = styles[key]
        plt.plot(steps, values, color=color, linestyle=linestyle, marker=marker, label=label)

    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Mean K-step Systemicness")
    plt.legend(title=legend_title)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate policy_c1_* figures from importance CSV outputs."
    )
    parser.add_argument("data_dir", help="Directory with importance_*.csv files")
    parser.add_argument("identifier", help="Graph identifier")
    parser.add_argument("depth", type=int, help="Depth used in importance files")
    parser.add_argument("--out-dir", default=None, help="Output directory for figures")
    parser.add_argument(
        "--graph-path",
        default=None,
        help="Path to the GEXF graph (used to compute node count).",
    )
    parser.add_argument(
        "--percents",
        default="1,5,10",
        help="Comma-separated percent levels to plot (default: 1,5,10).",
    )
    parser.add_argument(
        "--skip-missing",
        action="store_true",
        help="Skip percent levels if required files are missing.",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir) if args.out_dir else data_dir

    baseline_path = data_dir / f"importance_{args.identifier}-{args.depth}.csv"
    if not baseline_path.exists():
        raise FileNotFoundError(baseline_path)

    graph_path = Path(args.graph_path) if args.graph_path else None
    if graph_path is None:
        candidates = [
            data_dir / ".." / "30_data" / "Pypi" / f"{args.identifier}.gexf",
            data_dir / ".." / "30_data" / f"{args.identifier}.gexf",
            data_dir / f"{args.identifier}.gexf",
        ]
        for candidate in candidates:
            if candidate.exists():
                graph_path = candidate
                break

    if graph_path and graph_path.exists():
        graph = nx.read_gexf(graph_path)
        n_nodes = graph.number_of_nodes()
    else:
        baseline_df = pd.read_csv(baseline_path, sep=";", header=None)
        n_nodes = baseline_df.shape[0]
        print(
            "Warning: graph not found, inferring node count from baseline file. "
            "Pass --graph-path to ensure correct percent sizing."
        )
    baseline = load_means(baseline_path)
    steps = np.arange(1, len(baseline) + 1)

    percents = [int(p.strip()) for p in args.percents.split(",") if p.strip()]
    for pct in percents:
        k = percent_to_k(n_nodes, pct)
        indeg_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_indeg.csv"
        ef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_ef.csv"
        betef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_betef.csv"
        missing = [p for p in (indeg_path, ef_path, betef_path) if not p.exists()]
        if missing:
            if args.skip_missing:
                print(f"Skipping {pct}% (missing: {', '.join(str(p) for p in missing)})")
                continue
            raise FileNotFoundError(missing[0])

        series = {
            "model": baseline,
            "indeg": load_means(indeg_path),
            "ef": load_means(ef_path),
            "betef": load_means(betef_path),
        }

        out_file = out_dir / f"policy_c1_{pct}pct.png"
        plot_policy(
            steps,
            series,
            out_file,
            title="Mean K-step Simulation",
            legend_title=f"Targeting {pct}% based on",
        )


if __name__ == "__main__":
    main()
