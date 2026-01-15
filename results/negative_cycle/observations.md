# Graph: negative_cycle - Observations

*Generated: 2026-01-15T15:45:39.531609*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 8 |
| Edges | 9 |
| Density | 0.161 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 5 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 1 → 2 → 3 → 4 → 5
- **Total Distance**: 15
- **Iterations**: 8
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully (WARNING: Graph has negative weights - result may be incorrect)

### Bellman-Ford Algorithm

- **Path Found**: No path found
- **Total Distance**: infinity
- **Iterations**: 7
- **Success**: ✗ No
- **Negative Cycle Detected**: ⚠ Yes
- **Convergence Pattern**: monotonic_decrease
- **Notes**: Negative cycle detected - no valid shortest path exists

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 1 → 2 → 6 → 7 → 5
- **Total Distance**: 16.0
- **Final Energy**: 16.0
- **Total Iterations**: 50
- **Convergence Iteration**: 0
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Bellman-Ford detected negative cycle
2. Quantum-inspired used significantly more iterations (50 vs 8/7)

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 15 | infinity | 16.0 |
| Iterations | 8 | 7 | 50 |
| Success | ✓ | ✗ | ✓ |
| Paths Match | Different | Different | Different |
