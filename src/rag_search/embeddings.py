from database.embed_database import CRUD
from functools import wraps
from loguru import logger
from utils import generate_chunks, load_embedder
import time


# Decorator for logging
def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@log_function_call
def generate_Embeddings(path):
    """
    Generates the embedding out of the chunks of data

    Returns:
    - list: A list of embedding of dimensions 768
    """
    model = load_embedder()
    chunks = generate_chunks(path)
    embeddings = model.encode(chunks)
    return chunks, embeddings


@log_function_call
def add_embedding_to_database(self, path: str, name: str):
    """
    This finction adds the ebedding to the database
    """
    database = CRUD(name)
    chunks, embeddings = generate_Embeddings(path)
    for chunk, embedding in zip(chunks, embeddings):
        database.insert(chunk, embedding)

    logger.info(
        f"The Embeddings has been added to the database table:{self.database.table_name} Successfully"
    )
    database.close_db()
