# UI for the RAG KT Assistants
import streamlit as st
from app.query_engine import ask_llm
import os

st.title("Smart KT Assistant")

question = st.text_input("Ask a question about your repo or system")

if st.button("Ask"):
    with st.spinner("Thinking..."):
        result = ask_llm(question)

        # Confirm it's a tuple
        if isinstance(result, tuple):
            answer, image_path = result
        else:
            answer = result
            image_path = None

        if image_path:
            st.image(image_path, caption=f"Referenced Image: {os.path.basename(image_path)}")
        st.markdown(answer)
