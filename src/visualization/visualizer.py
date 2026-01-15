"""
Visualization utilities for shortest path algorithm comparison.
Uses matplotlib and networkx for graph and convergence plotting.
"""
import os
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

from src.graph import Graph


def plot_graph_with_paths(
    graph: Graph,
    paths: Dict[str, List[int]],
    output_path: str,
    title: str = "Graph with Shortest Paths"
) -> str:
    """
    Plot graph with paths from different algorithms highlighted.
    
    Args:
        graph: The graph to visualize
        paths: Dict mapping algorithm name -> path
        output_path: Path to save the figure
        title: Plot title
        
    Returns:
        Path to saved figure
    """
    if not HAS_NETWORKX:
        print("NetworkX not available, skipping graph visualization")
        return ""
    
    # Create NetworkX graph
    G = nx.DiGraph() if graph.directed else nx.Graph()
    
    for node in graph.nodes:
        G.add_node(node)
    
    for u, v, w in graph.edges:
        G.add_edge(u, v, weight=w)
    
    # Layout
    pos = nx.spring_layout(G, seed=42, k=2)
    
    # Setup figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Draw base graph
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
    
    # Draw edges with weights
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    
    # Draw paths with different colors
    colors = {'Dijkstra': 'red', 'Bellman-Ford': 'blue', 'Quantum-Inspired': 'green'}
    offsets = {'Dijkstra': -0.02, 'Bellman-Ford': 0, 'Quantum-Inspired': 0.02}
    
    legend_handles = []
    
    for algo_name, path in paths.items():
        if path and len(path) >= 2:
            color = colors.get(algo_name, 'purple')
            
            # Draw path edges
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(
                G, pos, edgelist=path_edges,
                edge_color=color, width=3, alpha=0.7,
                connectionstyle=f"arc3,rad={offsets.get(algo_name, 0)}",
                ax=ax
            )
            
            legend_handles.append(mpatches.Patch(color=color, label=algo_name))
    
    ax.legend(handles=legend_handles, loc='upper left')
    ax.set_title(title)
    ax.axis('off')
    
    # Save
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def plot_convergence(
    histories: Dict[str, List[Any]],
    output_path: str,
    title: str = "Algorithm Convergence"
) -> str:
    """
    Plot convergence behavior of all algorithms.
    
    Args:
        histories: Dict mapping algorithm name -> iteration history
        output_path: Path to save figure
        title: Plot title
        
    Returns:
        Path to saved figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = {'Dijkstra': 'red', 'Bellman-Ford': 'blue', 'Quantum-Inspired': 'green'}
    
    # Left plot: Distance/Energy over iterations
    ax1 = axes[0]
    
    for algo_name, history in histories.items():
        if not history:
            continue
            
        iterations = []
        values = []
        
        for h in history:
            if hasattr(h, 'iteration'):
                iterations.append(h.iteration)
            else:
                iterations.append(len(iterations) + 1)
            
            # Get relevant value
            if hasattr(h, 'current_energy'):
                values.append(h.current_energy)
            elif hasattr(h, 'distances'):
                # Use minimum non-inf distance
                dists = [v for v in h.distances.values() if v != float('inf')]
                values.append(min(dists) if dists else float('inf'))
            else:
                values.append(0)
        
        # Filter out infinity
        valid = [(i, v) for i, v in zip(iterations, values) if v != float('inf') and v < 10000]
        if valid:
            its, vals = zip(*valid)
            ax1.plot(its, vals, color=colors.get(algo_name, 'gray'), 
                    label=algo_name, linewidth=2, marker='o', markersize=3)
    
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Distance / Energy')
    ax1.set_title('Convergence Over Iterations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right plot: Iteration counts comparison
    ax2 = axes[1]
    
    algo_names = list(histories.keys())
    iteration_counts = [len(histories[name]) for name in algo_names]
    bars_colors = [colors.get(name, 'gray') for name in algo_names]
    
    bars = ax2.bar(algo_names, iteration_counts, color=bars_colors, alpha=0.7)
    ax2.set_ylabel('Total Iterations')
    ax2.set_title('Iteration Count Comparison')
    
    # Add value labels on bars
    for bar, count in zip(bars, iteration_counts):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path


def plot_comparison_chart(
    comparisons: List[Dict[str, Any]],
    output_path: str
) -> str:
    """
    Create overall comparison chart across all graphs.
    
    Args:
        comparisons: List of comparison summaries
        output_path: Path to save figure
        
    Returns:
        Path to saved figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    graph_names = [c['graph_name'] for c in comparisons]
    x = np.arange(len(graph_names))
    width = 0.25
    
    # Extract data
    dijkstra_iters = []
    bellman_iters = []
    quantum_iters = []
    
    dijkstra_dists = []
    bellman_dists = []
    quantum_dists = []
    
    for c in comparisons:
        di = c.get('dijkstra_iterations', 0)
        bi = c.get('bellman_iterations', 0)
        qi = c.get('quantum_iterations', 0)
        
        dijkstra_iters.append(di)
        bellman_iters.append(bi)
        quantum_iters.append(qi)
        
        dd = c.get('dijkstra_distance', float('inf'))
        bd = c.get('bellman_distance', float('inf'))
        qd = c.get('quantum_distance', float('inf'))
        
        dijkstra_dists.append(dd if dd != float('inf') else 0)
        bellman_dists.append(bd if bd != float('inf') else 0)
        quantum_dists.append(qd if qd != float('inf') else 0)
    
    # Plot 1: Iteration counts
    ax1 = axes[0, 0]
    ax1.bar(x - width, dijkstra_iters, width, label='Dijkstra', color='red', alpha=0.7)
    ax1.bar(x, bellman_iters, width, label='Bellman-Ford', color='blue', alpha=0.7)
    ax1.bar(x + width, quantum_iters, width, label='Quantum-Inspired', color='green', alpha=0.7)
    ax1.set_ylabel('Iterations')
    ax1.set_title('Iteration Count by Graph')
    ax1.set_xticks(x)
    ax1.set_xticklabels(graph_names, rotation=45, ha='right')
    ax1.legend()
    
    # Plot 2: Distances
    ax2 = axes[0, 1]
    ax2.bar(x - width, dijkstra_dists, width, label='Dijkstra', color='red', alpha=0.7)
    ax2.bar(x, bellman_dists, width, label='Bellman-Ford', color='blue', alpha=0.7)
    ax2.bar(x + width, quantum_dists, width, label='Quantum-Inspired', color='green', alpha=0.7)
    ax2.set_ylabel('Distance')
    ax2.set_title('Path Distance by Graph')
    ax2.set_xticks(x)
    ax2.set_xticklabels(graph_names, rotation=45, ha='right')
    ax2.legend()
    
    # Plot 3: Success rate pie
    ax3 = axes[1, 0]
    success_counts = {'Dijkstra': 0, 'Bellman-Ford': 0, 'Quantum-Inspired': 0}
    for c in comparisons:
        if c.get('dijkstra_success', False):
            success_counts['Dijkstra'] += 1
        if c.get('bellman_success', False):
            success_counts['Bellman-Ford'] += 1
        if c.get('quantum_success', False):
            success_counts['Quantum-Inspired'] += 1
    
    ax3.bar(success_counts.keys(), success_counts.values(), 
           color=['red', 'blue', 'green'], alpha=0.7)
    ax3.set_ylabel('Successful Runs')
    ax3.set_title(f'Success Count (out of {len(comparisons)} graphs)')
    
    # Plot 4: Best algorithm wins
    ax4 = axes[1, 1]
    best_counts = {'Dijkstra': 0, 'Bellman-Ford': 0, 'Quantum-Inspired': 0, 'Tie': 0}
    for c in comparisons:
        best = c.get('best_algorithm')
        if best in best_counts:
            best_counts[best] += 1
        elif best:
            best_counts['Tie'] += 1
    
    colors_pie = ['red', 'blue', 'green', 'gray']
    values = list(best_counts.values())
    labels = list(best_counts.keys())
    
    # Only show non-zero
    non_zero = [(l, v, c) for l, v, c in zip(labels, values, colors_pie) if v > 0]
    if non_zero:
        labels, values, colors_used = zip(*non_zero)
        ax4.pie(values, labels=labels, colors=colors_used, autopct='%1.0f%%', alpha=0.7)
    ax4.set_title('Best Algorithm Distribution')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path
