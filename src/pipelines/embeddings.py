import hashlib
from collections import Counter
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from preprocessing import load_and_split_documents

PERSIST_DIRECTORY = str(Path(__file__).resolve().parents[2] / "chroma_db")
COLLECTION_NAME = "bank_assistant"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_METADATA = {"hnsw:space": "cosine"}


def get_embedding_function():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        encode_kwargs={"normalize_embeddings": True},
    )


def _stable_id(index, chunk):
    source = chunk.metadata.get("source", "")
    page = chunk.metadata.get("page", "")
    digest = hashlib.md5(chunk.page_content.encode("utf-8")).hexdigest()
    return f"{source}:{page}:{index}:{digest}"


def build_vectorstore(chunks, embedding_function=None):
    embedding_function = embedding_function or get_embedding_function()
    ids = [_stable_id(i, chunk) for i, chunk in enumerate(chunks)]
    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
        ids=ids,
        collection_metadata=COLLECTION_METADATA,
    )


def load_vectorstore(embedding_function=None):
    embedding_function = embedding_function or get_embedding_function()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_function,
        persist_directory=PERSIST_DIRECTORY,
        collection_metadata=COLLECTION_METADATA,
    )


if __name__ == "__main__":
    chunks = load_and_split_documents()
    embedding_function = get_embedding_function()
    vectorstore = build_vectorstore(chunks, embedding_function)

    counts = Counter(Path(c.metadata.get("source", "?")).name for c in chunks)
    for source, count in sorted(counts.items()):
        print(f"  {source}: {count} chunks")

    dim = len(embedding_function.embed_query("test"))
    print(f"{vectorstore._collection.count()} chunks stockés dans Chroma ({PERSIST_DIRECTORY}), dimension={dim}")
 