"""
Graph generation utilities with curated test graphs designed to
highlight differences between shortest path algorithms.
"""
import random
from typing import Optional, Tuple, List
from src.graph import Graph


def validate_graph_complexity(graph: Graph, source: int, target: int) -> dict:
    """
    Validate that a graph has sufficient complexity for meaningful algorithm comparison.
    
    Returns:
        Dictionary with complexity metrics and recommendations.
    """
    result = {
        "valid": True,
        "warnings": [],
        "metrics": {}
    }
    
    # Check basic properties
    result["metrics"]["nodes"] = graph.num_nodes
    result["metrics"]["edges"] = graph.num_edges
    result["metrics"]["density"] = round(graph.density(), 3)
    result["metrics"]["has_negative_weights"] = graph.has_negative_weights()
    
    # Check if source and target exist
    if source not in graph.nodes:
        result["valid"] = False
        result["warnings"].append(f"Source node {source} not in graph")
    if target not in graph.nodes:
        result["valid"] = False
        result["warnings"].append(f"Target node {target} not in graph")
    
    # Check for sufficient edges
    if graph.num_edges < graph.num_nodes:
        result["warnings"].append("Very sparse graph - may have limited path options")
    
    # Check for uniform weights (boring case)
    weights = [w for _, _, w in graph.edges]
    if len(set(weights)) <= 2:
        result["warnings"].append("Low weight variety - algorithms may behave identically")
    
    # Check source has outgoing edges
    if len(graph.get_neighbors(source)) == 0:
        result["valid"] = False
        result["warnings"].append("Source has no outgoing edges")
    
    return result


def generate_random_graph(
    n_nodes: int,
    density: float = 0.3,
    weight_range: Tuple[int, int] = (1, 10),
    directed: bool = True,
    allow_negative: bool = False,
    negative_prob: float = 0.2,
    seed: Optional[int] = None
) -> Graph:
    """
    Generate a random graph with specified properties.
    
    Args:
        n_nodes: Number of nodes (will be labeled 0 to n_nodes-1)
        density: Edge density (0 to 1), probability of edge existing
        weight_range: (min, max) for edge weights
        directed: If True, create directed graph
        allow_negative: If True, some edges may have negative weights
        negative_prob: Probability of edge being negative when allow_negative=True
        seed: Random seed for reproducibility
    """
    if seed is not None:
        random.seed(seed)
    
    graph = Graph(directed=directed)
    
    # Add all nodes
    for i in range(n_nodes):
        graph.add_node(i)
    
    # Add edges based on density
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i == j:
                continue
            if not directed and j < i:
                continue  # Avoid duplicate edges for undirected
            
            if random.random() < density:
                weight = random.randint(weight_range[0], weight_range[1])
                if allow_negative and random.random() < negative_prob:
                    weight = -abs(weight)
                graph.add_edge(i, j, weight)
    
    return graph


