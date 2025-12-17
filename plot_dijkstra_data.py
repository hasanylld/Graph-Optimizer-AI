import pandas as pd
import matplotlib.pyplot as plt
import os


csv_filename = "graph_dijkstra_performance_dataset.csv"

if not os.path.exists(csv_filename):
    print(f"HATA: '{csv_filename}' dosyası bulunamadı!")
    print("Lütfen önce 'faz11_dijkstra_data.py' dosyasını çalıştırıp veriyi üretin.")
    exit()

df = pd.read_csv(csv_filename)
print(f"Veri seti yüklendi. Toplam {len(df)} satır.")


cols = ['NumNodes', 'DensityValue', 'Matrix_Exec_Time_ms', 'List_Exec_Time_ms']
for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')


unique_densities = sorted(df['DensityValue'].unique())

plt.figure(figsize=(12, 7))


colors = ['blue', 'green', 'red']
markers = ['o', 's', '^']

for i, density in enumerate(unique_densities):
    
    subset = df[df['DensityValue'] == density]
    
    grouped = subset.groupby('NumNodes')[['Matrix_Exec_Time_ms', 'List_Exec_Time_ms']].mean()
    
    
    plt.plot(grouped.index, grouped['Matrix_Exec_Time_ms'], 
             label=f'Matris (Yoğunluk: {density})', 
             color=colors[i % len(colors)], linestyle='-', marker=markers[i % len(markers)])
    
    
    plt.plot(grouped.index, grouped['List_Exec_Time_ms'], 
             label=f'Liste (Yoğunluk: {density})', 
             color=colors[i % len(colors)], linestyle='--', marker=markers[i % len(markers)])

plt.title('Dijkstra Performansı: Düğüm Sayısına Göre Süre (Matris vs Liste)')
plt.xlabel('Düğüm Sayısı (N)')
plt.ylabel('Çalışma Süresi (ms) - Logaritmik')
plt.yscale('log') 
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout()
plt.show()


unique_nodes = sorted(df['NumNodes'].unique())

plt.figure(figsize=(12, 7))

for i, nodes in enumerate(unique_nodes):
    
    if nodes < 50: continue 
    
    subset = df[df['NumNodes'] == nodes]
    grouped = subset.groupby('DensityValue')[['Matrix_Exec_Time_ms', 'List_Exec_Time_ms']].mean()
    
    plt.plot(grouped.index, grouped['Matrix_Exec_Time_ms'], 
             label=f'Matris (V={nodes})', linestyle='-', marker='o')
    
    plt.plot(grouped.index, grouped['List_Exec_Time_ms'], 
             label=f'Liste (V={nodes})', linestyle='--', marker='x')

plt.title('Dijkstra Performansı: Graf Yoğunluğuna Göre Süre')
plt.xlabel('Graf Yoğunluğu (0.0 - 1.0)')
plt.ylabel('Çalışma Süresi (ms) - Logaritmik')
plt.yscale('log')
plt.legend()
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout()
plt.show()