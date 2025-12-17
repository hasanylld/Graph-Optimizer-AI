import pandas as pd
import matplotlib.pyplot as plt
import os


desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
csv_filename = os.path.join(desktop_path, "graph_get_neighbors_performance_dataset.csv") # GetNeighbors veri dosyasının adı


try:
    df = pd.read_csv(csv_filename)
except FileNotFoundError:
    print(f"HATA: '{csv_filename}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()

print("GetNeighbors Veri setinden ilk 5 satır:")
print(df.head())
print(f"\nToplam {len(df)} satır GetNeighbors verisi okundu.")


numeric_cols = ['NumNodes', 'NumEdges', 'MaxPossibleEdges', 'DensityValue',
                'MatrixCreationTime_ms', 'ListCreationTime_ms',
                'AvgMatrixOpTime_ms', 'AvgListOpTime_ms'] 
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

if df.isnull().values.any():
    print("\nUyarı: GetNeighbors Veri setinde eksik değerler (NaN) bulundu.")

df_op = df[df['Algorithm'] == 'GetNeighbors'].copy()

plt.figure(figsize=(12, 8))
density_categories = df_op['DensityCategory'].unique()

for density in density_categories:
    subset = df_op[df_op['DensityCategory'] == density]
    avg_subset_matrix = subset.groupby('NumNodes')['AvgMatrixOpTime_ms'].mean()
    avg_subset_list = subset.groupby('NumNodes')['AvgListOpTime_ms'].mean()
    
    plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris GetNeighbors - {density}')
    plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste GetNeighbors - {density}')

plt.title('GetNeighbors: Düğüm Sayısına Göre Ortalama Operasyon Süresi')
plt.xlabel('Düğüm Sayısı (NumNodes)')
plt.ylabel('Ortalama Operasyon Süresi (ms)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log') 
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 8))
node_counts_for_plot = sorted(df_op['NumNodes'].unique())

for nodes in node_counts_for_plot:
    subset = df_op[df_op['NumNodes'] == nodes]
    avg_subset_matrix = subset.groupby('DensityValue')['AvgMatrixOpTime_ms'].mean().sort_index()
    avg_subset_list = subset.groupby('DensityValue')['AvgListOpTime_ms'].mean().sort_index()
    
    if not avg_subset_matrix.empty:
        plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris GetNeighbors - V={nodes}')
    if not avg_subset_list.empty:
        plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste GetNeighbors - V={nodes}')

plt.title('GetNeighbors: Graf Yoğunluğuna Göre Ortalama Operasyon Süresi')
plt.xlabel('Graf Yoğunluğu (Gerçekleşen Kenar / Maksimum Kenar)')
plt.ylabel('Ortalama Operasyon Süresi (ms)')
plt.legend(loc='upper left')
plt.grid(True)
plt.yscale('log') 
plt.tight_layout()
plt.show()



print("\nGetNeighbors grafikleri gösterildi.")