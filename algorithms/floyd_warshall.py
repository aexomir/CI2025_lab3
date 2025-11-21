"""
Floyd-Warshall algorithm for finding all pairs shortest paths.
"""
import numpy as np
from typing import Tuple, List, Optional


def shortest_path(graph: np.ndarray, start: int, end: int) -> Tuple[Optional[List[int]], float]:
    """
    Find the shortest path from start to end using Floyd-Warshall algorithm.
    
    Args:
        graph: Adjacency matrix representation of the graph
        start: Starting node index
        end: Ending node index
    
    Returns:
        Tuple of (path, distance):
        - path: List of node indices representing the shortest path, or None if no path exists
        - distance: The shortest distance from start to end, or -np.inf if negative cycle exists, np.inf if no path
    """
    n = len(graph)
    
    # Initialize distance matrix
    dist = graph.copy()
    
    # Initialize next array for path reconstruction
    next_node = np.full((n, n), -1)
    for i in range(n):
        for j in range(n):
            if i == j:
                next_node[i, j] = i
            elif graph[i, j] != np.inf:
                next_node[i, j] = j
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i, k] != np.inf and dist[k, j] != np.inf:
                    if dist[i, j] > dist[i, k] + dist[k, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]
                        next_node[i, j] = next_node[i, k]
    
    # Check for negative cycles on the diagonal
    for i in range(n):
        if dist[i, i] < 0:
            # Negative cycle exists - check if it affects path from start to end
            # If we can reach the cycle from start and reach end from the cycle
            if _path_exists(dist, start, i) and _path_exists(dist, i, end):
                return None, -np.inf
    
    # Check if path exists
    if dist[start, end] == np.inf:
        return None, np.inf
    
    # Reconstruct path
    if next_node[start, end] == -1:
        return None, np.inf
    
    path = []
    current = start
    visited = set()
    while current != end:
        if current in visited:
            # Cycle detected
            return None, -np.inf
        visited.add(current)
        path.append(current)
        current = next_node[current, end]
        if current == -1:
            return None, np.inf
    
    path.append(end)
    return path, float(dist[start, end])


def _path_exists(dist: np.ndarray, start: int, end: int) -> bool:
    """Check if a path exists using the distance matrix."""
    return dist[start, end] != np.inf and dist[start, end] != -np.inf

