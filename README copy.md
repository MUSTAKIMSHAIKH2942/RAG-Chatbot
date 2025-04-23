### README.md
# RAG Chatbot (Flask + Hugging Face + FAISS)

This is a lightweight Retrieval-Augmented Generation chatbot using only free resources:

- Hugging Face transformers (Flan-T5)
- SentenceTransformers (MiniLM)
- FAISS for fast document retrieval
- Flask API for interaction

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Test the Chatbot
```bash
curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the project about?"}'

## Folder Structure
```
rag_chatbot/
├── app.py
├── rag.py
├── requirements.txt
├── README.md
├── data/
│   └── knowledge.txt
├── vector_store/
│   └── faiss_index, faiss_index_docs.pkl
├── utils/
│   └── text_loader.py