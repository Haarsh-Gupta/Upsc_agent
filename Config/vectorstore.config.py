import os 
from pinecone import Pinecone
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")  
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")



class PineconeStore:
    def __init__(self, index_name: str = None, namespace: str = None):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        self.index_name = index_name or PINECONE_INDEX_NAME
        self.namespace = namespace or PINECONE_NAMESPACE

        self.index = self.pc.Index(self.index_name)

    def upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """Insert multiple vectors into Pinecone."""
        self.index.upsert(
            vectors=vectors,
            namespace=self.namespace
        )

    def delete_by_prefix(self, prefix: str):
        """Utility: delete all vectors starting with prefix."""
        self.index.delete(
            filter={"id": {"$eq": prefix}},
            namespace=self.namespace
        )
    def query(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the index for similar vectors."""
        response = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=self.namespace
        )
        return response['matches']
