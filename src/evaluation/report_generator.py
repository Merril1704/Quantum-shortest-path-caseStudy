"""
Report generator for creating organized markdown documentation
of algorithm comparison results.
"""
import os
from typing import Dict, Any, List
from src.evaluation.runner import AlgorithmComparison


def generate_graph_observations(comparison: AlgorithmComparison, output_dir: str) -> str:
    """
    Generate detailed observations markdown for a single graph.
    
    Args:
        comparison: Results from running all algorithms
        output_dir: Directory to save the report
        
    Returns:
        Path to generated observations.md file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    md = []
    md.append(f"# Graph: {comparison.graph_name} - Observations\n")
    md.append(f"*Generated: {comparison.timestamp}*\n")
    
    # Graph Properties Table
    md.append("## Graph Properties\n")
    md.append("| Property | Value |")
    md.append("|----------|-------|")
    md.append(f"| Nodes | {comparison.graph_info['nodes']} |")
    md.append(f"| Edges | {comparison.graph_info['edges']} |")
    md.append(f"| Density | {comparison.graph_info['density']} |")
    md.append(f"| Directed | {'Yes' if comparison.graph_info['directed'] else 'No'} |")
    md.append(f"| Has Negative Weights | {'Yes' if comparison.graph_info['has_negative_weights'] else 'No'} |")
    md.append(f"| Source → Target | {comparison.source} → {comparison.target} |")
    md.append("")
    
    # Algorithm Results
    md.append("## Algorithm Results\n")
    
    # Dijkstra
    md.append("### Dijkstra's Algorithm")
    md.append("")
    d = comparison.dijkstra_result
    md.append(f"- **Path Found**: {_format_path(d['path'])}")
    md.append(f"- **Total Distance**: {d['distance']}")
    md.append(f"- **Iterations**: {d['iterations']}")
    md.append(f"- **Success**: {'✓ Yes' if d['success'] else '✗ No'}")
    if d.get('convergence'):
        md.append(f"- **Convergence Pattern**: {d['convergence'].get('improvement_pattern', 'N/A')}")
    md.append(f"- **Notes**: {d['message']}")
    md.append("")
    
    # Bellman-Ford
    md.append("### Bellman-Ford Algorithm")
    md.append("")
    b = comparison.bellman_ford_result
    md.append(f"- **Path Found**: {_format_path(b['path'])}")
    md.append(f"- **Total Distance**: {b['distance']}")
    md.append(f"- **Iterations**: {b['iterations']}")
    md.append(f"- **Success**: {'✓ Yes' if b['success'] else '✗ No'}")
    md.append(f"- **Negative Cycle Detected**: {'⚠ Yes' if b.get('has_negative_cycle') else 'No'}")
    if b.get('convergence'):
        md.append(f"- **Convergence Pattern**: {b['convergence'].get('improvement_pattern', 'N/A')}")
    md.append(f"- **Notes**: {b['message']}")
    md.append("")
    
    # Quantum-Inspired
    md.append("### Quantum-Inspired Algorithm")
    md.append("")
    q = comparison.quantum_result
    md.append(f"- **Path Found**: {_format_path(q['path'])}")
    md.append(f"- **Total Distance**: {q['distance']}")
    md.append(f"- **Final Energy**: {round(q.get('energy', 0), 2)}")
    md.append(f"- **Total Iterations**: {q['iterations']}")
    md.append(f"- **Convergence Iteration**: {q.get('convergence_iteration', 'N/A')}")
    md.append(f"- **Success**: {'✓ Yes' if q['success'] else '✗ No'}")
    if q.get('convergence'):
        md.append(f"- **Convergence Pattern**: {q['convergence'].get('improvement_pattern', 'N/A')}")
    md.append(f"- **Notes**: {q['message']}")
    md.append("")
    
    # Key Differences
    md.append("## Key Differences Observed\n")
    summary = comparison.comparison_summary
    differences = summary.get('key_differences', [])
    
    if differences:
        for i, diff in enumerate(differences, 1):
            md.append(f"{i}. {diff}")
    else:
        md.append("- All algorithms produced similar results on this graph")
    md.append("")
    
    # Comparison Summary Table
    md.append("## Summary Comparison\n")
    md.append("| Metric | Dijkstra | Bellman-Ford | Quantum-Inspired |")
    md.append("|--------|----------|--------------|------------------|")
    md.append(f"| Distance | {d['distance']} | {b['distance']} | {q['distance']} |")
    md.append(f"| Iterations | {d['iterations']} | {b['iterations']} | {q['iterations']} |")
    md.append(f"| Success | {'✓' if d['success'] else '✗'} | {'✓' if b['success'] else '✗'} | {'✓' if q['success'] else '✗'} |")
    
    # Path comparison
    paths_match = "✓ Same" if summary.get('all_paths_identical') else "Different"
    md.append(f"| Paths Match | {paths_match} | {paths_match} | {paths_match} |")
    md.append("")
    
    # Write file
    filepath = os.path.join(output_dir, "observations.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    return filepath


def generate_graph_info(comparison: AlgorithmComparison, description: str, output_dir: str) -> str:
    """Generate graph information markdown."""
    os.makedirs(output_dir, exist_ok=True)
    
    md = []
    md.append(f"# Graph: {comparison.graph_name}\n")
    md.append(f"## Description\n")
    md.append(f"{description}\n")
    md.append(f"## Properties\n")
    md.append(f"- **Nodes**: {comparison.graph_info['nodes']}")
    md.append(f"- **Edges**: {comparison.graph_info['edges']}")
    md.append(f"- **Density**: {comparison.graph_info['density']}")
    md.append(f"- **Type**: {'Directed' if comparison.graph_info['directed'] else 'Undirected'}")
    md.append(f"- **Negative Weights**: {'Yes' if comparison.graph_info['has_negative_weights'] else 'No'}")
    md.append(f"\n## Test Pair\n")
    md.append(f"Source: **{comparison.source}** → Target: **{comparison.target}**")
    
    filepath = os.path.join(output_dir, "graph_info.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    return filepath


def generate_summary_report(comparisons: List[AlgorithmComparison], output_dir: str) -> str:
    """
    Generate overall summary report across all graphs.
    
    Args:
        comparisons: List of comparison results from all graphs
        output_dir: Root results directory
        
    Returns:
        Path to summary_report.md
    """
    os.makedirs(output_dir, exist_ok=True)
    
    md = []
    md.append("# Shortest Path Algorithm Comparison - Summary Report\n")
    md.append("## Overview\n")
    md.append("This report compares three shortest path algorithms across multiple graph configurations:\n")
    md.append("1. **Dijkstra's Algorithm** - Greedy, deterministic, non-negative weights only")
    md.append("2. **Bellman-Ford Algorithm** - Iterative relaxation, handles negative weights")
    md.append("3. **Quantum-Inspired Algorithm** - Probabilistic energy minimization\n")
    
    # Quick summary table
    md.append("## Results Summary\n")
    md.append("| Graph | Nodes | Best Algorithm | Best Distance | Notes |")
    md.append("|-------|-------|----------------|---------------|-------|")
    
    for comp in comparisons:
        summary = comp.comparison_summary
        best = summary.get('best_algorithm', 'N/A')
        best_dist = summary.get('best_distance', 'N/A')
        
        # Get notable observation
        diffs = summary.get('key_differences', [])
        note = diffs[0][:50] + "..." if diffs else "All similar"
        
        md.append(f"| [{comp.graph_name}](./{comp.graph_name}/observations.md) | {comp.graph_info['nodes']} | {best} | {best_dist} | {note} |")
    
    md.append("")
    
    # Algorithm performance summary
    md.append("## Algorithm Performance by Graph Type\n")
    
    # Group observations
    md.append("### Positive Weight Graphs")
    md.append("On graphs with only positive weights, all three algorithms typically find the same optimal path. ")
    md.append("Dijkstra's algorithm is most efficient in iteration count.\n")
    
    md.append("### Negative Weight Graphs")
    md.append("When negative weights are present:")
    md.append("- Dijkstra may find suboptimal paths (does not correctly handle negative weights)")
    md.append("- Bellman-Ford finds the true optimal path")
    md.append("- Quantum-Inspired can find optimal or near-optimal paths\n")
    
    md.append("### Graphs with Negative Cycles")
    md.append("- Bellman-Ford correctly detects negative cycles")
    md.append("- Other algorithms may produce incorrect results\n")
    
    # Key findings
    md.append("## Key Findings\n")
    
    # Count successes
    dijkstra_wins = sum(1 for c in comparisons if c.comparison_summary.get('best_algorithm') == 'Dijkstra')
    bf_wins = sum(1 for c in comparisons if c.comparison_summary.get('best_algorithm') == 'Bellman-Ford')
    qi_wins = sum(1 for c in comparisons if c.comparison_summary.get('best_algorithm') == 'Quantum-Inspired')
    
    md.append(f"1. **Best algorithm counts**: Dijkstra: {dijkstra_wins}, Bellman-Ford: {bf_wins}, Quantum-Inspired: {qi_wins}")
    md.append("2. **Iteration efficiency**: Dijkstra uses fewest iterations on positive-weight graphs")
    md.append("3. **Correctness**: Bellman-Ford is the only algorithm guaranteed correct for all graph types")
    md.append("4. **Quantum-Inspired behavior**: Higher iteration count but can escape local optima")
    
    filepath = os.path.join(output_dir, "summary_report.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    return filepath


def _format_path(path: List[int]) -> str:
    """Format path as readable string."""
    if not path:
        return "No path found"
    return " → ".join(str(n) for n in path)
