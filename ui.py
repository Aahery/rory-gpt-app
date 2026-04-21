import streamlit as st
import google.generativeai as genai

# ---------- 1. KONFIGURASI HALAMAN ----------
st.set_page_config(page_title="Libra AI - RomoHeryGPT", page_icon="⚖️", layout="wide")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- 2. SIDEBAR ----------
with st.sidebar:
    st.title("⚖️ Libra AI")
    st.caption("Asisten Cerdas Pak Hery")
    st.write("---")
    menu = st.radio("Pilih Menu:", ["🏠 Dashboard", "💬 Chat (Teks)", "⚙️ Pengaturan"])
    if st.button("🗑️ Hapus Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- 3. KONTEN ----------
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.info("Selamat datang Pak Hery. Jika muncul error 403, pastikan API Key sudah benar dari Google AI Studio.")

elif menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan")
    user_key = st.text_input("API Key Gemini:", value=st.session_state.api_key, type="password")
    if st.button("Simpan Pengaturan"):
        st.session_state.api_key = user_key
        st.success("✅ Kunci disimpan!")

elif menu == "💬 Chat (Teks)":
    st.title("💬 Chat Room")
    if not st.session_state.api_key:
        st.warning("⚠️ Masukkan API Key di Pengaturan dulu, Pak.")
    else:
        try:
            genai.configure(api_key=st.session_state.api_key)
            # Menggunakan model flash-latest yang lebih stabil untuk API Key baru
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ada yang bisa saya bantu?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Berpikir..."):
                        # Tambahkan penanganan error spesifik
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "403" in str(e):
                st.error("Error 403: Kunci Bapak ditolak. Solusi: Coba buat API Key baru di Google AI Studio dan pastikan pilih 'Gemini API' bukan yang lain.")
            else:
                st.error(f"Terjadi kendala: {e}")
