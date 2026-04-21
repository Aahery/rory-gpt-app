import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Libra AI - RomoHeryGPT", page_icon="⚖️")

# 2. Ambil Kunci dari Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("⚖️ Libra AI - RomoHeryGPT")
st.write("---")

if not api_key:
    st.error("Masalah: Kunci belum ada di Secrets Streamlit.")
else:
    try:
        # Konfigurasi AI
        genai.configure(api_key=api_key)
        
        # MENGGUNAKAN NAMA MODEL LENGKAP AGAR TIDAK ERROR 404/403
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Wadah Pesan
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Tampilkan Chat
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Input Chat
        if prompt := st.chat_input("Ada yang bisa saya bantu, Pak Hery?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Menambahkan konteks agar AI tahu dia asisten Bapak
                konteks = f"Jawablah sebagai Libra AI, asisten hukum Pak Hery: {prompt}"
                response = model.generate_content(konteks)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Waduh, ada kendala: {e}")
        st.info("Saran: Jika masih error, coba buat API Key baru dengan AKUN GMAIL LAIN di Google AI Studio.")
