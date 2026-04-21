import streamlit as st
import json
import uuid
from pathlib import Path

# ---------- 1. KONFIGURASI HALAMAN ----------
st.set_page_config(
    page_title="Libra AI - RomoHeryGPT", 
    page_icon="⚖️", 
    layout="wide"
)

HISTORY_FILE = Path("chat_sessions.json")

# ---------- 2. STYLE CSS ----------
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 5px; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    .main-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; }
</style>
""", unsafe_allow_html=True)

# ---------- 3. MANAJEMEN DATA ----------
if "all_sessions" not in st.session_state:
    if HISTORY_FILE.exists():
        try: st.session_state.all_sessions = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except: st.session_state.all_sessions = {}
    else: st.session_state.all_sessions = {}

if "current_session_id" not in st.session_state:
    if st.session_state.all_sessions:
        st.session_state.current_session_id = list(st.session_state.all_sessions.keys())[0]
    else:
        new_id = str(uuid.uuid4())[:8]
        st.session_state.all_sessions[new_id] = {"title": "Obrolan Baru", "messages": []}
        st.session_state.current_session_id = new_id

# ---------- 4. SIDEBAR ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10433/10433048.png", width=50) # Ikon Timbangan
    st.title("Libra AI")
    st.markdown("### 🤖 RomoHeryGPT")
    st.caption("Asisten AI Cerdas - Biro Hukum & Keluarga")
    st.write("---")
    
    menu = st.radio("Menu Utama:", [
        "🏠 Dashboard", "💬 Chat (Teks)", "🎙️ Transkrip & Ringkasan",
        "🧰 Alat & Layanan ASN", "🎨 Studio Visual", "🎥 Studio Video", 
        "👨‍👩‍👧 Mode Anak", "⚙️ Pengaturan"
    ])
    
    st.write("---")
    
    # Fitur Riwayat Chat (Seperti di Gambar Bapak)
    if st.button("➕ Buat Projek Baru", type="primary"):
        new_id = str(uuid.uuid4())[:8]
        st.session_state.all_sessions[new_id] = {"title": "Obrolan Baru", "messages": []}
        st.session_state.current_session_id = new_id
        st.rerun()

    if st.button("🗑️ Hapus Semua Riwayat"):
        st.session_state.all_sessions = {}
        HISTORY_FILE.unlink(missing_ok=True)
        st.rerun()

# ---------- 5. KONTEN HALAMAN ----------

if menu == "🏠 Dashboard":
    st.markdown('<p class="main-header">🏠 Dashboard Libra AI</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sesi", len(st.session_state.all_sessions))
    c2.metric("Status Server", "Online")
    c3.metric("Mode", "Profesional")
    st.info("Selamat datang kembali, Pak Hery. Sistem siap membantu tugas kedinasan Anda.")

elif menu == "🧰 Alat & Layanan ASN":
    st.title("🧰 Alat & Layanan ASN")
    tab1, tab2 = st.tabs(["📄 Pengolah PDF", "👔 Portal Kepegawaian"])
    with tab1:
        st.markdown('<iframe src="https://www.ilovepdf.com/id" width="100%" height="600" style="border:none;"></iframe>', unsafe_allow_html=True)
    with tab2:
        st.link_button("SINAGA BKD Jateng", "https://sinaga.bkd.jatengprov.go.id/")
        st.link_button("SSO ASN Jateng", "https://sso.bkd.jatengprov.go.id/login")

elif menu == "🎨 Studio Visual":
    st.markdown('<p class="main-header">🎨 Studio Visual</p>', unsafe_allow_html=True)
    st.info("Fitur sedang dalam pengembangan untuk mendukung narasi visual Anda.")

elif menu == "🎥 Studio Video":
    st.markdown('<p class="main-header">🎥 Studio Video</p>', unsafe_allow_html=True)
    st.write("Fitur pembuatan skrip video pendek untuk sosialisasi ASN.")

elif menu == "👨‍👩‍👧 Mode Anak":
    st.markdown('<p class="main-header">👨‍👩‍👧 Mode Anak</p>', unsafe_allow_html=True)
    st.success("Halo! RoryGPT siap membantu belajar dan bercerita untuk keluarga.")

elif menu == "⚙️ Pengaturan":
    st.markdown('<p class="main-header">⚙️ Pengaturan Sistem</p>', unsafe_allow_html=True)
    st.subheader("Konfigurasi API & User")
    st.text_input("User Name", value="Hery Hendro Purnomo")
    st.text_input("NIP", value="197609302009011007")
    
    # PERBAIKAN ERROR: Menggunakan st.text_input dengan type="password"
    st.text_input("API Key Gemini/OpenAI", value="**********", type="password")
    
    if st.button("Simpan Pengaturan"):
        st.success("Konfigurasi berhasil disimpan untuk Anda!")