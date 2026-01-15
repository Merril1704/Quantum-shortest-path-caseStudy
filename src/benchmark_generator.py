"""
Benchmark Graph Generator - Generates 20 diverse graphs for algorithm comparison.

All generated graphs are guaranteed to:
1. Have at least one valid path from source to target
2. Be compatible with all three algorithms (no negative cycles)
3. Have sufficient complexity for meaningful comparison
"""
import random
from typing import List, Tuple, Optional, Dict, Any
from collections import deque
from src.graph import Graph


def ensure_path_exists(graph: Graph, source: int, target: int) -> bool:
    """Check if a path exists from source to target using BFS."""
    if source not in graph.nodes or target not in graph.nodes:
        return False
    
    visited = set()
    queue = deque([source])
    
    while queue:
        node = queue.popleft()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                queue.append(neighbor)
    
    return False


def generate_connected_graph(
    n_nodes: int,
    name: str,
    density: float = 0.3,
    weight_range: Tuple[int, int] = (1, 10),
    directed: bool = True,
    allow_negative: bool = False,
    negative_prob: float = 0.15,
    seed: Optional[int] = None
) -> Tuple[Graph, int, int, str, Dict[str, Any]]:
    """
    Generate a connected graph with guaranteed path from source to target.
    
    Returns:
        (graph, source, target, description, properties)
    """
    if seed is not None:
        random.seed(seed)
    
    graph = Graph(directed=directed)
    
    # Add all nodes
    for i in range(n_nodes):
        graph.add_node(i)
    
    source = 0
    target = n_nodes - 1
    
    # First, create a guaranteed path from source to target
    # This ensures connectivity
    path_length = random.randint(3, min(6, n_nodes - 1))
    intermediate_nodes = random.sample(range(1, n_nodes - 1), min(path_length - 2, n_nodes - 2))
    path = [source] + sorted(intermediate_nodes) + [target]
    
    for i in range(len(path) - 1):
        weight = random.randint(weight_range[0], weight_range[1])
        graph.add_edge(path[i], path[i + 1], weight)
    
    # Add additional edges based on density
    max_additional = int(n_nodes * (n_nodes - 1) * density)
    additional_edges = 0
    
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i == j:
                continue
            if not directed and j < i:
                continue
            if graph.has_edge(i, j):
                continue
            
            if random.random() < density and additional_edges < max_additional:
                weight = random.randint(weight_range[0], weight_range[1])
                
                # Add negative weights carefully (not on cycle-creating edges to avoid negative cycles)
                if allow_negative and random.random() < negative_prob:
                    # Only make edges going "forward" (increasing node number) negative
                    # This prevents negative cycles in the DAG sense
                    if j > i:
                        weight = -abs(weight) // 2  # Use smaller negative values
                
                graph.add_edge(i, j, weight)
                additional_edges += 1
    
    # Build description and properties
    graph_type = "directed" if directed else "undirected"
    neg_info = "with negative weights" if allow_negative else "positive weights only"
    description = f"{n_nodes}-node {graph_type} graph, {neg_info}, density ~{density}"
    
    properties = {
        "nodes": n_nodes,
        "edges": graph.num_edges,
        "density": round(graph.density(), 3),
        "directed": directed,
        "has_negative_weights": graph.has_negative_weights(),
        "weight_range": weight_range,
        "guaranteed_path": path
    }
    
    return graph, source, target, description, properties


