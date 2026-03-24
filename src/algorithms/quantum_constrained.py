"""
Constrained Quantum-Inspired Shortest Path.

Extends the base energy-minimization approach to handle:
  1. Mandatory waypoints  — nodes that MUST appear in the path
  2. Forbidden nodes      — nodes that MUST NOT appear in the path

The key advantage over classical algorithms:
  - Classical (Dijkstra/BF) must enumerate all waypoint orderings (O(|W|!))
    and run a separate shortest-path for each segment.
  - This QI approach encodes all constraints directly in the energy function
    and satisfies them in a SINGLE run.

Energy Function:
    E = path_weight
      + λ1 * (|waypoints| - |waypoints found in path|)   <- missing waypoints
      + λ2 * |forbidden nodes found in path|             <- forbidden violations
      + λ3 * constraint_violations (invalid edges etc.)
"""
import random
import math
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from src.graph import Graph


@dataclass
class ConstrainedIteration:
    """State at each iteration of the constrained QI algorithm."""
    iteration: int
    current_path: List[int]
    current_energy: float
    temperature: float
    waypoints_satisfied: int
    forbidden_violations: int
    path_valid: bool


@dataclass
class ConstrainedResult:
    """Complete result from constrained QI algorithm."""
    path: Optional[List[int]]
    distance: float
    energy: float
    iterations: int
    history: List[ConstrainedIteration]
    success: bool
    constraints_met: bool
    waypoints_found: List[int]
    forbidden_found: List[int]
    convergence_iteration: int
    message: str


