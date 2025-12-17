import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Graph Optimizer AI",
    page_icon="🧠",
    layout="centered"
)


st.title("🧠 Graf Veri Yapısı Optimizasyonu")
st.markdown("""
Bu yapay zeka asistanı, graf verilerin için **Matris** mi yoksa **Liste** mi kullanman gerektiğini 
senin için analiz eder.
""")
st.divider()


try:
    
    model = joblib.load('graph_optimizer_model.pkl')
except FileNotFoundError:
    st.error("🚨 HATA: 'graph_optimizer_model.pkl' dosyası bulunamadı!")
    st.warning("Lütfen model dosyasının app.py ile aynı klasörde olduğundan emin olun.")
    st.stop()


st.sidebar.header("⚙️ Parametreler")

nodes = st.sidebar.slider("1. Düğüm Sayısı (NumNodes)", min_value=10, max_value=5000, value=500, step=10)

density = st.sidebar.slider("2. Yoğunluk (Density)", min_value=0.01, max_value=1.0, value=0.2, step=0.01)


algo_options = {
    "BFS (Genişlik Öncelikli Arama)": 0,
    "DFS (Derinlik Öncelikli Arama)": 1,
    "Get Neighbors (Komşuları Getir)": 2,
    "Has Edge (Kenar Kontrolü)": 3,
    "DIJKSTRA (En Kısa Yol)": 4
}

selected_algo_name = st.sidebar.selectbox(
    "3. Çalıştırılacak Algoritma",
    list(algo_options.keys())
)


algo_code = algo_options[selected_algo_name]




if st.button("ANALİZ ET VE ÖNER 🚀", type="primary"):
    
    
    input_data = pd.DataFrame({
        'NumNodes': [nodes],
        'DensityValue': [density],
        'Algorithm_Type_Code': [algo_code]
    })

    with st.spinner('Yapay zeka hesaplıyor...'):
        
        prediction = model.predict(input_data)[0]
        
        
        try:
            probs = model.predict_proba(input_data)[0]
            confidence = max(probs) * 100
        except:
            confidence = 0

    st.markdown("### 🎯 Analiz Sonucu")
    
    
    if prediction == 0:
        st.success(f"✅ ÖNERİ: KOMŞULUK MATRİSİ (Adjacency Matrix)")
        st.info(f"Yapay zeka bu senaryoda **Matris** yapısının daha hızlı olacağını öngörüyor.")
        if confidence > 0:
            st.caption(f"Güven Oranı: %{confidence:.2f}")
            
    else:
        st.success(f"✅ ÖNERİ: KOMŞULUK LİSTESİ (Adjacency List)")
        st.info(f"Yapay zeka bu senaryoda **Liste** yapısının daha hızlı olacağını öngörüyor.")
        if confidence > 0:
            st.caption(f"Güven Oranı: %{confidence:.2f}")

    
    st.divider()
    st.text(f"🔍 Seçilen Senaryo: {nodes} Düğüm | %{int(density*100)} Yoğunluk | {selected_algo_name}")

else:
    st.info("Tahmin yapmak için yan menüden parametreleri seçip butona basın. 👈")