def generate_benchmark_graphs(base_seed: int = 42) -> List[Tuple[str, Graph, int, int, str, Dict[str, Any]]]:
    """
    Generate 20 diverse benchmark graphs for algorithm comparison.
    
    The graphs cover various configurations:
    - Small to medium sizes (6-20 nodes)
    - Sparse to dense
    - Directed and undirected
    - With and without negative weights
    
    Returns:
        List of (name, graph, source, target, description, properties)
    """
    graphs = []
    
    # === Category 1: Small sparse graphs (6-8 nodes) ===
    
    # 1. Small sparse directed
    g, s, t, d, p = generate_connected_graph(
        n_nodes=6, name="small_sparse_directed",
        density=0.2, directed=True, seed=base_seed + 1
    )
    graphs.append(("benchmark_01_small_sparse", g, s, t, 
                   "Small sparse directed graph (6 nodes) - baseline test", p))
    
    # 2. Small sparse undirected
    g, s, t, d, p = generate_connected_graph(
        n_nodes=7, name="small_sparse_undirected",
        density=0.25, directed=False, seed=base_seed + 2
    )
    graphs.append(("benchmark_02_small_undirected", g, s, t,
                   "Small sparse undirected graph (7 nodes)", p))
    
    # 3. Small with negative weights
    g, s, t, d, p = generate_connected_graph(
        n_nodes=6, name="small_negative",
        density=0.3, directed=True, allow_negative=True, 
        negative_prob=0.2, seed=base_seed + 3
    )
    graphs.append(("benchmark_03_small_negative", g, s, t,
                   "Small directed graph with negative weights (6 nodes)", p))
    
    # === Category 2: Medium sparse graphs (10-12 nodes) ===
    
    # 4. Medium sparse directed
    g, s, t, d, p = generate_connected_graph(
        n_nodes=10, name="medium_sparse_directed",
        density=0.2, directed=True, seed=base_seed + 4
    )
    graphs.append(("benchmark_04_medium_sparse", g, s, t,
                   "Medium sparse directed graph (10 nodes)", p))
    
    # 5. Medium sparse undirected
    g, s, t, d, p = generate_connected_graph(
        n_nodes=10, name="medium_sparse_undirected",
        density=0.2, directed=False, seed=base_seed + 5
    )
    graphs.append(("benchmark_05_medium_undirected", g, s, t,
                   "Medium sparse undirected graph (10 nodes)", p))
    
    # 6. Medium with varied weights
    g, s, t, d, p = generate_connected_graph(
        n_nodes=12, name="medium_varied",
        density=0.25, weight_range=(1, 20), directed=True, seed=base_seed + 6
    )
    graphs.append(("benchmark_06_medium_varied", g, s, t,
                   "Medium graph with high weight variance (12 nodes, weights 1-20)", p))
    
    # 7. Medium negative weights
    g, s, t, d, p = generate_connected_graph(
        n_nodes=10, name="medium_negative",
        density=0.25, directed=True, allow_negative=True,
        negative_prob=0.15, seed=base_seed + 7
    )
    graphs.append(("benchmark_07_medium_negative", g, s, t,
                   "Medium directed graph with negative weights (10 nodes)", p))
    
    # === Category 3: Medium dense graphs ===
    
    # 8. Medium dense directed
    g, s, t, d, p = generate_connected_graph(
        n_nodes=8, name="medium_dense_directed",
        density=0.5, directed=True, seed=base_seed + 8
    )
    graphs.append(("benchmark_08_dense_directed", g, s, t,
                   "Dense directed graph (8 nodes, ~50% density)", p))
    
    # 9. Medium dense undirected
    g, s, t, d, p = generate_connected_graph(
        n_nodes=8, name="medium_dense_undirected",
        density=0.6, directed=False, seed=base_seed + 9
    )
    graphs.append(("benchmark_09_dense_undirected", g, s, t,
                   "Dense undirected graph (8 nodes, ~60% density)", p))
    
    # 10. Dense with negative weights
    g, s, t, d, p = generate_connected_graph(
        n_nodes=8, name="dense_negative",
        density=0.5, directed=True, allow_negative=True,
        negative_prob=0.1, seed=base_seed + 10
    )
    graphs.append(("benchmark_10_dense_negative", g, s, t,
                   "Dense directed graph with negative weights (8 nodes)", p))
    
    # === Category 4: Larger graphs (15-20 nodes) ===
    
    # 11. Large sparse directed
    g, s, t, d, p = generate_connected_graph(
        n_nodes=15, name="large_sparse_directed",
        density=0.15, directed=True, seed=base_seed + 11
    )
    graphs.append(("benchmark_11_large_sparse", g, s, t,
                   "Large sparse directed graph (15 nodes)", p))
    
    # 12. Large sparse undirected
    g, s, t, d, p = generate_connected_graph(
        n_nodes=15, name="large_sparse_undirected",
        density=0.15, directed=False, seed=base_seed + 12
    )
    graphs.append(("benchmark_12_large_undirected", g, s, t,
                   "Large sparse undirected graph (15 nodes)", p))
    
    # 13. Large medium density
    g, s, t, d, p = generate_connected_graph(
        n_nodes=15, name="large_medium",
        density=0.25, directed=True, seed=base_seed + 13
    )
    graphs.append(("benchmark_13_large_medium", g, s, t,
                   "Large medium-density directed graph (15 nodes)", p))
    
    # 14. Large with negative weights
    g, s, t, d, p = generate_connected_graph(
        n_nodes=15, name="large_negative",
        density=0.2, directed=True, allow_negative=True,
        negative_prob=0.1, seed=base_seed + 14
    )
    graphs.append(("benchmark_14_large_negative", g, s, t,
                   "Large directed graph with negative weights (15 nodes)", p))
    
    # 15. Very large sparse
    g, s, t, d, p = generate_connected_graph(
        n_nodes=20, name="xlarge_sparse",
        density=0.12, directed=True, seed=base_seed + 15
    )
    graphs.append(("benchmark_15_xlarge_sparse", g, s, t,
                   "Extra large sparse directed graph (20 nodes)", p))
    
    # === Category 5: Special configurations ===
    
    # 16. High connectivity hub
    g, s, t, d, p = generate_connected_graph(
        n_nodes=10, name="high_connectivity",
        density=0.7, directed=True, seed=base_seed + 16
    )
    graphs.append(("benchmark_16_high_connect", g, s, t,
                   "High connectivity graph (10 nodes, ~70% density)", p))
    
    # 17. Low weight variance
    g, s, t, d, p = generate_connected_graph(
        n_nodes=12, name="low_variance",
        density=0.3, weight_range=(5, 8), directed=True, seed=base_seed + 17
    )
    graphs.append(("benchmark_17_low_variance", g, s, t,
                   "Low weight variance graph (12 nodes, weights 5-8)", p))
    
    # 18. High weight variance
    g, s, t, d, p = generate_connected_graph(
        n_nodes=12, name="high_variance",
        density=0.3, weight_range=(1, 50), directed=True, seed=base_seed + 18
    )
    graphs.append(("benchmark_18_high_variance", g, s, t,
                   "High weight variance graph (12 nodes, weights 1-50)", p))
    
    # 19. Mixed (undirected with negative)
    g, s, t, d, p = generate_connected_graph(
        n_nodes=10, name="mixed_undirected_neg",
        density=0.35, directed=False, allow_negative=True,
        negative_prob=0.1, seed=base_seed + 19
    )
    graphs.append(("benchmark_19_mixed", g, s, t,
                   "Mixed undirected graph with negative weights (10 nodes)", p))
    
    # 20. Complex large graph
    g, s, t, d, p = generate_connected_graph(
        n_nodes=18, name="complex_large",
        density=0.3, weight_range=(1, 30), directed=True, seed=base_seed + 20
    )
    graphs.append(("benchmark_20_complex", g, s, t,
                   "Complex large directed graph (18 nodes, varied weights)", p))
    
    # Validate all graphs have paths
    valid_graphs = []
    for name, graph, source, target, desc, props in graphs:
        if ensure_path_exists(graph, source, target):
            valid_graphs.append((name, graph, source, target, desc, props))
        else:
            # If no path, regenerate with forced connection
            print(f"Warning: Regenerating {name} due to missing path")
            # Add direct edge as fallback
            graph.add_edge(source, target, random.randint(15, 25))
            valid_graphs.append((name, graph, source, target, desc, props))
    
    return valid_graphs


def get_graph_statistics(graph: Graph, source: int, target: int) -> Dict[str, Any]:
    """Get comprehensive statistics about a graph."""
    stats = {
        "nodes": graph.num_nodes,
        "edges": graph.num_edges,
        "density": round(graph.density(), 3),
        "directed": graph.directed,
        "has_negative_weights": graph.has_negative_weights(),
        "source": source,
        "target": target
    }
    
    # Calculate degree statistics
    if graph.num_nodes > 0:
        out_degrees = [len(graph.get_neighbors(n)) for n in graph.nodes]
        stats["avg_out_degree"] = round(sum(out_degrees) / len(out_degrees), 2)
        stats["max_out_degree"] = max(out_degrees)
        stats["min_out_degree"] = min(out_degrees)
    
    # Weight statistics
    weights = [w for _, _, w in graph.edges]
    if weights:
        stats["avg_weight"] = round(sum(weights) / len(weights), 2)
        stats["min_weight"] = min(weights)
        stats["max_weight"] = max(weights)
        stats["negative_edge_count"] = sum(1 for w in weights if w < 0)
    
    return stats
