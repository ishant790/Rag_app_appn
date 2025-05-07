import re
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_documents(pdf_path: str, user_agent: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    raw_text = "\n".join([doc.page_content for doc in docs])
    urls = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
        raw_text
        )

    headers = {"User-Agent": user_agent}
    web_docs = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            web_docs.append(Document(page_content=text, metadata={"source": url}))
        except Exception as e:
            print(f"Failed to load {url}: {e}")

    return docs + web_docs
