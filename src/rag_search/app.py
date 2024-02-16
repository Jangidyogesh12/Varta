import streamlit as st
from Varta import generate_response

st.set_page_config(page_title="Varta", page_icon="🤖")
with st.sidebar:
    st.title("🤖💬 Varta Chatbot")
    selected_model = st.sidebar.selectbox(
        "Choose a model",
        [
            "Mistral(7B)Instruct",
            "Mistral(7B)Instruct v0.2",
            "Mixtral(8x7B)Instruct v0.1",
        ],
        key="selected_model",
    )
    if selected_model == "Mistral(7B)Instruct":
        llm = "mistralai/Mistral-7B-Instruct-v0.1"
    elif selected_model == "Mistral(7B)Instruct v0.2":
        llm = "mistralai/Mistral-7B-Instruct-v0.2"
    elif selected_model == "Mixtral(8x7B)Instruct v0.1":
        llm = "mistralai/Mixtral-8x7B-Instruct-v0.1"


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Chat here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner(text="Thinking..."):
            response = generate_response(prompt, llm)
            full_response = f"{response}"
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": response})
