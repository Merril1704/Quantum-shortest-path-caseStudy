"""
Classical Multi-Objective Baseline using Weighted-Sum Dijkstra.

To approximate a Pareto front classically, we:
  1. Discretise the weight space into a K x K x K grid (w_dist, w_risk, w_hops)
  2. For each (w1,w2,w3) combination run a single-objective Dijkstra on the
     composite edge cost: w1*dist + w2*risk + w3*hops_proxy
  3. Collect unique non-dominated solutions

Complexity: O(K^d * (V log V + E)) for d objectives and K grid steps.
With K=5 and d=3, that's 125 Dijkstra calls.
QI achieves similar coverage in ~15 restarts.
"""
import heapq
import itertools
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from src.graph import Graph


@dataclass
class ClassicalMultiObjectiveResult:
    pareto_front: list       # list of (path, distance, risk, hops) tuples
    all_solutions: list
    dijkstra_calls: int
    message: str


def classical_multiobjective_shortest_path(
    graph: Graph,
    source: int,
    target: int,
    risk_attr: Optional[Dict[Tuple[int, int], float]] = None,
    weight_steps: int = 4,
) -> ClassicalMultiObjectiveResult:
    """
    Weighted-sum Dijkstra over a grid of (w_dist, w_risk, w_hops) values.

    Args:
        graph:          Graph to search
        source/target:  Start and end nodes
        risk_attr:      Dict (u,v)->risk score
        weight_steps:   Number of steps per objective (grid size = steps^3)

    Returns:
        ClassicalMultiObjectiveResult with Pareto front and Dijkstra call count
    """
    risk_attr = risk_attr or {}
    all_solutions = []
    dijkstra_calls = 0

    # Build weight grid — exclude (0,0,0), normalise rows
    step = 1.0 / weight_steps
    weight_vectors = []
    for i in range(weight_steps + 1):
        for j in range(weight_steps + 1):
            k = weight_steps - i - j
            if k < 0:
                continue
            w_d, w_r, w_h = i * step, j * step, k * step
            s = w_d + w_r + w_h
            if s == 0:
                continue
            weight_vectors.append((w_d / s, w_r / s, w_h / s))

    for w_dist, w_risk, w_hops in weight_vectors:
        path, dist_ = _dijkstra_composite(graph, source, target, risk_attr,
                                          w_dist, w_risk, w_hops)
        dijkstra_calls += 1
        if path is not None:
            dist = _path_distance(graph, path)
            risk = _path_risk(path, risk_attr)
            hops = len(path) - 1
            all_solutions.append((path, dist, risk, hops, (w_dist, w_risk, w_hops)))

    # Pareto filter
    pareto = _pareto_front(all_solutions)

    return ClassicalMultiObjectiveResult(
        pareto_front=pareto,
        all_solutions=all_solutions,
        dijkstra_calls=dijkstra_calls,
        message=f"Ran {dijkstra_calls} Dijkstra calls over weight grid; found {len(pareto)} Pareto solutions"
    )


def _dijkstra_composite(
    graph: Graph, source: int, target: int,
    risk_attr: Dict, w_dist: float, w_risk: float, w_hops: float
) -> Tuple[Optional[List[int]], float]:
    """Dijkstra on composite edge cost = w_dist*weight + w_risk*risk + w_hops*1."""
    dist: Dict[int, float] = {source: 0.0}
    prev: Dict[int, Optional[int]] = {source: None}
    heap = [(0.0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if u == target:
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
            edge_w = graph.get_weight(u, v)
            if edge_w is None:
                continue
            risk = risk_attr.get((u, v), 0.0)
            composite = w_dist * edge_w + w_risk * risk * 10 + w_hops * 5
            new_d = d + composite
            if new_d < dist.get(v, float('inf')):
                dist[v] = new_d
                prev[v] = u
                heapq.heappush(heap, (new_d, v))

    return None, float('inf')


def _pareto_front(solutions):
    pareto = []
    for sol in solutions:
        path, dist, risk, hops, wv = sol
        dominated = False
        for other in solutions:
            op, od, orisk, ohops, _ = other
            if other is sol:
                continue
            if (od <= dist and orisk <= risk and ohops <= hops and
                    (od < dist or orisk < risk or ohops < hops)):
                dominated = True
                break
        if not dominated:
            pareto.append(sol)
    seen = set()
    unique = []
    for sol in pareto:
        key = tuple(sol[0])
        if key not in seen:
            seen.add(key)
            unique.append(sol)
    return unique


def _path_distance(graph: Graph, path: List[int]) -> float:
    total = 0.0
    for i in range(len(path) - 1):
        w = graph.get_weight(path[i], path[i + 1])
        if w is None:
            return float('inf')
        total += w
    return total


def _path_risk(path: List[int], risk_attr: Dict) -> float:
    return sum(risk_attr.get((path[i], path[i + 1]), 0.0) for i in range(len(path) - 1))
