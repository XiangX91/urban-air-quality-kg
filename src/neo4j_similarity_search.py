"""
Explicit Neo4j Similarity Search

Performs semantic similarity search using embeddings stored explicitly in Neo4j.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 02/03/2025
"""

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "66666666"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def similarity_search(query_text: str, index_name: str, top_k: int = 5):
    query_embedding = model.encode(query_text, normalize_embeddings=True).tolist()

    with driver.session() as session:
        results = session.run(f"""
        CALL db.index.vector.queryNodes('{index_name}', {top_k}, $embedding)
        YIELD node, score
        RETURN node.name AS name, node.category AS category, score
        """, embedding=query_embedding)

        return [{"name": rec["name"], "category": rec["category"], "score": rec["score"]}
                for rec in results]

if __name__ == "__main__":
    query = "vehicle emissions"
    index = "source_embeddings"

    results = similarity_search(query, index)

    print("🔍 Explicitly retrieved similar nodes:")
    for record in results:
        print(f"- {record['name']} (Category: {record['category']}, Score: {record['score']:.3f})")

    driver.close()
