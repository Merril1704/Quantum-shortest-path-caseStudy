# Tables and Figures for Analysis

This document contains summary tables and figure references for the case study analysis.

---

## Table 1: Aggregate Results Summary (Section 7.1)

Summary comparison across all 26 graphs (6 curated + 20 benchmark).

| Metric | Dijkstra | Bellman–Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| **Optimal paths found** | 24/26 (92%) | 26/26 (100%) | 13/26 (50%) |
| **Suboptimal paths** | 2/26 (8%)* | 0/26 (0%) | 11/26 (42%) |
| **Failed to find path** | 0/26 (0%) | 0/26 (0%) | 2/26 (8%) |
| **Average iterations** | 5.6 | 2.8 | 94.7 |
| **Handles negative weights** | ❌ | ✅ | ✅ |
| **Negative cycle detection** | ❌ | ✅ | ❌ |
| **Deterministic** | ✅ | ✅ | ❌ (seeded) |

*Dijkstra's suboptimal results occur only on graphs with negative weights, where correctness is not guaranteed.

### Iteration Count Comparison

| Graph Category | Dijkstra (avg) | Bellman–Ford (avg) | Quantum-Inspired (avg) |
|----------------|----------------|--------------------|-----------------------|
| Small (6–7 nodes) | 5.3 | 2.0 | 51.7 |
| Medium (8–12 nodes) | 5.4 | 2.6 | 53.7 |
| Large (15–20 nodes) | 5.5 | 3.4 | 171.4 |

---

## Table 2: Solution Quality Distribution (Section 7.2)

Breakdown of solution quality across the quantum-inspired algorithm results.

| Outcome | Count | Percentage | Description |
|---------|-------|------------|-------------|
| **Optimal** | 13 | 50% | Found the same shortest path as classical algorithms |
| **Suboptimal** | 11 | 42% | Found a valid path, but not the shortest |
| **Failed** | 2 | 8% | Did not find a valid path within iteration limit |
| **Total** | 26 | 100% | — |

### Failure Analysis

| Failed Graph | Nodes | Density | Cause |
|--------------|-------|---------|-------|
| benchmark_11_large_sparse | 15 | 0.162 | Sparse structure limited valid neighbour transitions |
| benchmark_15_xlarge_sparse | 20 | 0.105 | Low connectivity prevented convergence to valid path |

---

## Table 3: Algorithm Characteristics Comparison (Section 7.4)

Side-by-side comparison of fundamental algorithm properties.

| Characteristic | Dijkstra | Bellman–Ford | Quantum-Inspired |
|----------------|----------|--------------|------------------|
| **Paradigm** | Greedy, priority-based | Iterative edge relaxation | Energy minimisation (annealing) |
| **Time Complexity** | O(V log V + E) | O(V × E) | O(iterations × path length) |
| **Optimality Guarantee** | Yes (non-negative weights) | Yes (no negative cycles) | No (approximate) |
| **Reproducibility** | Deterministic | Deterministic | Stochastic (seeded) |
| **Negative Weights** | Not supported | Fully supported | Supported (no detection) |
| **Negative Cycle Detection** | N/A | Yes | No |
| **Convergence Pattern** | Monotonic | Pass-based diminishing | Non-monotonic (oscillatory) |
| **Best Use Case** | Large sparse graphs, non-negative weights | Graphs with negative edges | Exploratory analysis, path diversity |
| **Iteration Efficiency** | Highest | High | Low |
| **Implementation Complexity** | Medium | Low | Medium-High |

---

## Table 4: Performance by Graph Structure (Section 7.1)

How each algorithm performs across different graph configurations.

| Graph Type | Dijkstra Performance | Bellman–Ford Performance | Quantum-Inspired Performance |
|------------|---------------------|-------------------------|------------------------------|
| **Small sparse** (6–7 nodes, <0.3 density) | ✅ Optimal, ~5 iterations | ✅ Optimal, ~2 iterations | ⚠️ Mixed, 50–55 iterations |
| **Medium dense** (8–12 nodes, >0.5 density) | ✅ Optimal, ~6 iterations | ✅ Optimal, ~2 iterations | ✅ Often optimal, ~50 iterations |
| **Large sparse** (15+ nodes, <0.2 density) | ✅ Optimal, ~8 iterations | ✅ Optimal, ~4 iterations | ❌ Often fails, 500 iterations |
| **Negative weights** | ⚠️ May be incorrect | ✅ Always correct | ⚠️ Mixed quality |
| **Negative cycles** | ❌ Undefined behaviour | ✅ Detects correctly | ❌ No detection |
| **Multiple equal paths** | ✅ Returns one | ✅ Returns one | ⚠️ May find alternatives |

### Legend
- ✅ Reliable, optimal performance
- ⚠️ Variable or conditional performance
- ❌ Unreliable or unsupported

---

## Figure References

The following figures support the analysis:

### Figure 1: Convergence Comparison
**Location**: `results/docs/convergence_comparison.png`
**Description**: Representative convergence behaviour showing the distinct patterns of each algorithm—Dijkstra's rapid monotonic convergence, Bellman–Ford's pass-based stabilisation, and Quantum-Inspired's oscillatory trajectory.

### Figure 2: Solution Quality Distribution
**Location**: `results/docs/solution_quality_chart.png`
**Description**: Pie chart visualising the quantum-inspired algorithm's solution quality breakdown: 50% optimal, 42% suboptimal, 8% failed.

### Figure 3: Iteration Count Comparison
**Location**: `results/docs/iteration_comparison.png`
**Description**: Bar chart comparing average iteration counts across algorithms and graph size categories.

### Figure 4: Algorithm Strengths Overview
**Location**: `results/docs/algorithm_strengths.png`
**Description**: Visual summary of each algorithm's key strengths for quick reference.

---

*Generated: 2026-01-16*
