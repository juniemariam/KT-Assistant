# app/query_engine.py — Gemini RAG with inline image return + CUDA embedding support

import os
import torch
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from PIL import Image
import mimetypes
import glob

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# Set up CUDA-accelerated embedding model using langchain_huggingface format
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load vector DB with embeddings
db = FAISS.load_local(
    "vector_store/faiss_index",
    embedder,
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(search_kwargs={"k": 3})

PROMPT_TEMPLATE = """
You are a helpful engineering assistant. Use the following context to answer the question:

{context}

Question: {question}
Answer:
"""

def find_slack_image(query):
    image_dir = "data/slack_images"
    image_files = glob.glob(f"{image_dir}/*.png") + glob.glob(f"{image_dir}/*.jpg")
    for img in image_files:
        if query.lower() in os.path.basename(img).lower():
            return img
    return None

def ask_llm(question, image_path=None):
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([
        f"[{doc.metadata.get('source', 'unknown')} → {doc.metadata.get('file', '')}]\n{doc.page_content}"
        for doc in docs
    ])
    full_prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    image_used = None
    if not image_path:
        image_path = find_slack_image(question)

    if image_path and os.path.exists(image_path):
        try:
            mime_type, _ = mimetypes.guess_type(image_path)
            if mime_type and mime_type.startswith("image"):
                image = Image.open(image_path)
                image_used = image_path
                response = model.generate_content([full_prompt, image])
                return response.text, image_used
        except Exception as e:
            return f"Image processing error: {str(e)}", None

    try:
        response = model.generate_content(full_prompt)
        return response.text, None
    except Exception as e:
        return f"Gemini error: {str(e)}", None

# Ready for fast CUDA-accelerated embeddings + image explanation
