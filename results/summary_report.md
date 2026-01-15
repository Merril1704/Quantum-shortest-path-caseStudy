# Shortest Path Algorithm Comparison - Summary Report

## Overview

This report compares three shortest path algorithms across multiple graph configurations:

1. **Dijkstra's Algorithm** - Greedy, deterministic, non-negative weights only
2. **Bellman-Ford Algorithm** - Iterative relaxation, handles negative weights
3. **Quantum-Inspired Algorithm** - Probabilistic energy minimization

## Results Summary

| Graph | Nodes | Best Algorithm | Best Distance | Notes |
|-------|-------|----------------|---------------|-------|
| [sparse_basic](./sparse_basic/observations.md) | 8 | Dijkstra | 10 | Quantum-inspired used significantly more iteration... |
| [dense_mesh](./dense_mesh/observations.md) | 12 | Dijkstra | 11 | Quantum-inspired used significantly more iteration... |
| [negative_shortcut](./negative_shortcut/observations.md) | 6 | Dijkstra | 4 | Quantum-inspired used significantly more iteration... |
| [bottleneck](./bottleneck/observations.md) | 15 | Dijkstra | 13 | Quantum-inspired used significantly more iteration... |
| [diamond_paths](./diamond_paths/observations.md) | 7 | Dijkstra | 15 | Quantum-inspired used significantly more iteration... |
| [negative_cycle](./negative_cycle/observations.md) | 8 | Dijkstra | 15 | Bellman-Ford detected negative cycle... |

## Algorithm Performance by Graph Type

### Positive Weight Graphs
On graphs with only positive weights, all three algorithms typically find the same optimal path. 
Dijkstra's algorithm is most efficient in iteration count.

### Negative Weight Graphs
When negative weights are present:
- Dijkstra may find suboptimal paths (does not correctly handle negative weights)
- Bellman-Ford finds the true optimal path
- Quantum-Inspired can find optimal or near-optimal paths

### Graphs with Negative Cycles
- Bellman-Ford correctly detects negative cycles
- Other algorithms may produce incorrect results

## Key Findings

1. **Best algorithm counts**: Dijkstra: 6, Bellman-Ford: 0, Quantum-Inspired: 0
2. **Iteration efficiency**: Dijkstra uses fewest iterations on positive-weight graphs
3. **Correctness**: Bellman-Ford is the only algorithm guaranteed correct for all graph types
4. **Quantum-Inspired behavior**: Higher iteration count but can escape local optima