import os
import streamlit as st
from openai import AzureOpenAI

# Configurações da API
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
API_VERSION = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
)

# Configuração da página
st.set_page_config(page_title="Mandinha – Boas-Vindas do Grupo Mulheres do Brasil", page_icon="🌸", layout="centered")

# Sidebar com links oficiais
st.sidebar.title("Menu de Navegação")
st.sidebar.markdown(
    """
    ### 📌 Atalhos
    - [Página Oficial do Grupo Mulheres do Brasil](https://grupomulheresdobrasil.org.br)
    - [Calendário de Eventos](https://grupomulheresdobrasil.org.br/eventos)
    - [Cadastro de Voluntárias](https://grupomulheresdobrasil.org.br/participe)
    - [Sobre o Projeto](https://grupomulheresdobrasil.org.br/sobre)
    """
)

# Escolha de tema (claro ou escuro)
theme = st.radio("Escolha o tema:", ["Claro", "Escuro"], horizontal=True)

# CSS personalizado
bg_color = "#FCE4EC" if theme == "Claro" else "#2C2C2C"
text_color = "#000" if theme == "Claro" else "#FFF"
user_color = "#1E88E5" if theme == "Claro" else "#90CAF9"
mandinha_color = "#E91E63" if theme == "Claro" else "#F48FB1"

st.markdown(
    f"""
    <style>
        .header {{
            background-color: {bg_color};
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header-logo {{
            flex: 1;
            text-align: right;
        }}
        @media (max-width: 768px) {{
            .header-container {{
                flex-direction: column;
                align-items: center;
            }}
            .header-logo {{
                text-align: center !important;
                margin-top: 10px;
            }}
        }}
        .chat-box {{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
        }}
        .user-msg {{
            color: {user_color};
            font-weight: bold;
        }}
        .mandinha-msg {{
            color: {mandinha_color};
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: {text_color};
        }}
        .footer a {{
            color: {mandinha_color};
            text-decoration: none;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho com descrição
st.markdown(
    f"""
    <div class="header">
        <div class="header-container">
            <div class="header-logo">
                <img src="logo_mulheres_brasil.png" width="120">
            </div>
        </div>
        <div style="text-align: center; margin-top:-60px;">
            <img src="mandinha_avatar.png" width="120" style="margin-bottom:10px;">
            <h1 style="margin-bottom:0; color:{mandinha_color};">Mandinha – Boas-Vindas</h1>
            <h3 style="margin-top:0; color:{text_color};">Grupo Mulheres do Brasil</h3>
            <p style="margin-top:10px; color:{text_color}; font-size:16px;">
                🌸 Mandinha é o chatbot oficial do Grupo Mulheres do Brasil, criado para acolher você e responder todas as suas dúvidas sobre participação, eventos e voluntariado.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Estado da conversa
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é a Mandinha, uma assistente acolhedora do Grupo Mulheres do Brasil."}
    ]

# Entrada do usuário
user_input = st.text_input("Digite sua pergunta:")

col1, col2 = st.columns([1,1])
with col1:
    enviar = st.button("Enviar")
with col2:
    limpar = st.button("Limpar conversa")

if enviar and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model=DEPLOYMENT,
        temperature=0.7,
        max_completion_tokens=500,
    )
    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})

if limpar:
    st.session_state.messages = [
        {"role": "system", "content": "Você é a Mandinha, uma assistente acolhedora do Grupo Mulheres do Brasil."}
    ]

# Exibir mensagens
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-box user-msg'>Você: {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box mandinha-msg'>Mandinha: {msg['content']}</div>", unsafe_allow_html=True)

# Rodapé
st.markdown(
    f"""
    <div class="footer">
        Projeto Mulheres do Brasil © 2025<br>
        Desenvolvido com 💖 para acolher e inspirar.<br>
        <a href="https://grupomulheresdobrasil.org.br" target="_blank">Página Oficial</a> |
        <a href="https://grupomulheresdobrasil.org.br/eventos" target="_blank">Eventos</a> |
        <a href="https://grupomulheresdobrasil.org.br/participe" target="_blank">Cadastro</a> |
        <a href="https://grupomulheresdobrasil.org.br/sobre" target="_blank">Sobre</a>
    </div>
    """,
    unsafe_allow_html=True
)
