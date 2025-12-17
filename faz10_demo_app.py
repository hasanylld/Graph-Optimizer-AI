import pandas as pd
import joblib
import os
import time
import sys

def clear_screen():
   
    os.system('cls' if os.name == 'nt' else 'clear')


model_filename = 'graph_optimizer_model.pkl'
if not os.path.exists(model_filename):
    print("HATA: Model dosyası (graph_optimizer_model.pkl) bulunamadı!")
    print("Lütfen önce 'faz8_train_model.py' dosyasını çalıştırarak modeli eğitin.")
    sys.exit()

model = joblib.load(model_filename)


algo_map = {
    1: {"name": "BFS (Genişlik Öncelikli Arama)", "code": 0},
    2: {"name": "DFS (Derinlik Öncelikli Arama)", "code": 1},
    3: {"name": "Get Neighbors (Komşuları Getir)", "code": 2},
    4: {"name": "Has Edge (Kenar Kontrolü)",      "code": 3},
    5: {"name": "DIJKSTRA (En Kısa Yol)",         "code": 4}
}

clear_screen()
print("========================================================")
print("   GRAF VERİ YAPISI OPTİMİZASYON ASİSTANI (vFinal)   ")
print("========================================================")

while True:
    print("\n" + "-"*55)
    try:
        
        nodes_input = input("1. Düğüm Sayısı (NumNodes) [Çıkış için 'q']: ")
        if nodes_input.lower() == 'q': break
        nodes = int(nodes_input)
        
        density = float(input("2. Yoğunluk (0.0 - 1.0 arası, örn: 0.2): "))
        
        print("\n3. Çalıştırılacak Algoritma:")
        print("   [1] BFS")
        print("   [2] DFS")
        print("   [3] Get Neighbors")
        print("   [4] Has Edge")
        print("   [5] DIJKSTRA")
        
        algo_choice = int(input("   Seçiminiz (1-5): "))
        
        if algo_choice not in algo_map:
            print("HATA: Geçersiz seçim, tekrar deneyin.")
            continue
        
        selected = algo_map[algo_choice]
        
       
        print("\nAnaliz ediliyor...")
        time.sleep(0.5) 
        
        
        input_data = pd.DataFrame([[nodes, density, selected['code']]], 
                                  columns=['NumNodes', 'DensityValue', 'Algorithm_Type_Code'])
        
        prediction = model.predict(input_data)[0]
        
        
        print("="*55)
        print(f"SENARYO: {selected['name']} | V={nodes} | Yoğunluk={density}")
        print("-" * 55)
        
        if prediction == 0:
            print(">> ÖNERİ: KOMŞULUK MATRİSİ (Adjacency Matrix)")
            print("   Sebep: Bu senaryoda Matris yapısı daha performanslıdır.")
        else:
            print(">> ÖNERİ: KOMŞULUK LİSTESİ (Adjacency List)")
            print("   Sebep: Bu senaryoda Liste yapısı daha performanslıdır.")
            
        print("="*55)
        
    except ValueError:
        print("HATA: Lütfen geçerli bir sayı giriniz!")
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        break