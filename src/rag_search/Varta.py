import requests
import faiss
from database.embed_database import CRUD
from utils import load_embedder, get_chunk_from_database
from data_pipeline.parsers import doc_parser


def get_answer_of_query(query, k=8):
    embedder = load_embedder()
    q_vec = embedder.encode(doc_parser(query).chunker())
    database = CRUD("Embeddings")
    embedding = database.get_data()
    database.close_db()
    index = faiss.IndexFlatL2(768)
    index.add(embedding)
    _, ind = index.search(q_vec, k)
    data = []
    for i in range(k):
        embd = embedding[ind[0][i]]
        data.append(get_chunk_from_database(embd))
    return data


# Global dictionary to store cached responses
response_cache = {}


def generate_response(question, model):
    rag_response = get_answer_of_query(question)
    url = "https://api.together.xyz/v1/completions"

    payload = {
        "model": f"{model}",
        "prompt": f"<s>[INST] {rag_response} [/INST]",
        "max_tokens": 512,
        "stop": ["</s>", "[/INST]"],
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "n": 1,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer d6a921d91b8b7d802a005b3d7293b22e0a53c907e6d929af725030f5a9abebf7",
    }

    # Check if the response is already cached
    if question in response_cache:
        return response_cache[question]

    # If not cached, make a request to the API
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the generated text from the response
        generated_text = data["choices"][0]["text"]
        # Cache the response
        response_cache[question] = generated_text
        return generated_text
    else:
        print("Error:", response.text)
