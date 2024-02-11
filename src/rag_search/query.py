import faiss
from database.embed_database import CRUD
from utils import load_embedder, get_chunk_from_database
from data_pipeline.parsers import doc_parser


def get_answer_of_query(query, k=5):
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
