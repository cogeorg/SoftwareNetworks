#!/usr/bin/env python3

import random
import subprocess
import sys
from pathlib import Path
from typing import Optional

import networkx as nx
import unittest

ROOT_DIR = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent
DATA_DIR = TEST_DIR / "data"
OUTPUT_DIR = TEST_DIR / "output"
PYTHON = sys.executable


def write_gexf(graph: nx.DiGraph, name: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"{name}.gexf"
    nx.write_gexf(graph, path)
    return path


def write_protection(name: str, nodes) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / name
    with path.open("w") as handle:
        for node in nodes:
            handle.write(f"{node}\n")
    return path


def bfs_counts(graph: nx.DiGraph, seed: str, depth: int):
    visited = {seed}
    frontier = [seed]
    counts = []
    for _ in range(depth):
        counts.append(len(visited))
        if not frontier:
            continue
        next_frontier = []
        for node in frontier:
            for nbr in graph.successors(node):
                if nbr not in visited:
                    visited.add(nbr)
                    next_frontier.append(nbr)
        frontier = next_frontier
    return counts


def run_contagion(
    identifier: str,
    depth: int,
    runs: int,
    seed: int,
    out_name: str,
    protect_file: Optional[str] = None,
    num_protected: Optional[int] = None,
    protect_label: Optional[str] = None,
):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / out_name
    if out_path.exists():
        out_path.unlink()

    cmd = [
        PYTHON,
        str(ROOT_DIR / "92_sample_contagion.py"),
        str(DATA_DIR),
        identifier,
        str(depth),
        "--runs",
        str(runs),
        "--workers",
        "1",
        "--seed",
        str(seed),
        "--out-dir",
        str(OUTPUT_DIR),
        "--out-name",
        out_name,
    ]
    if protect_file and num_protected and protect_label:
        cmd.extend(
            [
                "--protect-file",
                protect_file,
                "--num-protected",
                str(num_protected),
                "--protect-label",
                protect_label,
            ]
        )

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return out_path


class TestContagion(unittest.TestCase):
    def test_line_graph_counts(self):
        g = nx.DiGraph()
        g.add_edges_from([("0", "1"), ("1", "2"), ("2", "3")])
        write_gexf(g, "line")

        out_path = run_contagion(
            identifier="line",
            depth=4,
            runs=5,
            seed=123,
            out_name="importance_line-4.csv",
        )

        graph = nx.read_gexf(DATA_DIR / "line.gexf").reverse()
        nodes = list(graph.nodes())
        rng = random.Random(123)
        seeds = [rng.choice(nodes) for _ in range(5)]
        expected = [bfs_counts(graph, seed, 4) for seed in seeds]

        lines = out_path.read_text().strip().splitlines()
        self.assertEqual(len(lines), 5)
        for line, exp in zip(lines, expected, strict=True):
            parts = [int(x) for x in line.split(";")[1:]]
            self.assertEqual(parts, exp)

    def test_protection_removes_center(self):
        center = "C"
        leaves = [f"L{i}" for i in range(5)]
        g = nx.DiGraph()
        g.add_edges_from([(leaf, center) for leaf in leaves])
        write_gexf(g, "star")
        write_protection("protection_star.csv", [center])

        out_path = run_contagion(
            identifier="star",
            depth=3,
            runs=6,
            seed=7,
            out_name="importance_star-3_test.csv",
            protect_file="protection_star.csv",
            num_protected=1,
            protect_label="test",
        )

        lines = out_path.read_text().strip().splitlines()
        for line in lines:
            parts = [int(x) for x in line.split(";")[1:]]
            self.assertEqual(parts, [1, 1, 1])

    def test_random_graph_consistency(self):
        g = nx.gnp_random_graph(64, 0.05, seed=123, directed=True)
        g = nx.relabel_nodes(g, lambda n: str(n))
        write_gexf(g, "rand64")

        out_path = run_contagion(
            identifier="rand64",
            depth=3,
            runs=8,
            seed=99,
            out_name="importance_rand64-3.csv",
        )

        graph = nx.read_gexf(DATA_DIR / "rand64.gexf").reverse()
        nodes = list(graph.nodes())
        rng = random.Random(99)
        seeds = [rng.choice(nodes) for _ in range(8)]
        expected = [bfs_counts(graph, seed, 3) for seed in seeds]

        lines = out_path.read_text().strip().splitlines()
        self.assertEqual(len(lines), 8)
        for line, exp in zip(lines, expected, strict=True):
            parts = [int(x) for x in line.split(";")[1:]]
            self.assertEqual(parts, exp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
