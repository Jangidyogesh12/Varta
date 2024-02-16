from data_pipeline.document_loader import load
from data_pipeline.parsers import doc_parser

from sentence_transformers import SentenceTransformer
import numpy as np
import sqlite3


# function to generate chunks out of the documet
def generate_chunks(path):
    """
    Extract chunks from the loaded text using a document parser.

    Returns:
    - list: A list of text chunks.
    """
    txt = load(path)
    chunks = doc_parser(txt).chunker()
    return chunks


# function to load the embedding model you can choose your own embedding model based on your purpose
def load_embedder(model_name: str = "distilbert-base-uncased"):
    return SentenceTransformer(model_name)


# gets the chunk from the embedding database
def get_chunk_from_database(embedding):
    con = sqlite3.connect("src/rag_search/database/database.db")
    cur = con.cursor()
    embedding_bytes = np.array(embedding).astype(np.float32).tobytes()
    cur.execute(
        "SELECT chunk FROM Embeddings WHERE embedding_data = ?", (embedding_bytes,)
    )
    data = cur.fetchall()
    con.close()
    return data
