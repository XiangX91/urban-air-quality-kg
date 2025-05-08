"""
Explicit Neo4j-LangChain-Llama Local RAG Pipeline

This explicitly enables natural language Q&A over your Neo4j knowledge graph
using a local LLM and LangChain.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 02/03/2025
"""

from langchain_community.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.neo4j_vector import Neo4jVector
from langchain.graphs import Neo4jGraph
from langchain.chains import RetrievalQA

# Explicit configuration for Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "66666666"

# Connect explicitly to Neo4j graph
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)

# Explicit local embeddings (must match previous embeddings)
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')

# Explicit local LLM setup (LlamaCpp)
llm = LlamaCpp(
    model_path="/Users/nxx20/Library/Application Support/nomic.ai/GPT4All/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    temperature=0.1,
    max_tokens=512,
    n_ctx=2048,
    top_p=1
)

# Setup explicit vector store
vector_store = Neo4jVector.from_existing_graph(
    graph=graph,
    embedding=embeddings,
    index_name="source_embeddings",  # explicitly your Neo4j vector index
    node_label="Source",             # adjust explicitly if querying different nodes
    embedding_node_property="embedding",
    text_node_properties=["name", "category"]
)

# Setup explicit RAG QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Explicit function to query your pipeline
def query_kg(question):
    result = qa_chain({"query": question})
    answer = result["result"]
    sources = result["source_documents"]

    print(f"\n🔍 Question explicitly asked: {question}\n")
    print("📖 Answer from local LLM:\n", answer)

    # print("\n📌 Explicitly retrieved sources from Neo4j:")
    # for doc in sources:
    #     print(f"- {doc.page_content}")

# Example explicitly usage
if __name__ == "__main__":
    sample_question = "What are effective measures to mitigate vehicle emissions?"
    query_kg(sample_question)
