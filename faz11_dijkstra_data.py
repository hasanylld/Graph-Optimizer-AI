import networkx as nx
import numpy as np
import time
import random
import csv
import os
import heapq


def dijkstra_matrix(adj_matrix, start_node):
    num_nodes = adj_matrix.shape[0]
    dist = {node: float('inf') for node in range(num_nodes)}
    dist[start_node] = 0
    visited = [False] * num_nodes

    for _ in range(num_nodes):
        
        min_dist = float('inf')
        u = -1
        for i in range(num_nodes):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
        
        if u == -1: 
            break
            
        visited[u] = True
        
        
        for v in range(num_nodes):
            weight = adj_matrix[u][v]
            if weight > 0 and not visited[v]: 
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
    return dist


def dijkstra_list(adj_list, start_node):
    dist = {node: float('inf') for node in adj_list}
    dist[start_node] = 0
    pq = [(0, start_node)] 

    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, weight in adj_list.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    return dist


def create_weighted_random_graph(num_nodes, num_edges):
    if num_nodes <= 0: return nx.Graph()
    
    
    G = nx.gnm_random_graph(num_nodes, num_edges)
    
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 100)
        
    return G


def run_dijkstra_experiment(graph_nx, num_trials=5):
    if not graph_nx.nodes: return 0,0,0,0

    
    start = time.perf_counter()
    adj_matrix = nx.to_numpy_array(graph_nx, weight='weight', dtype=np.int32) 
    
    mt_create = (time.perf_counter() - start) * 1000

    
    start = time.perf_counter()
    adj_list = {}
    for node in graph_nx.nodes():
        adj_list[node] = []
        for neighbor in graph_nx.neighbors(node):
            w = graph_nx.edges[node, neighbor]['weight']
            adj_list[node].append((neighbor, w))
    lt_create = (time.perf_counter() - start) * 1000
    
    
    nodes = list(graph_nx.nodes())
    start_node = random.choice(nodes)
    
    
    total_m = 0
    for _ in range(num_trials):
        s = time.perf_counter()
        dijkstra_matrix(adj_matrix, start_node)
        total_m += (time.perf_counter() - s)
    avg_m_time = (total_m * 1000) / num_trials

    
    total_l = 0
    for _ in range(num_trials):
        s = time.perf_counter()
        dijkstra_list(adj_list, start_node)
        total_l += (time.perf_counter() - s)
    avg_l_time = (total_l * 1000) / num_trials
    
    return mt_create, lt_create, avg_m_time, avg_l_time


print("--- DIJKSTRA Veri Seti Oluşturuluyor (Bu biraz sürebilir...) ---")

node_counts = [10, 50, 100, 200, 500]
density_percentages = {"Sparse": 0.05, "Medium": 0.25, "Dense": 0.60}
rows = []
rows.append(["GraphID", "NumNodes", "DensityValue", "Matrix_Exec_Time_ms", "List_Exec_Time_ms", "Algorithm"])

for V in node_counts:
    print(f"Processing V={V}...")
    max_E = V * (V - 1) // 2
    for d_name, d_val in density_percentages.items():
        E = int(max_E * d_val)
        for rep in range(3): 
            G = create_weighted_random_graph(V, E)
            mc, lc, m_run, l_run = run_dijkstra_experiment(G)
            
            rows.append([f"dijkstra_{V}_{d_name}_{rep}", V, d_val, m_run, l_run, "Dijkstra"])


csv_name = "graph_dijkstra_performance_dataset.csv"
with open(csv_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\nTAMAMLANDI! '{csv_name}' dosyası oluşturuldu.")