def quantum_constrained_shortest_path(
    graph: Graph,
    source: int,
    target: int,
    waypoints: Optional[List[int]] = None,
    forbidden: Optional[List[int]] = None,
    max_iterations: int = 800,
    initial_temperature: float = 15.0,
    cooling_rate: float = 0.985,
    waypoint_penalty: float = 500.0,
    forbidden_penalty: float = 800.0,
    constraint_penalty: float = 1000.0,
    stability_threshold: int = 80,
    seed: Optional[int] = None
) -> ConstrainedResult:
    """
    Constrained shortest path via quantum-inspired energy minimization.

    Encodes waypoint coverage and forbidden avoidance directly in the
    energy landscape — no enumeration of orderings required.

    Args:
        graph:              Graph to search
        source:             Start node
        target:             End node
        waypoints:          Nodes that MUST appear in path
        forbidden:          Nodes that MUST NOT appear in path
        max_iterations:     Cap on optimization iterations
        initial_temperature: Starting annealing temperature
        cooling_rate:       Temperature decay per iteration
        waypoint_penalty:   Energy added per missing mandatory waypoint
        forbidden_penalty:  Energy added per forbidden node visited
        constraint_penalty: Energy added per invalid edge
        stability_threshold: Stop early if no improvement for this many iters
        seed:               Random seed for reproducibility

    Returns:
        ConstrainedResult with path, distance, constraint satisfaction details
    """
    if seed is not None:
        random.seed(seed)

    waypoints = list(waypoints) if waypoints else []
    forbidden = set(forbidden) if forbidden else set()
    history: List[ConstrainedIteration] = []
    nodes = graph.nodes

    # Remove forbidden nodes from graph's node pool for path generation
    usable_nodes = [n for n in nodes if n not in forbidden or n in (source, target)]

    # Initialize
    current_path = _init_constrained_path(graph, source, target, waypoints, forbidden)
    current_energy = _energy(graph, current_path, source, target,
                             waypoints, forbidden,
                             waypoint_penalty, forbidden_penalty, constraint_penalty)

    best_path = list(current_path)
    best_energy = current_energy
    best_valid = _is_valid(graph, current_path, source, target)
    best_constraints = _count_satisfied_waypoints(current_path, waypoints)

    temperature = initial_temperature
    stable_count = 0
    convergence_iteration = 0

    for iteration in range(max_iterations):
        new_path = _generate_constrained_neighbor(
            graph, current_path, source, target, waypoints, forbidden, usable_nodes
        )
        new_energy = _energy(graph, new_path, source, target,
                             waypoints, forbidden,
                             waypoint_penalty, forbidden_penalty, constraint_penalty)

        delta_e = new_energy - current_energy
        accepted = False

        if delta_e < 0:
            accepted = True
        else:
            prob = math.exp(-delta_e / temperature) if temperature > 0.01 else 0
            accepted = random.random() < prob

        if accepted:
            current_path = new_path
            current_energy = new_energy

            cur_valid = _is_valid(graph, current_path, source, target)
            cur_wp = _count_satisfied_waypoints(current_path, waypoints)

            # Prefer: more waypoints satisfied first, then lower energy
            better = (
                cur_wp > best_constraints or
                (cur_wp == best_constraints and current_energy < best_energy) or
                (cur_valid and not best_valid)
            )
            if better:
                best_path = list(current_path)
                best_energy = current_energy
                best_valid = cur_valid
                best_constraints = cur_wp
                convergence_iteration = iteration + 1
                stable_count = 0
            else:
                stable_count += 1
        else:
            stable_count += 1

        wp_sat = _count_satisfied_waypoints(current_path, waypoints)
        forb_viol = sum(1 for n in current_path if n in forbidden)
        history.append(ConstrainedIteration(
            iteration=iteration + 1,
            current_path=list(current_path),
            current_energy=current_energy,
            temperature=temperature,
            waypoints_satisfied=wp_sat,
            forbidden_violations=forb_viol,
            path_valid=_is_valid(graph, current_path, source, target)
        ))

        temperature *= cooling_rate

        # Early stop only if all constraints met AND path is valid
        all_wp_met = best_constraints == len(waypoints)
        no_forbidden = not any(n in forbidden for n in best_path)
        if stable_count >= stability_threshold and best_valid and all_wp_met and no_forbidden:
            break

    # Evaluate best found solution
    waypoints_found = [w for w in waypoints if w in best_path]
    forbidden_found = [n for n in best_path if n in forbidden]
    all_constraints_met = (
        len(waypoints_found) == len(waypoints) and
        len(forbidden_found) == 0 and
        best_valid
    )

    if best_valid:
        actual_dist = _path_distance(graph, best_path)
        return ConstrainedResult(
            path=best_path,
            distance=actual_dist,
            energy=best_energy,
            iterations=len(history),
            history=history,
            success=True,
            constraints_met=all_constraints_met,
            waypoints_found=waypoints_found,
            forbidden_found=forbidden_found,
            convergence_iteration=convergence_iteration,
            message="Valid path found" + (" (all constraints met)" if all_constraints_met else " (partial constraints)")
        )
    else:
        return ConstrainedResult(
            path=None,
            distance=float('inf'),
            energy=best_energy,
            iterations=len(history),
            history=history,
            success=False,
            constraints_met=False,
            waypoints_found=waypoints_found,
            forbidden_found=forbidden_found,
            convergence_iteration=convergence_iteration,
            message="No valid path found within iteration limit"
        )


# ─────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────

def _init_constrained_path(
    graph: Graph, source: int, target: int,
    waypoints: List[int], forbidden: Set[int]
) -> List[int]:
    """
    Try to build an initial path that visits waypoints in order.
    Falls back to random walk if greedy fails.
    """
    path = [source]
    visited = {source}
    stops = list(waypoints) + [target]
    current = source

    for stop in stops:
        if stop in visited:
            continue
        sub = _greedy_walk(graph, current, stop, visited, forbidden)
        if sub:
            for node in sub[1:]:
                if node not in visited:
                    path.append(node)
                    visited.add(node)
            current = stop
        else:
            # Can't reach stop — just teleport (will be penalized by energy)
            if stop not in visited:
                path.append(stop)
                visited.add(stop)
            current = stop

    if path[-1] != target:
        path.append(target)

    return path


