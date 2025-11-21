import random
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
    
    # Compute shortest path
    path, distance = algorithm_func(graph, start, end)
    
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
        print(f"  Path: {' -> '.join(map(str, path))}")
        print(f"  Cost: {distance:.2f}")
    print(f"{'='*80}")


def main():
    sizes = [10, 20, 50, 100, 200, 500, 1000]
    densities = [0.2, 0.5, 0.8, 1.0]
    noise_levels = [0.0, 0.1, 0.5, 0.8]
    negative_values_options = [False, True]
    
    # Total number of experiments
    total = len(sizes) * len(densities) * len(noise_levels) * len(negative_values_options)
    print(f"Running {total} experiments...")
    
    experiment_num = 0
    for size in sizes:
        for density in densities:
            for noise_level in noise_levels:
                for negative_values in negative_values_options:
                    experiment_num += 1
                    print(f"\nProgress: {experiment_num}/{total}")
                    run_experiment(
                        size=size,
                        density=density,
                        noise_level=noise_level,
                        negative_values=negative_values,
                        seed=42 + experiment_num,
                    )


if __name__ == "__main__":
    main()

