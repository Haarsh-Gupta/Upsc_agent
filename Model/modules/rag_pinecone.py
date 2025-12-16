import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX

emb = OpenAIEmbeddings()

def init_pinecone():
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    if PINECONE_INDEX not in pinecone.list_indexes():
        pinecone.create_index(PINECONE_INDEX, dimension=1536)

def rag_retrieve(query):
    init_pinecone()
    store = Pinecone.from_existing_index(PINECONE_INDEX, emb)
    docs = store.similarity_search(query, k=5)
    return docs
