import random
import time
import csv
import json
from datetime import datetime
from pathlib import Path
import numpy as np
from problem_creator import create_problem
from utils import choose_algorithm
from algorithms import dijkstra, bellman_ford, floyd_warshall


def run_experiment(
    size: int,
    density: float,
    noise_level: float,
    negative_values: bool,
    seed: int = None,
):
    if seed is None:
        seed = random.randint(0, 10000)
    
    # Generate graph
    graph = create_problem(
        size=size,
        density=density,
        negative_values=negative_values,
        noise_level=noise_level,
        seed=seed,
    )
    
    # Choose algorithm
    algorithm_name = choose_algorithm(size, density, negative_values)
    
    # Select algorithm function
    algorithm_map = {
        "dijkstra": dijkstra,
        "bellman_ford": bellman_ford,
        "floyd_warshall": floyd_warshall,
    }
    algorithm_func = algorithm_map[algorithm_name]
    
    # Pick two random nodes
    random.seed(seed)
    nodes = list(range(size))
    start, end = random.sample(nodes, 2)
    
    # Compute shortest path and measure time
    start_time = time.time()
    path, distance = algorithm_func(graph, start, end)
    execution_time = time.time() - start_time
    
    # Determine result status
    if path is None:
        if distance == -np.inf:
            result_status = "negative_cycle"
            path_str = None
        else:
            result_status = "no_path"
            path_str = None
    else:
        result_status = "success"
        path_str = " -> ".join(map(str, path))
    
    # Prepare result dictionary
    result = {
        "size": size,
        "density": density,
        "noise_level": noise_level,
        "negative_values": negative_values,
        "seed": seed,
        "algorithm": algorithm_name,
        "start_node": start,
        "end_node": end,
        "result_status": result_status,
        "path": path_str,
        "distance": distance if not np.isinf(distance) else ("-inf" if distance == -np.inf else "inf"),
        "execution_time_seconds": round(execution_time, 6),
        "path_length": len(path) if path else 0,
    }
    
    # Print results
    print(f"\n{'='*80}")
    print(f"Experiment: size={size}, density={density}, noise={noise_level}, "
          f"negative={negative_values}, seed={seed}")
    print(f"Algorithm: {algorithm_name}")
    print(f"Path from node {start} to node {end}:")
    if path is None:
        if distance == -np.inf:
            print(f"  Result: Negative cycle detected")
        else:
            print(f"  Result: No path exists")
    else:
        print(f"  Path: {path_str}")
        print(f"  Cost: {distance:.2f}")
    print(f"  Execution time: {execution_time:.6f}s")
    print(f"{'='*80}")
    
    return result


def generate_report(results, output_dir="reports"):
    """Generate CSV and JSON reports from experiment results."""
    Path(output_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate CSV report
    csv_filename = Path(output_dir) / f"experiment_report_{timestamp}.csv"
    if results:
        fieldnames = results[0].keys()
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"\nCSV report saved to: {csv_filename}")
    
    # Generate JSON report
    json_filename = Path(output_dir) / f"experiment_report_{timestamp}.json"
    with open(json_filename, 'w') as jsonfile:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_experiments": len(results),
            "results": results
        }, jsonfile, indent=2)
    print(f"JSON report saved to: {json_filename}")
    
    # Generate summary statistics
    summary = calculate_summary(results)
    summary_filename = Path(output_dir) / f"experiment_summary_{timestamp}.txt"
    with open(summary_filename, 'w') as summaryfile:
        summaryfile.write("EXPERIMENT SUMMARY\n")
        summaryfile.write("=" * 80 + "\n\n")
        summaryfile.write(f"Total Experiments: {len(results)}\n")
        summaryfile.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
        
        summaryfile.write("Results by Status:\n")
        for status, count in summary["by_status"].items():
            summaryfile.write(f"  {status}: {count}\n")
        summaryfile.write("\n")
        
        summaryfile.write("Results by Algorithm:\n")
        for algo, count in summary["by_algorithm"].items():
            summaryfile.write(f"  {algo}: {count}\n")
        summaryfile.write("\n")
        
        summaryfile.write("Average Execution Times (seconds):\n")
        for algo, avg_time in summary["avg_time_by_algorithm"].items():
            summaryfile.write(f"  {algo}: {avg_time:.6f}s\n")
        summaryfile.write("\n")
        
        summaryfile.write("Total Execution Time:\n")
        summaryfile.write(f"  {summary['total_time']:.6f}s ({summary['total_time']/60:.2f} minutes)\n")
    
    print(f"Summary report saved to: {summary_filename}")
    
    return csv_filename, json_filename, summary_filename


def calculate_summary(results):
    """Calculate summary statistics from results."""
    summary = {
        "by_status": {},
        "by_algorithm": {},
        "avg_time_by_algorithm": {},
        "total_time": 0.0,
    }
    
    algorithm_times = {}
    
    for result in results:
        # Count by status
        status = result["result_status"]
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        # Count by algorithm
        algo = result["algorithm"]
        summary["by_algorithm"][algo] = summary["by_algorithm"].get(algo, 0) + 1
        
        # Collect execution times by algorithm
        exec_time = result["execution_time_seconds"]
        summary["total_time"] += exec_time
        if algo not in algorithm_times:
            algorithm_times[algo] = []
        algorithm_times[algo].append(exec_time)
    
    # Calculate average times
    for algo, times in algorithm_times.items():
        summary["avg_time_by_algorithm"][algo] = sum(times) / len(times)
    
    return summary


def main():
    sizes = [10, 20, 50, 100, 200, 500, 1000]
    densities = [0.2, 0.5, 0.8, 1.0]
    noise_levels = [0.0, 0.1, 0.5, 0.8]
    negative_values_options = [False, True]
    
    # Total number of experiments
    total = len(sizes) * len(densities) * len(noise_levels) * len(negative_values_options)
    print(f"Running {total} experiments...")
    print(f"Started at: {datetime.now().isoformat()}")
    
    results = []
    experiment_num = 0
    overall_start_time = time.time()
    
    try:
        for size in sizes:
            for density in densities:
                for noise_level in noise_levels:
                    for negative_values in negative_values_options:
                        experiment_num += 1
                        print(f"\nProgress: {experiment_num}/{total}")
                        result = run_experiment(
                            size=size,
                            density=density,
                            noise_level=noise_level,
                            negative_values=negative_values,
                            seed=42 + experiment_num,
                        )
                        results.append(result)
    except KeyboardInterrupt:
        print(f"\n\nExperiments interrupted by user after {experiment_num}/{total} experiments.")
    
    overall_end_time = time.time()
    total_execution_time = overall_end_time - overall_start_time
    
    print(f"\n\n{'='*80}")
    print(f"All experiments completed!")
    print(f"Total execution time: {total_execution_time:.2f}s ({total_execution_time/60:.2f} minutes)")
    print(f"Completed at: {datetime.now().isoformat()}")
    print(f"{'='*80}\n")
    
    # Generate reports
    if results:
        print("Generating reports...")
        generate_report(results)
        print("\nReport generation completed!")
    else:
        print("No results to report.")


if __name__ == "__main__":
    main()

