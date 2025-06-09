from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

def create_qa_chain(api_key: str, retriever):
    prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant. Continue the conversation based on the following history and the new question.

        <conversation_history>
        {context}
        </conversation_history>

        New Question: {input}
    """)
    llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192")
    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain)
