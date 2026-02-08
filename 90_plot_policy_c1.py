#!/usr/bin/env python3

import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
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


def percent_to_k(n_nodes: int, pct: int) -> int:
    return max(1, math.ceil(n_nodes * (pct / 100.0)))


STYLES = {
    "model": ("black", "solid", "o", "Model"),
    "indeg": ("red", (0, (5, 3)), "o", "Indegree"),
    "ef": ("blue", (0, (3, 2, 1, 2)), "o", "Exp. Fatality"),
    "betef": ("magenta", (0, (1, 2)), "o", "Betweenness + Exp. Fatality"),
}


def _plot_series_on_ax(ax, steps, series, title, legend_title, ylim=None):
    """Helper to draw series on a given Axes object."""
    min_mean = None
    max_mean = None
    for key, values in series.items():
        color, linestyle, marker, label = STYLES[key]
        means = values["mean"]
        ax.plot(steps, means, color=color, linestyle=linestyle, marker=marker, label=label)
        local_min = np.nanmin(means)
        local_max = np.nanmax(means)
        min_mean = local_min if min_mean is None else min(min_mean, local_min)
        max_mean = local_max if max_mean is None else max(max_mean, local_max)

    ax.set_title(title)
    ax.set_xlabel("Step")
    ax.set_ylabel("Mean K-step Systemicness")
    if ylim is not None:
        ax.set_ylim(ylim)
    elif min_mean is not None and max_mean is not None:
        if np.isfinite(min_mean) and np.isfinite(max_mean):
            if min_mean == max_mean:
                pad = max(1.0, 0.05 * max_mean)
            else:
                pad = 0.05 * (max_mean - min_mean)
            ax.set_ylim(max(0.0, min_mean - pad), max_mean + pad)
    ax.legend(title=legend_title)


