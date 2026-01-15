"""
Benchmark Runner - Runs all algorithms on 20 generated benchmark graphs
and produces a comprehensive markdown report.

Usage:
    python run_benchmark.py [--seed=42] [--output=results/benchmark]
"""
import os
import sys
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.benchmark_generator import generate_benchmark_graphs, get_graph_statistics
from src.evaluation.runner import AlgorithmRunner
from src.graph_generator import validate_graph_complexity


def run_benchmark(output_dir: str = "results/benchmark", seed: int = 42, verbose: bool = True):
    """
    Run benchmark on 20 generated graphs and produce comprehensive report.
    
    Args:
        output_dir: Directory to save benchmark results
        seed: Random seed for reproducibility
        verbose: Print progress to console
    """
    if verbose:
        print("=" * 70)
        print("Shortest Path Algorithm Benchmark - 20 Generated Graphs")
        print("=" * 70)
        print()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate benchmark graphs
    if verbose:
        print("Generating 20 benchmark graphs...")
    
    graphs = generate_benchmark_graphs(base_seed=seed)
    
    if verbose:
        print(f"Generated {len(graphs)} graphs\n")
    
    # Create runner
    runner = AlgorithmRunner(quantum_seed=seed)
    
    # Run benchmarks and collect results
    all_results = []
    
    for idx, (name, graph, source, target, description, properties) in enumerate(graphs, 1):
        if verbose:
            print(f"\n[{idx:02d}/20] {name}")
            print(f"        {description}")
            print(f"        Nodes: {graph.num_nodes}, Edges: {graph.num_edges}, "
                  f"Density: {properties.get('density', 'N/A')}")
        
        # Validate graph complexity
        validation = validate_graph_complexity(graph, source, target)
        
        if not validation['valid']:
            if verbose:
                print(f"        [X] Skipping - invalid configuration")
            continue
        
        # Run comparison
        try:
            comparison = runner.run_all(graph, source, target, graph_name=name)
            stats = get_graph_statistics(graph, source, target)
            
            # Collect result data
            result = {
                "name": name,
                "description": description,
                "properties": properties,
                "statistics": stats,
                "dijkstra": comparison.dijkstra_result,
                "bellman_ford": comparison.bellman_ford_result,
                "quantum": comparison.quantum_result,
                "summary": comparison.comparison_summary
            }
            all_results.append(result)
            
            if verbose:
                summary = comparison.comparison_summary
                d_dist = comparison.dijkstra_result['distance']
                b_dist = comparison.bellman_ford_result['distance']
                q_dist = comparison.quantum_result['distance']
                
                print(f"        Results: D={d_dist}, BF={b_dist}, QI={q_dist}")
                print(f"        Best: {summary.get('best_algorithm', 'N/A')} "
                      f"(distance: {summary.get('best_distance', 'N/A')})")
                
        except Exception as e:
            if verbose:
                print(f"        [!] Error: {str(e)}")
    
    # Generate comprehensive markdown report
    if verbose:
        print("\n" + "=" * 70)
        print("Generating benchmark report...")
    
    report_path = generate_benchmark_report(all_results, output_dir, seed)
    
    if verbose:
        print(f"\nBenchmark complete!")
        print(f"Report saved to: {os.path.abspath(report_path)}")
        print("=" * 70)
    
    return all_results


