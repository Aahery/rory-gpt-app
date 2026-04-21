import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Libra AI", page_icon="⚖️")

# Ambil kunci dari Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("⚖️ Libra AI - RomoHeryGPT")

if not api_key:
    st.error("Kunci tidak ditemukan di Secrets!")
else:
    try:
        genai.configure(api_key=api_key)
        
        # MENCARI MODEL YANG TERSEDIA SECARA OTOMATIS
        # Kode ini akan mencari model mana saja yang 'boleh' dipakai akun Bapak
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        
        if not models:
            st.error("Google melaporkan: Tidak ada model AI yang tersedia untuk akun ini. Kemungkinan akun Bapak dibatasi oleh Google.")
        else:
            # Gunakan model pertama yang ditemukan (biasanya yang paling stabil)
            selected_model = models[0]
            st.caption(f"Menggunakan mesin: {selected_model}")
            
            model = genai.GenerativeModel(selected_model)
            
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for m in st.session_state.messages:
                with st.chat_message(m["role"]): st.markdown(m["content"])

            if p := st.chat_input("Tes sapaan..."):
                st.session_state.messages.append({"role": "user", "content": p})
                with st.chat_message("user"): st.markdown(p)
                
                response = model.generate_content(p)
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
    except Exception as e:
        st.error(f"Gagal terhubung ke Google: {e}")
