"""
Multi-Objective Quantum-Inspired Shortest Path.

Classical Dijkstra minimises a SINGLE scalar (distance). When the problem
has multiple competing objectives — e.g. minimise travel cost AND risk AND
number of hops — there is no single "optimal" answer. The solution is a
PARETO FRONT of non-dominated trade-off paths.

Classical approach: run weighted-sum Dijkstra for every (w1,w2,w3) combo
  → O(K^d) runs for K weight steps and d objectives.
QI approach: run multiple restarts with different randomly sampled weight
  vectors, collecting diverse Pareto-optimal solutions in one sweep.

Edge attributes used:
  - weight (distance / travel cost)
  - risk    (0-10 scale, stored in graph._risk)
"""
import random
import math
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from src.graph import Graph


@dataclass
class MultiObjectiveIteration:
    iteration: int
    current_path: List[int]
    current_energy: float
    temperature: float
    objectives: Dict[str, float]    # distance, risk, hops


@dataclass
class ParetoSolution:
    path: List[int]
    distance: float
    risk: float
    hops: int
    weight_vector: Tuple[float, float, float]   # (w_dist, w_risk, w_hops)


@dataclass
class MultiObjectiveResult:
    pareto_front: List[ParetoSolution]
    all_solutions: List[ParetoSolution]
    iterations_total: int
    restarts: int
    message: str


def quantum_multiobjective_shortest_path(
    graph: Graph,
    source: int,
    target: int,
    risk_attr: Optional[Dict[Tuple[int, int], float]] = None,
    n_restarts: int = 15,
    max_iterations: int = 300,
    initial_temperature: float = 12.0,
    cooling_rate: float = 0.98,
    constraint_penalty: float = 1000.0,
    seed: Optional[int] = None
) -> MultiObjectiveResult:
    """
    Multi-objective shortest path via QI with Pareto front collection.

    Randomly samples objective weight vectors across restarts so one run
    covers the full trade-off space that would need O(K^3) classical runs.

    Args:
        graph:              Graph to search
        source / target:    Start and end nodes
        risk_attr:          Dict mapping (u,v) -> risk score (0-10)
        n_restarts:         Number of QI runs with different weight vectors
        max_iterations:     Per-restart iteration budget
        initial_temperature, cooling_rate: Annealing schedule
        constraint_penalty: Penalty for invalid-edge use
        seed:               Random seed for reproducibility

    Returns:
        MultiObjectiveResult with Pareto front and all found solutions
    """
    if seed is not None:
        random.seed(seed)

    risk_attr = risk_attr or {}
    all_solutions: List[ParetoSolution] = []
    total_iterations = 0

    for restart in range(n_restarts):
        # Sample random weight vector from simplex (sums to 1)
        raw = [random.random() for _ in range(3)]
        s = sum(raw)
        w_dist, w_risk, w_hops = raw[0] / s, raw[1] / s, raw[2] / s

        path, iters = _run_single(
            graph, source, target, risk_attr,
            w_dist, w_risk, w_hops,
            max_iterations, initial_temperature, cooling_rate, constraint_penalty
        )
        total_iterations += iters

        if path is not None and _is_valid(graph, path, source, target):
            dist = _path_distance(graph, path)
            risk = _path_risk(path, risk_attr)
            hops = len(path) - 1
            sol = ParetoSolution(
                path=path, distance=dist, risk=risk, hops=hops,
                weight_vector=(w_dist, w_risk, w_hops)
            )
            all_solutions.append(sol)

    # Compute Pareto front (non-dominated solutions)
    pareto = _pareto_front(all_solutions)

    return MultiObjectiveResult(
        pareto_front=pareto,
        all_solutions=all_solutions,
        iterations_total=total_iterations,
        restarts=n_restarts,
        message=f"Found {len(pareto)} Pareto-optimal solutions across {n_restarts} restarts"
    )


