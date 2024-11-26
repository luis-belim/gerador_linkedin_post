import streamlit as st
from datetime import datetime
import json
import sys

# Adiciona o diretório 'sample_data' ao sys.path para importar o agente
sys.path.append('./sample_data')

# Importa o agente do arquivo localizado na pasta sample_data
from agente_gerador_post_linkedin import agente

# Arquivo para armazenar as requisições dos usuários
usage_file = "usage_data.json"

# Função para carregar dados de uso
def load_usage():
    try:
        with open(usage_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar dados de uso
def save_usage(data):
    with open(usage_file, "w") as f:
        json.dump(data, f)

# Função para verificar se o limite foi atingido
def can_generate(user_id):
    usage_data = load_usage()
    today = datetime.now().strftime("%Y-%m-%d")

    # Verifica o uso do dia atual
    if user_id not in usage_data:
        usage_data[user_id] = {today: 0}
    if today not in usage_data[user_id]:
        usage_data[user_id][today] = 0

    # Permite se ainda não atingiu o limite de 3
    if usage_data[user_id][today] < 3:
        usage_data[user_id][today] += 1
        save_usage(usage_data)
        return True, 3 - usage_data[user_id][today]  # Retorna quantas tentativas restam
    else:
        return False, 0

# Interface Streamlit
def main():
    st.title("Gerador de Posts para LinkedIn 🚀")
    st.write("Teste o protótipo! Limite: 3 posts por dia.")

    # Simula o ID do usuário
    user_id = st.text_input("Identificador do usuário (ex.: e-mail ou ID):", "user_default")

    if st.button("Verificar Limite"):
        allowed, remaining = can_generate(user_id)
        if allowed:
            st.success(f"Você ainda pode gerar {remaining} posts hoje!")
        else:
            st.error("Você atingiu o limite de 3 posts para hoje. Tente novamente amanhã!")

    tema = st.text_input("📌 Digite o tema do post:")
    if st.button("Gerar Post"):
        if tema:
            allowed, remaining = can_generate(user_id)
            if allowed:
                # Usa o agente importado para gerar o post
                resultado = agente.gerar_post(tema)
                st.subheader("Seu Post:")
                st.write(resultado)

                # Adiciona uma área de texto com o conteúdo gerado
                st.text_area("Texto Gerado:", resultado, height=150)

                # Adiciona um botão para copiar o texto gerado
                st.download_button(
                    label="Copiar Texto",
                    data=resultado,
                    file_name="post_linkedin.txt",
                    mime="text/plain",
                )

                st.success(f"Você ainda pode gerar {remaining} posts hoje!")
            else:
                st.error("Você atingiu o limite de 3 posts para hoje. Tente novamente amanhã!")
        else:
            st.error("Por favor, insira um tema.")

if __name__ == "__main__":
    main()
