import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib  


df = pd.read_csv('final_ml_dataset.csv')

print("Veri Seti Yüklendi. Boyut:", df.shape)


features = ['NumNodes', 'DensityValue', 'Algorithm_Type_Code']
target = 'Best_Representation'  

X = df[features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Eğitim Verisi: {len(X_train)} adet")
print(f"Test Verisi: {len(X_test)} adet")


print("\nModel Eğitiliyor...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


acc = accuracy_score(y_test, y_pred)
print("-" * 40)
print(f"MODEL BAŞARISI (Accuracy): %{acc * 100:.2f}")
print("-" * 40)

print("Detaylı Rapor:")
print(classification_report(y_test, y_pred, target_names=['Matris (0)', 'Liste (1)']))

print("Karmaşıklık Matrisi (Confusion Matrix):")
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, 'graph_optimizer_model.pkl')
print("\nModel başarıyla 'graph_optimizer_model.pkl' olarak kaydedildi.")

print("\n--- CANLI TEST (Örnek Senaryo) ---")
ornek_senaryo = pd.DataFrame([[500, 0.60, 3]], columns=features)
tahmin = model.predict(ornek_senaryo)[0]

sonuc = "KOMŞULUK LİSTESİ" if tahmin == 1 else "KOMŞULUK MATRİSİ"
print(f"Senaryo: 500 Düğüm, %60 Yoğunluk, has_edge işlemi")
print(f"Modelin Önerisi: {sonuc}")