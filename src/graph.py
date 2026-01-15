"""
Graph data structure supporting directed/undirected weighted graphs.
Handles both positive and negative edge weights.
"""
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict


class Graph:
    """
    Weighted graph supporting directed and undirected edges.
    Uses adjacency list representation for efficiency.
    """
    
    def __init__(self, directed: bool = True):
        """
        Initialize a graph.
        
        Args:
            directed: If True, creates a directed graph. Otherwise undirected.
        """
        self.directed = directed
        self._adj: Dict[int, Dict[int, float]] = defaultdict(dict)
        self._nodes: Set[int] = set()
    
    def add_node(self, node: int) -> None:
        """Add a node to the graph."""
        self._nodes.add(node)
    
    def add_edge(self, u: int, v: int, weight: float) -> None:
        """
        Add an edge from u to v with given weight.
        For undirected graphs, also adds edge from v to u.
        
        Args:
            u: Source node
            v: Target node  
            weight: Edge weight (can be negative)
        """
        self._nodes.add(u)
        self._nodes.add(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight
    
    def get_neighbors(self, node: int) -> List[int]:
        """Get all neighbors of a node."""
        return list(self._adj[node].keys())
    
    def get_weight(self, u: int, v: int) -> Optional[float]:
        """Get weight of edge (u, v). Returns None if edge doesn't exist."""
        return self._adj[u].get(v)
    
    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge (u, v) exists."""
        return v in self._adj[u]
    
    @property
    def nodes(self) -> List[int]:
        """Return all nodes in the graph."""
        return sorted(self._nodes)
    
    @property
    def num_nodes(self) -> int:
        """Return number of nodes."""
        return len(self._nodes)
    
    @property
    def edges(self) -> List[Tuple[int, int, float]]:
        """Return all edges as (u, v, weight) tuples."""
        edge_list = []
        seen = set()
        for u in self._adj:
            for v, w in self._adj[u].items():
                if self.directed or (v, u) not in seen:
                    edge_list.append((u, v, w))
                    seen.add((u, v))
        return edge_list
    
    @property
    def num_edges(self) -> int:
        """Return number of edges."""
        return len(self.edges)
    
    def density(self) -> float:
        """Calculate graph density (0 to 1)."""
        n = self.num_nodes
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1) if self.directed else n * (n - 1) // 2
        return self.num_edges / max_edges if max_edges > 0 else 0.0
    
    def has_negative_weights(self) -> bool:
        """Check if graph has any negative edge weights."""
        return any(w < 0 for _, _, w in self.edges)
    
    def to_adjacency_matrix(self) -> List[List[Optional[float]]]:
        """
        Convert to adjacency matrix representation.
        None indicates no edge exists.
        """
        nodes = self.nodes
        node_idx = {n: i for i, n in enumerate(nodes)}
        n = len(nodes)
        matrix = [[None] * n for _ in range(n)]
        
        for u, v, w in self.edges:
            matrix[node_idx[u]][node_idx[v]] = w
            if not self.directed:
                matrix[node_idx[v]][node_idx[u]] = w
        
        return matrix
    
    def get_edge_list(self) -> List[Tuple[int, int, float]]:
        """Get all edges for iteration (useful for Bellman-Ford)."""
        return self.edges
    
    def __repr__(self) -> str:
        graph_type = "Directed" if self.directed else "Undirected"
        return f"{graph_type}Graph(nodes={self.num_nodes}, edges={self.num_edges})"
