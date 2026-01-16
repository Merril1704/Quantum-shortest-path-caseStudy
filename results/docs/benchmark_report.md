# Benchmark Report: 20 Generated Graphs

*Generated: 2026-01-15T20:58:32.284249*
*Random Seed: 42*

## Executive Summary

This benchmark evaluates three shortest path algorithms across 20 randomly generated graphs:

1. **Dijkstra's Algorithm** - Greedy, optimal for non-negative weights
2. **Bellman-Ford Algorithm** - Handles negative weights, detects negative cycles
3. **Quantum-Inspired Algorithm** - Energy-based probabilistic optimization

### Key Metrics

- **Graphs Tested**: 20
- **Graphs with Negative Weights**: 5
- **Algorithm Win Counts**: Dijkstra: 20, Bellman-Ford: 0, Quantum-Inspired: 0
- **Success Rates**: Dijkstra: 20/20, Bellman-Ford: 20/20, Quantum-Inspired: 18/20

---

## Results Overview

| # | Graph Name | Nodes | Edges | Density | Neg Weights | Dijkstra | Bellman-Ford | Quantum | Best |
|---|------------|-------|-------|---------|-------------|----------|--------------|---------|------|
| 1 | benchmark_01_small_sparse | 6 | 8 | 0.267 | No | 11 | 11 | 11.0 | Dijkstra |
| 2 | benchmark_02_small_undirected | 7 | 8 | 0.381 | No | 16 | 16 | 17.0 | Dijkstra |
| 3 | benchmark_03_small_negative | 6 | 8 | 0.267 | Yes | 5 | 5 | 5.0 | Dijkstra |
| 4 | benchmark_04_medium_sparse | 10 | 20 | 0.222 | No | 9 | 9 | 9.0 | Dijkstra |
| 5 | benchmark_05_medium_undirected | 10 | 11 | 0.244 | No | 6 | 6 | 6.0 | Dijkstra |
| 6 | benchmark_06_medium_varied | 12 | 37 | 0.28 | No | 18 | 18 | 19.0 | Dijkstra |
| 7 | benchmark_07_medium_negative | 10 | 23 | 0.256 | Yes | 9 | 9 | 9.0 | Dijkstra |
| 8 | benchmark_08_dense_directed | 8 | 33 | 0.589 | No | 6 | 6 | 6.0 | Dijkstra |
| 9 | benchmark_09_dense_undirected | 8 | 17 | 0.607 | No | 6 | 6 | 6.0 | Dijkstra |
| 10 | benchmark_10_dense_negative | 8 | 32 | 0.571 | Yes | 3 | 3 | 8.0 | Dijkstra |
| 11 | benchmark_11_large_sparse | 15 | 34 | 0.162 | No | 15 | 15 | ∞ | Dijkstra |
| 12 | benchmark_12_large_undirected | 15 | 15 | 0.143 | No | 7 | 17 | 7.0 | Dijkstra |
| 13 | benchmark_13_large_medium | 15 | 54 | 0.257 | No | 8 | 8 | 8.0 | Dijkstra |
| 14 | benchmark_14_large_negative | 15 | 44 | 0.21 | Yes | 3 | 3 | 3.0 | Dijkstra |
| 15 | benchmark_15_xlarge_sparse | 20 | 40 | 0.105 | No | 15 | 15 | ∞ | Dijkstra |
| 16 | benchmark_16_high_connect | 10 | 65 | 0.722 | No | 2 | 2 | 2.0 | Dijkstra |
| 17 | benchmark_17_low_variance | 12 | 38 | 0.288 | No | 13 | 13 | 28.0 | Dijkstra |
| 18 | benchmark_18_high_variance | 12 | 43 | 0.326 | No | 31 | 31 | 79.0 | Dijkstra |
| 19 | benchmark_19_mixed | 10 | 22 | 0.489 | Yes | 6 | 6 | 6.0 | Dijkstra |
| 20 | benchmark_20_complex | 18 | 87 | 0.284 | No | 13 | 13 | 13.0 | Dijkstra |

---

## Detailed Observations by Graph

### 1. benchmark_01_small_sparse

