# Quantum-Inspired Shortest Path — Case Study

A comparative case study of three shortest-path algorithms on curated and randomly generated graphs, evaluating correctness, efficiency, and solution quality.

## Algorithms Compared

| Algorithm | Type | Handles Negative Weights |
|---|---|---|
| **Dijkstra's Algorithm** | Greedy / Priority-Queue | ❌ |
| **Bellman-Ford Algorithm** | Dynamic Programming | ✅ (+ detects negative cycles) |
| **Quantum-Inspired** | Energy-based Probabilistic Optimization | ✅ |

The quantum-inspired algorithm models path selection as an energy minimization problem, using temperature annealing and interference-like probability updates to explore the solution space without a quantum computer.

---

## Project Structure

```
Quantum_shortest_path/
├── src/
│   ├── algorithms/
│   │   ├── dijkstra.py               # Dijkstra with iteration history
│   │   ├── bellman_ford.py           # Bellman-Ford with negative-cycle detection
│   │   ├── quantum_inspired.py       # Quantum-inspired shortest path (standard)
│   │   ├── quantum_constrained.py    # Quantum variant: mandatory waypoints / forbidden zones
│   │   ├── quantum_multiobjective.py # Quantum variant: Pareto-front multi-objective search
│   │   ├── classical_constrained.py  # Classical baseline for constrained paths
│   │   └── classical_multiobjective.py
│   ├── evaluation/
│   │   ├── runner.py                 # Runs all 3 algorithms and collects results
│   │   ├── metrics.py                # Performance metric helpers
│   │   └── report_generator.py      # Markdown report generation
│   ├── visualization/
│   │   └── visualizer.py             # Graph + convergence plots (matplotlib)
│   ├── graph.py                      # Core Graph data structure
│   ├── graph_generator.py            # Curated test-graph factory (9 scenarios)
│   └── benchmark_generator.py        # Random benchmark-graph generator (20 graphs)
├── experiments/
│   ├── experiment_constrained.py     # Constrained-path experiment (waypoints / forbidden)
│   ├── experiment_multiobjective.py  # Multi-objective Pareto experiment
│   └── experiment_stochastic.py      # Stochastic / probabilistic edge-weight experiment
├── tests/
│   ├── test_algorithms.py
│   └── test_graph.py
├── main.py                           # Case-study entry point (9 curated graphs)
├── run_benchmark.py                  # Benchmark entry point  (20 random graphs)
└── requirements.txt
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Merril1704/Quantum-shortest-path-caseStudy.git
cd Quantum-shortest-path-caseStudy
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

### ▶ Case Study — 9 Curated Graphs

Runs all three algorithms on nine hand-crafted graphs designed to highlight specific algorithmic trade-offs (sparse, dense, negative weights, diamond paths, bottlenecks, etc.).

```bash
python main.py
```

Results are saved to `results/raw_results/` — one sub-folder per graph containing:
- `path_comparison.png` — side-by-side path visualizations
- `convergence.png` — iteration-by-iteration distance convergence
- `observations.md` — written observations
- `results.json` — raw numeric results

**Options:**

```bash
python main.py --output results/my_run   # Custom output directory
python main.py --seed 123               # Different random seed
python main.py --quiet                  # Suppress console output
```

---

### ▶ Benchmark — 20 Randomly Generated Graphs

Generates 20 random graphs spanning different sizes and densities and produces a comprehensive Markdown report.

```bash
python run_benchmark.py
```

Report saved to `results/benchmarks/benchmark_report.md`.

**Options:**

```bash
python run_benchmark.py --output results/my_benchmark
python run_benchmark.py --seed 99
python run_benchmark.py --quiet
```

---

### ▶ Specialised Experiments

Three additional experiments test the algorithms on non-standard problem variants where classical methods are structurally limited:

```bash
# Constrained paths: mandatory waypoints + forbidden zones
python experiments/experiment_constrained.py

# Multi-objective: Pareto-front search (minimise distance + hops simultaneously)
python experiments/experiment_multiobjective.py

# Stochastic edges: probabilistic / uncertain edge weights
python experiments/experiment_stochastic.py
```

---

### ▶ Tests

```bash
pytest tests/
```

---

## Key Findings

- **Dijkstra** is the fastest on positive-weight graphs and always optimal under its constraints.
- **Bellman-Ford** is the authoritative solver for graphs with negative weights; it also reliably detects negative cycles.
- **Quantum-Inspired** explores a broader solution space and becomes structurally advantageous in constrained and multi-objective scenarios where classical methods either fail or require combinatorial enumeration.

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `networkx` | ≥ 3.0 | Graph data structures |
| `matplotlib` | ≥ 3.7 | Visualizations |
| `numpy` | ≥ 1.24 | Numerical operations |
| `pytest` | ≥ 7.0 | Testing |

---

## License

This project is released for academic and educational purposes.
