

import networkx as nx
import numpy as np
import time
import random
import csv
import os


def get_neighbors_list(adj_list, node_u):
    if node_u in adj_list:
        return adj_list[node_u] 
    return []

def get_neighbors_matrix(adj_matrix, node_u):
    num_nodes = adj_matrix.shape[0]
    neighbors = []
    if 0 <= node_u < num_nodes:
        for v_node in range(num_nodes):
            if adj_matrix[node_u, v_node] == 1: 
                neighbors.append(v_node)
    return neighbors


def create_random_graph(num_nodes, num_edges):
    if num_nodes <= 0:
        return nx.Graph()
    max_edges = num_nodes * (num_nodes - 1) // 2
    actual_num_edges = max(0, min(num_edges, max_edges))
    if actual_num_edges == 0 and num_nodes > 0:
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))
        return G
    elif actual_num_edges == 0 and num_nodes == 0:
        return nx.Graph()
    return nx.gnm_random_graph(num_nodes, actual_num_edges)


def run_get_neighbors_experiment_for_dataset(graph_nx, num_ops_per_graph=1000):
    if not graph_nx.nodes:
        return 0.0, 0.0, 0.0, 0.0 

    
    start_time_matrix_creation = time.perf_counter()
    adj_matrix = nx.to_numpy_array(graph_nx, dtype=np.int8)
    end_time_matrix_creation = time.perf_counter()
    time_matrix_creation_ms = (end_time_matrix_creation - start_time_matrix_creation) * 1000

    start_time_list_creation = time.perf_counter()
    adj_list = {node: list(graph_nx.neighbors(node)) for node in graph_nx.nodes()}
    end_time_list_creation = time.perf_counter()
    time_list_creation_ms = (end_time_list_creation - start_time_list_creation) * 1000
    
    nodes_list_for_ops = list(graph_nx.nodes())
    if not nodes_list_for_ops: 
        return time_matrix_creation_ms, time_list_creation_ms, 0.0, 0.0

   
    op_nodes = [random.choice(nodes_list_for_ops) for _ in range(num_ops_per_graph)]

   
    start_time = time.perf_counter()
    for node_u in op_nodes:
        get_neighbors_matrix(adj_matrix, node_u)
    end_time = time.perf_counter()
    time_matrix_op_ms = ((end_time - start_time) * 1000) / num_ops_per_graph if num_ops_per_graph > 0 else 0

    
    start_time = time.perf_counter()
    for node_u in op_nodes:
        get_neighbors_list(adj_list, node_u) 
    end_time = time.perf_counter()
    time_list_op_ms = ((end_time - start_time) * 1000) / num_ops_per_graph if num_ops_per_graph > 0 else 0
    
    return time_matrix_creation_ms, time_list_creation_ms, time_matrix_op_ms, time_list_op_ms



print("\n--- GetNeighbors Veri Seti Oluşturma ---")

node_counts = [10, 50, 100, 200, 500] 
density_percentages = {
    "Sparse": 0.05,
    "Medium": 0.25,
    "Dense": 0.60
}
replications_per_setting = 5
num_operations_per_graph_instance = 2000 

dataset_rows = []
csv_header = [
    "GraphID", "NumNodes", "NumEdges", "MaxPossibleEdges", "DensityCategory", "DensityValue",
    "MatrixCreationTime_ms", "ListCreationTime_ms",
    "AvgMatrixOpTime_ms", "AvgListOpTime_ms", "Algorithm" 
]
dataset_rows.append(csv_header)
graph_id_counter = 0

for V in node_counts:
    print(f"Processing graphs with V={V} nodes for GetNeighbors...")
    max_E_for_V = V * (V - 1) // 2 if V > 1 else 0
    
    for density_name, density_perc in density_percentages.items():
        if V <= 1 and density_perc > 0 :
            num_E = 0
        elif V > 1 and density_perc > 0:
            min_edges_for_connectivity_approx = V -1 
            calculated_edges = int(max_E_for_V * density_perc)
            num_E = max(min_edges_for_connectivity_approx if density_name == "Sparse" else 0 , calculated_edges)
            num_E = min(num_E, max_E_for_V)
        else:
            num_E = 0

        print(f"  Density: {density_name} (Target E ~ {num_E})")
        
        for rep in range(replications_per_setting):
            graph_id_counter += 1
            current_graph_id = f"g_getneigh_{V}_{density_name}_{rep+1}" 
            
            G = create_random_graph(V, num_E)
            actual_E = G.number_of_edges()

            if G.number_of_nodes() == 0 :
                mc_time, lc_time, mop_time, lop_time = 0,0,0,0
            else:
               
                mc_time, lc_time, mop_time, lop_time = run_get_neighbors_experiment_for_dataset(G, num_operations_per_graph_instance)
            
            row = [
                current_graph_id, V, actual_E, max_E_for_V, density_name, 
                (actual_E / max_E_for_V if max_E_for_V > 0 else 0),
                mc_time, lc_time, mop_time, lop_time, "GetNeighbors" 
            ]
            dataset_rows.append(row)
            
            if (rep + 1) % 2 == 0 :
                 print(f"    GetNeighbors Rep {rep+1}/{replications_per_setting} done. V={V}, E_actual={actual_E}, MatrixOp: {mop_time:.6f}ms, ListOp: {lop_time:.6f}ms")


desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
csv_filename = os.path.join(desktop_path, "graph_get_neighbors_performance_dataset.csv")

try:
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(dataset_rows)
    print(f"\nGetNeighbors Veri seti başarıyla '{csv_filename}' dosyasına kaydedildi.")
except IOError:
    print(f"\nHATA: '{csv_filename}' dosyasına yazılamadı.")