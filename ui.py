import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libra AI", page_icon="⚖️")

# Ambil kunci dari brankas Rahasia (Secrets)
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("⚖️ Libra AI - Cek Koneksi")

if not api_key:
    st.error("Kunci belum ada di 'Secrets' Streamlit, Pak.")
else:
    try:
        genai.configure(api_key=api_key)
        
        # MENAMPILKAN DAFTAR MODEL YANG TERSEDIA
        # Ini untuk mengecek model apa yang dibolehkan untuk akun Bapak
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        
        st.write("Model yang tersedia untuk akun Bapak:")
        st.json(available_models)
        
        # Coba gunakan model pertama yang tersedia secara otomatis
        selected_model = available_models[0] if available_models else 'models/gemini-1.5-flash'
        model = genai.GenerativeModel(selected_model)
        
        prompt = st.chat_input("Tes sapaan di sini, Pak...")
        if prompt:
            st.chat_message("user").write(prompt)
            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)
            
    except Exception as e:
        st.error(f"Pesan dari Google: {str(e)}")
        if "403" in str(e):
            st.info("Saran: Gunakan akun Gmail berbeda untuk membuat API Key baru di AI Studio.")
