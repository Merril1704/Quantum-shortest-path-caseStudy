"""
Dijkstra's Algorithm implementation with per-iteration tracking.
Greedy, deterministic algorithm for non-negative edge weights.
"""
import heapq
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from src.graph import Graph


@dataclass
class DijkstraIteration:
    """Records state at each iteration of Dijkstra's algorithm."""
    iteration: int
    current_node: int
    distances: Dict[int, float]
    visited: set
    tentative_path: Dict[int, List[int]]


@dataclass 
class DijkstraResult:
    """Complete result from Dijkstra's algorithm."""
    path: Optional[List[int]]
    distance: float
    iterations: int
    history: List[DijkstraIteration]
    success: bool
    message: str


def dijkstra(graph: Graph, source: int, target: int) -> DijkstraResult:
    """
    Dijkstra's shortest path algorithm with iteration tracking.
    
    Args:
        graph: The graph to search
        source: Starting node
        target: Destination node
        
    Returns:
        DijkstraResult with path, distance, and iteration history
    
    Note:
        Dijkstra's algorithm does NOT correctly handle negative edge weights.
        If the graph has negative weights, results may be incorrect.
    """
    history: List[DijkstraIteration] = []
    
    # Check for negative weights (warning)
    has_negative = graph.has_negative_weights()
    
    # Initialize distances
    distances: Dict[int, float] = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    
    # Track paths
    predecessors: Dict[int, Optional[int]] = {node: None for node in graph.nodes}
    
    # Priority queue: (distance, node)
    pq = [(0, source)]
    visited: set = set()
    
    iteration = 0
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
            
        visited.add(current)
        iteration += 1
        
        # Build current tentative paths for history
        tentative_paths = {}
        for node in graph.nodes:
            if predecessors[node] is not None or node == source:
                path = _reconstruct_path(predecessors, source, node)
                tentative_paths[node] = path
        
        # Record iteration state
        history.append(DijkstraIteration(
            iteration=iteration,
            current_node=current,
            distances=dict(distances),
            visited=set(visited),
            tentative_path=tentative_paths
        ))
        
        # Found target
        if current == target:
            path = _reconstruct_path(predecessors, source, target)
            message = "Path found successfully"
            if has_negative:
                message += " (WARNING: Graph has negative weights - result may be incorrect)"
            return DijkstraResult(
                path=path,
                distance=distances[target],
                iterations=iteration,
                history=history,
                success=True,
                message=message
            )
        
        # Relax neighbors
        for neighbor in graph.get_neighbors(current):
            if neighbor in visited:
                continue
                
            weight = graph.get_weight(current, neighbor)
            new_dist = current_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    # Target not reachable
    return DijkstraResult(
        path=None,
        distance=float('inf'),
        iterations=iteration,
        history=history,
        success=False,
        message=f"No path exists from {source} to {target}"
    )


def _reconstruct_path(predecessors: Dict[int, Optional[int]], source: int, target: int) -> List[int]:
    """Reconstruct path from predecessors dictionary."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = predecessors[current]
    path.reverse()
    return path if path and path[0] == source else []
