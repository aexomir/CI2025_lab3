"""
Dijkstra's algorithm for finding the shortest path in a graph with non-negative weights.
"""
import numpy as np
from typing import Tuple, List, Optional


def shortest_path(graph: np.ndarray, start: int, end: int) -> Tuple[Optional[List[int]], float]:
    """
    Find the shortest path from start to end using Dijkstra's algorithm.
    
    Args:
        graph: Adjacency matrix representation of the graph
        start: Starting node index
        end: Ending node index
    
    Returns:
        Tuple of (path, distance):
        - path: List of node indices representing the shortest path, or None if no path exists
        - distance: The shortest distance from start to end, or np.inf if no path exists
    """
    n = len(graph)
    
    # Initialize distances with infinity
    distances = np.full(n, np.inf)
    distances[start] = 0
    
    # Initialize parent array for path reconstruction
    parents = np.full(n, -1)
    
    # Priority queue: unvisited nodes
    unvisited = set(range(n))
    
    while unvisited:
        # Find the unvisited node with the smallest distance
        current = min(unvisited, key=lambda x: distances[x])
        
        # If we've reached the end, reconstruct and return the path
        if current == end:
            if distances[end] == np.inf:
                return None, np.inf
            
            # Reconstruct path
            path = []
            node = end
            while node != -1:
                path.append(node)
                node = parents[node]
            path.reverse()
            return path, float(distances[end])
        
        # If the smallest distance is infinity, remaining nodes are unreachable
        if distances[current] == np.inf:
            break
        
        unvisited.remove(current)
        
        # Update distances to neighbors
        for neighbor in range(n):
            if neighbor in unvisited and graph[current, neighbor] != np.inf:
                alt_distance = distances[current] + graph[current, neighbor]
                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    parents[neighbor] = current
    
    # No path found
    return None, np.inf

