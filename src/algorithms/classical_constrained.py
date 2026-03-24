"""
Classical Constrained Shortest Path Baseline.

For a path that must visit mandatory waypoints W = {w1, w2, ..., wk}:
  - Must try all k! orderings of waypoints
  - For each ordering, run Dijkstra on each sub-segment
  - Pick the ordering with minimum total cost

Complexity: O(k! * V log V)  — exponential in number of waypoints.
This is the "correct" classical approach and demonstrates why QI is
preferable when |W| grows: QI does it in ONE run regardless of |W|.
"""
import heapq
import itertools
from typing import List, Optional, Dict, Tuple, Set
from dataclasses import dataclass
from src.graph import Graph


@dataclass
class ClassicalConstrainedResult:
    """Result from classical constrained shortest path."""
    path: Optional[List[int]]
    distance: float
    waypoint_order: Optional[List[int]]   # Which ordering was chosen
    dijkstra_calls: int                   # How many Dijkstra runs were needed
    success: bool
    constraints_met: bool
    message: str


def classical_constrained_shortest_path(
    graph: Graph,
    source: int,
    target: int,
    waypoints: Optional[List[int]] = None,
    forbidden: Optional[List[int]] = None,
) -> ClassicalConstrainedResult:
    """
    Classical baseline: Tries all permutations of waypoints and runs
    segment-by-segment Dijkstra for each.

    Args:
        graph:      Graph to search
        source:     Start node
        target:     End node
        waypoints:  Nodes that must be visited (in any order)
        forbidden:  Nodes that must not appear in the path

    Returns:
        ClassicalConstrainedResult with best valid path found
    """
    waypoints = list(waypoints) if waypoints else []
    forbidden_set = set(forbidden) if forbidden else set()

    # Build a forbidden-filtered graph view (no structural change — handled in Dijkstra)
    dijkstra_calls = 0
    best_path = None
    best_dist = float('inf')
    best_order = None

    if not waypoints:
        # Simple case: just run Dijkstra once
        result = _dijkstra(graph, source, target, forbidden_set)
        dijkstra_calls = 1
        if result is not None:
            path, dist = result
            return ClassicalConstrainedResult(
                path=path, distance=dist, waypoint_order=[],
                dijkstra_calls=dijkstra_calls, success=True,
                constraints_met=True, message="No waypoints — direct Dijkstra"
            )
        else:
            return ClassicalConstrainedResult(
                path=None, distance=float('inf'), waypoint_order=None,
                dijkstra_calls=dijkstra_calls, success=False,
                constraints_met=False, message="No valid path found"
            )

    # Try all orderings of waypoints
    for ordering in itertools.permutations(waypoints):
        stops = [source] + list(ordering) + [target]
        full_path = []
        total_dist = 0.0
        feasible = True

        for i in range(len(stops) - 1):
            seg_src, seg_tgt = stops[i], stops[i + 1]
            if seg_src == seg_tgt:
                continue
            result = _dijkstra(graph, seg_src, seg_tgt, forbidden_set)
            dijkstra_calls += 1

            if result is None:
                feasible = False
                break

            seg_path, seg_dist = result
            if full_path:
                full_path.extend(seg_path[1:])  # Skip duplicate junction node
            else:
                full_path = seg_path
            total_dist += seg_dist

        if feasible and total_dist < best_dist:
            best_dist = total_dist
            best_path = full_path
            best_order = list(ordering)

    if best_path is not None:
        # Verify no forbidden nodes slipped through
        forbidden_in_path = [n for n in best_path if n in forbidden_set]
        constraints_met = len(forbidden_in_path) == 0
        return ClassicalConstrainedResult(
            path=best_path,
            distance=best_dist,
            waypoint_order=best_order,
            dijkstra_calls=dijkstra_calls,
            success=True,
            constraints_met=constraints_met,
            message=f"Found via {dijkstra_calls} Dijkstra calls ({len(list(itertools.permutations(waypoints)))} orderings tried)"
        )
    else:
        return ClassicalConstrainedResult(
            path=None,
            distance=float('inf'),
            waypoint_order=None,
            dijkstra_calls=dijkstra_calls,
            success=False,
            constraints_met=False,
            message=f"No feasible constrained path found after {dijkstra_calls} Dijkstra calls"
        )


def _dijkstra(
    graph: Graph, source: int, target: int,
    forbidden: Set[int]
) -> Optional[Tuple[List[int], float]]:
    """
    Standard Dijkstra avoiding forbidden nodes.
    Returns (path, distance) or None if unreachable.
    """
    dist: Dict[int, float] = {source: 0.0}
    prev: Dict[int, Optional[int]] = {source: None}
    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if u == target:
            # Reconstruct path
            path = []
            node = target
            while node is not None:
                path.append(node)
                node = prev[node]
            path.reverse()
            return path, d

        if d > dist.get(u, float('inf')):
            continue

        for v in graph.get_neighbors(u):
            if v in forbidden and v != target:
                continue
            w = graph.get_weight(u, v)
            if w is None:
                continue
            new_dist = d + w
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return None  # Target unreachable
