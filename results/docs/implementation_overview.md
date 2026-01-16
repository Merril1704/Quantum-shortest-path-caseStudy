# Implementation Overview

## Purpose and Scope

The implementation developed for this case study serves an educational and investigative purpose rather than a performance-driven objective. The primary goal is to facilitate a behavioural comparison among three distinct shortest path algorithms: Dijkstra's algorithm, the Bellman–Ford algorithm, and an energy-based quantum-inspired algorithm. Rather than optimising for computational speed or scalability, the implementation emphasises clarity, reproducibility, and observability. This approach enables detailed examination of how each algorithm arrives at its solution, the nature of its convergence behaviour, and the conditions under which it succeeds or fails.

The scope of the implementation is intentionally limited to small and medium-sized graph instances, ranging from five to twenty nodes. This constraint allows for meaningful observation of algorithmic behaviour without the complexity introduced by large-scale datasets. The implementation is designed for academic exploration and is not intended for production deployment or real-time applications.

## Common Graph Representation

To ensure a fair and consistent comparison, all three algorithms operate on a unified graph data structure. The graphs are represented using an adjacency list model, which stores nodes and their corresponding weighted edges. This representation supports both directed and undirected graphs and accommodates positive as well as negative edge weights. Each graph instance is constructed once and passed identically to all algorithms, eliminating any structural bias that might arise from differing representations.

The graph structure provides standard operations such as retrieving neighbours of a given node, obtaining the weight of an edge, and calculating graph-level properties including density and the presence of negative weights. By maintaining a single, consistent representation, the implementation ensures that observed differences in algorithm behaviour are attributable to the algorithms themselves rather than to variations in input format.

## Algorithm Implementations

### Dijkstra's Algorithm

Dijkstra's algorithm is implemented as a deterministic, greedy shortest path method suitable for graphs with non-negative edge weights. The algorithm maintains a priority-based exploration strategy, always expanding the node with the smallest known distance from the source. As each node is visited, its neighbours are examined and their tentative distances are updated if a shorter path is discovered.

The implementation includes comprehensive state tracking at each iteration, recording which node is being expanded, the current distance estimates for all nodes, and the set of nodes already visited. This level of detail supports post-hoc analysis of how the algorithm progressively builds the shortest path tree. A warning mechanism is incorporated to alert users when the input graph contains negative weights, as the algorithm's correctness guarantees do not extend to such cases.

### Bellman–Ford Algorithm

The Bellman–Ford algorithm is implemented as an iterative edge relaxation method capable of handling graphs with negative edge weights. Unlike Dijkstra's algorithm, Bellman–Ford does not rely on greedy node selection. Instead, it performs a series of passes over all edges in the graph, updating distance estimates whenever a shorter path is discovered through relaxation.

The algorithm is configured to perform at most one fewer pass than the number of nodes in the graph, which is sufficient to guarantee correct shortest path distances in the absence of negative cycles. An additional pass is performed to detect the presence of any negative cycle; if further relaxation is possible after the standard passes, a negative cycle is reported. The implementation records the number of relaxations performed in each pass and the specific edges that were updated, enabling detailed observation of how the algorithm converges to the final solution.

### Energy-Based Quantum-Inspired Algorithm

The quantum-inspired algorithm represents a fundamentally different approach to shortest path computation. Rather than following a deterministic procedure, it employs a probabilistic optimisation strategy inspired by the principles of quantum annealing and simulated annealing. The algorithm formulates the shortest path problem as an energy minimisation task, where the objective is to find the path configuration with the lowest total energy.

The energy of a candidate path is defined as the sum of its edge weights combined with a penalty term for constraint violations. Constraint violations include paths that do not correctly originate from the source node, do not terminate at the target node, or traverse edges that do not exist in the graph. The penalty for such violations is set sufficiently high to ensure that valid paths are strongly preferred over invalid configurations.

At each iteration, the algorithm generates a neighbouring solution by applying a random modification to the current path. These modifications include swapping intermediate nodes, inserting or removing nodes, or replacing a node with an alternative. The algorithm then evaluates whether to accept the new solution based on a probabilistic acceptance criterion. Improvements in energy are always accepted, while solutions with higher energy may still be accepted with a probability that decreases as the system temperature is lowered. This mechanism allows the algorithm to escape local minima during early exploration while gradually focusing on refinement as the search progresses.

The temperature parameter governs the probability of accepting suboptimal moves and is reduced according to a predefined cooling schedule. The algorithm terminates either when a maximum number of iterations is reached or when the solution remains stable for a specified number of consecutive iterations.

## Convergence and Iteration Behaviour

Each algorithm exhibits distinct convergence characteristics that are captured through detailed iteration tracking. Dijkstra's algorithm demonstrates monotonic progress, with distance estimates decreasing or remaining stable as nodes are expanded. The algorithm terminates as soon as the target node is reached, and the number of iterations corresponds directly to the number of node expansions.

Bellman–Ford's convergence is characterised by pass-based relaxation. In early passes, substantial changes to distance estimates are common, while later passes show diminishing updates as the algorithm approaches its final solution. Early termination occurs if a pass produces no relaxations, indicating that all shortest paths have been determined.

The quantum-inspired algorithm exhibits non-monotonic and exploratory behaviour. Its energy trajectory may fluctuate, particularly in early iterations when the temperature is high and suboptimal transitions are permitted. As the temperature decreases, the algorithm becomes increasingly conservative, and the energy stabilises. Convergence is considered achieved when the best-known solution remains unchanged for a defined stability period. This stochastic nature means that different runs may produce different results unless a fixed random seed is employed.

## Experimental Controls

The implementation incorporates several controls to ensure fair and reproducible comparisons. All algorithms receive identical graph instances with the same source and target node specifications. The graphs are generated using a deterministic process governed by a fixed random seed, enabling exact reproduction of experimental conditions.

For the quantum-inspired algorithm, the random seed also governs the stochastic elements of the search process, ensuring that repeated executions with the same seed produce identical results. This reproducibility is essential for validating observations and supporting academic scrutiny.

No algorithm-specific optimisations have been introduced. Data structures and operations are implemented in a straightforward manner to avoid introducing implementation-level biases that might obscure algorithmic differences. The focus remains on observable behaviour rather than execution efficiency.

## Data Recorded Per Execution

For each algorithm execution, the implementation records a comprehensive set of observations. These include the final path produced (if any), the total path cost or distance, and whether the algorithm successfully found a valid path. For Bellman–Ford, additional information regarding the presence of negative cycles is recorded.

Iteration-level data is also captured for all algorithms. This includes the state of distance estimates or energy values at each step, the nodes or edges processed, and whether transitions or relaxations were accepted. For the quantum-inspired algorithm, additional metrics such as temperature values and path validity at each iteration are recorded.

This detailed logging supports both quantitative analysis, such as iteration counts and cost comparisons, and qualitative analysis, such as examining convergence trajectories and identifying failure modes.

## Limitations and Disclaimer

The implementation presented in this case study is designed for educational and experimental purposes. It is not optimised for large-scale graphs, real-time processing, or deployment in production environments. The emphasis on clarity and observability may result in higher memory usage and slower execution compared to optimised implementations.

The quantum-inspired algorithm, in particular, represents a heuristic approach without formal guarantees of optimality. Its performance is sensitive to hyperparameter settings, including the initial temperature, cooling rate, and constraint penalty values. The results presented should be interpreted as illustrative of algorithmic behaviour rather than as definitive claims of superiority or inferiority.

This implementation serves as a platform for understanding and comparing algorithmic paradigms within the context of the shortest path problem, contributing to academic learning and further research exploration.
