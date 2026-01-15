# Graph: diamond_paths - Observations

*Generated: 2026-01-15T15:45:39.124455*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 7 |
| Edges | 8 |
| Density | 0.381 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 6 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 1 → 3 → 4 → 6
- **Total Distance**: 15
- **Iterations**: 7
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Bellman-Ford Algorithm

- **Path Found**: 0 → 1 → 3 → 4 → 6
- **Total Distance**: 15
- **Iterations**: 2
- **Success**: ✓ Yes
- **Negative Cycle Detected**: No
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 2 → 3 → 4 → 6
- **Total Distance**: 15.0
- **Final Energy**: 15.0
- **Total Iterations**: 73
- **Convergence Iteration**: 23
- **Success**: ✓ Yes
- **Convergence Pattern**: oscillating
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Quantum-inspired used significantly more iterations (73 vs 7/2)

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 15 | 15 | 15.0 |
| Iterations | 7 | 2 | 73 |
| Success | ✓ | ✓ | ✓ |
| Paths Match | Different | Different | Different |
