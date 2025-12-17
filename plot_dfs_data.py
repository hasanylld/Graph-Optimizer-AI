import pandas as pd
import matplotlib.pyplot as plt
import os


desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
csv_filename = os.path.join(desktop_path, "graph_dfs_performance_dataset.csv") # DFS veri dosyasının adı


try:
    df = pd.read_csv(csv_filename)
except FileNotFoundError:
    print(f"HATA: '{csv_filename}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()

print("DFS Veri setinden ilk 5 satır:")
print(df.head())
print(f"\nToplam {len(df)} satır DFS verisi okundu.")


numeric_cols = ['NumNodes', 'NumEdges', 'MaxPossibleEdges', 'DensityValue',
                'MatrixCreationTime_ms', 'ListCreationTime_ms',
                'AvgMatrixDFSTime_ms', 'AvgListDFSTime_ms'] 
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

if df.isnull().values.any():
    print("\nUyarı: DFS Veri setinde eksik değerler (NaN) bulundu.")


df_algo = df[df['Algorithm'] == 'DFS'].copy()


plt.figure(figsize=(12, 8))
density_categories = df_algo['DensityCategory'].unique()

for density in density_categories:
    subset = df_algo[df_algo['DensityCategory'] == density]
    avg_subset_matrix = subset.groupby('NumNodes')['AvgMatrixDFSTime_ms'].mean()
    avg_subset_list = subset.groupby('NumNodes')['AvgListDFSTime_ms'].mean()
    
    plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris DFS - {density}')
    plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste DFS - {density}')

plt.title('DFS: Düğüm Sayısına Göre Ortalama Çalışma Süresi')
plt.xlabel('Düğüm Sayısı (NumNodes)')
plt.ylabel('Ortalama DFS Süresi (ms)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log') 
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 8))
node_counts_for_plot = sorted(df_algo['NumNodes'].unique())

for nodes in node_counts_for_plot:
    subset = df_algo[df_algo['NumNodes'] == nodes]
    avg_subset_matrix = subset.groupby('DensityValue')['AvgMatrixDFSTime_ms'].mean().sort_index()
    avg_subset_list = subset.groupby('DensityValue')['AvgListDFSTime_ms'].mean().sort_index()
    
    if not avg_subset_matrix.empty:
        plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris DFS - V={nodes}')
    if not avg_subset_list.empty:
        plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste DFS - V={nodes}')

plt.title('DFS: Graf Yoğunluğuna Göre Ortalama Çalışma Süresi')
plt.xlabel('Graf Yoğunluğu (Gerçekleşen Kenar / Maksimum Kenar)')
plt.ylabel('Ortalama DFS Süresi (ms)')
plt.legend(loc='upper left')
plt.grid(True)
plt.yscale('log') 
plt.tight_layout()
plt.show()

print("\nDFS grafikleri gösterildi.")