import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Libra AI", page_icon="⚖️")

# Inisialisasi API Key di Session State agar tidak hilang saat pindah menu
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("⚖️ Libra AI")
    menu = st.radio("Pilih Menu:", ["⚙️ Pengaturan", "💬 Chat (Teks)"])

# Menu Pengaturan
if menu == "⚙️ Pengaturan":
    st.title("⚙️ Pengaturan")
    # Input ini akan langsung memperbarui session_state
    st.session_state.api_key = st.text_input("Tempel API Key Gemini Bapak di sini:", value=st.session_state.api_key, type="password")
    if st.button("Simpan Kunci"):
        st.success("Kunci berhasil dikunci di sistem!")

# Menu Chat
elif menu == "💬 Chat (Teks)":
    st.title("💬 Chat Room")
    
    if not st.session_state.api_key:
        st.warning("⚠️ Kunci belum ada. Silakan ke menu Pengaturan dulu ya, Pak.")
    else:
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Tampilkan riwayat chat
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Input chat
            if prompt := st.chat_input("Ada yang bisa saya bantu, Pak Hery?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sepertinya ada masalah: {e}")
