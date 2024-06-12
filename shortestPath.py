import heapq
import time
import tracemalloc

def findMidPoint(graph):
    return graph['vertices'][len(graph['vertices']) // 2]

def splitGraph(graph, mid_point):
    mid_index = graph['vertices'].index(mid_point)
    subgraph1 = {
        'vertices': graph['vertices'][:mid_index + 1],
        'edges': {k: v for k, v in graph['edges'].items() if k[0] in graph['vertices'][:mid_index + 1] and k[1] in graph['vertices'][:mid_index + 1]}
    }
    subgraph2 = {
        'vertices': graph['vertices'][mid_index:],
        'edges': {k: v for k, v in graph['edges'].items() if k[0] in graph['vertices'][mid_index:] and k[1] in graph['vertices'][mid_index:]}
    }
    return subgraph1, subgraph2

def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph['vertices']}
    previous_nodes = {vertex: None for vertex in graph['vertices']}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex == end:
            break

        for neighbor, weight in [(k[1], v) for k, v in graph['edges'].items() if k[0] == current_vertex]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path if path[0] == start else []

def shortestPathDnC(graph, start, end):
    if len(graph['vertices']) < 3 or (start, end) in graph['edges']:
        return dijkstra(graph, start, end)

    mid_point = findMidPoint(graph)
    subgraph1, subgraph2 = splitGraph(graph, mid_point)

    if start in subgraph1['vertices'] and end in subgraph1['vertices']:
        return dijkstra(subgraph1, start, end)
    elif start in subgraph2['vertices'] and end in subgraph2['vertices']:
        return dijkstra(subgraph2, start, end)

    path1 = shortestPathDnC(subgraph1, start, mid_point) if start in subgraph1['vertices'] else []
    path2 = shortestPathDnC(subgraph2, mid_point, end) if end in subgraph2['vertices'] else []

    if path1 and path2:
        combined_path = path1 + path2[1:]
    else:
        combined_path = []

    direct_path = dijkstra(graph, start, end)
    return combined_path if combined_path and sum(graph['edges'].get((combined_path[i], combined_path[i+1]), float('inf')) for i in range(len(combined_path)-1)) < sum(graph['edges'].get((direct_path[i], direct_path[i+1]), float('inf')) for i in range(len(direct_path)-1)) else direct_path


def selectVertexToRemove(graph, start, end):
    for vertex in graph['vertices']:
        if vertex not in [start, end]:
            return vertex
    return None

def removeVertex(graph, vertex):
    if vertex is None:
        return graph
    new_vertices = [v for v in graph['vertices'] if v != vertex]
    new_edges = {k: v for k, v in graph['edges'].items() if vertex not in k}
    return {'vertices': new_vertices, 'edges': new_edges}

def updatePathWithVertex(graph, path, removed_vertex):
    if removed_vertex:
        return path + [removed_vertex]
    return path

def shortestPathDeC(graph, start, end):
    if len(graph['vertices']) == 2:
        return dijkstra(graph, start, end)

    removed_vertex = selectVertexToRemove(graph, start, end)
    reduced_graph = removeVertex(graph, removed_vertex)
    path_without_vertex = dijkstra(reduced_graph, start, end)

    path_with_vertex = dijkstra(graph, start, end)  
    return path_with_vertex if sum(graph['edges'].get((path_with_vertex[i], path_with_vertex[i+1]), float('inf')) for i in range(len(path_with_vertex)-1)) < sum(graph['edges'].get((path_without_vertex[i], path_without_vertex[i+1]), float('inf')) for i in range(len(path_without_vertex)-1)) else path_without_vertex


def make_undirected(graph):
    undirected_edges = {}
    for (u, v), weight in graph['edges'].items():
        undirected_edges[(u, v)] = weight
        undirected_edges[(v, u)] = weight
    return {
        'vertices': graph['vertices'],
        'edges': undirected_edges
    }

def main():
    graph = {
        'vertices': ['A', 'B', 'C', 'D', 'E', 'F'],
        'edges': {
            ('A', 'B'): 1,
            ('B', 'C'): 2,
            ('C', 'E'): 10,
            ('A', 'D'): 10,
            ('D', 'E'): 4,
            ('E', 'F'): 10,
        }
    }

    undirected_graph = make_undirected(graph)

    start = 'A'
    end = 'F'

    start_time = time.time()
    tracemalloc.start()
    path_DnC = shortestPathDnC(undirected_graph, start, end)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()
    end_time = time.time()
    print("Path using Divide and Conquer:", path_DnC)
    print(end_time - start_time)

    start_time1 = time.time()
    tracemalloc.start()
    path_DeC = shortestPathDeC(undirected_graph, start, end)
    print(tracemalloc.get_traced_memory())
    tracemalloc.stop()
    end_time1 = time.time()
    print("Path using Decrease and Conquer:", path_DeC)
    print(end_time1 - start_time1)

main()