def create_sparse_basic() -> Tuple[Graph, int, int, str]:
    """
    Sparse directed graph with multiple paths of different lengths.
    Good for observing greedy vs optimal behavior.
    
    Returns: (graph, source, target, description)
    """
    graph = Graph(directed=True)
    
    # Structure: 0 -> 1 -> 2 -> 7 (greedy path, total=15)
    #            0 -> 3 -> 4 -> 5 -> 7 (longer but cheaper, total=10)
    edges = [
        (0, 1, 3), (1, 2, 4), (2, 7, 8),   # Direct path: 15
        (0, 3, 1), (3, 4, 2), (4, 5, 3), (5, 7, 4),  # Longer path: 10
        (0, 6, 5), (6, 7, 12),  # Another option: 17
        (1, 4, 6),  # Cross-connection
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 7, "Sparse graph with greedy trap - direct path looks good but longer path is cheaper"


def create_dense_mesh() -> Tuple[Graph, int, int, str]:
    """
    Dense undirected mesh with many alternatives.
    Tests algorithm efficiency with many path options.
    """
    graph = Graph(directed=False)
    
    # 12-node mesh with varied weights
    edges = [
        (0, 1, 4), (0, 2, 2), (0, 3, 7),
        (1, 2, 1), (1, 4, 5), (1, 5, 3),
        (2, 3, 3), (2, 5, 8), (2, 6, 6),
        (3, 6, 2), (3, 7, 4),
        (4, 5, 2), (4, 8, 6), (4, 9, 3),
        (5, 6, 1), (5, 8, 7), (5, 9, 4),
        (6, 7, 3), (6, 9, 5), (6, 10, 2),
        (7, 10, 1), (7, 11, 8),
        (8, 9, 2), (8, 11, 5),
        (9, 10, 3), (9, 11, 4),
        (10, 11, 2),
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 11, "Dense mesh with 12 nodes - many alternative paths to explore"


def create_negative_shortcut() -> Tuple[Graph, int, int, str]:
    """
    Graph with negative edge that creates a shorter path.
    Dijkstra will fail here; Bellman-Ford should find optimal.
    """
    graph = Graph(directed=True)
    
    # Without negative edge: 0->1->2->5 = 12
    # With negative edge: 0->3->4->5 = 14 + (-6) = 8
    edges = [
        (0, 1, 3), (1, 2, 4), (2, 5, 5),   # Positive path: 12
        (0, 3, 6), (3, 4, 8), (4, 5, -6),  # Path with negative: 8
        (0, 2, 10),  # Direct but expensive
        (1, 4, 7),   # Cross connection
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 5, "Contains negative edge (4->5, weight=-6) that creates shorter path - Dijkstra will fail"


def create_bottleneck() -> Tuple[Graph, int, int, str]:
    """
    Graph with a single chokepoint node that all paths must pass through.
    Tests how algorithms handle constrained topology.
    """
    graph = Graph(directed=True)
    
    # All paths from 0 to 14 must pass through node 7
    # Left cluster: 0-6, Right cluster: 8-14, Bottleneck: 7
    edges = [
        # Left cluster paths to bottleneck
        (0, 1, 2), (0, 2, 4), (0, 3, 1),
        (1, 4, 3), (1, 5, 6),
        (2, 4, 2), (2, 5, 4), (2, 6, 5),
        (3, 5, 3), (3, 6, 2),
        (4, 7, 4), (5, 7, 2), (6, 7, 3),
        
        # Right cluster from bottleneck
        (7, 8, 2), (7, 9, 3), (7, 10, 5),
        (8, 11, 4), (8, 12, 3),
        (9, 11, 2), (9, 12, 5), (9, 13, 4),
        (10, 12, 2), (10, 13, 1),
        (11, 14, 3), (12, 14, 2), (13, 14, 4),
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 14, "Bottleneck topology - all paths must pass through node 7"


def create_diamond_paths() -> Tuple[Graph, int, int, str]:
    """
    Simple diamond with two paths of nearly equal length.
    Good for observing tie-breaking behavior.
    """
    graph = Graph(directed=False)
    
    # Diamond: 0 -> (1 or 2) -> 3 -> (4 or 5) -> 6
    edges = [
        (0, 1, 3), (0, 2, 4),    # Two starts
        (1, 3, 5), (2, 3, 4),    # Converge
        (3, 4, 3), (3, 5, 3),    # Split again
        (4, 6, 4), (5, 6, 5),    # Two ends
    ]
    
    # Path via 1,3,4: 3+5+3+4 = 15
    # Path via 2,3,4: 4+4+3+4 = 15  (tie!)
    # Path via 1,3,5: 3+5+3+5 = 16
    # Path via 2,3,5: 4+4+3+5 = 16
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 6, "Diamond structure with two equal-cost optimal paths - tests tie-breaking"


def create_negative_cycle_test() -> Tuple[Graph, int, int, str]:
    """
    Graph containing a negative cycle.
    Bellman-Ford should detect this; others will fail or loop.
    """
    graph = Graph(directed=True)
    
    edges = [
        (0, 1, 4), (1, 2, 3), (2, 3, 2),
        (3, 4, 5), (4, 5, 1),
        # Negative cycle: 2 -> 6 -> 7 -> 2 (total: 3 + 2 - 8 = -3)
        (2, 6, 3), (6, 7, 2), (7, 2, -8),
        (7, 5, 4),  # Exit from cycle
    ]
    
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    
    return graph, 0, 5, "Contains negative cycle (2->6->7->2) - Bellman-Ford should detect this"


def get_all_test_graphs() -> List[Tuple[str, Graph, int, int, str]]:
    """
    Return all curated test graphs.
    
    Returns:
        List of (name, graph, source, target, description) tuples
    """
    creators = [
        ("sparse_basic", create_sparse_basic),
        ("dense_mesh", create_dense_mesh),
        ("negative_shortcut", create_negative_shortcut),
        ("bottleneck", create_bottleneck),
        ("diamond_paths", create_diamond_paths),
        ("negative_cycle", create_negative_cycle_test),
    ]
    
    result = []
    for name, creator in creators:
        graph, source, target, desc = creator()
        result.append((name, graph, source, target, desc))
    
    return result
