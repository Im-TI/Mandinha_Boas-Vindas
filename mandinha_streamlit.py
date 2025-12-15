
import os
import streamlit as st
from openai import AzureOpenAI

API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
API_VERSION = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
)

st.set_page_config(page_title="Mandinha Chatbot", page_icon="🌸")

# Avatar
st.image("mandinha_avatar.png", width=120)  # coloque sua imagem na pasta

st.title("Mandinha - Grupo Mulheres do Brasil")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é a Mandinha, uma assistente acolhedora do Grupo Mulheres do Brasil."}
    ]

user_input = st.text_input("Digite sua pergunta:")

if st.button("Enviar") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model=DEPLOYMENT,
        temperature=0.7,
        max_completion_tokens=500,
    )
    answer = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"**Você:** {msg['content']}")
    else:
        st.markdown(f"**Mandinha:** {msg['content']}")
