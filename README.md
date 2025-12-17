# 🧠 Graph Data Structure Optimizer AI (GDSO)

**GDSO**, çizge (graph) tabanlı verilerle çalışan yazılım geliştiriciler ve veri bilimciler için geliştirilmiş, yapay zeka tabanlı bir performans optimizasyon çözümüdür. Sistem; grafın boyutunu, yoğunluğunu ve üzerinde çalıştırılacak algoritmayı analiz ederek; "**Komşuluk Matrisi (Adjacency Matrix)** mi yoksa **Komşuluk Listesi (Adjacency List)** mi kullanılmalı?" sorusuna bilimsel bir yanıt verir.



## 📌 Proje Özeti
Graf algoritmalarında (BFS, DFS, Dijkstra vb.) veri yapısı seçimi, işlem süresi ve bellek kullanımı üzerinde kritik bir etkiye sahiptir. GDSO:
* Farklı yoğunluk ve boyuttaki graflar üzerinde gerçek zamanlı deneyler yaparak performans verisi toplar.
* Toplanan verilerle bir Makine Öğrenmesi (ML) modeli eğitir.
* Geliştiricilere, kendi özel senaryoları için en hızlı veri yapısını öneren interaktif bir arayüz sunar.

## 🛠️ Teknik Altyapı
* **Geliştirme Ortamı:** Python 3.14.0 (Venv Sanal Ortam)
* **Donanım:** Apple Silicon (M4)
* **Veri İşleme:** Pandas, NumPy, NetworkX
* **Makine Öğrenmesi:** Scikit-Learn (Random Forest Classifier), Joblib
* **Arayüz (UI):** Streamlit (Web) ve CLI (Terminal)
* **Görselleştirme:** Matplotlib

## 📂 Proje Aşamaları ve Dosya Yapısı

Proje, verinin üretiminden ürünleştirilmesine kadar 11 ana aşamadan oluşmaktadır:

| Dosya Adı | Açıklama |
| :--- | :--- |
| `app.py` | Streamlit tabanlı interaktif web arayüzü. |
| `faz3_test.py` | Has Edge (Bağlantı Kontrolü) algoritması için veri üretimi. |
| `faz4_bfs_data.py` | BFS (Genişlik Öncelikli Arama) için performans ölçümü. |
| `faz5a_get_neighbors_data.py` | Komşu bulma performansı analizi. |
| `faz6a_dfs_data.py` | DFS (Derinlik Öncelikli Arama) için veri seti üretimi. |
| `faz7_merge_data.py` | Tüm CSV dosyalarını birleştirme ve etiketleme işlemi. |
| `faz8_train_model.py` | Random Forest modelinin eğitilmesi ve kaydedilmesi. |
| `faz9_verify_model.py` | Model doğrulama ve özellik önem analizi. |
| `faz10_demo_app.py` | CLI (Terminal) üzerinden çalışan demo uygulaması. |
| `faz11_dijkstra_data.py` | Dijkstra (En Kısa Yol) algoritması için veri üretimi. |

## 📊 Önemli Bulgular ve Analiz
Yapılan kapsamlı testler sonucunda elde edilen performans verileri şunları göstermiştir:
* **Has Edge (Bağlantı Kontrolü):** Yoğun graflarda (%20+) Matris yapısı $O(1)$ erişim hızıyla daha üstündür.
* **BFS & DFS (Gezinme):** Liste yapısı $O(V+E)$ karmaşıklığı ile çok daha hızlı sonuç vermektedir.
* **Dijkstra (En Kısa Yol):** Priority Queue kullanan Liste yapısı, Matrisin $O(V^2)$ yapısına göre belirgin şekilde daha performanslıdır.


## 📈 Model Başarısı
* **Doğruluk Oranı (Accuracy):** Test verileri üzerinde **%100**, 5-Katlı Çapraz Doğrulamada **%99.71**.
* **Karar Kriterleri:** Model, kararlarının %62'sini algoritma türüne, %37'sini ise grafın yapısal özelliklerine (düğüm sayısı ve yoğunluk) bakarak vermektedir.

## 🚀 Kurulum ve Çalıştırma

1. **Gerekli Kütüphaneleri Kurun:**
   ```bash
   pip install -r requirements.txt
2. **Web Uygulamasını Başlatın:**
   ```bash
   streamlit run app.py

## Kullanım
* Uygulama arayüzünden Düğüm Sayısı, Yoğunluk ve Algoritma türünü seçerek "Analiz Et" butonuna basın. Yapay zeka size en uygun veri yapısını anlık olarak önerecektir.
