import os
import numpy as np
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

with open("doc.txt", 'r', encoding="utf-8") as f:
    document = f.read()

def simple_chunking(document:str, chunk_size:int = 25, overlap:int=3) -> list[str]:
    words = document.split()
    chunks = []
    for i in range(0, len(words), chunk_size-overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def get_embeddings(docs:list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="mistral-embed",
        inputs=docs
    )
    return [d.embedding for d in response.data]

def retrieve(query:str, chunks:list[str], top_k:int=2) -> list[str]:
    emb_query = get_embeddings([query])[0]
    emb_chunks = get_embeddings(chunks)

    similarity_scores = np.dot(emb_chunks, emb_query)
    print("DBG - similarity_scores:", similarity_scores)

    top_idx = np.argsort(similarity_scores)[::-1][:top_k]
    print("DBG - top_idx:", top_idx)
    return [chunks[i] for i in top_idx]

def generate(query:str):
    context_chunks = retrieve(query, chunks)
    context_str = "\n".join(context_chunks)

    prompt_str = f"""Answer the question using only the provided context.
    CONTEXT:
    {context_str}

    QUESTION:
    {query}
    """

    response = client.chat.complete(
        model = "mistral-large-latest",
        messages=[
            {"role":"user","content":prompt_str}
        ]
    )

    return response.choices[0].message.content

chunks = simple_chunking(document)
query = "Where is the European Space Agency’s Juice mission currently traveling to?"
query = "Where is the European Space Agency’s Apollo mission currently traveling to?"
print(generate(query))