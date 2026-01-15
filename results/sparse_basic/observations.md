# Graph: sparse_basic - Observations

*Generated: 2026-01-15T15:45:36.915214*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 8 |
| Edges | 10 |
| Density | 0.179 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 7 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 3 → 4 → 5 → 7
- **Total Distance**: 10
- **Iterations**: 8
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Bellman-Ford Algorithm

- **Path Found**: 0 → 3 → 4 → 5 → 7
- **Total Distance**: 10
- **Iterations**: 2
- **Success**: ✓ Yes
- **Negative Cycle Detected**: No
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 6 → 7
- **Total Distance**: 17.0
- **Final Energy**: 17.0
- **Total Iterations**: 50
- **Convergence Iteration**: 0
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Quantum-inspired used significantly more iterations (50 vs 8/2)

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 10 | 10 | 17.0 |
| Iterations | 8 | 2 | 50 |
| Success | ✓ | ✓ | ✓ |
| Paths Match | Different | Different | Different |