**Description**: Small sparse directed graph (6 nodes) - baseline test

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 6 |
| Edges | 8 |
| Density | 0.267 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 5 |
| Avg Out-Degree | 1.33 |
| Avg Weight | 5.88 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 3 → 5
- Distance: 11
- Iterations: 5
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 3 → 5
- Distance: 11
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 3 → 5
- Distance: 11.0
- Final Energy: 11.0
- Iterations: 55
- Convergence at: 5
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 11
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (55 vs 5/2)

---

### 2. benchmark_02_small_undirected

**Description**: Small sparse undirected graph (7 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 7 |
| Edges | 8 |
| Density | 0.381 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 6 |
| Avg Out-Degree | 2.29 |
| Avg Weight | 4.5 |
| Weight Range | 1 to 9 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 1 → 2 → 4 → 5 → 6
- Distance: 16
- Iterations: 7
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 1 → 2 → 4 → 5 → 6
- Distance: 16
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 3 → 4 → 5 → 6
- Distance: 17.0
- Final Energy: 17.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 16
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 7/2)

---

### 3. benchmark_03_small_negative

**Description**: Small directed graph with negative weights (6 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 6 |
| Edges | 8 |
| Density | 0.267 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 5 |
| Avg Out-Degree | 1.33 |
| Avg Weight | 4.25 |
| Weight Range | -1 to 7 |
| Negative Edges | 1 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 3 → 5
- Distance: 5
- Iterations: 4
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 3 → 5
- Distance: 5
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 3 → 5
- Distance: 5.0
- Final Energy: 5.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 5
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 4/2)

---

### 4. benchmark_04_medium_sparse

**Description**: Medium sparse directed graph (10 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 10 |
| Edges | 20 |
| Density | 0.222 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 9 |
| Avg Out-Degree | 2.0 |
| Avg Weight | 5.55 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 6 → 9
- Distance: 9
- Iterations: 5
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 6 → 9
- Distance: 9
- Iterations: 4
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 6 → 9
- Distance: 9.0
- Final Energy: 9.0
- Iterations: 72
- Convergence at: 22
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 9
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (72 vs 5/4)

---

### 5. benchmark_05_medium_undirected

**Description**: Medium sparse undirected graph (10 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 10 |
| Edges | 11 |
| Density | 0.244 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 9 |
| Avg Out-Degree | 2.2 |
| Avg Weight | 5.82 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 9
- Distance: 6
- Iterations: 2
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 9
- Distance: 6
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 9
- Distance: 6.0
- Final Energy: 6.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 6
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 2/2)

---

### 6. benchmark_06_medium_varied

**Description**: Medium graph with high weight variance (12 nodes, weights 1-20)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 12 |
| Edges | 37 |
| Density | 0.28 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 11 |
| Avg Out-Degree | 3.08 |
| Avg Weight | 10.27 |
| Weight Range | 1 to 20 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 1 → 11
- Distance: 18
- Iterations: 8
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 1 → 11
- Distance: 18
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 8 → 11
- Distance: 19.0
- Final Energy: 19.0
- Iterations: 56
- Convergence at: 6
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 18
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (56 vs 8/3)

---

### 7. benchmark_07_medium_negative

**Description**: Medium directed graph with negative weights (10 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 10 |
| Edges | 23 |
| Density | 0.256 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 9 |
| Avg Out-Degree | 2.3 |
| Avg Weight | 5.52 |
| Weight Range | -2 to 10 |
| Negative Edges | 2 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 9
- Distance: 9
- Iterations: 3
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 9
- Distance: 9
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 9
- Distance: 9.0
- Final Energy: 9.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 9
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 3/3)

---

### 8. benchmark_08_dense_directed

**Description**: Dense directed graph (8 nodes, ~50% density)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 8 |
| Edges | 33 |
| Density | 0.589 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 7 |
| Avg Out-Degree | 4.12 |
| Avg Weight | 6.36 |
| Weight Range | 2 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 7
- Distance: 6
- Iterations: 6
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 7
- Distance: 6
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 7
- Distance: 6.0
- Final Energy: 6.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 6
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 6/2)

---

### 9. benchmark_09_dense_undirected

**Description**: Dense undirected graph (8 nodes, ~60% density)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 8 |
| Edges | 17 |
| Density | 0.607 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 7 |
| Avg Out-Degree | 4.25 |
| Avg Weight | 4.47 |
| Weight Range | 1 to 8 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 7
- Distance: 6
- Iterations: 5
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 7
- Distance: 6
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 7
- Distance: 6.0
- Final Energy: 6.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 6
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 5/2)

