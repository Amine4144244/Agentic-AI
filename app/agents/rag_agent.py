from sentence_transformers import SentenceTransformer
import chromadb
from config.groq_config import get_groq_response, MODELS

class RAGAgent:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="agent_docs")

    def _embed_text(self, text):
        """Get embeddings locally"""
        return self.embedding_model.encode(text).tolist()

    def add_document(self, content, filename):
        """Add a document to the vector store"""
        embedding = self._embed_text(content)
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            ids=[filename]
        )

    def query(self, query):
        """Query the vector store and generate a response"""
        query_embedding = self._embed_text(query)
        results = self.collection.query(query_embeddings=[query_embedding], n_results=3)
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant information found.", []

        context = "\n".join(results['documents'][0])
        sources = results['ids'][0]

        messages = [
            {"role": "system", "content": f"Answer based on context: {context}"},
            {"role": "user", "content": query}
        ]

        response = get_groq_response(messages, model=MODELS["fast"])
        return response, sources