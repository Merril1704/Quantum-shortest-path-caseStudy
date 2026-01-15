"""
Algorithm comparison runner - executes all algorithms on the same graph
and collects structured results.
"""
import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from src.graph import Graph
from src.algorithms.dijkstra import dijkstra, DijkstraResult
from src.algorithms.bellman_ford import bellman_ford, BellmanFordResult
from src.algorithms.quantum_inspired import quantum_inspired_shortest_path, QuantumResult
from src.evaluation.metrics import (
    verify_path_correctness, 
    calculate_path_length,
    analyze_convergence
)


@dataclass
class AlgorithmComparison:
    """Results from comparing all algorithms on a single graph."""
    graph_name: str
    graph_info: Dict[str, Any]
    source: int
    target: int
    dijkstra_result: Dict[str, Any]
    bellman_ford_result: Dict[str, Any]
    quantum_result: Dict[str, Any]
    comparison_summary: Dict[str, Any]
    timestamp: str


class AlgorithmRunner:
    """
    Runs all shortest path algorithms on a graph and collects results.
    """
    
    def __init__(self, quantum_seed: Optional[int] = 42):
        """
        Initialize the runner.
        
        Args:
            quantum_seed: Random seed for quantum-inspired algorithm reproducibility
        """
        self.quantum_seed = quantum_seed
    
    def run_all(
        self, 
        graph: Graph, 
        source: int, 
        target: int, 
        graph_name: str = "unnamed"
    ) -> AlgorithmComparison:
        """
        Run all three algorithms on the same graph.
        
        Args:
            graph: The graph to analyze
            source: Source node
            target: Target node
            graph_name: Name for identification
            
        Returns:
            AlgorithmComparison with all results
        """
        # Collect graph info
        graph_info = {
            "nodes": graph.num_nodes,
            "edges": graph.num_edges,
            "density": round(graph.density(), 3),
            "directed": graph.directed,
            "has_negative_weights": graph.has_negative_weights()
        }
        
        # Run Dijkstra
        dijkstra_res = self._run_dijkstra(graph, source, target)
        
        # Run Bellman-Ford
        bellman_res = self._run_bellman_ford(graph, source, target)
        
        # Run Quantum-Inspired
        quantum_res = self._run_quantum(graph, source, target)
        
        # Generate comparison summary
        summary = self._generate_summary(
            graph, source, target,
            dijkstra_res, bellman_res, quantum_res
        )
        
        return AlgorithmComparison(
            graph_name=graph_name,
            graph_info=graph_info,
            source=source,
            target=target,
            dijkstra_result=dijkstra_res,
            bellman_ford_result=bellman_res,
            quantum_result=quantum_res,
            comparison_summary=summary,
            timestamp=datetime.now().isoformat()
        )
    
    def _run_dijkstra(self, graph: Graph, source: int, target: int) -> Dict[str, Any]:
        """Run Dijkstra and format results."""
        result = dijkstra(graph, source, target)
        
        convergence = analyze_convergence(result.history)
        
        return {
            "algorithm": "Dijkstra",
            "path": result.path,
            "distance": result.distance if result.distance != float('inf') else "infinity",
            "iterations": result.iterations,
            "success": result.success,
            "message": result.message,
            "convergence": convergence,
            "path_verification": verify_path_correctness(graph, result.path, source, target) if result.path else None
        }
    
    def _run_bellman_ford(self, graph: Graph, source: int, target: int) -> Dict[str, Any]:
        """Run Bellman-Ford and format results."""
        result = bellman_ford(graph, source, target)
        
        convergence = analyze_convergence(result.history)
        
        return {
            "algorithm": "Bellman-Ford",
            "path": result.path,
            "distance": result.distance if result.distance != float('inf') else "infinity",
            "iterations": result.iterations,
            "success": result.success,
            "has_negative_cycle": result.has_negative_cycle,
            "message": result.message,
            "convergence": convergence,
            "path_verification": verify_path_correctness(graph, result.path, source, target) if result.path else None
        }
    
    def _run_quantum(self, graph: Graph, source: int, target: int) -> Dict[str, Any]:
        """Run Quantum-Inspired algorithm and format results."""
        result = quantum_inspired_shortest_path(
            graph, source, target, 
            seed=self.quantum_seed,
            max_iterations=500
        )
        
        convergence = analyze_convergence(result.history)
        
        return {
            "algorithm": "Quantum-Inspired",
            "path": result.path,
            "distance": result.distance if result.distance != float('inf') else "infinity",
            "energy": result.energy,
            "iterations": result.iterations,
            "success": result.success,
            "convergence_iteration": result.convergence_iteration,
            "message": result.message,
            "convergence": convergence,
            "path_verification": verify_path_correctness(graph, result.path, source, target) if result.path else None
        }
    
    def _generate_summary(
        self,
        graph: Graph,
        source: int,
        target: int,
        dijkstra_res: Dict,
        bellman_res: Dict,
        quantum_res: Dict
    ) -> Dict[str, Any]:
        """Generate comparison summary."""
        results = [dijkstra_res, bellman_res, quantum_res]
        successful = [r for r in results if r["success"]]
        
        # Find best distance
        distances = []
        for r in results:
            if r["success"] and r["distance"] != "infinity":
                distances.append((r["algorithm"], r["distance"]))
        
        distances.sort(key=lambda x: x[1])
        
        best_distance = distances[0] if distances else None
        
        # Check agreement
        paths = [r["path"] for r in results if r["path"]]
        all_same_path = len(set(tuple(p) for p in paths)) <= 1 if paths else False
        
        # Iteration comparison
        iterations = {r["algorithm"]: r["iterations"] for r in results}
        
        return {
            "algorithms_succeeded": len(successful),
            "best_algorithm": best_distance[0] if best_distance else None,
            "best_distance": best_distance[1] if best_distance else None,
            "all_paths_identical": all_same_path,
            "iteration_counts": iterations,
            "key_differences": self._identify_differences(dijkstra_res, bellman_res, quantum_res, graph)
        }
    
    def _identify_differences(
        self, 
        dijkstra_res: Dict, 
        bellman_res: Dict, 
        quantum_res: Dict,
        graph: Graph
    ) -> List[str]:
        """Identify key behavioral differences between algorithms."""
        differences = []
        
        # Check if Dijkstra failed due to negative weights
        if graph.has_negative_weights():
            if dijkstra_res["success"] and bellman_res["success"]:
                d_dist = dijkstra_res["distance"]
                b_dist = bellman_res["distance"]
                if d_dist != "infinity" and b_dist != "infinity" and d_dist != b_dist:
                    differences.append(
                        f"Dijkstra found distance {d_dist} but Bellman-Ford found {b_dist} "
                        f"(negative weights affected Dijkstra)"
                    )
        
        # Check for negative cycle
        if bellman_res.get("has_negative_cycle"):
            differences.append("Bellman-Ford detected negative cycle")
        
        # Iteration comparison
        if quantum_res["iterations"] > max(dijkstra_res["iterations"], bellman_res["iterations"]) * 3:
            differences.append(
                f"Quantum-inspired used significantly more iterations "
                f"({quantum_res['iterations']} vs {dijkstra_res['iterations']}/{bellman_res['iterations']})"
            )
        
        # Path differences
        if dijkstra_res["path"] and bellman_res["path"]:
            if dijkstra_res["path"] != bellman_res["path"]:
                differences.append("Dijkstra and Bellman-Ford found different paths")
        
        return differences


def save_comparison_results(comparison: AlgorithmComparison, output_dir: str) -> str:
    """Save comparison results to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{comparison.graph_name}_results.json"
    filepath = os.path.join(output_dir, filename)
    
    # Convert to dict (handle dataclass)
    data = asdict(comparison)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    return filepath
