"""
Explicit Neo4j-LangChain-Llama Local RAG Pipeline

This explicitly enables natural language Q&A over your Neo4j knowledge graph
using a local LLM and LangChain.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 02/03/2025
"""

"""
Explicit Neo4j-LangChain-Llama Local RAG Pipeline

This explicitly enables natural language Q&A over your Neo4j knowledge graph 
using a local LLM and LangChain.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 23/01/2025
"""

from langchain_community.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.graphs import Neo4jGraph
from langchain.chains import RetrievalQA
import getpass
import os

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

def setup_graph(password=None):
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    
    if not password:
        password_input = getpass.getpass("Enter Neo4j password explicitly (leave empty for default): ").strip()
        password = password_input if password_input else "66666666"
    
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=password)
    return graph

def setup_llm(model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model file explicitly not found at: {model_path}")

    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.1,
        max_tokens=512,
        n_ctx=2048,
        top_p=1
    )
    return llm

def setup_rag_pipeline(graph, llm):
    vector_store = Neo4jVector.from_existing_graph(
        graph=graph,
        embedding=embeddings,
        index_name="source_embeddings",
        node_label="Source",
        embedding_node_property="embedding",
        text_node_properties=["name", "category"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    return qa_chain

def query_kg(qa_chain, question):
    result = qa_chain({"query": question})
    answer = result["result"]
    sources = result["source_documents"]

    print(f"\n🔍 Question explicitly asked: {question}\n")
    print("📖 Answer from local LLM:\n", answer)

if __name__ == "__main__":
    graph = setup_graph()
    llm = setup_llm()  # You can explicitly specify the model_path here
    qa_chain = setup_rag_pipeline(graph, llm)
    
    sample_question = "What are effective measures to mitigate vehicle emissions?"
    query_kg(qa_chain, sample_question)
