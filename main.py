"""
Shortest Path Algorithm Comparison - Case Study

Main entry point for running algorithm comparisons across curated test graphs.
Generates organized results with visualizations and documentation.
"""
import os
import sys
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.graph_generator import get_all_test_graphs, validate_graph_complexity
from src.evaluation.runner import AlgorithmRunner, save_comparison_results
from src.evaluation.report_generator import (
    generate_graph_observations,
    generate_graph_info,
    generate_summary_report
)
from src.visualization.visualizer import plot_graph_with_paths, plot_convergence
from src.algorithms.dijkstra import dijkstra
from src.algorithms.bellman_ford import bellman_ford
from src.algorithms.quantum_inspired import quantum_inspired_shortest_path


def run_comparison(output_dir: str = "results", seed: int = 42, verbose: bool = True):
    """
    Run full algorithm comparison on all curated test graphs.
    
    Args:
        output_dir: Directory to save results
        seed: Random seed for reproducibility
        verbose: Print progress to console
    """
    if verbose:
        print("=" * 60)
        print("Shortest Path Algorithm Comparison - Case Study")
        print("=" * 60)
        print()
    
    # Create runner
    runner = AlgorithmRunner(quantum_seed=seed)
    
    # Get all test graphs
    test_graphs = get_all_test_graphs()
    
    if verbose:
        print(f"Running comparison on {len(test_graphs)} curated test graphs...\n")
    
    all_comparisons = []
    
    for name, graph, source, target, description in test_graphs:
        if verbose:
            print(f"\n{'-' * 50}")
            print(f"Graph: {name}")
            print(f"Description: {description}")
            print(f"Nodes: {graph.num_nodes}, Edges: {graph.num_edges}")
            print(f"Source: {source} -> Target: {target}")
        
        # Validate complexity
        validation = validate_graph_complexity(graph, source, target)
        if validation['warnings'] and verbose:
            for warning in validation['warnings']:
                print(f"  [!] {warning}")
        
        if not validation['valid']:
            if verbose:
                print(f"  [X] Skipping - invalid graph configuration")
            continue
        
        # Run comparison
        comparison = runner.run_all(graph, source, target, graph_name=name)
        all_comparisons.append(comparison)
        
        # Create output directory for this graph
        graph_dir = os.path.join(output_dir, name)
        os.makedirs(graph_dir, exist_ok=True)
        
        # Generate documentation
        generate_graph_info(comparison, description, graph_dir)
        generate_graph_observations(comparison, graph_dir)
        
        # Save raw results
        save_comparison_results(comparison, graph_dir)
        
        # Generate visualizations
        paths = {
            'Dijkstra': comparison.dijkstra_result.get('path'),
            'Bellman-Ford': comparison.bellman_ford_result.get('path'),
            'Quantum-Inspired': comparison.quantum_result.get('path')
        }
        paths = {k: v for k, v in paths.items() if v}  # Remove None paths
        
        if paths:
            plot_graph_with_paths(
                graph, paths,
                os.path.join(graph_dir, "path_comparison.png"),
                title=f"Paths on {name}"
            )
        
        # Get iteration histories for convergence plot
        d_result = dijkstra(graph, source, target)
        b_result = bellman_ford(graph, source, target)
        q_result = quantum_inspired_shortest_path(graph, source, target, seed=seed)
        
        histories = {
            'Dijkstra': d_result.history,
            'Bellman-Ford': b_result.history,
            'Quantum-Inspired': q_result.history
        }
        
        plot_convergence(
            histories,
            os.path.join(graph_dir, "convergence.png"),
            title=f"Convergence - {name}"
        )
        
        if verbose:
            # Print summary
            summary = comparison.comparison_summary
            print(f"\n  Results:")
            print(f"    Best algorithm: {summary.get('best_algorithm', 'N/A')}")
            print(f"    Best distance: {summary.get('best_distance', 'N/A')}")
            print(f"    Iterations - D: {comparison.dijkstra_result['iterations']}, "
                  f"BF: {comparison.bellman_ford_result['iterations']}, "
                  f"QI: {comparison.quantum_result['iterations']}")
            
            if summary.get('key_differences'):
                print(f"    Key differences:")
                for diff in summary['key_differences'][:2]:
                    print(f"      - {diff}")
    
    # Generate summary report
    generate_summary_report(all_comparisons, output_dir)
    
    if verbose:
        print(f"\n{'=' * 60}")
        print(f"Comparison complete!")
        print(f"Results saved to: {os.path.abspath(output_dir)}")
        print(f"\nKey files:")
        print(f"  - summary_report.md - Overall findings")
        for comp in all_comparisons:
            print(f"  - {comp.graph_name}/observations.md - Detailed observations")
        print("=" * 60)
    
    return all_comparisons


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Shortest Path Algorithm Comparison Case Study"
    )
    parser.add_argument(
        '-o', '--output',
        default='results',
        help='Output directory for results (default: results)'
    )
    parser.add_argument(
        '-s', '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress console output'
    )
    
    args = parser.parse_args()
    
    run_comparison(
        output_dir=args.output,
        seed=args.seed,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
