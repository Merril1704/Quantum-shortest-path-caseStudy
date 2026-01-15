# Graph: bottleneck - Observations

*Generated: 2026-01-15T15:45:38.564232*

## Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 15 |
| Edges | 26 |
| Density | 0.124 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 14 |

## Algorithm Results

### Dijkstra's Algorithm

- **Path Found**: 0 → 3 → 6 → 7 → 8 → 12 → 14
- **Total Distance**: 13
- **Iterations**: 15
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Bellman-Ford Algorithm

- **Path Found**: 0 → 3 → 5 → 7 → 8 → 12 → 14
- **Total Distance**: 13
- **Iterations**: 2
- **Success**: ✓ Yes
- **Negative Cycle Detected**: No
- **Convergence Pattern**: plateau
- **Notes**: Path found successfully

### Quantum-Inspired Algorithm

- **Path Found**: 0 → 3 → 6 → 7 → 10 → 12 → 14
- **Total Distance**: 15.0
- **Final Energy**: 15.0
- **Total Iterations**: 50
- **Convergence Iteration**: 0
- **Success**: ✓ Yes
- **Convergence Pattern**: plateau
- **Notes**: Valid path found via energy minimization

## Key Differences Observed

1. Quantum-inspired used significantly more iterations (50 vs 15/2)
2. Dijkstra and Bellman-Ford found different paths

## Summary Comparison

| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |
|--------|----------|--------------|------------------|
| Distance | 13 | 13 | 15.0 |
| Iterations | 15 | 2 | 50 |
| Success | ✓ | ✓ | ✓ |
| Paths Match | Different | Different | Different |
