import pandas as pd
import matplotlib.pyplot as plt
import os


desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
csv_filename = os.path.join(desktop_path, "graph_bfs_performance_dataset.csv") 


try:
    df = pd.read_csv(csv_filename)
except FileNotFoundError:
    print(f"HATA: '{csv_filename}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()

print("BFS Veri setinden ilk 5 satır:")
print(df.head())
print(f"\nToplam {len(df)} satır BFS verisi okundu.")


numeric_cols = ['NumNodes', 'NumEdges', 'MaxPossibleEdges', 'DensityValue',
                'MatrixCreationTime_ms', 'ListCreationTime_ms',
                'AvgMatrixBFSTime_ms', 'AvgListBFSTime_ms'] 
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

if df.isnull().values.any():
    print("\nUyarı: BFS Veri setinde eksik değerler (NaN) bulundu.")


df_bfs = df[df['Algorithm'] == 'BFS'].copy()


plt.figure(figsize=(12, 8))
density_categories = df_bfs['DensityCategory'].unique()

for density in density_categories:
    subset = df_bfs[df_bfs['DensityCategory'] == density]
    avg_subset_matrix = subset.groupby('NumNodes')['AvgMatrixBFSTime_ms'].mean()
    avg_subset_list = subset.groupby('NumNodes')['AvgListBFSTime_ms'].mean()
    
    plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris BFS - {density}')
    plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste BFS - {density}')

plt.title('BFS: Düğüm Sayısına Göre Ortalama Çalışma Süresi')
plt.xlabel('Düğüm Sayısı (NumNodes)')
plt.ylabel('Ortalama BFS Süresi (ms)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log') 
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 8))
node_counts_for_plot = sorted(df_bfs['NumNodes'].unique())

for nodes in node_counts_for_plot:
    subset = df_bfs[df_bfs['NumNodes'] == nodes]
    avg_subset_matrix = subset.groupby('DensityValue')['AvgMatrixBFSTime_ms'].mean().sort_index()
    avg_subset_list = subset.groupby('DensityValue')['AvgListBFSTime_ms'].mean().sort_index()
    
    if not avg_subset_matrix.empty:
        plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris BFS - V={nodes}')
    if not avg_subset_list.empty:
        plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste BFS - V={nodes}')

plt.title('BFS: Graf Yoğunluğuna Göre Ortalama Çalışma Süresi')
plt.xlabel('Graf Yoğunluğu (Gerçekleşen Kenar / Maksimum Kenar)')
plt.ylabel('Ortalama BFS Süresi (ms)')
plt.legend(loc='upper left')
plt.grid(True)
plt.yscale('log')
plt.tight_layout()
plt.show()




print("\nBFS grafikleri gösterildi.")