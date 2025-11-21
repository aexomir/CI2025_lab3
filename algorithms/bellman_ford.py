"""
Bellman-Ford algorithm for finding the shortest path in a graph with potentially negative weights.
"""
import numpy as np
from typing import Tuple, List, Optional


def shortest_path(graph: np.ndarray, start: int, end: int) -> Tuple[Optional[List[int]], float]:
    """
    Find the shortest path from start to end using Bellman-Ford algorithm.
    
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
    
    # Initialize distances
    distances = np.full(n, np.inf)
    distances[start] = 0
    
    # Initialize parent array for path reconstruction
    parents = np.full(n, -1)
    
    # Relax edges (n-1) times
    for _ in range(n - 1):
        for u in range(n):
            if distances[u] == np.inf:
                continue
            for v in range(n):
                if graph[u, v] != np.inf:
                    if distances[u] + graph[u, v] < distances[v]:
                        distances[v] = distances[u] + graph[u, v]
                        parents[v] = u
    
    # Check for negative cycles that are reachable from start and affect path to end
    # First, check if we can reach end
    if distances[end] == np.inf:
        return None, np.inf
    
    # Check for negative cycles by doing one more relaxation pass
    negative_cycle_detected = False
    for u in range(n):
        if distances[u] == np.inf:
            continue
        for v in range(n):
            if graph[u, v] != np.inf:
                if distances[u] + graph[u, v] < distances[v]:
                    # Negative cycle found - check if it affects path to end
                    # If node v is on any path to end, there's a negative cycle affecting the result
                    if _can_reach(v, end, parents) or _can_reach(end, v, graph):
                        negative_cycle_detected = True
                        break
        if negative_cycle_detected:
            break
    
    if negative_cycle_detected:
        return None, -np.inf
    
    # Reconstruct path
    path = []
    node = end
    visited = set()
    while node != -1:
        if node in visited:
            # Cycle detected in path reconstruction, should not happen but safety check
            return None, -np.inf
        visited.add(node)
        path.append(node)
        node = parents[node]
    path.reverse()
    
    return path, float(distances[end])


def _can_reach(start: int, end: int, graph_or_parents) -> bool:
    """Helper function to check if end is reachable from start."""
    if isinstance(graph_or_parents, np.ndarray) and graph_or_parents.ndim == 2:
        # It's a graph adjacency matrix
        graph = graph_or_parents
        n = len(graph)
        visited = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node == end:
                return True
            if node in visited:
                continue
            visited.add(node)
            for neighbor in range(n):
                if graph[node, neighbor] != np.inf and neighbor not in visited:
                    stack.append(neighbor)
        return False
    else:
        # It's a parent array - traverse backwards
        node = end
        visited = set()
        while node != -1:
            if node == start:
                return True
            if node in visited:
                return False
            visited.add(node)
            node = graph_or_parents[node] if graph_or_parents[node] != -1 else -1
        return False

