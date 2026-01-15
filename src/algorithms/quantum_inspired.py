"""
Energy-Based Quantum-Inspired Algorithm for Shortest Path.

This is a probabilistic, optimization-driven approach that formulates
the shortest path problem as energy minimization, inspired by quantum
annealing concepts.

The energy function penalizes:
1. Total path weight (minimize distance)
2. Invalid paths (constraint violations)
3. Disconnected segments

Uses simulated annealing-style probabilistic state transitions.
"""
import random
import math
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from src.graph import Graph


@dataclass
class QuantumIteration:
    """Records state at each iteration of the quantum-inspired algorithm."""
    iteration: int
    current_path: List[int]
    current_energy: float
    temperature: float
    accepted_transition: bool
    path_valid: bool


@dataclass
class QuantumResult:
    """Complete result from quantum-inspired algorithm."""
    path: Optional[List[int]]
    distance: float
    energy: float
    iterations: int
    history: List[QuantumIteration]
    success: bool
    convergence_iteration: int
    stability_runs: int
    message: str


def quantum_inspired_shortest_path(
    graph: Graph, 
    source: int, 
    target: int,
    max_iterations: int = 500,
    initial_temperature: float = 10.0,
    cooling_rate: float = 0.98,
    constraint_penalty: float = 1000.0,
    stability_threshold: int = 50,
    seed: Optional[int] = None
) -> QuantumResult:
    """
    Quantum-inspired energy minimization for shortest path.
    
    Energy Function:
        E(path) = Σ edge_weights + λ * constraint_violations
        
    Where constraint violations include:
        - Non-existent edges (high penalty)
        - Path doesn't reach target (high penalty)
        - Path doesn't start from source (high penalty)
    
    Args:
        graph: The graph to search
        source: Starting node
        target: Destination node
        max_iterations: Maximum optimization iterations
        initial_temperature: Starting temperature for annealing
        cooling_rate: Temperature decay per iteration (0 < rate < 1)
        constraint_penalty: Penalty multiplier for invalid paths
        stability_threshold: Iterations without improvement before early stop
        seed: Random seed for reproducibility
        
    Returns:
        QuantumResult with path, energy, and detailed iteration history
    """
    if seed is not None:
        random.seed(seed)
    
    history: List[QuantumIteration] = []
    nodes = graph.nodes
    
    # Initialize with a random valid path (if possible) or random sequence
    current_path = _initialize_path(graph, source, target)
    current_energy = _calculate_energy(graph, current_path, source, target, constraint_penalty)
    
    best_path = list(current_path)
    best_energy = current_energy
    best_valid = _is_valid_path(graph, current_path, source, target)
    
    temperature = initial_temperature
    stable_count = 0
    convergence_iteration = 0
    
    for iteration in range(max_iterations):
        # Generate neighbor solution
        new_path = _generate_neighbor(graph, current_path, source, target)
        new_energy = _calculate_energy(graph, new_path, source, target, constraint_penalty)
        
        # Metropolis acceptance criterion (quantum-inspired probabilistic transition)
        delta_e = new_energy - current_energy
        accepted = False
        
        if delta_e < 0:
            # Always accept improvements
            accepted = True
        else:
            # Probabilistically accept worse solutions (escape local minima)
            acceptance_prob = math.exp(-delta_e / temperature) if temperature > 0.01 else 0
            accepted = random.random() < acceptance_prob
        
        if accepted:
            current_path = new_path
            current_energy = new_energy
            
            # Update best solution
            current_valid = _is_valid_path(graph, current_path, source, target)
            if current_energy < best_energy or (current_valid and not best_valid):
                best_path = list(current_path)
                best_energy = current_energy
                best_valid = current_valid
                convergence_iteration = iteration + 1
                stable_count = 0
            else:
                stable_count += 1
        else:
            stable_count += 1
        
        # Record iteration
        history.append(QuantumIteration(
            iteration=iteration + 1,
            current_path=list(current_path),
            current_energy=current_energy,
            temperature=temperature,
            accepted_transition=accepted,
            path_valid=_is_valid_path(graph, current_path, source, target)
        ))
        
        # Cool down
        temperature *= cooling_rate
        
        # Early termination if stable
        if stable_count >= stability_threshold and best_valid:
            break
    
    # Calculate actual distance if path is valid
    if best_valid:
        actual_distance = _calculate_path_distance(graph, best_path)
        return QuantumResult(
            path=best_path,
            distance=actual_distance,
            energy=best_energy,
            iterations=len(history),
            history=history,
            success=True,
            convergence_iteration=convergence_iteration,
            stability_runs=1,
            message="Valid path found via energy minimization"
        )
    else:
        return QuantumResult(
            path=None,
            distance=float('inf'),
            energy=best_energy,
            iterations=len(history),
            history=history,
            success=False,
            convergence_iteration=convergence_iteration,
            stability_runs=0,
            message="No valid path found - algorithm did not converge to valid solution"
        )


