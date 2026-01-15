"""
Bellman-Ford Algorithm implementation with per-iteration tracking.
Handles negative edge weights and detects negative cycles.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from src.graph import Graph


@dataclass
class BellmanFordIteration:
    """Records state at each iteration (pass) of Bellman-Ford."""
    iteration: int
    distances: Dict[int, float]
    relaxations_made: int
    edges_relaxed: List[tuple]  # List of (u, v, new_dist) that were updated


@dataclass
class BellmanFordResult:
    """Complete result from Bellman-Ford algorithm."""
    path: Optional[List[int]]
    distance: float
    iterations: int
    history: List[BellmanFordIteration]
    success: bool
    has_negative_cycle: bool
    message: str


def bellman_ford(graph: Graph, source: int, target: int) -> BellmanFordResult:
    """
    Bellman-Ford shortest path algorithm with iteration tracking.
    
    Key Properties:
        - Handles negative edge weights correctly
        - Detects negative cycles
        - O(V * E) time complexity
        - Performs V-1 passes over all edges
    
    Args:
        graph: The graph to search
        source: Starting node
        target: Destination node
        
    Returns:
        BellmanFordResult with path, distance, iteration history, and cycle detection
    """
    history: List[BellmanFordIteration] = []
    
    nodes = graph.nodes
    edges = graph.get_edge_list()
    n = len(nodes)
    
    # Initialize distances
    distances: Dict[int, float] = {node: float('inf') for node in nodes}
    distances[source] = 0
    
    # Track predecessors for path reconstruction
    predecessors: Dict[int, Optional[int]] = {node: None for node in nodes}
    
    # Main algorithm: V-1 passes
    for i in range(n - 1):
        relaxations_made = 0
        edges_relaxed = []
        
        # Relax all edges
        for u, v, weight in edges:
            if distances[u] != float('inf'):
                new_dist = distances[u] + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    relaxations_made += 1
                    edges_relaxed.append((u, v, new_dist))
        
        # Record iteration
        history.append(BellmanFordIteration(
            iteration=i + 1,
            distances=dict(distances),
            relaxations_made=relaxations_made,
            edges_relaxed=edges_relaxed
        ))
        
        # Early termination: if no relaxations, we're done
        if relaxations_made == 0:
            break
    
    # Check for negative cycles (one more pass)
    has_negative_cycle = False
    for u, v, weight in edges:
        if distances[u] != float('inf'):
            if distances[u] + weight < distances[v]:
                has_negative_cycle = True
                break
    
    # Build result
    if has_negative_cycle:
        return BellmanFordResult(
            path=None,
            distance=float('inf'),
            iterations=len(history),
            history=history,
            success=False,
            has_negative_cycle=True,
            message="Negative cycle detected - no valid shortest path exists"
        )
    
    if distances[target] == float('inf'):
        return BellmanFordResult(
            path=None,
            distance=float('inf'),
            iterations=len(history),
            history=history,
            success=False,
            has_negative_cycle=False,
            message=f"No path exists from {source} to {target}"
        )
    
    # Reconstruct path
    path = _reconstruct_path(predecessors, source, target)
    
    return BellmanFordResult(
        path=path,
        distance=distances[target],
        iterations=len(history),
        history=history,
        success=True,
        has_negative_cycle=False,
        message="Path found successfully"
    )


def _reconstruct_path(predecessors: Dict[int, Optional[int]], source: int, target: int) -> List[int]:
    """Reconstruct path from predecessors dictionary."""
    path = []
    current = target
    max_steps = len(predecessors) + 1  # Prevent infinite loop
    steps = 0
    
    while current is not None and steps < max_steps:
        path.append(current)
        if current == source:
            break
        current = predecessors[current]
        steps += 1
    
    path.reverse()
    return path if path and path[0] == source else []
