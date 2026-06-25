import streamlit as st
import pandas as pd

# Konfigurasi halaman agar rapi
st.set_page_config(page_title="Mading Resep & Chatbot", page_icon="🍳", layout="wide")

# URL Data CSV dari GitHub kamu
csv_url = "https://raw.githubusercontent.com/2406025-dotcom/mading-resep/main/Indonesian_Food_Recipes.csv"

try:
    # Membaca data CSV
    df = pd.read_csv(csv_url)
    
    # 1. TAMPILAN AWAL: Tabel Data Menu Mading Resep
    st.write("### 📋 Daftar Menu Mading Resep")
    
    # Membuat format tabel agar mirip tampilan awal
    tabel_data = df[['RecipeName', 'Ingredients']].copy()
    tabel_data.columns = ['Nama Resep', 'Bahan Utama']
    
    # Menampilkan tabel data di halaman utama
    st.dataframe(tabel_data, use_container_width=True)
    
    st.write("---")
    
    # 2. TAMPILAN AWAL: Chatbot Asisten Resep Berwarna Orange
    st.write("### 🤖 Chatbot Asisten Resep")
    st.write("Tanyakan resep makanan yang kamu inginkan di bawah ini!")
    
    # Kotak Sambutan Chatbot (Warna Orange khas Streamlit)
    st.info("🤖 **Halo! Mau cari resep apa hari ini?** Ketik nama makanannya ya (contoh: Sop ayam, Ayam Geprek, Ayam suwir)")
    
    # Kolom Input Chat
    user_input = st.text_input("Ketik pesan kamu di sini...", placeholder="Misal: Sop ayam")
    
    if user_input:
        # Tampilkan chat bubble dari user
        st.chat_message("user").write(user_input)
        
        # Cari resep berdasarkan input user
        resep_ketemu = df[df['RecipeName'].str.lower() == user_input.lower()]
        
        if not resep_ketemu.empty:
            # Mengambil data dari CSV kamu yang aslinya tidak ada kolom 'Description'
            nama = resep_ketemu.iloc[0]['RecipeName']
            bahan_list = resep_ketemu.iloc[0]['Ingredients'].replace('--', '\n- ')
            langkah_masak = resep_ketemu.iloc[0]['Instructions']
            
            # Tampilkan respon chatbot jika ketemu
            with st.chat_message("assistant"):
                st.success(f"🎉 **Resep {nama} Ditemukan!**")
                st.write("### 🛒 Bahan-bahan:")
                st.write(f"- {bahan_list}")
                st.write("### 🍳 Cara Membuat:")
                st.write(langkah_masak)
        else:
            # Tampilkan respon chatbot jika tidak ketemu
            with st.chat_message("assistant"):
                st.error(f"⚠️ Maaf, resep untuk '{user_input}' belum tersedia di database mading kita. Coba ketik resep lain ya!")

except Exception as e:
    st.error("Gagal memuat data mading resep. Pastikan file CSV kamu ada di GitHub.")