def _run_single(
    graph: Graph, source: int, target: int,
    risk_attr: Dict, w_dist: float, w_risk: float, w_hops: float,
    max_iterations: int, initial_temperature: float,
    cooling_rate: float, constraint_penalty: float
) -> Tuple[Optional[List[int]], int]:
    """One annealing run with a given objective weight vector."""
    nodes = graph.nodes
    current_path = _init_path(graph, source, target)
    current_energy = _energy(graph, current_path, source, target,
                             risk_attr, w_dist, w_risk, w_hops, constraint_penalty)

    best_path = list(current_path)
    best_energy = current_energy
    best_valid = _is_valid(graph, current_path, source, target)

    temperature = initial_temperature
    stable = 0

    for i in range(max_iterations):
        new_path = _neighbor(graph, current_path, source, target, nodes)
        new_energy = _energy(graph, new_path, source, target,
                             risk_attr, w_dist, w_risk, w_hops, constraint_penalty)

        delta = new_energy - current_energy
        if delta < 0 or (temperature > 0.01 and random.random() < math.exp(-delta / temperature)):
            current_path = new_path
            current_energy = new_energy
            cur_valid = _is_valid(graph, current_path, source, target)
            if current_energy < best_energy or (cur_valid and not best_valid):
                best_path = list(current_path)
                best_energy = current_energy
                best_valid = cur_valid
                stable = 0
            else:
                stable += 1
        else:
            stable += 1

        temperature *= cooling_rate
        if stable >= 50 and best_valid:
            break

    return (best_path if best_valid else None), i + 1


def _pareto_front(solutions: List[ParetoSolution]) -> List[ParetoSolution]:
    """Return only non-dominated solutions (lower is better for all objectives)."""
    pareto = []
    for sol in solutions:
        dominated = False
        for other in solutions:
            if other is sol:
                continue
            if (other.distance <= sol.distance and
                    other.risk <= sol.risk and
                    other.hops <= sol.hops and
                    (other.distance < sol.distance or
                     other.risk < sol.risk or
                     other.hops < sol.hops)):
                dominated = True
                break
        if not dominated:
            pareto.append(sol)
    # Deduplicate by path tuple
    seen = set()
    unique = []
    for sol in pareto:
        key = tuple(sol.path)
        if key not in seen:
            seen.add(key)
            unique.append(sol)
    return unique


def _energy(
    graph: Graph, path: List[int], source: int, target: int,
    risk_attr: Dict, w_dist: float, w_risk: float, w_hops: float,
    constraint_penalty: float
) -> float:
    if not path:
        return constraint_penalty * 10
    violations = 0
    dist = 0.0
    if path[0] != source:
        violations += 1
    if path[-1] != target:
        violations += 1
    for i in range(len(path) - 1):
        w = graph.get_weight(path[i], path[i + 1])
        if w is not None:
            dist += w
        else:
            violations += 2
    risk = _path_risk(path, risk_attr)
    hops = len(path) - 1
    return w_dist * dist + w_risk * risk * 10 + w_hops * hops * 5 + constraint_penalty * violations


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


def _is_valid(graph: Graph, path: List[int], source: int, target: int) -> bool:
    if not path or len(path) < 2:
        return False
    if path[0] != source or path[-1] != target:
        return False
    return all(graph.has_edge(path[i], path[i + 1]) for i in range(len(path) - 1))


def _init_path(graph: Graph, source: int, target: int) -> List[int]:
    path = [source]
    current = source
    visited = {source}
    for _ in range(graph.num_nodes * 2):
        if current == target:
            break
        neighbors = [n for n in graph.get_neighbors(current) if n not in visited]
        if not neighbors:
            break
        next_node = min(neighbors, key=lambda n: abs(n - target)) if random.random() < 0.7 else random.choice(neighbors)
        path.append(next_node)
        visited.add(next_node)
        current = next_node
    if path[-1] != target:
        path.append(target)
    return path


def _neighbor(graph: Graph, path: List[int], source: int, target: int, nodes: List[int]) -> List[int]:
    if len(path) <= 2:
        return list(path)
    new_path = list(path)
    op = random.choice(['insert', 'remove', 'replace', 'swap'])
    if op == 'insert':
        available = [n for n in nodes if n not in new_path]
        if available:
            new_path.insert(random.randint(1, len(new_path) - 1), random.choice(available))
    elif op == 'remove' and len(new_path) > 2:
        new_path.pop(random.randint(1, len(new_path) - 2))
    elif op == 'replace' and len(new_path) > 2:
        available = [n for n in nodes if n not in new_path]
        if available:
            new_path[random.randint(1, len(new_path) - 2)] = random.choice(available)
    elif op == 'swap' and len(new_path) > 3:
        i, j = random.randint(1, len(new_path) - 2), random.randint(1, len(new_path) - 2)
        if i != j:
            new_path[i], new_path[j] = new_path[j], new_path[i]
    if new_path[0] != source:
        new_path[0] = source
    if new_path[-1] != target:
        new_path[-1] = target
    return new_path
