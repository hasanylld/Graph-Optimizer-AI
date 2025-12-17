import pandas as pd
import numpy as np
import os

# GÜNCELLENMİŞ DOSYA LİSTESİ (Dijkstra Eklendi)
files_map = {
    "graph_bfs_performance_dataset.csv":          {"name": "BFS",          "code": 0},
    "graph_dfs_performance_dataset.csv":          {"name": "DFS",          "code": 1},
    "graph_get_neighbors_performance_dataset.csv":{"name": "GetNeighbors", "code": 2},
    "graph_has_edge_performance_dataset.csv":     {"name": "HasEdge",      "code": 3},
    "graph_dijkstra_performance_dataset.csv":     {"name": "Dijkstra",     "code": 4} 
}

dfs = []
print("--- VERİ BİRLEŞTİRME (DIJKSTRA DAHİL) ---")

for filename, algo_info in files_map.items():
    if os.path.exists(filename):
        print(f"Ekleniyor: {filename}")
        df = pd.read_csv(filename)
        
        df['Algorithm_Name'] = algo_info['name']
        df['Algorithm_Type_Code'] = algo_info['code']
        
        # Sütun isimlerini düzeltme
        matrix_col = [c for c in df.columns if 'Matrix' in c and 'Time' in c and 'Creation' not in c][0]
        list_col = [c for c in df.columns if 'List' in c and 'Time' in c and 'Creation' not in c][0]
        
        df.rename(columns={matrix_col: 'Matrix_Exec_Time_ms', list_col: 'List_Exec_Time_ms'}, inplace=True)
        
        # Etiketleme
        conditions = [
            (df['Matrix_Exec_Time_ms'] <= df['List_Exec_Time_ms']),
            (df['Matrix_Exec_Time_ms'] > df['List_Exec_Time_ms'])
        ]
        df['Best_Representation'] = np.select(conditions, [0, 1])
        dfs.append(df)
    else:
        print(f"UYARI: {filename} bulunamadı. (Eğer oluşturmadıysan normal)")

if dfs:
    master_df = pd.concat(dfs, ignore_index=True)
    master_df.to_csv("final_ml_dataset.csv", index=False)
    print("\nYeni 'final_ml_dataset.csv' oluşturuldu.")
    print(master_df['Best_Representation'].value_counts())