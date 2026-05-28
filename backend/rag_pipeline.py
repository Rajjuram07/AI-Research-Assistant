import uuid
from backend.embeddings import get_embedding
from backend.pinecone_db import store_embedding, query_embedding

def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks

def store_document(text):
    chunks = chunk_text(text)

    for chunk in chunks:
        embedding = get_embedding(chunk)

        store_embedding(
            str(uuid.uuid4()),
            embedding,
            chunk
        )

def retrieve_context(query):
    query_embedding_vector = get_embedding(query)

    results = query_embedding(query_embedding_vector)

    context = ""

    for match in results["matches"]:
        context += match["metadata"]["text"] + "\n"

    return context