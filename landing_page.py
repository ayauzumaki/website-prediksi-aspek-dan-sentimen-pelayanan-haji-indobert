import streamlit as st
import pandas as pd
import os
import gdown
import re
import string
from transformers import AutoTokenizer, BertForSequenceClassification, BertConfig
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ===================== KONSTANTA =====================
KAMUS_CSV_URL = "https://drive.google.com/uc?id=1fGWZu5qVYJa-pv078spaLE4urs5zDDPV"
KAMUS_PATH = "kamus.csv"

# ===================== UTILITY FUNCTIONS =====================
def download_kamus():
    if not os.path.exists(KAMUS_PATH):
        with st.spinner("Mengunduh kamus slang..."):
            gdown.download(KAMUS_CSV_URL, KAMUS_PATH, quiet=False)

@st.cache_resource(show_spinner=True)
def load_tokenizer(folder):
    return AutoTokenizer.from_pretrained(folder)

@st.cache_resource(show_spinner=True)
def load_model(folder):
    config = BertConfig.from_pretrained(folder)
    model = BertForSequenceClassification.from_pretrained(folder, config=config)
    model.eval()
    return model

@st.cache_resource
def load_kamus():
    df = pd.read_csv(KAMUS_PATH)
    return dict(zip(df['slang'], df['formal']))

def preprocess(text, kamus_slang):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join([kamus_slang.get(word, word) for word in text.split()])
    return text.strip()

# ===================== SETUP =====================
st.set_page_config(layout="centered")
st.title("Aplikasi Prediksi Aspek Pelayanan Haji 2024")

# ===================== DESKRIPSI APLIKASI =====================
st.markdown("""
### Analisis Opini Publik dengan IndoBERT
Aplikasi ini menggunakan **transformer model** berbasis IndoBERT untuk memprediksi aspek dan sentimen dari opini publik di media sosial terkait **pelayanan haji tahun 2024**.

Silakan unggah file `.csv` yang berisi kolom `tweet` untuk dianalisis.
""")

# ===================== TAMPILKAN LINK PREDIKSI PER ASPEK =====================
st.header("🔗 Link Prediksi Sentimen per Aspek")
aspek_links = {
    "Pelayanan Petugas": "https://aspek-sentimen-petugas.streamlit.app",
    "Pelayanan Ibadah": "https://aspek-sentimen-ibadah.streamlit.app",
    "Pelayanan Transportasi": "https://aspek-sentimen-transportasi.streamlit.app",
    "Pelayanan Akomodasi": "https://aspek-sentimen-akomodasi.streamlit.app",
    "Pelayanan Konsumsi": "https://aspek-sentimen-konsumsi.streamlit.app",
    "Pelayanan Lainnya": "https://aspek-sentimen-lainnya.streamlit.app"
}
for aspek, url in aspek_links.items():
    st.markdown(f"👉 [{aspek}]({url})", unsafe_allow_html=True)

st.markdown("---")

# ===================== MAIN APP UNTUK WORDCLOUD & UPLOAD =====================
def main():
    uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        if 'tweet' not in df.columns:
            st.error("File harus memiliki kolom 'tweet'.")
            return

        download_kamus()
        kamus = load_kamus()

        st.subheader("Word Cloud dari Tweet")
        with st.spinner("Memproses teks dan membentuk word cloud..."):
            df['cleaned'] = df['tweet'].astype(str).apply(lambda x: preprocess(x, kamus))
            all_text = ' '.join(df['cleaned'].tolist())
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

        st.success("Word cloud berhasil ditampilkan!")

# ===================== JALANKAN APP =====================
if __name__ == '__main__':
    main()
