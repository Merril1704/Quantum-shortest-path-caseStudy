"""
Tests for graph data structures.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import Graph
from src.graph_generator import (
    generate_random_graph,
    create_sparse_basic,
    create_negative_shortcut,
    validate_graph_complexity
)


class TestGraph:
    """Tests for Graph class."""
    
    def test_create_directed_graph(self):
        """Test creating a directed graph."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 5)
        g.add_edge(1, 2, 3)
        
        assert g.num_nodes == 3
        assert g.num_edges == 2
        assert g.directed == True
    
    def test_create_undirected_graph(self):
        """Test creating an undirected graph."""
        g = Graph(directed=False)
        g.add_edge(0, 1, 5)
        
        # Should have both directions
        assert g.has_edge(0, 1)
        assert g.has_edge(1, 0)
        assert g.get_weight(0, 1) == 5
        assert g.get_weight(1, 0) == 5
    
    def test_get_neighbors(self):
        """Test neighbor retrieval."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 2)
        g.add_edge(0, 3, 3)
        
        neighbors = g.get_neighbors(0)
        assert set(neighbors) == {1, 2, 3}
    
    def test_negative_weights(self):
        """Test graphs with negative weights."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 5)
        g.add_edge(1, 2, -3)
        
        assert g.has_negative_weights() == True
        assert g.get_weight(1, 2) == -3
    
    def test_density(self):
        """Test density calculation."""
        g = Graph(directed=True)
        # Complete graph on 3 nodes has 6 edges
        for i in range(3):
            for j in range(3):
                if i != j:
                    g.add_edge(i, j, 1)
        
        assert g.density() == 1.0
    
    def test_adjacency_matrix(self):
        """Test adjacency matrix conversion."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 5)
        g.add_edge(1, 2, 3)
        
        matrix = g.to_adjacency_matrix()
        assert matrix[0][1] == 5
        assert matrix[1][2] == 3
        assert matrix[0][2] is None


class TestGraphGenerator:
    """Tests for graph generation utilities."""
    
    def test_generate_random_graph(self):
        """Test random graph generation."""
        g = generate_random_graph(10, density=0.5, seed=42)
        
        assert g.num_nodes == 10
        assert g.num_edges > 0
    
    def test_sparse_basic_graph(self):
        """Test curated sparse graph."""
        graph, source, target, desc = create_sparse_basic()
        
        assert graph.num_nodes == 8
        assert source == 0
        assert target == 7
        assert not graph.has_negative_weights()
    
    def test_negative_shortcut_graph(self):
        """Test graph with negative weights."""
        graph, source, target, desc = create_negative_shortcut()
        
        assert graph.has_negative_weights()
        # Check specific negative edge exists
        assert graph.get_weight(4, 5) == -6
    
    def test_validate_graph_complexity(self):
        """Test graph complexity validation."""
        graph, source, target, _ = create_sparse_basic()
        result = validate_graph_complexity(graph, source, target)
        
        assert result['valid'] == True
        assert 'nodes' in result['metrics']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
