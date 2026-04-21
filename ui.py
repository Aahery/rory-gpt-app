import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libra AI - RomoHeryGPT", page_icon="⚖️")

# Ambil kunci dari Secrets (Brankas) atau Session State
api_key = st.secrets.get("GOOGLE_API_KEY") or st.session_state.get("api_key", "")

with st.sidebar:
    st.title("⚖️ Libra AI")
    if not api_key:
        st.session_state.api_key = st.text_input("API Key:", type="password")
    else:
        st.success("✅ API Terhubung")

st.title("💬 Chat Room")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Kita coba model paling ringan: gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])

        if p := st.chat_input("Tanya sesuatu..."):
            st.session_state.messages.append({"role": "user", "content": p})
            with st.chat_message("user"): st.markdown(p)
            
            response = model.generate_content(p)
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Waduh, masih ditolak (Error 403). Coba pastikan akun Google Bapak sudah mengaktifkan 'Generative AI' di setelan akun.")
else:
    st.warning("Silakan masukkan API Key di sidebar atau di Secrets.")
