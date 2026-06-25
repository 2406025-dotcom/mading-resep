import streamlit as st
import pandas as pd

# Set konfigurasi halaman
st.set_page_config(page_title="Mading Resep Makanan Indonesia", page_icon="🍳", layout="centered")

# Judul Utama
st.title("🍳 Mading Resep Makanan Indonesia")
st.write("Selamat datang di mading resep masakan praktis pilihan!")

# Load Data CSV dari GitHub
csv_url = "https://raw.githubusercontent.com/2406025-dotcom/mading-resep/main/Indonesian_Food_Recipes.csv"

try:
    df = pd.read_csv(csv_url)
    
    st.subheader("📋 Daftar Resep yang Tersedia")
    # Menampilkan nama resep dalam bentuk bullet points
    for nama_resep in df['RecipeName'].unique():
        st.write(f"- **{nama_resep}**")
        
    st.write("---")
    
    # Fitur Chatbot Asisten Resep
    st.subheader("💬 Chatbot Asisten Resep")
    st.write("Tanyakan resep makanan yang ada di daftar atas!")
    
    # Input dari pengguna
    user_input = st.text_input("Ketik nama resep di sini (contoh: Sop ayam, Ayam Geprek):")
    
    if user_input:
        # Cari resep yang cocok (tidak sensitif huruf besar/kecil)
        resep_ketemu = df[df['RecipeName'].str.lower() == user_input.lower()]
        
        if not resep_ketemu.empty:
            nama = resep_ketemu.iloc[0]['RecipeName']
            bahan = resep_ketemu.iloc[0]['Ingredients'].replace('--', '\n- ')
            cara = resep_ketemu.iloc[0]['Instructions']
            
            st.success(f"### 🎉 Resep {nama} Ditemukan!")
            
            st.write("### 🛒 Bahan-bahan:")
            st.write(f"- {bahan}")
            
            st.write("### 🍳 Cara Membuat:")
            st.write(cara)
        else:
            st.error(f"Maaf, resep untuk '{user_input}' belum tersedia atau salah ketik. Coba lihat daftar di atas ya!")

except Exception as e:
    st.error("Gagal memuat data resep. Pastikan file Indonesian_Food_Recipes.csv sudah benar di GitHub.")
