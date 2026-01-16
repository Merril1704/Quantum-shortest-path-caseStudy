# Case Study Setup

## Overview

This case study prioritises conceptual clarity and observational depth over raw performance evaluation. By carefully controlling the experimental environment, the study enables meaningful insights into the behavioural characteristics of three distinct shortest path algorithms: Dijkstra's algorithm, the Bellman–Ford algorithm, and an energy-based quantum-inspired algorithm.

## Graph Configuration

### Design Philosophy

The graphs are intentionally constrained to small and medium-sized instances (five to twenty nodes), enabling detailed observation of algorithmic behaviour that would be obscured in large-scale datasets. This supports both quantitative metrics and qualitative analysis of how each algorithm navigates the problem space.

### Edge Characteristics

All graphs employ weighted edges with positive numerical values in most cases. Select test graphs include negative edge weights to examine algorithmic behaviour under conditions where not all algorithms are guaranteed to produce correct results. Both directed and undirected configurations are supported, depending on the specific test case.

### Curated Test Graphs

Six hand-crafted graphs form the first testing layer, each designed to expose specific algorithmic behaviours:

- **Sparse Basic** (8 nodes, 10 directed edges): A greedy trap where the direct path appears optimal but is more expensive than an alternative route.
- **Dense Mesh** (12 nodes, 27 undirected edges): A highly interconnected structure testing navigation through complex solution spaces.
- **Negative Shortcut** (6 nodes, 8 directed edges): Contains a negative edge weight creating a cheaper path than positive-weight alternatives.
- **Bottleneck** (15 nodes, 26 directed edges): All paths must traverse a single intermediate node, creating a chokepoint.
- **Diamond Paths** (7 nodes, 8 undirected edges): Exactly two equal-cost optimal paths, testing tie-breaking behaviour.
- **Negative Cycle** (8 nodes, 9 directed edges): Contains a negative cycle for testing detection capabilities.

### Benchmark Graphs

Twenty automatically generated benchmark graphs provide broader validation across diverse configurations, spanning six to twenty nodes with varying density levels. A subset includes negative edge weights, though all exclude negative cycles. All benchmark graphs use a fixed random seed for reproducibility.

## Algorithms Compared

### Selection Rationale

The three algorithms represent fundamentally different approaches: a greedy deterministic approach, an iterative relaxation approach, and a probabilistic optimisation approach. This diversity reveals fundamental contrasts in how algorithms conceptualise and solve the problem.

### Dijkstra's Algorithm

Dijkstra's algorithm represents the deterministic greedy paradigm, maintaining a priority queue of nodes ordered by tentative distance from the source. Nodes are finalised in order of increasing distance, with correctness guaranteed for non-negative edge weights. The implementation includes comprehensive state tracking and warnings for negative edge weight detection.

### Bellman–Ford Algorithm

Bellman–Ford adopts iterative edge relaxation, performing multiple passes over all edges. This approach correctly handles negative edge weights and can detect negative cycles. Distance estimates converge through diminishing updates across passes, with detailed per-pass information captured by the implementation.

### Energy-Based Quantum-Inspired Algorithm

The quantum-inspired algorithm treats shortest path finding as an optimisation task, minimising an energy function encoding path cost and constraint satisfaction. Operating through probabilistic acceptance of random perturbations with a cooling schedule, it can escape local minima but does not guarantee optimality.

## Evaluation Criteria

The evaluation framework emphasises behavioural comparison over raw performance benchmarking:

- **Path Correctness**: Whether the algorithm identifies a valid shortest path, with verification of path traversability.
- **Convergence Behaviour**: How solutions evolve over iterations—monotonic for Dijkstra's, pass-based for Bellman–Ford, and non-monotonic for the quantum-inspired approach.
- **Iteration Count**: Computational effort measured through node expansions, edge passes, or candidate evaluations respectively.
- **Sensitivity to Graph Structure**: How graph properties (sparsity, density, bottlenecks, negative weights) affect each algorithm differently.
- **Interpretability**: How easily algorithmic decisions can be understood and predicted by human observers.

## Experimental Controls

### Ensuring Fair Comparison

All algorithms receive identical graph instances with the same source and destination specifications. Graphs are constructed once and passed to each algorithm without modification.

### Reproducibility Mechanisms

All graph generation processes are governed by fixed random seeds. The quantum-inspired algorithm's stochastic elements are similarly controlled, enabling validation and independent replication.

### Absence of Algorithm-Specific Optimisations

The implementation avoids algorithm-specific optimisations, prioritising clarity over efficiency to ensure performance differences reflect algorithmic properties rather than implementation details.

## Alignment with Case Study Objectives

This setup aligns with educational objectives through small graph sizes enabling detailed observation, diverse structures exposing different behaviours, multiple evaluation criteria capturing quantitative and qualitative aspects, and rigorous controls ensuring fair comparison and reproducibility.
