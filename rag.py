import os
import faiss
import pickle
import hashlib
from pathlib import Path
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from utils.text_loader import load_documents

class RAGPipeline:
    def __init__(self):
        print("Initializing RAG pipeline... (This may take a moment)")

        base_dir = Path(__file__).parent.resolve()
        self.vector_store_dir = base_dir / "vector_store"
        self.index_path = self.vector_store_dir / "faiss_index"
        self.docs_path = self.vector_store_dir / "faiss_index_docs.pkl"
        self.checksum_path = self.vector_store_dir / "checksum.sha256"

        # ✅ Auto-create directory
        os.makedirs(self.vector_store_dir, exist_ok=True)

        self.initialize_models()
        self.initialize_index()

    def initialize_models(self):
        print("🔍 Loading embedding model...")
        self.embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

        print("💬 Loading QA model...")
        self.qa_model = pipeline("text2text-generation", model="google/flan-t5-base", device=-1)

    def initialize_index(self):
        for attempt in range(2):
            try:
                if self.index_path.exists() and self.docs_path.exists():
                    print("📦 Loading saved FAISS index and docs...")
                    self.index = faiss.read_index(str(self.index_path))
                    with open(self.docs_path, 'rb') as f:
                        self.docs = pickle.load(f)
                    return

                print("🛠️ No valid index found. Creating new index...")
                self._build_and_save_index()
                return

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                self._cleanup_files()

        raise RuntimeError("❌ Failed to initialize FAISS index after retries.")

    def _build_and_save_index(self):
        print("📄 Loading documents...")
        self.docs = load_documents("data/knowledge.txt")
        if not self.docs:
            raise ValueError("No documents loaded from knowledge.txt")

        print("🧠 Generating embeddings...")
        embeddings = self.embedder.encode(self.docs, show_progress_bar=True)

        print("📊 Creating FAISS index...")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        self._save_index()

    def _save_index(self):
        try:
            print("💾 Saving index...")

            os.makedirs(self.vector_store_dir, exist_ok=True)

            faiss.write_index(self.index, str(self.index_path))
            with open(self.docs_path, 'wb') as f:
                pickle.dump(self.docs, f)

            with open(self.checksum_path, 'w') as f:
                f.write(self._calculate_checksum())

            print("✅ Index saved successfully.")
        except Exception as e:
            print(f"❌ Error saving index: {e}")
            raise

    def _calculate_checksum(self):
        hasher = hashlib.sha256()
        for file in [self.index_path, self.docs_path]:
            with open(file, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
        return hasher.hexdigest()

    def _cleanup_files(self):
        print("🧹 Cleaning up corrupted files...")
        for file in [self.index_path, self.docs_path, self.checksum_path]:
            try:
                if file.exists():
                    file.unlink()
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")

    def query(self, user_query):
        if not user_query.strip():
            return "Please provide a non-empty question."

        try:
            print("🔎 Encoding query...")
            query_embedding = self.embedder.encode([user_query])
            _, top_indices = self.index.search(query_embedding, k=3)
            context = "\n".join(self.docs[i] for i in top_indices[0])

            if not context:
                return "I couldn't find relevant info to answer that."

            prompt = f"Context: {context}\n\nQuestion: {user_query}\nAnswer:"
            result = self.qa_model(prompt, max_length=256, num_beams=4, early_stopping=True)

            return result[0]["generated_text"].strip()
        except Exception as e:
            print(f"❌ Error during query: {e}")
            return "There was an error processing your query."
