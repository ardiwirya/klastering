# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from google.generativeai import configure, GenerativeModel

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Analisis Klaster Produktivitas Padi",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Judul dan Pengenalan Aplikasi ---
st.markdown("<h1 style='text-align: center; color: #0d9488;'>Analisis Produktivitas Padi - Kabupaten Bireuen</h1>", unsafe_allow_html=True)
st.markdown("""
    Aplikasi ini menyajikan hasil analisis klasterisasi produktivitas padi di 17 kecamatan Kabupaten Bireuen untuk tahun 2022.
    Dengan menggunakan algoritma Fuzzy C-Means, kami mengelompokkan kecamatan ke dalam tiga kategori—Tinggi, Sedang, dan Rendah—
    untuk membantu pemerintah daerah merumuskan kebijakan pertanian yang lebih strategis dan tepat sasaran.
""")

# --- Data Dummy (Ganti dengan data dari SQL Anda) ---
# DataFrame ini berfungsi sebagai pengganti data dari database SQL
data_kecamatan = {
    'name': ["Samalanga", "Sp. Mamplam", "Pandrah", "Jeunieb", "Peulimbang", "Peudada", "Juli", "Jeumpa", "Kota Juang", "Kuala", "Jangka", "Peusangan", "Peusangan Selatan", "Peusangan Sb Krueng", "Makmur", "Gandapura", "Kuta Blang"],
    'cluster': ["Sedang", "Sedang", "Tinggi", "Sedang", "Tinggi", "Rendah", "Tinggi", "Rendah", "Tinggi", "Rendah", "Rendah", "Sedang", "Tinggi", "Tinggi", "Rendah", "Rendah", "Rendah"],
    'Lahan': [0.644, 0.686, 0.068, 0.775, 0.187, 0.427, 0.010, 0.466, 0.034, 0.194, 0.309, 1.000, 0.000, 0.186, 0.346, 0.596, 0.424],
    'Tanam': [0.867, 0.669, 0.197, 1.000, 0.192, 0.490, 0.095, 0.257, 0.107, 0.302, 0.333, 0.764, 0.000, 0.138, 0.348, 0.614, 0.602],
    'Panen': [0.855, 0.710, 0.233, 1.000, 0.294, 0.480, 0.025, 0.359, 0.000, 0.111, 0.392, 0.963, 0.040, 0.169, 0.542, 0.503, 0.558],
    'Produksi': [0.855, 0.677, 0.203, 0.950, 0.255, 0.431, 0.000, 0.369, 0.015, 0.137, 0.438, 1.000, 0.003, 0.119, 0.466, 0.411, 0.542],
    'Produktivitas': [0.688, 0.531, 0.375, 0.513, 0.344, 0.375, 0.188, 0.750, 0.938, 1.000, 1.000, 0.825, 0.000, 0.094, 0.250, 0.125, 0.594],
    'Hujan': [0.223, 0.092, 0.251, 0.187, 0.129, 0.119, 0.102, 1.000, 0.129, 0.202, 0.080, 0.000, 0.069, 0.185, 0.115, 0.122, 0.112],
    'Irigasi': [0.909, 0.671, 0.276, 0.985, 0.446, 0.390, 0.165, 0.673, 0.301, 0.487, 0.564, 1.000, 0.000, 0.000, 0.394, 0.000, 0.580],
    'Bibit': [0.867, 0.669, 0.197, 1.000, 0.192, 0.490, 0.095, 0.257, 0.107, 0.302, 0.333, 0.764, 0.000, 0.138, 0.348, 0.614, 0.602],
    'Pupuk': [0.867, 0.669, 0.197, 1.000, 0.192, 0.490, 0.095, 0.257, 0.107, 0.302, 0.333, 0.764, 0.000, 0.138, 0.348, 0.614, 0.601],
    'OPT': [0.627, 0.000, 0.896, 0.522, 1.000, 0.672, 0.179, 0.776, 0.493, 0.164, 0.179, 0.716, 0.597, 0.358, 0.746, 0.254, 0.388]
}
df = pd.DataFrame(data_kecamatan)

# --- Konfigurasi Gemini API (Ganti dengan kunci API Anda) ---
# Anda harus mendapatkan API Key dari Google AI Studio dan memasangnya di sini.
API_KEY = "AIzaSyC71s3vAu1r28bS2tBW24ybibTIZNmh3qo"
try:
    configure(api_key=API_KEY)
    model = GenerativeModel("gemini-2.5-flash-preview-05-20")
    gemini_configured = True
except Exception as e:
    st.error(f"Gagal mengonfigurasi Gemini API: {e}. Pastikan API Key sudah benar.")
    st.warning("Fitur Analisis Cerdas tidak akan berfungsi tanpa API Key yang valid.")
    gemini_configured = False

# --- Bagian Peta Sebaran (Simulasi) ---
st.header("Peta Sebaran Klaster Produktivitas")
st.write("Visualisasi ini adalah representasi non-interaktif dari sebaran klaster berdasarkan data.")

