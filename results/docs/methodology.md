# Case Study Methodology: Shortest Path Algorithm Comparison

This document describes the experimental setup and implementation details for comparing Dijkstra's, Bellman-Ford, and Energy-Based Quantum-Inspired shortest path algorithms.

---

## 5. Case Study Setup

### 5.1 Graph Configuration

The case study employs a dual-layered testing strategy combining **curated test graphs** designed to expose specific algorithmic behaviors with **randomly generated benchmark graphs** for broader validation.

#### Curated Test Graphs (6 Graphs)

Hand-crafted graphs designed to challenge each algorithm's core characteristics:

| Graph Name | Nodes | Edges | Type | Special Feature |
|------------|-------|-------|------|-----------------|
| `sparse_basic` | 8 | 10 | Directed | Greedy trap — direct path appears optimal but longer path is cheaper |
| `dense_mesh` | 12 | 27 | Undirected | Many alternative paths with varied weights |
| `negative_shortcut` | 6 | 8 | Directed | Contains negative edge (4→5, weight=-6) creating a cheaper path |
| `bottleneck` | 15 | 26 | Directed | All paths must traverse a single chokepoint (node 7) |
| `diamond_paths` | 7 | 8 | Undirected | Two equal-cost optimal paths — tests tie-breaking behavior |
| `negative_cycle` | 8 | 9 | Directed | Contains a negative cycle (2→6→7→2, sum=-3) |

#### Benchmark Graphs (20 Graphs)

Automatically generated graphs with diverse configurations:

| Category | Count | Node Range | Density Range | Negative Weights |
|----------|-------|------------|---------------|------------------|
| Small sparse | 3 | 6–7 | 0.20–0.38 | 1 graph |
| Medium sparse | 4 | 10–12 | 0.22–0.29 | 2 graphs |
| Medium/high dense | 3 | 8 | 0.57–0.61 | 1 graph |
| Large sparse | 3 | 15 | 0.14–0.16 | 1 graph |
| Large/XL | 4 | 15–20 | 0.10–0.28 | 0 graphs |
| Special config (high connect, variance tests) | 3 | 10–12 | 0.29–0.72 | 0 graphs |

**Generation Constraints:**
- All graphs guaranteed to have a valid path from source to target
- No negative cycles in benchmark graphs (to ensure Dijkstra/BF can find valid solutions)
- Reproducible via fixed random seed (default: 42)

### 5.2 Algorithms Compared

The following three algorithms are evaluated under identical conditions:

#### 1. Dijkstra's Algorithm
```
Type: Deterministic, greedy
Data Structure: Min-heap priority queue
Time Complexity: O(V log V + E)
Edge Weight Support: Non-negative only
```

**Implementation Details:**
- Uses `heapq` for priority queue operations
- Tracks per-iteration state: current node, distance map, visited set, tentative paths
- Early termination upon reaching target node
- Includes warning detection for negative weights (results may be incorrect)

#### 2. Bellman–Ford Algorithm
```
Type: Deterministic, iterative edge relaxation
Passes Required: V-1 (plus one for cycle detection)
Time Complexity: O(V × E)
Edge Weight Support: Negative weights, negative cycle detection
```

**Implementation Details:**
- Relaxes all edges in each pass
- Tracks per-iteration state: distances, relaxation counts, edges relaxed
- Early termination when no relaxations occur
- Explicit negative cycle detection via V-th pass

#### 3. Energy-Based Quantum-Inspired Algorithm
```
Type: Probabilistic, optimization-driven (simulated annealing-style)
Approach: Energy minimization with Metropolis acceptance criterion
Iteration Limit: 500 (configurable)
Edge Weight Support: Any weights (no cycle detection)
```

**Implementation Details:**
- **Energy Function:** `E(path) = Σ edge_weights + λ × constraint_violations`
- **Constraint Penalty (λ):** 1000.0 (default) — penalizes non-existent edges, incorrect endpoints
- **Temperature Schedule:** Initial = 10.0, cooling rate = 0.98 per iteration
- **Acceptance Rule:** Always accept improvements; accept worse moves with probability `exp(-ΔE / T)`
- **Convergence:** Stops after 50 stable iterations (no improvement)
- **Neighbor Generation:** Random operations — swap, insert, remove, replace intermediate nodes

### 5.3 Evaluation Criteria

