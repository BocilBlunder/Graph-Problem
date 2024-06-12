import tracemalloc
import time

def decrease_and_conquer_coloring(graph):
    if not graph:
        return {}
    node = next(iter(graph))
    subgraph = {n: [neighbor for neighbor in neighbors if neighbor != node] for n, neighbors in graph.items() if n != node}
    result = decrease_and_conquer_coloring(subgraph)
    used_colors = {result.get(neighbor) for neighbor in graph[node] if neighbor in result}
    color = 1
    while color in used_colors:
        color += 1
    result[node] = color
    return result

def divide_and_conquer_coloring(graph):
    if len(graph) < 2:
        if graph:
            return {list(graph.keys())[0]: 1}
        else:
            return {}
    nodes = list(graph.keys())
    mid = len(nodes) // 2
    subgraph1 = {node: set(graph[node]) for node in nodes[:mid]}
    subgraph2 = {node: set(graph[node]) for node in nodes[mid:]}

    colored1 = divide_and_conquer_coloring(subgraph1)
    colored2 = divide_and_conquer_coloring(subgraph2)

    result = colored1
    for node in colored2:
        used_colors = {result[neighbor] for neighbor in graph[node] if neighbor in result}
        color = colored2[node]
        while color in used_colors:
            color += 1
        result[node] = color

    return result

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C'],
}

start_time = time.time()
tracemalloc.start()
print("Decrease and Conquer Coloring:", decrease_and_conquer_coloring(graph))
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
end_time = time.time()
print(end_time - start_time)

start_time1 = time.time()
tracemalloc.start()
print("Divide and Conquer Coloring:", divide_and_conquer_coloring(graph))
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
end_time1 = time.time()
print(end_time1 - start_time1)