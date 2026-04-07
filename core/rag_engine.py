import chromadb
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, collection_name="faq_knowledge"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(collection_name)
        self.encoder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    def index_documents(self, documents):
        for i, doc in enumerate(documents):
            embedding = self.encoder.encode(doc["content"]).tolist()
            self.collection.add(
                embeddings=[embedding],
                documents=[doc["content"]],
                metadatas=[{"title": doc.get("title", "")}],
                ids=[f"doc_{i}"]
            )
    
    def retrieve_context(self, query, k=3):
        query_embedding = self.encoder.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        return results['documents'][0] if results['documents'] else []