def plot_policy(
    steps: np.ndarray,
    series: dict,
    out_path: Path,
    title: str,
    legend_title: str,
    ylim=None,
):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    _plot_series_on_ax(ax, steps, series, title, legend_title, ylim=ylim)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_policy_panel(
    steps: np.ndarray,
    panels: list,
    out_path: Path,
    ylim=None,
):
    """Create a multi-panel figure (one column per panel).

    Parameters
    ----------
    panels : list of dict
        Each dict has keys 'series', 'title', 'legend_title'.
    """
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(5.5 * n, 4.5), sharey=True)
    if n == 1:
        axes = [axes]
    for ax, panel in zip(axes, panels):
        _plot_series_on_ax(
            ax, steps, panel["series"], panel["title"], panel["legend_title"],
            ylim=ylim,
        )
    # Only label y-axis on leftmost panel
    for ax in axes[1:]:
        ax.set_ylabel("")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


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
        "--top-counts",
        default=None,
        help="Comma-separated top-N levels to plot (e.g., 10,100,1000).",
    )
    parser.add_argument(
        "--skip-missing",
        action="store_true",
        help="Skip percent levels if required files are missing.",
    )
    parser.add_argument(
        "--suffix",
        default="",
        help="Suffix appended to CSV filenames before .csv (e.g. '_lam0.5').",
    )
    parser.add_argument(
        "--ylim",
        default=None,
        type=float,
        nargs=2,
        metavar=("YMIN", "YMAX"),
        help="Fixed y-axis limits (e.g. --ylim 0 350).",
    )
    parser.add_argument(
        "--panel",
        default=None,
        help=(
            "Comma-separated suffixes for a combined multi-panel figure "
            "(e.g. '_lam0.25,_lam0.5,_lam0.75'). "
            "Only used with --top-counts (first count only)."
        ),
    )
    parser.add_argument(
        "--panel-out",
        default=None,
        help="Output filename for the panel figure (e.g. 'policy_c1_lambda_panel.png').",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir) if args.out_dir else data_dir

    sfx = args.suffix
    baseline_path = data_dir / f"importance_{args.identifier}-{args.depth}{sfx}.csv"
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
    ylim_arg = tuple(args.ylim) if args.ylim else None

    baseline_mean, baseline_std = load_stats(baseline_path)
    steps = np.arange(1, len(baseline_mean) + 1)

    def warn_zero_std(label: str, stds: np.ndarray, path: Path):
        if stds is None:
            return
        if np.all(np.isnan(stds)) or np.allclose(np.nan_to_num(stds), 0.0):
            print(f"Warning: std is zero for {label} ({path})")

    def _load_series(k, suffix):
        bl_path = data_dir / f"importance_{args.identifier}-{args.depth}{suffix}.csv"
        if not bl_path.exists():
            raise FileNotFoundError(bl_path)
        bl_mean, bl_std = load_stats(bl_path)
        indeg_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_indeg{suffix}.csv"
        ef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_ef{suffix}.csv"
        betef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_betef{suffix}.csv"
        missing = [p for p in (indeg_path, ef_path, betef_path) if not p.exists()]
        if missing:
            raise FileNotFoundError(missing[0])
        indeg_stats = load_stats(indeg_path)
        ef_stats = load_stats(ef_path)
        betef_stats = load_stats(betef_path)
        return {
            "model": {"mean": bl_mean, "std": bl_std},
            "indeg": dict(zip(("mean", "std"), indeg_stats)),
            "ef": dict(zip(("mean", "std"), ef_stats)),
            "betef": dict(zip(("mean", "std"), betef_stats)),
        }

    if args.top_counts:
        top_counts = [int(p.strip()) for p in args.top_counts.split(",") if p.strip()]
        for k in top_counts:
            indeg_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_indeg{sfx}.csv"
            ef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_ef{sfx}.csv"
            betef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_betef{sfx}.csv"
            missing = [p for p in (indeg_path, ef_path, betef_path) if not p.exists()]
            if missing:
                if args.skip_missing:
                    print(f"Skipping top {k} (missing: {', '.join(str(p) for p in missing)})")
                    continue
                raise FileNotFoundError(missing[0])

            indeg_stats = load_stats(indeg_path)
            ef_stats = load_stats(ef_path)
            betef_stats = load_stats(betef_path)
            warn_zero_std("indeg", indeg_stats[1], indeg_path)
            warn_zero_std("ef", ef_stats[1], ef_path)
            warn_zero_std("betef", betef_stats[1], betef_path)

            series = {
                "model": {"mean": baseline_mean, "std": baseline_std},
                "indeg": dict(zip(("mean", "std"), indeg_stats)),
                "ef": dict(zip(("mean", "std"), ef_stats)),
                "betef": dict(zip(("mean", "std"), betef_stats)),
            }

            out_file = out_dir / f"policy_c1_top{k}{sfx}.png"
            plot_policy(
                steps,
                series,
                out_file,
                title="Mean K-step Simulation",
                legend_title=f"Targeting top {k} nodes based on",
                ylim=ylim_arg,
            )
    else:
        percents = [int(p.strip()) for p in args.percents.split(",") if p.strip()]
        for pct in percents:
            k = percent_to_k(n_nodes, pct)
            indeg_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_indeg{sfx}.csv"
            ef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_ef{sfx}.csv"
            betef_path = data_dir / f"importance_{args.identifier}-{k}-{args.depth}_betef{sfx}.csv"
            missing = [p for p in (indeg_path, ef_path, betef_path) if not p.exists()]
            if missing:
                if args.skip_missing:
                    print(f"Skipping {pct}% (missing: {', '.join(str(p) for p in missing)})")
                    continue
                raise FileNotFoundError(missing[0])

            indeg_stats = load_stats(indeg_path)
            ef_stats = load_stats(ef_path)
            betef_stats = load_stats(betef_path)
            warn_zero_std("indeg", indeg_stats[1], indeg_path)
            warn_zero_std("ef", ef_stats[1], ef_path)
            warn_zero_std("betef", betef_stats[1], betef_path)

            series = {
                "model": {"mean": baseline_mean, "std": baseline_std},
                "indeg": dict(zip(("mean", "std"), indeg_stats)),
                "ef": dict(zip(("mean", "std"), ef_stats)),
                "betef": dict(zip(("mean", "std"), betef_stats)),
            }

            out_file = out_dir / f"policy_c1_{pct}pct{sfx}.png"
            plot_policy(
                steps,
                series,
                out_file,
                title="Mean K-step Simulation",
                legend_title=f"Targeting {pct}% based on",
                ylim=ylim_arg,
            )

    # --- Combined multi-panel figure (e.g. for Online Appendix) ---
    if args.panel and args.top_counts:
        panel_suffixes = [s.strip() for s in args.panel.split(",") if s.strip()]
        k = top_counts[0]
        panels = []
        for ps in panel_suffixes:
            lam_val = ps.replace("_lam", "")
            series = _load_series(k, ps)
            panels.append({
                "series": series,
                "title": f"$\\lambda = {lam_val}$",
                "legend_title": f"Targeting top {k} nodes based on",
            })
        panel_out = out_dir / (args.panel_out or f"policy_c1_lambda_panel.png")
        plot_policy_panel(steps, panels, panel_out, ylim=ylim_arg)
        print(f"Panel figure saved to {panel_out}")


if __name__ == "__main__":
    main()
