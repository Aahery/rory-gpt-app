import streamlit as st
import json
import uuid
from pathlib import Path
import google.generativeai as genai

# ---------- 1. KONFIGURASI HALAMAN ----------
st.set_page_config(page_title="Libra AI - RomoHeryGPT", page_icon="⚖️", layout="wide")

HISTORY_FILE = Path("chat_sessions.json")

# ---------- 2. MANAJEMEN DATA ----------
if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = {}

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# ---------- 3. SIDEBAR ----------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10433/10433048.png", width=50)
    st.title("Libra AI")
    st.caption("Asisten AI Cerdas - Biro Hukum")
    st.write("---")
    menu = st.radio("Menu Utama:", ["🏠 Dashboard", "💬 Chat (Teks)", "⚙️ Pengaturan"])

# ---------- 4. KONTEN HALAMAN ----------
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard Libra AI")
    st.info(f"Selamat datang, Pak Hery Hendro Purnomo. Silakan ke menu Pengaturan untuk memasukkan API Key, lalu mulai Chat.")

elif menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan")
    st.session_state.api_key = st.text_input("Masukkan API Key Gemini Bapak:", value=st.session_state.api_key, type="password")
    if st.button("Simpan"):
        st.success("API Key berhasil disimpan!")

elif menu == "💬 Chat (Teks)":
    st.title("💬 Chat Room")
    if not st.session_state.api_key:
        st.warning("⚠️ Bapak belum memasukkan API Key di menu Pengaturan.")
    else:
        genai.configure(api_key=st.session_state.api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ketik pesan di sini, Pak..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
