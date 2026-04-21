import streamlit as st
import google.generativeai as genai

# ---------- 1. KONFIGURASI HALAMAN ----------
st.set_page_config(
    page_title="Libra AI - RomoHeryGPT", 
    page_icon="⚖️", 
    layout="wide"
)

# ---------- 2. INISIALISASI MEMORI (SESSION STATE) ----------
# Agar data tidak hilang saat pindah menu
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- 3. SIDEBAR (MENU SAMPING) ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10433/10433048.png", width=60)
    st.title("Libra AI")
    st.subheader("Asisten Cerdas Pak Hery")
    st.write("---")
    
    menu = st.radio("Pilih Menu:", [
        "🏠 Dashboard", 
        "💬 Chat (Teks)", 
        "⚙️ Pengaturan"
    ])
    
    st.write("---")
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- 4. KONTEN HALAMAN ----------

# --- MENU DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard Utama")
    st.markdown(f"""
    Selamat datang di **Libra AI (RomoHeryGPT)**. 
    Aplikasi ini dirancang untuk membantu tugas Bapak di **Biro Hukum** serta menjadi teman belajar bagi keluarga.
    
    **Cara Memulai:**
    1. Pergi ke menu **⚙️ Pengaturan**.
    2. Masukkan API Key Gemini Bapak.
    3. Klik Simpan.
    4. Mulai mengobrol di menu **💬 Chat (Teks)**.
    """)
    st.info("Status Sistem: Online & Siap Melayani.")

# --- MENU PENGATURAN ---
elif menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan Sistem")
    st.write("Masukkan konfigurasi API agar kecerdasan buatan aktif.")
    
    # Input API Key
    user_key = st.text_input(
        "API Key Gemini Bapak:", 
        value=st.session_state.api_key, 
        type="password",
        help="Dapatkan kunci di Google AI Studio"
    )
    
    if st.button("Simpan Pengaturan"):
        st.session_state.api_key = user_key
        st.success("✅ Kunci berhasil disimpan! Silakan menuju menu Chat.")

# --- MENU CHAT ---
elif menu == "💬 Chat (Teks)":
    st.title("💬 Chat Room (Libra AI)")
    
    if not st.session_state.api_key:
        st.warning("⚠️ Bapak belum memasukkan API Key. Silakan ke menu ⚙️ Pengaturan terlebih dahulu.")
    else:
        try:
            # Konfigurasi AI dengan Model Terbaru
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Tampilkan pesan chat sebelumnya
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Input Chat dari User
            if prompt := st.chat_input("Ada yang bisa saya bantu, Pak Hery?"):
                # Simpan & Tampilkan pesan User
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Respon dari AI
                with st.chat_message("assistant"):
                    with st.spinner("Sedang berpikir..."):
                        # Instruksi dasar agar AI tahu identitasnya
                        context = f"Kamu adalah Libra AI, asisten cerdas Pak Hery yang ahli di bidang hukum dan sangat edukatif. Pertanyaan: {prompt}"
                        response = model.generate_content(context)
                        
                        st.markdown(response.text)
                        # Simpan pesan AI
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        
        except Exception as e:
            st.error(f"Terjadi kendala teknis: {e}")
            st.info("Tips: Pastikan API Key benar dan 'google-generativeai' sudah ada di requirements.txt")

# ---------- 5. FOOTER ----------
st.sidebar.caption("© 2026 RomoHery Tech - Central Java")