def generate_benchmark_report(results: list, output_dir: str, seed: int) -> str:
    """
    Generate comprehensive markdown report for all benchmark results.
    
    Args:
        results: List of result dictionaries from benchmark run
        output_dir: Directory to save report
        seed: Random seed used for reproducibility
        
    Returns:
        Path to generated report file
    """
    md = []
    timestamp = datetime.now().isoformat()
    
    # === Header ===
    md.append("# Benchmark Report: 20 Generated Graphs")
    md.append("")
    md.append(f"*Generated: {timestamp}*")
    md.append(f"*Random Seed: {seed}*")
    md.append("")
    
    # === Executive Summary ===
    md.append("## Executive Summary")
    md.append("")
    md.append("This benchmark evaluates three shortest path algorithms across 20 randomly generated graphs:")
    md.append("")
    md.append("1. **Dijkstra's Algorithm** - Greedy, optimal for non-negative weights")
    md.append("2. **Bellman-Ford Algorithm** - Handles negative weights, detects negative cycles")
    md.append("3. **Quantum-Inspired Algorithm** - Energy-based probabilistic optimization")
    md.append("")
    
    # Calculate summary statistics
    total = len(results)
    dijkstra_wins = sum(1 for r in results if r['summary'].get('best_algorithm') == 'Dijkstra')
    bf_wins = sum(1 for r in results if r['summary'].get('best_algorithm') == 'Bellman-Ford')
    qi_wins = sum(1 for r in results if r['summary'].get('best_algorithm') == 'Quantum-Inspired')
    
    # Count ties (multiple algorithms with same best distance)
    ties = total - dijkstra_wins - bf_wins - qi_wins
    
    dijkstra_successes = sum(1 for r in results if r['dijkstra']['success'])
    bf_successes = sum(1 for r in results if r['bellman_ford']['success'])
    qi_successes = sum(1 for r in results if r['quantum']['success'])
    
    neg_weight_graphs = sum(1 for r in results if r['statistics'].get('has_negative_weights', False))
    
    md.append("### Key Metrics")
    md.append("")
    md.append(f"- **Graphs Tested**: {total}")
    md.append(f"- **Graphs with Negative Weights**: {neg_weight_graphs}")
    md.append(f"- **Algorithm Win Counts**: Dijkstra: {dijkstra_wins}, Bellman-Ford: {bf_wins}, Quantum-Inspired: {qi_wins}")
    md.append(f"- **Success Rates**: Dijkstra: {dijkstra_successes}/{total}, Bellman-Ford: {bf_successes}/{total}, Quantum-Inspired: {qi_successes}/{total}")
    md.append("")
    
    # === Results Overview Table ===
    md.append("---")
    md.append("")
    md.append("## Results Overview")
    md.append("")
    md.append("| # | Graph Name | Nodes | Edges | Density | Neg Weights | Dijkstra | Bellman-Ford | Quantum | Best |")
    md.append("|---|------------|-------|-------|---------|-------------|----------|--------------|---------|------|")
    
    for idx, r in enumerate(results, 1):
        name = r['name']
        nodes = r['statistics']['nodes']
        edges = r['statistics']['edges']
        density = r['statistics']['density']
        has_neg = "Yes" if r['statistics'].get('has_negative_weights') else "No"
        
        d_dist = r['dijkstra']['distance']
        b_dist = r['bellman_ford']['distance']
        q_dist = r['quantum']['distance']
        
        best = r['summary'].get('best_algorithm', 'N/A')
        
        # Format distances
        d_str = str(d_dist) if d_dist != "infinity" else "∞"
        b_str = str(b_dist) if b_dist != "infinity" else "∞"
        q_str = str(round(q_dist, 1)) if isinstance(q_dist, float) else str(q_dist) if q_dist != "infinity" else "∞"
        
        md.append(f"| {idx} | {name} | {nodes} | {edges} | {density} | {has_neg} | {d_str} | {b_str} | {q_str} | {best} |")
    
    md.append("")
    
    # === Detailed Observations for Each Graph ===
    md.append("---")
    md.append("")
    md.append("## Detailed Observations by Graph")
    md.append("")
    
    for idx, r in enumerate(results, 1):
        md.append(f"### {idx}. {r['name']}")
        md.append("")
        md.append(f"**Description**: {r['description']}")
        md.append("")
        
        # Graph Properties Table
        md.append("#### Graph Properties")
        md.append("")
        md.append("| Property | Value |")
        md.append("|----------|-------|")
        md.append(f"| Nodes | {r['statistics']['nodes']} |")
        md.append(f"| Edges | {r['statistics']['edges']} |")
        md.append(f"| Density | {r['statistics']['density']} |")
        md.append(f"| Directed | {'Yes' if r['statistics']['directed'] else 'No'} |")
        md.append(f"| Has Negative Weights | {'Yes' if r['statistics'].get('has_negative_weights') else 'No'} |")
        md.append(f"| Source → Target | {r['statistics']['source']} → {r['statistics']['target']} |")
        
        if 'avg_out_degree' in r['statistics']:
            md.append(f"| Avg Out-Degree | {r['statistics']['avg_out_degree']} |")
        if 'avg_weight' in r['statistics']:
            md.append(f"| Avg Weight | {r['statistics']['avg_weight']} |")
        if 'min_weight' in r['statistics']:
            md.append(f"| Weight Range | {r['statistics']['min_weight']} to {r['statistics']['max_weight']} |")
        if r['statistics'].get('negative_edge_count', 0) > 0:
            md.append(f"| Negative Edges | {r['statistics']['negative_edge_count']} |")
        
        md.append("")
        
        # Algorithm Results
        md.append("#### Algorithm Results")
        md.append("")
        
        # Dijkstra
        d = r['dijkstra']
        md.append("**Dijkstra's Algorithm:**")
        md.append(f"- Path: {_format_path(d['path'])}")
        md.append(f"- Distance: {d['distance']}")
        md.append(f"- Iterations: {d['iterations']}")
        md.append(f"- Success: {'✓' if d['success'] else '✗'}")
        md.append("")
        
        # Bellman-Ford
        b = r['bellman_ford']
        md.append("**Bellman-Ford Algorithm:**")
        md.append(f"- Path: {_format_path(b['path'])}")
        md.append(f"- Distance: {b['distance']}")
        md.append(f"- Iterations: {b['iterations']}")
        md.append(f"- Success: {'✓' if b['success'] else '✗'}")
        if b.get('has_negative_cycle'):
            md.append("- ⚠ **Negative Cycle Detected!**")
        md.append("")
        
        # Quantum-Inspired
        q = r['quantum']
        md.append("**Quantum-Inspired Algorithm:**")
        md.append(f"- Path: {_format_path(q['path'])}")
        q_dist = q['distance']
        md.append(f"- Distance: {round(q_dist, 2) if isinstance(q_dist, float) else q_dist}")
        md.append(f"- Final Energy: {round(q.get('energy', 0), 2)}")
        md.append(f"- Iterations: {q['iterations']}")
        md.append(f"- Convergence at: {q.get('convergence_iteration', 'N/A')}")
        md.append(f"- Success: {'✓' if q['success'] else '✗'}")
        md.append("")
        
        # Comparison Summary
        summary = r['summary']
        md.append("#### Comparison Summary")
        md.append("")
        md.append(f"- **Best Algorithm**: {summary.get('best_algorithm', 'N/A')}")
        md.append(f"- **Best Distance**: {summary.get('best_distance', 'N/A')}")
        md.append(f"- **Paths Identical**: {'Yes' if summary.get('all_paths_identical') else 'No'}")
        
        # Key differences
        diffs = summary.get('key_differences', [])
        if diffs:
            md.append("- **Key Observations**:")
            for diff in diffs:
                md.append(f"  - {diff}")
        
        md.append("")
        md.append("---")
        md.append("")
    
    # === Analysis by Category ===
    md.append("## Analysis by Graph Category")
    md.append("")
    
    # Separate results by category
    small_graphs = [r for r in results if r['statistics']['nodes'] <= 8]
    medium_graphs = [r for r in results if 8 < r['statistics']['nodes'] <= 12]
    large_graphs = [r for r in results if r['statistics']['nodes'] > 12]
    neg_weight_results = [r for r in results if r['statistics'].get('has_negative_weights')]
    
    md.append("### Performance by Graph Size")
    md.append("")
    md.append("| Category | Graphs | Dijkstra Avg Iter | BF Avg Iter | QI Avg Iter |")
    md.append("|----------|--------|-------------------|-------------|-------------|")
    
    for cat_name, cat_results in [("Small (≤8 nodes)", small_graphs), 
                                   ("Medium (9-12 nodes)", medium_graphs),
                                   ("Large (>12 nodes)", large_graphs)]:
        if cat_results:
            d_avg = sum(r['dijkstra']['iterations'] for r in cat_results) / len(cat_results)
            b_avg = sum(r['bellman_ford']['iterations'] for r in cat_results) / len(cat_results)
            q_avg = sum(r['quantum']['iterations'] for r in cat_results) / len(cat_results)
            md.append(f"| {cat_name} | {len(cat_results)} | {d_avg:.1f} | {b_avg:.1f} | {q_avg:.1f} |")
    
    md.append("")
    
    # === Analysis: Negative Weight Graphs ===
    if neg_weight_results:
        md.append("### Negative Weight Graph Analysis")
        md.append("")
        md.append("Performance on graphs containing negative edge weights:")
        md.append("")
        
        d_correct = 0
        for r in neg_weight_results:
            d_dist = r['dijkstra']['distance']
            b_dist = r['bellman_ford']['distance']
            if d_dist == b_dist:
                d_correct += 1
        
        md.append(f"- **Total graphs with negative weights**: {len(neg_weight_results)}")
        md.append(f"- **Dijkstra matched Bellman-Ford**: {d_correct}/{len(neg_weight_results)} graphs")
        md.append("")
        
        if d_correct < len(neg_weight_results):
            md.append("**Note**: Dijkstra's algorithm is not guaranteed to find optimal paths in graphs with negative weights. "
                     "Bellman-Ford is the authoritative source for these graphs.")
        md.append("")
    
    # === Conclusions ===
    md.append("---")
    md.append("")
    md.append("## Conclusions")
    md.append("")
    md.append("### Algorithm Strengths")
    md.append("")
    md.append("1. **Dijkstra's Algorithm**")
    md.append("   - Most iteration-efficient on positive-weight graphs")
    md.append("   - Deterministic and predictable behavior")
    md.append("   - Limitation: May produce incorrect results with negative weights")
    md.append("")
    md.append("2. **Bellman-Ford Algorithm**")
    md.append("   - Correctly handles all graph types including negative weights")
    md.append("   - Detects negative cycles")
    md.append("   - Higher iteration count but guaranteed correctness")
    md.append("")
    md.append("3. **Quantum-Inspired Algorithm**")
    md.append("   - Probabilistic approach can explore diverse solution space")
    md.append("   - May find alternative valid paths")
    md.append("   - Highest iteration count; solution quality varies")
    md.append("")
    
    md.append("### Recommendations")
    md.append("")
    md.append("- Use **Dijkstra** for graphs with only positive weights when efficiency is critical")
    md.append("- Use **Bellman-Ford** when correctness is paramount or negative weights may exist")
    md.append("- Use **Quantum-Inspired** for exploration or when traditional algorithms don't converge well")
    md.append("")
    
    # Write report
    report_path = os.path.join(output_dir, "benchmark_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    
    return report_path


def _format_path(path) -> str:
    """Format path as readable string."""
    if not path:
        return "No path found"
    return " → ".join(str(n) for n in path)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run benchmark on 20 generated graphs for algorithm comparison"
    )
    parser.add_argument(
        '-o', '--output',
        default='results/benchmark',
        help='Output directory for benchmark results (default: results/benchmark)'
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
    
    run_benchmark(
        output_dir=args.output,
        seed=args.seed,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
