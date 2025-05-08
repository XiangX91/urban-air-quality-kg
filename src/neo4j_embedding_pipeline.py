"""
Explicit Neo4j Embedding Pipeline

Generates and stores semantic embeddings for Urban Air Quality KG nodes explicitly.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 02/03/2025
"""

from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
import getpass

# Explicit Neo4j connection setup
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"

password_input = getpass.getpass("Enter Neo4j password: ").strip()
NEO4J_PASSWORD = password_input if password_input else "66666666"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Explicit embedding model setup
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def fetch_nodes(tx):
    query = """
    MATCH (n)
    WHERE n.name IS NOT NULL
    RETURN n.name AS label,
           labels(n)[0] AS group,
           coalesce(n.category, "Uncategorized") AS category
    """
    return [{"label": rec["label"], "group": rec["group"], "category": rec["category"]}
            for rec in tx.run(query)]

def store_embeddings(tx, nodes):
    for node in nodes:
        tx.run("""
            MATCH (n {name: $label})
            SET n.embedding = $embedding
        """, label=node["label"], embedding=node["embedding"])

def generate_embeddings():
    # Fetch explicitly nodes from Neo4j
    with driver.session() as session:
        nodes = session.execute_read(fetch_nodes)

    if not nodes:
        print("⚠️ No nodes found explicitly in Neo4j.")
        return

    texts = [f"{node['label']} ({node['group']}, {node['category']})" for node in nodes]
    embeddings = model.encode(texts, normalize_embeddings=True)

    for node, emb in zip(nodes, embeddings):
        node["embedding"] = emb.tolist()

    # Explicitly store embeddings back into Neo4j
    with driver.session() as session:
        session.execute_write(store_embeddings, nodes)

    print("✅ Embeddings explicitly generated and stored.")

    driver.close()

if __name__ == "__main__":
    generate_embeddings()
