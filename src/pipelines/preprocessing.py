from langchain_community.document_loaders import PyPDFLoader, TextLoader
from dotenv import load_dotenv
import os
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
    "CHEMIN_OUVRIR_COMPTE_EN_LIGNE",
]


def load_and_split_documents():
    raw_documents = []
    for env_var in PDF_ENV_VARS:
        loader = PyPDFLoader(os.getenv(env_var))
        raw_documents.extend(loader.load())

    for env_var in TXT_ENV_VARS:
        loader = TextLoader(os.getenv(env_var), encoding="utf-8")
        raw_documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(raw_documents)

    print(f"{len(raw_documents)} pages -> {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    load_and_split_documents()