def _greedy_walk(
    graph: Graph, start: int, end: int,
    global_visited: Set[int], forbidden: Set[int],
    max_steps: int = 50
) -> Optional[List[int]]:
    """Greedy walk from start to end avoiding forbidden + already visited."""
    path = [start]
    current = start
    local_visited = {start}

    for _ in range(max_steps):
        if current == end:
            return path
        neighbors = [
            n for n in graph.get_neighbors(current)
            if n not in local_visited and n not in forbidden
        ]
        if not neighbors:
            # Allow revisiting if stuck
            neighbors = [
                n for n in graph.get_neighbors(current)
                if n not in forbidden and n != current
            ]
        if not neighbors:
            break
        # Prefer neighbor closest to end by node ID proxy
        next_node = min(neighbors, key=lambda n: abs(n - end))
        path.append(next_node)
        local_visited.add(next_node)
        current = next_node

    return path if path[-1] == end else None


def _generate_constrained_neighbor(
    graph: Graph, path: List[int], source: int, target: int,
    waypoints: List[int], forbidden: Set[int], usable_nodes: List[int]
) -> List[int]:
    """Generate neighboring solution with constraint-aware mutations."""
    if len(path) <= 2:
        return list(path)

    new_path = list(path)
    # Weight operations: inserting waypoints is preferred
    missing_wp = [w for w in waypoints if w not in new_path]

    if missing_wp and random.random() < 0.5:
        # Insert a missing waypoint at a random interior position
        wp = random.choice(missing_wp)
        pos = random.randint(1, len(new_path) - 1)
        new_path.insert(pos, wp)
    else:
        operation = random.choice(['insert', 'remove', 'replace', 'swap'])

        if operation == 'insert':
            available = [n for n in usable_nodes if n not in new_path and n not in forbidden]
            if available:
                node = random.choice(available)
                pos = random.randint(1, len(new_path) - 1)
                new_path.insert(pos, node)

        elif operation == 'remove' and len(new_path) > 2:
            # Don't remove mandatory waypoints
            removable = [
                i for i in range(1, len(new_path) - 1)
                if new_path[i] not in waypoints
            ]
            if removable:
                new_path.pop(random.choice(removable))

        elif operation == 'replace' and len(new_path) > 2:
            # Replace a non-waypoint intermediate
            replaceable = [
                i for i in range(1, len(new_path) - 1)
                if new_path[i] not in waypoints
            ]
            available = [n for n in usable_nodes if n not in new_path and n not in forbidden]
            if replaceable and available:
                pos = random.choice(replaceable)
                new_path[pos] = random.choice(available)

        elif operation == 'swap' and len(new_path) > 3:
            i = random.randint(1, len(new_path) - 2)
            j = random.randint(1, len(new_path) - 2)
            if i != j:
                new_path[i], new_path[j] = new_path[j], new_path[i]

    # Fix endpoints
    if new_path[0] != source:
        new_path[0] = source
    if new_path[-1] != target:
        new_path[-1] = target

    return new_path


def _energy(
    graph: Graph, path: List[int], source: int, target: int,
    waypoints: List[int], forbidden: Set[int],
    waypoint_penalty: float, forbidden_penalty: float, constraint_penalty: float
) -> float:
    """Compute total energy of a constrained path."""
    if not path:
        return constraint_penalty * 100

    energy = 0.0
    violations = 0

    if path[0] != source:
        violations += 1
    if path[-1] != target:
        violations += 1

    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        w = graph.get_weight(u, v)
        if w is not None:
            energy += w
        else:
            violations += 2

    # Penalise missing waypoints
    missing = sum(1 for wp in waypoints if wp not in path)
    energy += waypoint_penalty * missing

    # Penalise forbidden nodes in path
    forbidden_count = sum(1 for n in path if n in forbidden)
    energy += forbidden_penalty * forbidden_count

    energy += constraint_penalty * violations
    return energy


def _is_valid(graph: Graph, path: List[int], source: int, target: int) -> bool:
    if not path or len(path) < 2:
        return False
    if path[0] != source or path[-1] != target:
        return False
    return all(graph.has_edge(path[i], path[i + 1]) for i in range(len(path) - 1))


def _count_satisfied_waypoints(path: List[int], waypoints: List[int]) -> int:
    return sum(1 for wp in waypoints if wp in path)


def _path_distance(graph: Graph, path: List[int]) -> float:
    total = 0.0
    for i in range(len(path) - 1):
        w = graph.get_weight(path[i], path[i + 1])
        if w is None:
            return float('inf')
        total += w
    return total
