import streamlit as st
from agent import create_agent

st.set_page_config(page_title="Employee Agent", page_icon="🤖")
st.title("🤖 Agentic Employee Management")

# Initialize agent once
if "agent" not in st.session_state:
    agent, session_manager = create_agent()
    st.session_state.agent = agent
    st.session_state.session_manager = session_manager
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Manage employees...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call agent
    response = st.session_state.agent(user_input)

    assistant_reply = str(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)