The evaluation emphasizes **behavioral and conceptual comparison** rather than raw performance benchmarking.

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| **Path Correctness** | Does the algorithm find the optimal shortest path? | Core measure of algorithm effectiveness |
| **Convergence Behavior** | How do solutions evolve over iterations? | Reveals optimization dynamics and stability |
| **Iteration Count** | Number of updates required to stabilize | Measures computational effort for comparison |
| **Solution Stability** | Consistency across multiple runs (for stochastic methods) | Important for probabilistic algorithms |
| **Failure Modes** | How does the algorithm behave on edge cases? | Identifies limitations and applicable domains |
| **Sensitivity to Graph Structure** | Performance on sparse vs dense, small vs large graphs | Determines when each algorithm is appropriate |

### 5.4 Experimental Controls

To ensure fair comparison:
- **Same graphs** used for all three algorithms
- **Same source–target pairs** per graph
- **Fixed random seed** (42) for reproducibility of quantum-inspired results
- **No low-level optimizations** — focus on algorithmic behavior, not implementation speed
- **Identical output format** — standardized result structures with iteration history

---

## 6. Implementation Overview

The implementation prioritizes **clarity, reproducibility, and educational value** over production optimization.

### 6.1 Project Architecture

```
Quantum_shortest_path/
├── main.py                      # CLI for curated graph comparison
├── run_benchmark.py             # CLI for 20-graph benchmark suite
├── src/
│   ├── graph.py                 # Graph data structure (adjacency list)
│   ├── graph_generator.py       # Curated test graph definitions
│   ├── benchmark_generator.py   # Random graph generator with constraints
│   ├── algorithms/
│   │   ├── dijkstra.py          # Dijkstra with iteration tracking
│   │   ├── bellman_ford.py      # Bellman-Ford with cycle detection
│   │   └── quantum_inspired.py  # Energy-based probabilistic algorithm
│   ├── evaluation/
│   │   ├── runner.py            # Algorithm execution wrapper
│   │   └── report_generator.py  # Markdown report generation
│   └── visualization/
│       └── visualizer.py        # Graph and convergence plotting
├── results/                     # Generated output (per-graph + summaries)
└── tests/                       # Unit tests for all components
```

### 6.2 Key Implementation Choices

#### Graph Representation
```python
class Graph:
    """Weighted graph supporting directed and undirected edges."""
    def __init__(self, directed: bool = True):
        self._adj: Dict[int, Dict[int, float]] = defaultdict(dict)
        self._nodes: Set[int] = set()
```
- **Adjacency list** representation for efficient neighbor traversal
- Supports both **directed** and **undirected** graphs
- Handles **positive and negative** edge weights
- Provides utility methods: `density()`, `has_negative_weights()`, `to_adjacency_matrix()`

#### Algorithm Result Structures

Each algorithm returns a **dataclass** containing:

| Field | Type | Description |
|-------|------|-------------|
| `path` | `List[int]` or `None` | Ordered sequence of nodes from source to target |
| `distance` | `float` | Total path weight (∞ if no path found) |
| `iterations` | `int` | Number of algorithm iterations executed |
| `history` | `List[*Iteration]` | Per-iteration state snapshots |
| `success` | `bool` | Whether a valid path was found |
| `message` | `str` | Human-readable status message |

*Bellman-Ford additionally includes:* `has_negative_cycle: bool`

*Quantum-Inspired additionally includes:* `energy`, `convergence_iteration`, `stability_runs`

#### Iteration History Tracking

All algorithms record detailed iteration state for analysis:

```python
# Dijkstra records per-node expansion
@dataclass
class DijkstraIteration:
    iteration: int
    current_node: int
    distances: Dict[int, float]
    visited: set
    tentative_path: Dict[int, List[int]]

# Bellman-Ford records per-pass relaxations
@dataclass
class BellmanFordIteration:
    iteration: int
    distances: Dict[int, float]
    relaxations_made: int
    edges_relaxed: List[tuple]

# Quantum-Inspired records optimization trajectory
@dataclass
class QuantumIteration:
    iteration: int
    current_path: List[int]
    current_energy: float
    temperature: float
    accepted_transition: bool
    path_valid: bool
```

### 6.3 Quantum-Inspired Algorithm Details

The quantum-inspired implementation uses **simulated annealing** concepts with a custom energy function:

