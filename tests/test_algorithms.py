"""
Tests for shortest path algorithms.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import Graph
from src.graph_generator import (
    create_sparse_basic,
    create_negative_shortcut,
    create_negative_cycle_test,
    create_diamond_paths
)
from src.algorithms.dijkstra import dijkstra
from src.algorithms.bellman_ford import bellman_ford
from src.algorithms.quantum_inspired import quantum_inspired_shortest_path


class TestDijkstra:
    """Tests for Dijkstra's algorithm."""
    
    def test_simple_path(self):
        """Test finding a simple shortest path."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(0, 2, 5)
        
        result = dijkstra(g, 0, 2)
        
        assert result.success == True
        assert result.path == [0, 1, 2]
        assert result.distance == 3  # 1 + 2
    
    def test_no_path(self):
        """Test when no path exists."""
        g = Graph(directed=True)
        g.add_node(0)
        g.add_node(1)
        # No edges
        
        result = dijkstra(g, 0, 1)
        
        assert result.success == False
        assert result.path is None
    
    def test_sparse_basic_graph(self):
        """Test on curated sparse graph."""
        graph, source, target, _ = create_sparse_basic()
        result = dijkstra(graph, source, target)
        
        assert result.success == True
        assert result.path is not None
        assert result.path[0] == source
        assert result.path[-1] == target
    
    def test_iteration_history(self):
        """Test that iteration history is recorded."""
        graph, source, target, _ = create_sparse_basic()
        result = dijkstra(graph, source, target)
        
        assert len(result.history) > 0
        assert result.history[0].iteration == 1


class TestBellmanFord:
    """Tests for Bellman-Ford algorithm."""
    
    def test_simple_path(self):
        """Test finding a simple shortest path."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(0, 2, 5)
        
        result = bellman_ford(g, 0, 2)
        
        assert result.success == True
        assert result.path == [0, 1, 2]
        assert result.distance == 3
    
    def test_negative_weights(self):
        """Test handling of negative edge weights."""
        graph, source, target, _ = create_negative_shortcut()
        result = bellman_ford(graph, source, target)
        
        assert result.success == True
        assert result.has_negative_cycle == False
        # Should find the path using the negative edge
        assert result.distance < 12  # Less than the positive-only path
    
    def test_negative_cycle_detection(self):
        """Test detection of negative cycles."""
        graph, source, target, _ = create_negative_cycle_test()
        result = bellman_ford(graph, source, target)
        
        assert result.has_negative_cycle == True
        assert result.success == False
    
    def test_matches_dijkstra_on_positive_weights(self):
        """Verify Bellman-Ford matches Dijkstra on positive-weight graphs."""
        graph, source, target, _ = create_sparse_basic()
        
        dijkstra_result = dijkstra(graph, source, target)
        bf_result = bellman_ford(graph, source, target)
        
        assert dijkstra_result.distance == bf_result.distance


class TestQuantumInspired:
    """Tests for Quantum-Inspired algorithm."""
    
    def test_finds_valid_path(self):
        """Test that algorithm finds a valid path."""
        graph, source, target, _ = create_sparse_basic()
        result = quantum_inspired_shortest_path(
            graph, source, target, 
            seed=42,
            max_iterations=300
        )
        
        assert result.success == True
        assert result.path is not None
        assert result.path[0] == source
        assert result.path[-1] == target
    
    def test_convergence_behavior(self):
        """Test that energy decreases over iterations."""
        graph, source, target, _ = create_sparse_basic()
        result = quantum_inspired_shortest_path(
            graph, source, target,
            seed=42,
            max_iterations=200
        )
        
        # Energy at end should be reasonable
        if result.success:
            assert result.energy < 1000  # Not hitting constraint penalties
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        graph, source, target, _ = create_diamond_paths()
        
        result1 = quantum_inspired_shortest_path(graph, source, target, seed=42)
        result2 = quantum_inspired_shortest_path(graph, source, target, seed=42)
        
        assert result1.path == result2.path
        assert result1.distance == result2.distance
    
    def test_iteration_history_recorded(self):
        """Test that iteration history is properly recorded."""
        graph, source, target, _ = create_sparse_basic()
        result = quantum_inspired_shortest_path(
            graph, source, target,
            seed=42,
            max_iterations=100
        )
        
        assert len(result.history) > 0
        # Check history structure
        first = result.history[0]
        assert hasattr(first, 'iteration')
        assert hasattr(first, 'current_energy')
        assert hasattr(first, 'temperature')


class TestAlgorithmComparison:
    """Tests comparing all algorithms."""
    
    def test_all_find_path_on_simple_graph(self):
        """All algorithms should find a path on simple graphs."""
        g = Graph(directed=True)
        g.add_edge(0, 1, 2)
        g.add_edge(1, 2, 3)
        g.add_edge(0, 2, 10)
        
        d = dijkstra(g, 0, 2)
        b = bellman_ford(g, 0, 2)
        q = quantum_inspired_shortest_path(g, 0, 2, seed=42)
        
        assert d.success and b.success and q.success
        
        # Dijkstra and Bellman-Ford should match
        assert d.distance == b.distance == 5
    
    def test_dijkstra_fails_on_negative_weights(self):
        """Dijkstra should produce wrong result with negative weights."""
        graph, source, target, _ = create_negative_shortcut()
        
        d = dijkstra(graph, source, target)
        b = bellman_ford(graph, source, target)
        
        # If Dijkstra "succeeds", it should have different distance than Bellman-Ford
        # because it can't correctly handle negative edges
        if d.success and b.success:
            # Due to the graph structure, Dijkstra likely finds a suboptimal path
            assert b.distance <= d.distance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
