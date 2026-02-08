#!/usr/bin/env python3

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_stats(path: Path):
    df = pd.read_csv(path, sep=";", header=None, dtype=str)
    if df.shape[1] > 1 and df.iloc[:, -1].isna().all():
        df = df.iloc[:, :-1]
    counts = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    means = counts.mean(axis=0, skipna=True).to_numpy()
    stds = counts.std(axis=0, skipna=True, ddof=1).to_numpy()
    return means, stds


def plot_policy(steps: np.ndarray, series: dict, out_path: Path):
    styles = {
        "model": ("black", "solid", "o", "Model"),
        "c1pct": ("orange", (0, (5, 3)), "o", "1 percent"),
        "c5pct": ("green", (0, (3, 2, 1, 2)), "o", "5 percent"),
        "c10pct": ("red", (0, (1, 2)), "o", "10 percent"),
        "c20pct": ("blue", (0, (5, 2, 1, 2)), "o", "20 percent"),
        "c30pct": ("magenta", (0, (1, 1)), "o", "30 percent"),
    }

    plt.figure(figsize=(8, 4.5))
    min_mean = None
    max_mean = None
    for key, values in series.items():
        color, linestyle, marker, label = styles[key]
        means = values["mean"]
        plt.plot(steps, means, color=color, linestyle=linestyle, marker=marker, label=label)
        local_min = np.nanmin(means)
        local_max = np.nanmax(means)
        min_mean = local_min if min_mean is None else min(min_mean, local_min)
        max_mean = local_max if max_mean is None else max(max_mean, local_max)

    plt.title("Mean K-step Simulation")
    plt.xlabel("Step")
    plt.ylabel("Mean K-step Systemicness")
    if min_mean is not None and max_mean is not None:
        if np.isfinite(min_mean) and np.isfinite(max_mean):
            if min_mean == max_mean:
                pad = max(1.0, 0.05 * max_mean)
            else:
                pad = 0.05 * (max_mean - min_mean)
            plt.ylim(max(0.0, min_mean - pad), max_mean + pad)
    plt.legend(title="Relative increase\ncost of dependencies")
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate policy_c2 figure from AI contagion outputs."
    )
    parser.add_argument("data_dir", help="Directory with ai_c2_*.csv files")
    parser.add_argument("--out-dir", default=None, help="Output directory for figure")
    parser.add_argument(
        "--policies",
        default="model,c1pct,c5pct,c10pct,c20pct,c30pct",
        help="Comma-separated policy labels to plot.",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir) if args.out_dir else data_dir

    policies = [p.strip() for p in args.policies.split(",") if p.strip()]
    series = {}
    baseline = None
    for policy in policies:
        path = data_dir / f"ai_c2_{policy}.csv"
        if not path.exists():
            raise FileNotFoundError(path)
        mean, std = load_stats(path)
        series[policy] = {"mean": mean, "std": std}
        if baseline is None:
            baseline = mean

    steps = np.arange(1, len(next(iter(series.values()))["mean"]) + 1)
    out_path = out_dir / "policy_c2.png"
    plot_policy(steps, series, out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
