import streamlit as st
import sqlite3

if sqlite3.sqlite_version_info < (3, 35, 0):
    raise RuntimeError("SQLite 3.35.0 ou superior é necessário. Atualize sua versão.")

import os
from agente_gerador_post_linkedin import gerar_post  # Importa o agente que gera posts

# Configura as chaves API usando os Secrets do Streamlit
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerador de Posts para LinkedIn", page_icon="🚀")

# Função para gerar o post e exibir na interface
def gerar_post_streamlit():
    # Identificador do usuário
    user_id = st.text_input("Identificador do usuário (ex.: e-mail ou ID):", value="user_default")

    # Verificar limite de posts por usuário
    if st.button("Verificar Limite"):
        # Aqui você pode implementar uma lógica para verificar o limite de posts por dia
        st.success("Você ainda pode gerar 3 posts hoje!")

    # Input para o tema do post
    tema = st.text_input("📌 Digite o tema do post:", value="")

    # Botão para gerar o post
    if st.button("Gerar Post"):
        if tema.strip():
            try:
                # Gera o post usando o agente
                post_gerado = gerar_post(tema)
                st.success("✨ Post criado com sucesso!")

                # Exibe o post gerado
                st.subheader("Seu Post:")
                st.write(post_gerado)

                # Botão para copiar o texto gerado
                st.code(post_gerado, language="text")
                st.button("Copiar Texto", on_click=lambda: st.write("Texto copiado!"))  # Simula botão de cópia

            except Exception as e:
                st.error(f"Erro ao gerar o post: {e}")
        else:
            st.error("Por favor, insira um tema para o post.")

# Rodar a função principal
st.title("Gerador de Posts para LinkedIn 🚀")
st.caption("Teste o protótipo! Limite: 3 posts por dia.")
gerar_post_streamlit()
