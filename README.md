# Smart Knowledge Transfer Assistant

A scalable, enterprise-ready RAG (Retrieval-Augmented Generation) platform designed to accelerate onboarding and engineering productivity. This multimodal assistant allows developers to ask questions about their codebase, documentation, Slack threads, Confluence pages, and screenshots—all from a single unified interface.

---

## Features

- **Multimodal RAG Architecture**: Combines text and image understanding via LangChain, FAISS, and Gemini Pro.
- **Live Slack & Confluence Integration**: Continuously ingests and indexes Slack messages, Confluence pages, and repository content.
- **Vision-Aware Querying**: Supports screenshot-based answers using OCR and Gemini Vision models.
- **Contextual Responses**: Displays answers with reference to source (code/Slack/image/Confluence).
- **Streamlit UI**: Intuitive web interface to interact with the assistant.
- **GPU Support**: CUDA-compatible backend built for GKE GPU node pools.

---

## Tech Stack

| Layer        | Tech                                          |
|--------------|-----------------------------------------------|
| Backend      | Python, FastAPI, LangChain, FAISS             |
| Frontend     | Streamlit                                     |
| ML Models    | Gemini 1.5 Pro (Vision + Text), SBERT         |
| Storage      | ChromaDB / FAISS (Vector Store)               |
| Cloud        | Google Cloud Platform (GKE, Container Registry) |
| DevOps       | Docker, Kubernetes, GitHub Actions            |
| Integrations | Slack API, Confluence API                     |

---


---

## 🛠 Setup

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.backend.txt

```
2. Embed Documents

```bash
python ingest/embed_docs.py
```
3. Push Docker images
```bash
docker push juniemariam/kt-backend:latest
docker push juniemariam/kt-frontend:latest
```

5. Apply K8s YAMLs
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/ui-deployment.yaml
kubectl apply -f k8s/ui-service.yaml
```