---

### 10. benchmark_10_dense_negative

**Description**: Dense directed graph with negative weights (8 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 8 |
| Edges | 32 |
| Density | 0.571 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 7 |
| Avg Out-Degree | 4.0 |
| Avg Weight | 5.47 |
| Weight Range | -1 to 10 |
| Negative Edges | 1 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 4 → 5 → 7
- Distance: 3
- Iterations: 7
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 4 → 5 → 7
- Distance: 3
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 7
- Distance: 8.0
- Final Energy: 8.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 3
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 7/2)

---

### 11. benchmark_11_large_sparse

**Description**: Large sparse directed graph (15 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 15 |
| Edges | 34 |
| Density | 0.162 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 14 |
| Avg Out-Degree | 2.27 |
| Avg Weight | 6.18 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 7 → 11 → 12 → 14
- Distance: 15
- Iterations: 11
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 7 → 11 → 12 → 14
- Distance: 15
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: No path found
- Distance: infinity
- Final Energy: 2000.0
- Iterations: 500
- Convergence at: 32
- Success: ✗

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 15
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (500 vs 11/3)

---

### 12. benchmark_12_large_undirected

**Description**: Large sparse undirected graph (15 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 15 |
| Edges | 15 |
| Density | 0.143 |
| Directed | No |
| Has Negative Weights | No |
| Source → Target | 0 → 14 |
| Avg Out-Degree | 2.0 |
| Avg Weight | 5.0 |
| Weight Range | 1 to 9 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 11 → 14
- Distance: 7
- Iterations: 6
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 9 → 14
- Distance: 17
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 11 → 14
- Distance: 7.0
- Final Energy: 7.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 7
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 6/2)
  - Dijkstra and Bellman-Ford found different paths

---

### 13. benchmark_13_large_medium

**Description**: Large medium-density directed graph (15 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 15 |
| Edges | 54 |
| Density | 0.257 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 14 |
| Avg Out-Degree | 3.6 |
| Avg Weight | 5.78 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 4 → 14
- Distance: 8
- Iterations: 4
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 4 → 14
- Distance: 8
- Iterations: 4
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 4 → 14
- Distance: 8.0
- Final Energy: 8.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 8
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 4/4)

---

### 14. benchmark_14_large_negative

**Description**: Large directed graph with negative weights (15 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 15 |
| Edges | 44 |
| Density | 0.21 |
| Directed | Yes |
| Has Negative Weights | Yes |
| Source → Target | 0 → 14 |
| Avg Out-Degree | 2.93 |
| Avg Weight | 5.0 |
| Weight Range | -5 to 10 |
| Negative Edges | 3 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 14
- Distance: 3
- Iterations: 2
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 14
- Distance: 3
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 14
- Distance: 3.0
- Final Energy: 3.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 3
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 2/3)

---

### 15. benchmark_15_xlarge_sparse

**Description**: Extra large sparse directed graph (20 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 20 |
| Edges | 40 |
| Density | 0.105 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 19 |
| Avg Out-Degree | 2.0 |
| Avg Weight | 5.75 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 1 → 19
- Distance: 15
- Iterations: 7
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 1 → 19
- Distance: 15
- Iterations: 5
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: No path found
- Distance: infinity
- Final Energy: 2000.0
- Iterations: 500
- Convergence at: 58
- Success: ✗

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 15
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (500 vs 7/5)

---

### 16. benchmark_16_high_connect

**Description**: High connectivity graph (10 nodes, ~70% density)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 10 |
| Edges | 65 |
| Density | 0.722 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 9 |
| Avg Out-Degree | 6.5 |
| Avg Weight | 5.02 |
| Weight Range | 1 to 10 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 9
- Distance: 2
- Iterations: 2
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 9
- Distance: 2
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 9
- Distance: 2.0
- Final Energy: 2.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 2
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 2/3)

---

### 17. benchmark_17_low_variance

**Description**: Low weight variance graph (12 nodes, weights 5-8)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 12 |
| Edges | 38 |
| Density | 0.288 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 11 |
| Avg Out-Degree | 3.17 |
| Avg Weight | 6.53 |
| Weight Range | 5 to 8 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 2 → 11
- Distance: 13
- Iterations: 6
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 2 → 11
- Distance: 13
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 4 → 9 → 8 → 11
- Distance: 28.0
- Final Energy: 28.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 13
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 6/2)

