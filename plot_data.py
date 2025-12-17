import pandas as pd
import matplotlib.pyplot as plt
import os


desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
csv_filename = os.path.join(desktop_path, "graph_has_edge_performance_dataset.csv")


try:
    df = pd.read_csv(csv_filename)
except FileNotFoundError:
    print(f"HATA: '{csv_filename}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
    exit()

print("Veri setinden ilk 5 satır:")
print(df.head())
print(f"\nToplam {len(df)} satır veri okundu.")


numeric_cols = ['NumNodes', 'NumEdges', 'MaxPossibleEdges', 'DensityValue',
                'MatrixCreationTime_ms', 'ListCreationTime_ms',
                'AvgMatrixQueryTime_ms', 'AvgListQueryTime_ms']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce') 


if df.isnull().values.any():
    print("\nUyarı: Veri setinde eksik değerler (NaN) bulundu. Bu durum grafikleri etkileyebilir.")
   

df_has_edge = df[df['Algorithm'] == 'has_edge'].copy() 
plt.figure(figsize=(12, 8))
density_categories = df_has_edge['DensityCategory'].unique()

for density in density_categories:
    subset = df_has_edge[df_has_edge['DensityCategory'] == density]
   
    avg_subset_matrix = subset.groupby('NumNodes')['AvgMatrixQueryTime_ms'].mean()
    avg_subset_list = subset.groupby('NumNodes')['AvgListQueryTime_ms'].mean()
    
    plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris - {density}')
    plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste - {density}')

plt.title('`has_edge`: Düğüm Sayısına Göre Ortalama Sorgu Süresi')
plt.xlabel('Düğüm Sayısı (NumNodes)')
plt.ylabel('Ortalama Sorgu Süresi (ms)')
plt.legend()
plt.grid(True)
plt.xscale('log') 
plt.yscale('log')
plt.tight_layout()
plt.show()



plt.figure(figsize=(12, 8))
node_counts_for_plot = df_has_edge['NumNodes'].unique()


for nodes in node_counts_for_plot:
    subset = df_has_edge[df_has_edge['NumNodes'] == nodes]
   
    avg_subset_matrix = subset.groupby('DensityValue')['AvgMatrixQueryTime_ms'].mean().sort_index()
    avg_subset_list = subset.groupby('DensityValue')['AvgListQueryTime_ms'].mean().sort_index()
    
    if not avg_subset_matrix.empty:
        plt.plot(avg_subset_matrix.index, avg_subset_matrix.values, marker='o', linestyle='-', label=f'Matris - V={nodes}')
    if not avg_subset_list.empty:
        plt.plot(avg_subset_list.index, avg_subset_list.values, marker='x', linestyle='--', label=f'Liste - V={nodes}')

plt.title('`has_edge`: Graf Yoğunluğuna Göre Ortalama Sorgu Süresi')
plt.xlabel('Graf Yoğunluğu (Gerçekleşen Kenar / Maksimum Kenar)')
plt.ylabel('Ortalama Sorgu Süresi (ms)')
plt.legend(loc='upper left')
plt.grid(True)

plt.yscale('log') 
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))

avg_matrix_creation = df_has_edge.groupby('NumNodes')['MatrixCreationTime_ms'].mean()
avg_list_creation = df_has_edge.groupby('NumNodes')['ListCreationTime_ms'].mean()

plt.plot(avg_matrix_creation.index, avg_matrix_creation.values, marker='o', linestyle='-', label='Matris Oluşturma')
plt.plot(avg_list_creation.index, avg_list_creation.values, marker='x', linestyle='--', label='Liste Oluşturma')

plt.title('Düğüm Sayısına Göre Ortalama Temsil Oluşturma Süresi')
plt.xlabel('Düğüm Sayısı (NumNodes)')
plt.ylabel('Ortalama Oluşturma Süresi (ms)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
plt.show()

print("\nGrafikler gösterildi.")