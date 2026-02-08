# Test Suite (Contagion)

## Structure
- `test_contagion.py`: unit tests for contagion logic and protected-node handling.
- `data/`: generated small graph fixtures (GEXF) and protection lists.
- `output/`: generated outputs from test runs.

## Run
```
./test/run_tests.sh
```

## Tests (details)
### `test_line_graph_counts`
- **Input files created:** `data/line.gexf`
- **Output files:** `output/importance_line-4.csv`
- **Python entrypoint:** `92_sample_contagion.py` (CLI invoked by `run_contagion`)
- **Core routine exercised:** `kstep_counts` BFS expansion on the reversed graph
- **Expectation:** For the deterministic seeds generated with `seed=123`, the CSV rows match exact BFS counts for a 4‑node line graph (monotone non‑decreasing counts).

### `test_protection_removes_center`
- **Input files created:** `data/star.gexf`, `data/protection_star.csv`
- **Output files:** `output/importance_star-3_test.csv`
- **Python entrypoint:** `92_sample_contagion.py` with `--protect-file`, `--num-protected`, `--protect-label`
- **Core routine exercised:** protected-node removal in `92_sample_contagion.py` and subsequent BFS counts
- **Expectation:** All output rows are `1;1;1` (only the seed itself remains reachable after the hub is removed).

### `test_random_graph_consistency`
- **Input files created:** `data/rand64.gexf`
- **Output files:** `output/importance_rand64-3.csv`
- **Python entrypoint:** `92_sample_contagion.py`
- **Core routine exercised:** `kstep_counts` BFS expansion on a random 64‑node graph
- **Expectation:** CSV rows match BFS counts computed in‑test for the same deterministic seeds (`seed=99`).

## Notes
- Tests generate and overwrite fixtures under `data/` and `output/`.
- Keep new test graphs and outputs confined to these folders.
