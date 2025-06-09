import re
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_documents(pdf_path: str, user_agent: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    raw_text = "\n".join([doc.page_content for doc in docs])
    urls = re.findall(r"http[s]?://\S+", raw_text)
    web_docs = []
    for url in urls:
        try:
            res = requests.get(url, headers={"User-Agent": user_agent}, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
            web_docs.append(Document(page_content=soup.get_text(), metadata={"source": url}))
        except:
            continue
    return docs + web_docs
