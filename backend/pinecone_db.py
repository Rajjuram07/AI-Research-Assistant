from pinecone import Pinecone
from backend.config import PINECONE_API_KEY, PINECONE_INDEX

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX)

def store_embedding(id, embedding, text):

    index.upsert(
        vectors=[
            {
                "id": id,
                "values": embedding,
                "metadata": {"text": text}
            }
        ]
    )

def query_embedding(embedding):

    results = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )

    return results