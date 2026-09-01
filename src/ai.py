import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from pydantic import SecretStr
from langchain_community.document_loaders import PyPDFLoader


sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
MISTRALL_SMALL=ChatMistralAI(
    model_name="mistral-small",
    api_key=SecretStr(os.getenv("MISTRAL_API_KEY","0")),
    temperature=0.24
)

#Guide_Attijari_Mobile.pdf
loader = PyPDFLoader(Path(__file__).resolve().parents[3] / "documents" / "Guide_Attijari_Mobile.pdf")
data = loader.load()
print(data)
