# CI2025_lab3

Shortest path algorithms implementation and experiment framework.

## Repository Structure

```
├── algorithms/
│   ├── dijkstra.py          # Dijkstra's algorithm implementation
│   ├── bellman_ford.py      # Bellman-Ford algorithm implementation
│   ├── floyd_warshall.py    # Floyd-Warshall algorithm implementation
│   └── __init__.py          # Package initialization
├── problem_creator.py        # Graph generation function for creating lab problems
├── utils.py                  # Utility functions for algorithm selection
├── main.py                   # Main experiment runner
├── reports/                  # Generated experiment reports (created after running experiments)
│   ├── experiment_report_*.csv     # CSV report with all experiment results
│   ├── experiment_report_*.json    # JSON report with all experiment results
│   └── experiment_summary_*.txt    # Text summary with statistics
└── README.md                 # This file
```

## Overview

This repository implements three shortest path algorithms and provides a framework for running experiments with various graph configurations:

- **Dijkstra's Algorithm**: Efficient for graphs with non-negative edge weights
- **Bellman-Ford Algorithm**: Handles graphs with negative edge weights and detects negative cycles
- **Floyd-Warshall Algorithm**: Computes all-pairs shortest paths, useful for small dense graphs

## Algorithm Implementations

All algorithms are located in the `algorithms/` package and provide a unified interface:

```python
path, distance = algorithm.shortest_path(graph, start, end)
```

Returns:

- `path`: List of node indices representing the shortest path, or `None` if no path exists
- `distance`: The shortest distance from start to end, or `np.inf` if no path exists, or `-np.inf` if a negative cycle is detected

## Problem Generator

The `problem_creator.py` module contains the `create_problem()` function used to generate graphs for lab experiments. This function creates adjacency matrices with configurable:

- **Size**: Number of nodes in the graph
- **Density**: Probability of edges existing between nodes
- **Negative values**: Whether to allow negative edge weights
- **Noise level**: Multiplier for edge weights
- **Seed**: Random seed for reproducibility

## Algorithm Selection

The `utils.py` module provides an intelligent algorithm selection function:

- **Dijkstra**: Used when `negative_values=False` (default)
- **Bellman-Ford**: Used when `negative_values=True`
- **Floyd-Warshall**: Used for small dense graphs (size ≤ 100, density ≥ 0.8) without negative values

## Running Experiments

### Basic Usage

Run all experiments with default parameters:

```bash
python main.py
```

This will iterate over all parameter combinations and generate reports upon completion:

- **Sizes**: [10, 20, 50, 100, 200, 500, 1000]
- **Densities**: [0.2, 0.5, 0.8, 1.0]
- **Noise levels**: [0.0, 0.1, 0.5, 0.8]
- **Negative values**: [False, True]

After all experiments complete, detailed reports are automatically generated in the `reports/` directory.

### Experiment Reports

Once all experiments finish, three types of reports are generated:

1. **CSV Report** (`experiment_report_YYYYMMDD_HHMMSS.csv`):

   - Tabular format with all experiment results
   - Columns include: size, density, noise_level, negative_values, seed, algorithm, start_node, end_node, result_status, path, distance, execution_time_seconds, path_length
   - Easy to import into spreadsheet applications or data analysis tools

2. **JSON Report** (`experiment_report_YYYYMMDD_HHMMSS.json`):

   - Structured data format with timestamp and all results
   - Useful for programmatic analysis and visualization
   - Includes metadata and complete experiment data

3. **Summary Report** (`experiment_summary_YYYYMMDD_HHMMSS.txt`):
   - Text summary with statistics:
     - Total number of experiments
     - Results breakdown by status (success, no_path, negative_cycle)
     - Results breakdown by algorithm used
     - Average execution times per algorithm
     - Total execution time

**Report Fields:**

- `size`: Number of nodes in the graph
- `density`: Graph density parameter
- `noise_level`: Noise level multiplier
- `negative_values`: Whether negative weights were allowed
- `seed`: Random seed used for reproducibility
- `algorithm`: Algorithm used (dijkstra, bellman_ford, floyd_warshall)
- `start_node`: Starting node index
- `end_node`: Ending node index
- `result_status`: Outcome (success, no_path, negative_cycle)
- `path`: Shortest path as string (e.g., "0 -> 3 -> 5") or None
- `distance`: Shortest path distance (or inf/-inf)
- `execution_time_seconds`: Time taken to compute the path
- `path_length`: Number of nodes in the path (0 if no path)

### Using Individual Components

#### Generate a Problem

```python
from problem_creator import create_problem
import numpy as np

graph = create_problem(
    size=50,
    density=0.5,
    negative_values=False,
    noise_level=0.1,
    seed=42
)
```

#### Select an Algorithm

```python
from utils import choose_algorithm

algorithm_name = choose_algorithm(size=50, density=0.5, negative_values=False)
```

#### Compute Shortest Path

```python
from algorithms import dijkstra

path, distance = dijkstra(graph, start=0, end=10)
print(f"Path: {path}, Distance: {distance}")
```

### Switching Between Algorithms

You can manually select algorithms instead of using the automatic selection:

```python
from algorithms import dijkstra, bellman_ford, floyd_warshall

# Use Dijkstra
path, dist = dijkstra(graph, start, end)

# Use Bellman-Ford
path, dist = bellman_ford(graph, start, end)

# Use Floyd-Warshall
path, dist = floyd_warshall(graph, start, end)
```

## Dependencies

- `numpy`: For array operations and graph representation
- `random`: For random node selection in experiments

## Notes

- All algorithms work with adjacency matrix representations (NumPy arrays)
- Edge weights can be positive, negative, or infinity (for non-existent edges)
- The diagonal is always zero (self-loops have zero weight)
- Negative cycles are detected by Bellman-Ford and Floyd-Warshall algorithms
- Reports are generated automatically after experiments complete
- You can interrupt experiments (Ctrl+C) and partial results will still be reported

## Disclaimer

**AI Assistance**: The algorithm implementations in this repository (Dijkstra's, Bellman-Ford, and Floyd-Warshall) were developed with substantial assistance from AI tools. While the algorithms implement well-known graph algorithms, the code structure and implementation details were created with the help of AI assistance.
