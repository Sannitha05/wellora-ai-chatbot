import json
import os
from typing import List, Dict

class RAGEngine:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.knowledge_base = self._load_data()

    def _load_data(self) -> List[Dict]:
        if not os.path.exists(self.data_path):
            return []
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def retrieve_context(self, query: str) -> str:
        # Simple keyword-based retrieval for demonstration
        query_lower = query.lower()
        relevant_chunks = []
        
        for item in self.knowledge_base:
            # Check if any symptoms or the topic matches the query
            if item['topic'].lower() in query_lower or any(s.lower() in query_lower for s in item['symptoms']):
                relevant_chunks.append(f"Topic: {item['topic']}\nSymptoms: {', '.join(item['symptoms'])}\nGuidance: {item['guidance']}")
        
        if not relevant_chunks:
            return "No specific medical context found for this query."
            
        return "\n\n---\n\n".join(relevant_chunks)

# Initialize global engine
rag_engine = RAGEngine(os.path.join(os.path.dirname(__file__), "data", "medical_knowledge.json"))