cluster_colors = {
    'Tinggi': '#0d9488',
    'Sedang': '#0284c7',
    'Rendah': '#f59e0b'
}

cols = st.columns(4)
for i, row in df.iterrows():
    with cols[i % 4]:
        st.markdown(
            f"""
            <div style="background-color: {cluster_colors[row['cluster']]}; color: white; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 10px;">
                <p style="font-weight: bold; margin: 0;">{row['name']}</p>
                <p style="margin: 0; font-size: 0.8em;">{row['cluster']}</p>
            </div>
            """, unsafe_allow_html=True
        )

st.write("---")

# --- Distribusi Klaster dengan Grafik Batang ---
st.header("Distribusi Klaster & Statistik")
cluster_counts = df['cluster'].value_counts().reindex(['Tinggi', 'Sedang', 'Rendah'])
fig = px.bar(
    x=cluster_counts.index,
    y=cluster_counts.values,
    color=cluster_counts.index,
    color_discrete_map=cluster_colors,
    labels={'x': 'Klaster', 'y': 'Jumlah Kecamatan'},
    title='Jumlah Kecamatan per Klaster'
)
fig.update_layout(xaxis_title='Klaster', yaxis_title='Jumlah Kecamatan')
st.plotly_chart(fig, use_container_width=True)

st.write("---")

# --- Analisis Detail Per Kecamatan ---
st.header("Analisis Detail Kecamatan")
st.write("Pilih sebuah kecamatan untuk melihat 'sidik jari' produktivitasnya pada grafik radar.")

kecamatan_list = df['name'].tolist()
selected_kecamatan = st.selectbox("Pilih Kecamatan:", kecamatan_list)

# Filter data untuk kecamatan yang dipilih
selected_data = df[df['name'] == selected_kecamatan].iloc[0]
variables = ['Lahan', 'Tanam', 'Panen', 'Produksi', 'Produktivitas', 'Hujan', 'Irigasi', 'Bibit', 'Pupuk', 'OPT']
radar_data = selected_data[variables].tolist()

# Tampilkan grafik radar
fig_radar = px.line_polar(
    r=radar_data,
    theta=variables,
    line_close=True,
    title=f"Analisis Multivariabel untuk {selected_kecamatan}",
    color_discrete_sequence=[cluster_colors[selected_data['cluster']]]
)
fig_radar.update_traces(fill='toself')
st.plotly_chart(fig_radar, use_container_width=True)

# Tombol dan logika Gemini API
if st.button('✨ Analisis Cerdas ✨'):
    if gemini_configured:
        with st.spinner('Menganalisis data dengan Gemini...'):
            prompt = f"""
            Anda adalah seorang ahli agrikultur dan data saintis. Saya memiliki data klasterisasi produktivitas padi untuk 17 kecamatan di Kabupaten Bireuen, yang dikelompokkan menjadi 3 klaster: Tinggi, Sedang, dan Rendah.
            
            Saya ingin Anda menganalisis data untuk satu kecamatan:
            - Nama Kecamatan: {selected_data['name']}
            - Klaster: {selected_data['cluster']}
            - Nilai Variabel (dinormalisasi 0-1):
            {pd.Series(selected_data[variables].values, index=variables).to_string()}
            
            Berdasarkan data ini, berikan analisis yang komprehensif. Jelaskan secara ringkas posisi kecamatan ini, identifikasi 2-3 variabel terkuat dan 2-3 variabel terlemahnya, dan berikan 2-3 rekomendasi strategis yang spesifik untuk meningkatkan produktivitas padi di kecamatan ini.
            Gunakan bahasa yang profesional dan mudah dipahami, seolah-olah Anda sedang memberikan laporan kepada dinas pertanian setempat.
            """
            try:
                response = model.generate_content(prompt)
                st.subheader("Analisis Gemini:")
                st.info(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memanggil Gemini API: {e}")
    else:
        st.warning("Silakan konfigurasikan API Key Gemini Anda di bagian atas skrip untuk menggunakan fitur ini.")

st.write("---")

# --- Metodologi ---
st.header("Metodologi: Fuzzy C-Means Clustering")
with st.expander("Klik untuk melihat alur proses algoritma"):
    st.write("""
    Proses klasterisasi menggunakan algoritma Fuzzy C-Means, sebuah metode yang memungkinkan satu titik data (kecamatan) menjadi anggota dari beberapa klaster dengan derajat keanggotaan yang berbeda.
    """)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("1. Input Data\n\n10 Variabel dari 17 Kecamatan")
    with col2:
        st.info("2. Normalisasi\n\nMengubah data ke skala 0-1")
    with col3:
        st.info("3. Iterasi FCM\n\nMenghitung pusat & keanggotaan klaster")
    with col4:
        st.info("4. Hasil Klaster\n\nPenentuan klaster akhir")

    st.markdown("""
    #### Parameter Kunci:
    - Jumlah Klaster: 3
    - Eksponen Fuzziness: 2
    - Iterasi Maks: 100
    - Error Min: 0.0001
    """)
