from llama_index.graph_stores.neo4j import Neo4jGraphStore

NEO4J_URI = "neo4j+s://49de7a4f.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "wKUPjUOwQ2LN4khzVqV-qWtN8eta7JesjSqRUDbdYo8"
NEO4J_DATABASE = "neo4j"

graph_store = Neo4jGraphStore(
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    url=NEO4J_URI,
    database=NEO4J_DATABASE,
)


graph_store.query(
    """
MATCH (n) DETACH DELETE n
"""
)