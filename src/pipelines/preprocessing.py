import os
import re
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_ENV_VARS = [
    "CHEMIN_MOBILE",
    "CHEMIN_TARIFICATION",
    "CHEMIN_TAXE",
    "CHEMIN_ATTIJARI_NET",
    "CHEMIN_MANAGEMENT_PAIEMENTS",
]

TXT_ENV_VARS = [
    "CHEMIN_OUVRIR_COMPTE_PARTICULIER",
    "CHEMIN_OUVRIR_COMPTE_TPE",
    "CHEMIN_OUVRIR_COMPTE_MRE",
]

MIN_CHUNK_LENGTH = 30


def _clean_text(text):
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if len(stripped) <= 2 and stripped.isdigit():
            continue  # numero de page isole
        lines.append(stripped)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _humanize_title(source_path):
    return Path(source_path).stem.replace("_", " ").replace("-", " ").strip()


def _add_context_header(chunk):
    title = _humanize_title(chunk.metadata.get("source", ""))
    page = chunk.metadata.get("page")
    header = f"[{title} - page {page + 1}]" if page is not None else f"[{title}]"
    chunk.page_content = f"{header}\n{chunk.page_content}"
    return chunk


def load_and_split_documents():
    raw_documents = []
    for env_var in PDF_ENV_VARS:
        loader = PyPDFLoader(os.getenv(env_var))
        raw_documents.extend(loader.load())

    for env_var in TXT_ENV_VARS:
        loader = TextLoader(os.getenv(env_var), encoding="utf-8")
        raw_documents.extend(loader.load())

    for doc in raw_documents:
        doc.page_content = _clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(raw_documents)
    chunks = [c for c in chunks if len(c.page_content.strip()) >= MIN_CHUNK_LENGTH]

    for chunk in chunks:
        _add_context_header(chunk)

    print(f"{len(raw_documents)} pages -> {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    load_and_split_documents()


