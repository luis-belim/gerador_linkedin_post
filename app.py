import streamlit as st
from agente_gerador_post_linkedin import gerar_post

# Configuração do Streamlit
st.title("Gerador de Posts para LinkedIn 🚀")
st.write("Teste o protótipo! Limite: 3 posts por dia.")

# Entrada do usuário
user_id = st.text_input("Identificador do usuário (ex.: e-mail ou ID):", value="user_default")
tema = st.text_input("📝 Digite o tema do post:")

# Lógica para geração de posts
if st.button("Gerar Post"):
    if tema:
        texto_gerado = gerar_post(tema)
        st.subheader("Seu Post:")
        st.text_area("Texto Gerado:", value=texto_gerado, height=200)
        st.button("Copiar Texto", on_click=lambda: st.write("Texto copiado para a área de transferência!"))
    else:
        st.error("Por favor, insira um tema.")