#### Energy Function
```python
def _calculate_energy(graph, path, source, target, constraint_penalty):
    energy = 0.0
    violations = 0
    
    # Constraint violations: wrong source/target endpoints
    if path[0] != source: violations += 1
    if path[-1] != target: violations += 1
    
    # Sum edge weights; penalize non-existent edges
    for i in range(len(path) - 1):
        weight = graph.get_weight(path[i], path[i+1])
        if weight is not None:
            energy += weight
        else:
            violations += 2  # Heavy penalty for invalid edges
    
    return energy + constraint_penalty * violations
```

#### Neighbor Generation

Four mutation operations with equal probability:

1. **Swap** — Exchange two intermediate nodes
2. **Insert** — Add a random unvisited node
3. **Remove** — Delete an intermediate node
4. **Replace** — Substitute an intermediate node with a random one

#### Hyperparameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `max_iterations` | 500 | Upper bound on optimization steps |
| `initial_temperature` | 10.0 | Starting temperature for Metropolis criterion |
| `cooling_rate` | 0.98 | Multiplicative decay per iteration |
| `constraint_penalty` | 1000.0 | Multiplier for constraint violations |
| `stability_threshold` | 50 | Iterations without improvement before early stop |

### 6.4 Observations Recorded Per Run

For each graph-algorithm combination, the following are logged:

| Category | Data Captured |
|----------|---------------|
| **Input** | Graph structure, node/edge counts, source–target pair |
| **Output** | Final path, total distance, success status |
| **Process** | Full iteration history, convergence point |
| **Comparison** | Distance delta vs optimal, path differences |

### 6.5 Reproducibility

- **Deterministic algorithms** (Dijkstra, Bellman-Ford): Identical output on every run
- **Stochastic algorithm** (Quantum-Inspired): Reproducible via `seed` parameter (default: 42)
- **Benchmark graphs**: Regenerated identically using fixed seed

### 6.6 Output Artifacts

The implementation generates comprehensive output:

```
results/
├── summary_report.md           # Cross-graph comparison table
├── methodology.md              # This document
├── analysis_and_discussions.md # Detailed findings and conclusions
├── benchmark/
│   └── benchmark_report.md     # 20-graph benchmark analysis
├── sparse_basic/
│   ├── observations.md         # Detailed behavioral notes
│   ├── graph_info.md           # Graph specification
│   ├── path_comparison.png     # Visual overlay of all paths
│   ├── convergence.png         # Iteration-by-iteration progress
│   └── results.json            # Machine-readable results
├── dense_mesh/
│   └── ...
└── [other graphs]/
```

### 6.7 Validation

The implementation includes:
- **Graph complexity validation**: Ensures meaningful comparison (sufficient edges, reachable target)
- **Algorithm correctness tests**: Unit tests verifying expected behavior on known graphs
- **Negative cycle detection**: Bellman-Ford correctly identifies and reports cycles
- **Path validity checking**: All returned paths verified for edge existence

---

## 7. Running the Experiments

### 7.1 Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
```

**Required packages:**
- `matplotlib` — for visualization
- `networkx` — for graph layouts (visualization only)

### 7.2 Running Curated Graph Comparison

```bash
# Run comparison on 6 curated test graphs
python main.py --output results --seed 42

# Quiet mode (suppress console output)
python main.py -q
```

**Output:** Individual results in `results/<graph_name>/` directories plus `summary_report.md`

### 7.3 Running Benchmark Suite

```bash
# Run 20-graph benchmark
python run_benchmark.py --output results/benchmark --seed 42
```

**Output:** Comprehensive `benchmark_report.md` with cross-graph analysis

### 7.4 Customization

```python
# Adjust quantum-inspired hyperparameters
from src.algorithms.quantum_inspired import quantum_inspired_shortest_path

result = quantum_inspired_shortest_path(
    graph, source, target,
    max_iterations=1000,        # Increase for complex graphs
    initial_temperature=20.0,   # Higher for more exploration
    cooling_rate=0.95,          # Slower cooling
    constraint_penalty=500.0,   # Lower penalty for softer constraints
    stability_threshold=100,    # Longer stable period before stopping
    seed=42
)
```

---

*This implementation serves to demonstrate and compare algorithm behavior, not to claim computational superiority. The focus is on observable differences in decision-making, convergence patterns, and failure modes.*

---

*Document generated: 2026-01-16*
*Benchmark seed: 42*
