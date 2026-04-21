import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libra AI - RomoHeryGPT", page_icon="⚖️")

if "api_key" not in st.session_state: st.session_state.api_key = ""
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.title("⚖️ Libra AI")
    menu = st.radio("Menu:", ["🏠 Dashboard", "💬 Chat", "⚙️ Pengaturan"])

if menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan")
    st.session_state.api_key = st.text_input("Tempel API Key Baru Bapak:", value=st.session_state.api_key, type="password")
    if st.button("Simpan"):
        st.success("Kunci berhasil diperbarui!")

elif menu == "💬 Chat":
    st.title("💬 Chat Room")
    if not st.session_state.api_key:
        st.warning("Silakan masukkan API Key di Pengaturan.")
    else:
        try:
            genai.configure(api_key=st.session_state.api_key)
            # Menggunakan model paling standar agar tidak ditolak server
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            for m in st.session_state.messages:
                with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("Tanya sesuatu, Pak..."):
                st.session_state.messages.append({"role": "user", "content": p})
                with st.chat_message("user"): st.markdown(p)
                
                with st.chat_message("assistant"):
                    # Tambahkan penanganan error yang lebih informatif
                    r = model.generate_content(p)
                    st.markdown(r.text)
                    st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            st.error(f"Akses Ditolak (403): Silakan buat API Key baru di Google AI Studio dan pastikan Bapak memilih 'Create API key in NEW project'.")

else:
    st.title("🏠 Dashboard")
    st.write("Selamat datang, Pak Hery!")
