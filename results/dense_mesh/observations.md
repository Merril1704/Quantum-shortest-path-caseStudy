# Graph: dense_mesh - Observations

*Generated: 2026-01-15T15:45:37.667633*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 12 |
| Edges | 27 |
| Density | 0.409 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 11 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 2 → 3 → 6 → 10 → 11
- **Total Distance**: 11
- **Iterations**: 11
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Bellman-Ford Algorithm

- **Path Found**: 0 → 2 → 3 → 6 → 10 → 11
- **Total Distance**: 11
- **Iterations**: 2
- **Success**: ✓ Yes
- **Negative Cycle Detected**: No
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 3 → 7 → 11
- **Total Distance**: 19.0
- **Final Energy**: 19.0
- **Total Iterations**: 50
- **Convergence Iteration**: 0
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Quantum-inspired used significantly more iterations (50 vs 11/2)

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 11 | 11 | 19.0 |
| Iterations | 11 | 2 | 50 |
| Success | ✓ | ✓ | ✓ |
| Paths Match | Different | Different | Different |