def _initialize_path(graph: Graph, source: int, target: int) -> List[int]:
    """Initialize with a greedy path attempt or random walk."""
    path = [source]
    current = source
    visited = {source}
    max_steps = graph.num_nodes * 2
    
    for _ in range(max_steps):
        if current == target:
            break
            
        neighbors = [n for n in graph.get_neighbors(current) if n not in visited]
        
        if not neighbors:
            # Dead end - restart with random node
            unvisited = [n for n in graph.nodes if n not in visited and n != source]
            if not unvisited:
                break
            current = random.choice(unvisited)
            path.append(current)
            visited.add(current)
        else:
            # Greedy: prefer neighbor closest to target (by node ID as proxy)
            # Or random for exploration
            if random.random() < 0.7:
                next_node = min(neighbors, key=lambda n: abs(n - target))
            else:
                next_node = random.choice(neighbors)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
    
    # Ensure target is in path
    if path[-1] != target and target not in path:
        path.append(target)
    
    return path


def _generate_neighbor(graph: Graph, path: List[int], source: int, target: int) -> List[int]:
    """Generate a neighboring solution by modifying the path."""
    if len(path) <= 2:
        return list(path)
    
    new_path = list(path)
    operation = random.choice(['swap', 'insert', 'remove', 'replace'])
    
    if operation == 'swap' and len(new_path) > 3:
        # Swap two intermediate nodes
        i = random.randint(1, len(new_path) - 2)
        j = random.randint(1, len(new_path) - 2)
        if i != j:
            new_path[i], new_path[j] = new_path[j], new_path[i]
            
    elif operation == 'insert':
        # Insert a random node
        available = [n for n in graph.nodes if n not in new_path]
        if available:
            node = random.choice(available)
            pos = random.randint(1, len(new_path) - 1)
            new_path.insert(pos, node)
            
    elif operation == 'remove' and len(new_path) > 2:
        # Remove an intermediate node
        if len(new_path) > 2:
            pos = random.randint(1, len(new_path) - 2)
            new_path.pop(pos)
            
    elif operation == 'replace' and len(new_path) > 2:
        # Replace an intermediate node with a random one
        available = [n for n in graph.nodes if n not in new_path]
        if available:
            pos = random.randint(1, len(new_path) - 2)
            new_path[pos] = random.choice(available)
    
    # Ensure source and target are correct
    if new_path[0] != source:
        new_path[0] = source
    if new_path[-1] != target:
        new_path[-1] = target
    
    return new_path


def _calculate_energy(
    graph: Graph, 
    path: List[int], 
    source: int, 
    target: int, 
    constraint_penalty: float
) -> float:
    """
    Calculate total energy of a path solution.
    
    Energy = path_weight + penalty * violations
    """
    if not path:
        return constraint_penalty * 10
    
    energy = 0.0
    violations = 0
    
    # Check source and target
    if path[0] != source:
        violations += 1
    if path[-1] != target:
        violations += 1
    
    # Sum edge weights and check validity
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        weight = graph.get_weight(u, v)
        
        if weight is not None:
            energy += weight
        else:
            # Edge doesn't exist - heavy penalty
            violations += 2
    
    # Add constraint penalty
    energy += constraint_penalty * violations
    
    return energy


def _is_valid_path(graph: Graph, path: List[int], source: int, target: int) -> bool:
    """Check if path is valid (exists in graph and connects source to target)."""
    if not path or len(path) < 2:
        return False
    if path[0] != source or path[-1] != target:
        return False
    
    for i in range(len(path) - 1):
        if not graph.has_edge(path[i], path[i + 1]):
            return False
    
    return True


def _calculate_path_distance(graph: Graph, path: List[int]) -> float:
    """Calculate actual distance of a valid path."""
    total = 0.0
    for i in range(len(path) - 1):
        weight = graph.get_weight(path[i], path[i + 1])
        if weight is not None:
            total += weight
        else:
            return float('inf')
    return total
