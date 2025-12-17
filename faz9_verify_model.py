import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt


try:
    df = pd.read_csv('final_ml_dataset.csv')
except FileNotFoundError:
    print("HATA: 'final_ml_dataset.csv' bulunamadı.")
    exit()

X = df[['NumNodes', 'DensityValue', 'Algorithm_Type_Code']]
y = df['Best_Representation']

model = RandomForestClassifier(n_estimators=100, random_state=42)


k_fold = KFold(n_splits=5, shuffle=True, random_state=42)

print("--- MODEL DOĞRULAMASI (Dijkstra Dahil) ---")
print("Çapraz Doğrulama (Cross-Validation) yapılıyor...")

scores = cross_val_score(model, X, y, cv=k_fold)

print(f"\n5 Farklı Test Sonucu: {scores}")
print(f"ORTALAMA BAŞARI: %{scores.mean() * 100:.2f}")


model.fit(X, y)
importances = model.feature_importances_
feature_names = X.columns

print("\nModel Karar Verirken Neye Baktı?")
for name, score in zip(feature_names, importances):
    print(f"{name}: %{score * 100:.2f}")


plt.figure(figsize=(8, 5))
plt.bar(feature_names, importances, color=['blue', 'green', 'orange'])
plt.title('Yapay Zeka Karar Kriterleri (Dijkstra Dahil)')
plt.ylabel('Önem Düzeyi')
plt.show()