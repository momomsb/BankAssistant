from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import UnstructuredCHMLoader
from dotenv import load_dotenv
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

Mobile_loader = PyPDFLoader(os.getenv("CHEMIN_MOBILE"))
Mobile_data = Mobile_loader.load()
#print(Mobile_data)

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=800,
    chunk_overlap=150
)

doc= splitter.split_documents(Mobile_data)
print(doc)