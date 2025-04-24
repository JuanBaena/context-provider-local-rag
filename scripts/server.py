# Run this serve with the command: fastapi dev server.py

"""
This is an example of a server that can be used with the "http" context provider.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaEmbeddings
from fastapi.middleware.cors import CORSMiddleware
import chromadb

EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DB_PATH = "../db/chroma"
COLLECTION_NAME = "text_documents"

class ContextProviderInput(BaseModel):
    query: str
    fullInput: str

class QTestInput(BaseModel):
    input: str


app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Ollama embeddings
ollama_embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
)
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_collection(name= COLLECTION_NAME)

def get_embeddings_from_query(query):
    embedding = ollama_embeddings.embed_query(query)
    return embedding

def get_documents_from_collection(embeddings):
    query_result = collection.query(
        query_embeddings=embeddings,
        n_results=5,
    )
    return query_result.get('documents')


@app.post("/retrieve", operation_id="get_retrieved_documents")
async def create_item(item: ContextProviderInput):
    print('query', item.query)
    print('\n')

    print('full input', item.fullInput)
    print('\n')

    steps_embeddings = get_embeddings_from_query(item.fullInput)
    results = get_documents_from_collection(steps_embeddings)

    # Construct the "context item" format expected by Continue
    context_items = []
   
    for idx, result in enumerate(results):
        step_name = f"Query {idx+1}"
        context_items.append({
            "name": step_name,
            "description": step_name,
            "content": str(result),
        })

    return context_items