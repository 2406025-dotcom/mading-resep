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

# Link gambar estetik untuk tampilan awal web
link_gambar_awal = {
    "Nasi Goreng Kampung": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?q=80&w=300&auto=format&fit=crop",
    "Sate Ayam Madura": "https://images.unsplash.com/photo-1529042410759-befb1204b468?q=80&w=300&auto=format&fit=crop",
    "Soto Ayam Lamongan": "https://images.unsplash.com/photo-1626804475315-9644b37a2f43?q=80&w=300&auto=format&fit=crop",
    "Rendang Daging": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?q=80&w=300&auto=format&fit=crop",
    "Es Cendol": "https://images.unsplash.com/photo-1568254183919-78a4f43a2877?q=80&w=300&auto=format&fit=crop"
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

# Kamus database bumbu rahasia lengkap dengan ikon masing-masing masakan
database_rahasia = {
    "nasi goreng": {
        "ikon": "🍳",
        "bumbu": """• 1 piring penuh Nasi putih dingin
• 3 siung Bawang putih (cincang halus)
• 4 siung Bawang merah (iris tipis)
• 3 tangkai Cabai rawit merah (ulek kasar)
• 2 sendok makan Kecap manis
• 1 sendok teh Garam & Kaldu bubuk
• 1 butir Telur ayam
• 2 potong Ayam suwir (untuk taburan)"""
    },
    "sate ayam": {
        "ikon": "🍢",
        "bumbu": """• 500 gram Daging ayam filet (potong dadu)
• 200 gram Kacang tanah (goreng lalu haluskan)
• 3 siung Bawang putih
• 5 siung Bawang merah
• 4 sendok makan Kecap manis
• 1 potong Gula merah (sisir halus)
• 1 buah Jeruk limau (peras airnya)
• 20 batang Tusuk sate"""
    },
    "soto ayam": {
        "ikon": "🍲",
        "bumbu": """• 500 gram Daging ayam (potong menjadi 4 bagian)
• 50 gram Soun (seduh air panas)
• 50 gram Toge (siangi)
• 2 tangkai Daun bawang (iris halus)
• 2 ruas jari Kunyit (haluskan)
• 2 batang Serai (memarkan)
• 4 lembar Daun jeruk
• 5 potong Krupuk udang (dihaluskan untuk bubuk koya)"""
    },
    "rendang": {
        "ikon": "🥩",
        "bumbu": """• 1000 gram (1 Kg) Daging sapi (potong menjadi 20-24 bagian)
• 1000 ml Santan kental (dari 3 butir kelapa tua)
• 2 batang Serai (memarkan)
• 1 lembar Daun kunyit (ikat simpul)
• 2 buah Asam kandis
• 12 siung Bawang merah (bumbu halus)
• 8 siung Bawang putih (bumbu halus)
• 150 gram Cabai merah keriting (bumbu halus)
• 3 ruas jari Lengkuas (memarkan)"""
    },
    "es cendol": {
        "ikon": "🍹",
        "bumbu": """• 200 gram Cendol/Dawet siap pakai
• 400 ml Santan cair (rebus dengan sedikit garam)
• 200 gram Gula merah (cairkan dengan 100ml air)
• 3 potong Es batu besar (serut/hancurkan)
• 2 lembar Daun pandan (simpulkan)"""
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo! Mau cari resep apa hari ini? Ketik nama makanannya ya (contoh: Nasi Goreng, Sate, Soto, Rendang, Es Cendol)"}]

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
    
    Kunci = user_input.lower()
    resep_ketemu = df[df['RecipeName'].str.lower().str.contains(Kunci, na=False)]
    
    with st.chat_message("assistant"):
        if not resep_ketemu.empty:
            nama = resep_ketemu.iloc[0]['RecipeName']
            kategori = resep_ketemu.iloc[0]['Category']
            deskripsi = resep_ketemu.iloc[0]['Description']
            
            bahan_bumbu = "Takaran bumbu belum dimasukkan."
            ikon_dinamis = "🍽️" # Default jika tidak ketemu
            
            for makanan, data in database_rahasia.items():
                if makanan in Kunci:
                    bahan_bumbu = data["bumbu"]
                    ikon_dinamis = data["ikon"] # <-- Mengambil ikon yang sesuai
                    break
            
            with st.status("🤖 Sedang mengambil detail takaran...", expanded=True) as status:
                time.sleep(0.8)
                status.update(label="Takaran bumbu siap!", state="complete", expanded=False)
            
            # Tampilan output dengan ikon dinamis (Tidak melulu wajan!)
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
                
            respons_gagal = f"Maaf, resep untuk '{user_input}' belum tersedia di database mading kita. Coba ketik resep lain ya!"
            st.error(respons_gagal)
            st.session_state.messages.append({"role": "assistant", "content": respons_gagal})
