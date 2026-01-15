# Graph: negative_shortcut - Observations

*Generated: 2026-01-15T15:45:38.136603*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 6 |
| Edges | 8 |
| Density | 0.267 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 5 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 1 → 4 → 5
- **Total Distance**: 4
- **Iterations**: 6
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully (WARNING: Graph has negative weights - result may be incorrect)

### Bellman-Ford Algorithm

- **Path Found**: 0 → 1 → 4 → 5
- **Total Distance**: 4
- **Iterations**: 2
- **Success**: ✓ Yes
- **Negative Cycle Detected**: No
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 1 → 4 → 5
- **Total Distance**: 4.0
- **Final Energy**: 4.0
- **Total Iterations**: 88
- **Convergence Iteration**: 38
- **Success**: ✓ Yes
- **Convergence Pattern**: monotonic_decrease
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Quantum-inspired used significantly more iterations (88 vs 6/2)

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 4 | 4 | 4.0 |
| Iterations | 6 | 2 | 88 |
| Success | ✓ | ✓ | ✓ |
| Paths Match | ✓ Same | ✓ Same | ✓ Same |
