import streamlit as st
import pandas as pd
import time

st.title("Mading Resep Makanan Indonesia")

# 1. Membaca data resep utama
df = pd.read_csv("Indonesian_Food_Recipes.csv")

st.write("Halo! Di bawah ini adalah jumlah data resep kita:")
st.write(f"Total resep yang ada di buku: {df.shape[0]} resep")

# MENAMPILKAN GAMBAR SESUAI JUDUL DI HALAMAN UTAMA (Awal Web)
st.write("### 📸 Galeri Visual Masakan")
kolom_gambar = st.columns(3)

# Link gambar estetik disesuaikan dengan menu AYAM asli di database kamu
link_gambar_awal = {
    "Sop Ayam Lezat": "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=300&auto=format&fit=crop",
    "Ayam Geprek Pedas": "https://images.unsplash.com/photo-1626132647523-66f5bf380027?q=80&w=300&auto=format&fit=crop",
    "Ayam Garang Asem": "https://images.unsplash.com/photo-1598515214211-89d3c73ae83b?q=80&w=300&auto=format&fit=crop"
}

# Loop untuk nampilin gambar masakan di awal sesuai judul resepnya
for i, (nama_resep, url_foto) in enumerate(link_gambar_awal.items()):
    with kolom_gambar[i % 3]:
        st.image(url_foto, caption=nama_resep, use_container_width=True)

st.write("#### 📊 Tabel Data Terstruktur")
st.dataframe(df)

st.write("---")

# 2. FITUR CHATBOT DENGAN IKON & TAKARAN DINAMIS
st.subheader("🤖 Chatbot Asisten Resep")
st.write("Tanyakan resep makanan yang kamu inginkan di bawah ini!")

# Kamus bumbu rahasia DIUBAH TOTAL sesuai dengan isi file CSV asli kamu!
database_rahasia = {
    "sop ayam": {
        "ikon": "🍲",
        "bumbu": """• 500 gram Daging Ayam (potong dadu)
• 2 buah Wortel (potong bulat)
• 2 buah Kentang (potong dadu)
• 3 siung Bawang putih & Bawang merah (tumis)
• 1 batang Daun bawang & Seledri
• 1 sendok teh Garam, Merica, dan Pala bubuk"""
    },
    "geprek": {
        "ikon": "🌶️",
        "bumbu": """• 500 gram Ayam goreng tepung (crispy)
• 10 buah Cabai rawit merah (sesuai selera)
• 3 siung Bawang putih
• 1/2 sendok teh Garam & Penyedap rasa
• 2 sendok makan Minyak goreng panas (untuk menyiram sambal)"""
    },
    "suwir": {
        "ikon": "🍗",
        "bumbu": """• 500 gram Dada ayam (rebus lalu suwir-suwir)
• 5 siung Bawang merah & 3 siung Bawang putih
• 3 buah Cabai merah keriting
• 2 lembar Daun jeruk & 1 batang Serai
• 1 sendok makan Kecap manis & Garam secukupnya"""
    },
    "nugget": {
        "ikon": "🧆",
        "bumbu": """• 300 gram Daging ayam giling
• 2 butir Telur ayam
• 3 sendok makan Tepung tapioka / Terigu
• 2 siung Bawang putih (haluskan)
• 100 gram Tepung roti/panir (untuk baluran luar)"""
    },
    "asem": {
        "ikon": "🍲",
        "bumbu": """• 500 gram Daging ayam (potong kecil)
• 5 buah Belimbing wuluh (potong bulat)
• 2 buah Tomat hijau
• 4 butir Bawang merah & 3 siung Bawang putih (iris)
• 5 buah Cabai rawit utuh
• 65 ml Santan kental & Daun pisang (untuk membungkus)"""
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo! Mau cari resep apa hari ini? Ketik nama makanannya ya (contoh: Sop ayam, Ayam Geprek, Ayam suwir, Nugget, Garang Asem)"}]

for msg in st.session_state.messages:
    if isinstance(msg["content"], dict):
        with st.chat_message(msg["role"]):
            st.success(f"### {msg['content']['ikon']} {msg['content']['nama']}")
            st.caption(f"📂 Kategori: {msg['content']['kategori']}")
            st.write(f"ℹ️ **Deskripsi:** {msg['content']['deskripsi']}")
            with st.expander("🌶️ Detail Takaran Bumbu & Bahan (Klik di sini)"):
                st.write(msg["content"]["bumbu"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("Ketik pesan kamu di sini..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    Kunci = user_input.lower().strip()
    resep_ketemu = df[df['RecipeName'].str.lower().str.contains(Kunci, na=False)]
    
    with st.chat_message("assistant"):
        if not resep_ketemu.empty:
            row_data = resep_ketemu.iloc[0]
            nama = row_data['RecipeName']
            
            kategori = row_data.get('Category', 'Olahan Ayam Nusantara')
            
            if 'Description' in row_data:
                deskripsi = row_data['Description']
            elif 'Ingredients' in row_data:
                deskripsi = str(row_data['Ingredients']).replace('--', ', ')
            else:
                deskripsi = "Resep hidangan ayam lezat tradisional khas Indonesia."
            
            bahan_bumbu = "Takaran bumbu tambahan otomatis diambil dari sistem mading."
            ikon_dinamis = "🍽️" 
            
            for makanan, data in database_rahasia.items():
                if makanan in Kunci or makanan in nama.lower():
                    bahan_bumbu = data["bumbu"]
                    ikon_dinamis = data["ikon"] 
                    break
            
            with st.status("🤖 Sedang mengambil detail takaran...", expanded=True) as status:
                time.sleep(0.8)
                status.update(label="Takaran bumbu siap!", state="complete", expanded=False)
            
            st.success(f"### {ikon_dinamis} {nama}")
            st.caption(f"📂 Kategori: {kategori}")
            st.write(f"ℹ️ **Deskripsi:** {deskripsi}")
            with st.expander("🌶️ Detail Takaran Bumbu & Bahan (Klik di sini)"):
                st.write(bahan_bumbu)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": {"nama": nama, "kategori": kategori, "deskripsi": deskripsi, "bumbu": bahan_bumbu, "ikon": ikon_dinamis}
            })
        else:
            with st.status("🤖 Mencari di database...", expanded=True) as status:
                time.sleep(0.5)
                status.update(label="Pencarian selesai", state="error", expanded=False)
                
            respons_gagal = f"Maaf, resep untuk '{user_input}' belum tersedia di database mading kita. Coba lihat daftar tabel di atas ya!"
            st.error(respons_gagal)
            st.session_state.messages.append({"role": "assistant", "content": respons_gagal})