---

### 18. benchmark_18_high_variance

**Description**: High weight variance graph (12 nodes, weights 1-50)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 12 |
| Edges | 43 |
| Density | 0.326 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 11 |
| Avg Out-Degree | 3.58 |
| Avg Weight | 22.65 |
| Weight Range | 2 to 47 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 2 → 11
- Distance: 31
- Iterations: 7
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 2 → 11
- Distance: 31
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 5 → 10 → 8 → 7 → 11
- Distance: 79.0
- Final Energy: 79.0
- Iterations: 80
- Convergence at: 30
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 31
- **Paths Identical**: No
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (80 vs 7/2)

---

### 19. benchmark_19_mixed

**Description**: Mixed undirected graph with negative weights (10 nodes)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 10 |
| Edges | 22 |
| Density | 0.489 |
| Directed | No |
| Has Negative Weights | Yes |
| Source → Target | 0 → 9 |
| Avg Out-Degree | 4.4 |
| Avg Weight | 5.0 |
| Weight Range | -5 to 10 |
| Negative Edges | 1 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 9
- Distance: 6
- Iterations: 6
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 9
- Distance: 6
- Iterations: 2
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 9
- Distance: 6.0
- Final Energy: 6.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 6
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 6/2)

---

### 20. benchmark_20_complex

**Description**: Complex large directed graph (18 nodes, varied weights)

#### Graph Properties

| Property | Value |
|----------|-------|
| Nodes | 18 |
| Edges | 87 |
| Density | 0.284 |
| Directed | Yes |
| Has Negative Weights | No |
| Source → Target | 0 → 17 |
| Avg Out-Degree | 4.83 |
| Avg Weight | 14.0 |
| Weight Range | 1 to 30 |

#### Algorithm Results

**Dijkstra's Algorithm:**
- Path: 0 → 17
- Distance: 13
- Iterations: 10
- Success: ✓

**Bellman-Ford Algorithm:**
- Path: 0 → 17
- Distance: 13
- Iterations: 3
- Success: ✓

**Quantum-Inspired Algorithm:**
- Path: 0 → 17
- Distance: 13.0
- Final Energy: 13.0
- Iterations: 50
- Convergence at: 0
- Success: ✓

#### Comparison Summary

- **Best Algorithm**: Dijkstra
- **Best Distance**: 13
- **Paths Identical**: Yes
- **Key Observations**:
  - Quantum-inspired used significantly more iterations (50 vs 10/3)

---

## Analysis by Graph Category

### Performance by Graph Size

| Category | Graphs | Dijkstra Avg Iter | BF Avg Iter | QI Avg Iter |
|----------|--------|-------------------|-------------|-------------|
| Small (≤8 nodes) | 6 | 5.7 | 2.0 | 50.8 |
| Medium (9-12 nodes) | 8 | 4.9 | 2.6 | 57.2 |
| Large (>12 nodes) | 6 | 6.7 | 3.3 | 200.0 |

### Negative Weight Graph Analysis

Performance on graphs containing negative edge weights:

- **Total graphs with negative weights**: 5
- **Dijkstra matched Bellman-Ford**: 5/5 graphs


---

## Conclusions

### Algorithm Strengths

1. **Dijkstra's Algorithm**
   - Most iteration-efficient on positive-weight graphs
   - Deterministic and predictable behavior
   - Limitation: May produce incorrect results with negative weights

2. **Bellman-Ford Algorithm**
   - Correctly handles all graph types including negative weights
   - Detects negative cycles
   - Higher iteration count but guaranteed correctness

3. **Quantum-Inspired Algorithm**
   - Probabilistic approach can explore diverse solution space
   - May find alternative valid paths
   - Highest iteration count; solution quality varies

### Recommendations

- Use **Dijkstra** for graphs with only positive weights when efficiency is critical
- Use **Bellman-Ford** when correctness is paramount or negative weights may exist
- Use **Quantum-Inspired** for exploration or when traditional algorithms don't converge well
