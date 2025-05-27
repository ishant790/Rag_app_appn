from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def create_qa_chain(api_key: str, retriever):
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the questions based on the provided context only.
        <context>
        {context}
        <context>
        Question: {input}
        """
    )
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192")
    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain)
