def choose_algorithm(size: int, density: float, negative_values: bool) -> str:
    if negative_values:
        return "bellman_ford"
    
    # For non-negative graphs, prefer Dijkstra, but use Floyd-Warshall for small dense graphs
    if size <= 100 and density >= 0.8:
        return "floyd_warshall"
    
    return "dijkstra"

