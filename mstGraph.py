import networkx as nx
import tracemalloc
import time

def divide_and_conquer_mst(graph):
    if graph.number_of_nodes() <= 2:
        return graph

    nodes = list(graph.nodes())
    mid = len(nodes) // 2
    subgraph1 = graph.subgraph(nodes[:mid]).copy()
    subgraph2 = graph.subgraph(nodes[mid:]).copy()

    mst1 = divide_and_conquer_mst(subgraph1)
    mst2 = divide_and_conquer_mst(subgraph2)

    combined_graph = nx.compose(mst1, mst2)
    for u, v, data in graph.edges(data=True):
        combined_graph.add_edge(u, v, weight=data['weight'])
    return nx.minimum_spanning_tree(combined_graph, weight='weight')

def decrease_and_conquer_mst(graph):
    if graph.number_of_nodes() == 1:
        return graph

    node = next(iter(graph.nodes()))
    reduced_graph = graph.copy()
    reduced_graph.remove_node(node)

    mst_reduced = decrease_and_conquer_mst(reduced_graph)

    edges = [(node, neighbor, graph[node][neighbor]['weight']) for neighbor in graph.neighbors(node)]
    reduced_graph.add_weighted_edges_from(edges)
    return nx.minimum_spanning_tree(reduced_graph, weight='weight')

G = nx.Graph()
edges = [
    ('A', 'B', 2),
    ('A', 'C', 3),
    ('B', 'D', 1),
    ('C', 'D', 4),
    ('D', 'E', 5),
    ('E', 'A', 7)
]
G.add_weighted_edges_from(edges)

start_time = time.time()
tracemalloc.start()
mst_div_conq = divide_and_conquer_mst(G)
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
end_time = time.time()
print("Divide and Conquer MST:", mst_div_conq.edges(data=True))
print(end_time - start_time)

start_time1 = time.time()
tracemalloc.start()
mst_dec_conq = decrease_and_conquer_mst(G)
print(tracemalloc.get_traced_memory())
tracemalloc.stop()
end_time1 = time.time()
print("Decrease and Conquer MST:", mst_dec_conq.edges(data=True))
print(end_time1 - start_time1)