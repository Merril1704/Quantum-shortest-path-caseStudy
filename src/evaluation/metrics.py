"""
Evaluation metrics for shortest path algorithm comparison.
"""
from typing import List, Dict, Optional, Any
from src.graph import Graph


def verify_path_correctness(graph: Graph, path: List[int], source: int, target: int) -> Dict[str, Any]:
    """
    Verify that a path is valid and correctly connects source to target.
    
    Returns:
        Dictionary with validation results:
        - valid: bool
        - starts_at_source: bool
        - ends_at_target: bool
        - all_edges_exist: bool
        - issues: list of strings describing problems
    """
    result = {
        "valid": True,
        "starts_at_source": True,
        "ends_at_target": True,
        "all_edges_exist": True,
        "issues": []
    }
    
    if not path:
        result["valid"] = False
        result["issues"].append("Path is empty")
        return result
    
    # Check source
    if path[0] != source:
        result["starts_at_source"] = False
        result["valid"] = False
        result["issues"].append(f"Path starts at {path[0]}, expected {source}")
    
    # Check target
    if path[-1] != target:
        result["ends_at_target"] = False
        result["valid"] = False
        result["issues"].append(f"Path ends at {path[-1]}, expected {target}")
    
    # Check all edges exist
    for i in range(len(path) - 1):
        if not graph.has_edge(path[i], path[i + 1]):
            result["all_edges_exist"] = False
            result["valid"] = False
            result["issues"].append(f"Edge ({path[i]} -> {path[i + 1]}) does not exist")
    
    return result


def calculate_path_length(graph: Graph, path: List[int]) -> float:
    """Calculate total weight of a path."""
    if not path or len(path) < 2:
        return float('inf')
    
    total = 0.0
    for i in range(len(path) - 1):
        weight = graph.get_weight(path[i], path[i + 1])
        if weight is None:
            return float('inf')
        total += weight
    
    return total


def count_iterations(history: List[Any]) -> int:
    """Count total iterations from history."""
    return len(history)


def analyze_convergence(history: List[Any], distance_key: str = "distances") -> Dict[str, Any]:
    """
    Analyze convergence behavior from iteration history.
    
    Args:
        history: List of iteration records
        distance_key: Key to access distance/energy values
        
    Returns:
        Dictionary with convergence analysis:
        - total_iterations: int
        - converged_at: int (iteration where solution stabilized)
        - improvement_pattern: str (monotonic, oscillating, plateau)
        - final_stable_iterations: int (iterations without change at end)
    """
    if not history:
        return {
            "total_iterations": 0,
            "converged_at": 0,
            "improvement_pattern": "unknown",
            "final_stable_iterations": 0
        }
    
    total = len(history)
    
    # Track when the solution stabilized
    # For different algorithm types, we look at different attributes
    values = []
    for h in history:
        if hasattr(h, 'current_energy'):
            values.append(h.current_energy)
        elif hasattr(h, 'distances'):
            # For Dijkstra/Bellman-Ford, track current best distance
            distances = h.distances
            values.append(min(distances.values()) if distances else float('inf'))
        else:
            values.append(0)
    
    # Find convergence point (last significant change)
    threshold = 0.0001
    converged_at = 1
    for i in range(1, len(values)):
        if abs(values[i] - values[i-1]) > threshold:
            converged_at = i + 1
    
    # Count stable iterations at end
    stable_count = total - converged_at
    
    # Determine pattern
    if len(values) <= 1:
        pattern = "immediate"
    else:
        increasing = sum(1 for i in range(1, len(values)) if values[i] > values[i-1])
        decreasing = sum(1 for i in range(1, len(values)) if values[i] < values[i-1])
        
        if decreasing > 0 and increasing == 0:
            pattern = "monotonic_decrease"
        elif increasing > 0 and decreasing == 0:
            pattern = "monotonic_increase"
        elif increasing > 0 and decreasing > 0:
            pattern = "oscillating"
        else:
            pattern = "plateau"
    
    return {
        "total_iterations": total,
        "converged_at": converged_at,
        "improvement_pattern": pattern,
        "final_stable_iterations": stable_count
    }


def compare_paths(path1: Optional[List[int]], path2: Optional[List[int]]) -> Dict[str, Any]:
    """Compare two paths for similarity."""
    if path1 is None and path2 is None:
        return {"identical": True, "both_failed": True}
    if path1 is None or path2 is None:
        return {"identical": False, "one_failed": True}
    
    identical = path1 == path2
    common_nodes = set(path1) & set(path2)
    
    return {
        "identical": identical,
        "path1_length": len(path1),
        "path2_length": len(path2),
        "common_nodes": len(common_nodes),
        "overlap_ratio": len(common_nodes) / max(len(set(path1)), len(set(path2)))
    }
