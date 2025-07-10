# embed the documents
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

with open("data/chunks.jsonl") as f:
    chunks = [json.loads(line) for line in f]

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

documents = []
for chunk in chunks:
    splits = splitter.create_documents([chunk["content"]])
    for doc in splits:
        doc.metadata = {"source": chunk["source"], "file": chunk["file"]}
        documents.append(doc)

db = FAISS.from_documents(documents, embedder)
db.save_local("vector_store/faiss_index")
print(f"Embedded and saved {len(documents)} chunks to vector DB")
