import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Sentimen Pelayanan Haji 2024", layout="wide")

st.title("📊 Dashboard Sentimen Pelayanan Haji 2024")

# ======= Data Dummy Persentase Keseluruhan =======
overall_sentimen = {
    'Positif': 270,
    'Negatif': 542,
    'Netral': 75
}

df_overall = pd.DataFrame({
    'Sentimen': ['Positif', 'Negatif', 'Netral'],
    'Jumlah': [270, 542, 75]
})

colors_overall = ['green', 'red', 'yellow']

fig_overall = px.pie(
    df_overall, names='Sentimen', values='Jumlah',
    title='Persentase Sentimen Keseluruhan',
    category_orders={'Sentimen': ['Positif', 'Negatif', 'Netral']}
)

fig_overall.update_traces(marker=dict(colors=colors_overall), textposition='inside', textinfo='percent+label')

st.plotly_chart(fig_overall, use_container_width=True)

st.markdown("---")

# ======= Data Dummy Persentase per Aspek =======
aspek_data = {
    "Petugas": [203, 97, 12],        # Positif, Negatif, Netral
    "Ibadah": [156, 75, 4],
    "Transportasi": [179, 242, 35],
    "Akomodasi": [190, 378, 51],
    "Konsumsi": [191, 404, 54],
    "Lainnya": [177, 242, 39]
}

aspek_list = list(aspek_data.keys())

colors_per_aspek = ['green', 'red', 'yellow']

st.header("📈 Persentase Sentimen per Aspek")
for i in range(0, len(aspek_list), 3):
    cols = st.columns(3)
    for j, aspek in enumerate(aspek_list[i:i+3]):
        df = pd.DataFrame({
            'Sentimen': ['Positif', 'Negatif', 'Netral'],
            'Jumlah': aspek_data[aspek]
        })
        fig = px.pie(
            df, names='Sentimen', values='Jumlah', title=aspek,
            category_orders={'Sentimen': ['Positif', 'Negatif', 'Netral']}
        )
        fig.update_traces(marker=dict(colors=colors_per_aspek), textposition='inside', textinfo='percent+label')
        cols[j].plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ======= Word Cloud Per Aspek (3x2) =======
st.header("☁️ Word Cloud per Aspek")
for i in range(0, len(aspek_list), 3):
    cols = st.columns(3)
    for j, aspek in enumerate(aspek_list[i:i+3]):
        cols[j].subheader(aspek)
        img_path = f"wordclouds/{aspek.lower()}.png"  # Pastikan file gambarnya ada
        cols[j].image(img_path, width=300)

st.markdown("---")

# ======= Word Cloud Sentimen Positif & Negatif (2 kolom) =======
st.header("☁️ Word Cloud Sentimen Positif & Negatif")
col1, col2 = st.columns(2)
col1.subheader("✅ Positif")
col1.image("wordclouds/positif.png", width=400)
col2.subheader("❌ Negatif")
col2.image("wordclouds/negatif.png", width=400)

st.markdown("---")

# ======= Daftar Link Prediksi per Aspek =======
st.header("🔗 Link Prediksi Sentimen per Aspek")
aspek_links = {
    "Pelayanan Petugas": "https://aspek-sentimen-petugas-bsstccnkq6p9jbkatfjnio.streamlit.app",
    "Pelayanan Ibadah": "https://aspek-sentimen-ibadah-2u6k7kfpadkqm47u5rkc4s.streamlit.app",
    "Pelayanan Transportasi": "https://aspek-sentimen-transportasi-uukwhjbkmappqzlbyzwfbbo.streamlit.app",
    "Pelayanan Akomodasi": "https://aspek-sentimen-akomodasi-wbtwj3tex2mnpysxh4awkf.streamlit.app",
    "Pelayanan Konsumsi": "https://aspek-sentimen-konsumsi-sfrudivexbxwaracbrdrcq.streamlit.app",
    "Pelayanan Lainnya": "https://aspek-sentimen-lainnya-3rg6z9al9qt7lbrqmmcd7a.streamlit.app"
}

for aspek, url in aspek_links.items():
    st.markdown(f"👉 [{aspek}]({url})", unsafe_allow_html=True)
