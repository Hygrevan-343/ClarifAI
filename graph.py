import os
import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://49de7a4f.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "wKUPjUOwQ2LN4khzVqV-qWtN8eta7JesjSqRUDbdYo8"

default_cypher = "MATCH (s)-[r]->(t) RETURN s, r, t LIMIT 150"

def fetch_graph_data(cypher: str = default_cypher):
    driver = GraphDatabase.driver(
        uri=NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )
    session = driver.session()
    result = session.run(cypher)
    nodes = set()
    edges = []
    for record in result:
        s = record['s']
        t = record['t']
        r = record['r']
        
        nodes.add(s.id)
        nodes.add(t.id)
        edges.append((s.id, t.id, r.type))
    
    session.close()
    driver.close()
    return nodes, edges

def plot_graph(nodes, edges, save_path="graph_image.png"):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    for edge in edges:
        G.add_edge(edge[0], edge[1], label=edge[2])
    
    plt.figure(figsize=(15, 15)) 
    pos = nx.spring_layout(G, k=0.5, iterations=50) 

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue", alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color="gray")
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color="darkred")

    plt.title("Neo4j Graph Visualization")
    plt.savefig(save_path, format="PNG", bbox_inches="tight", dpi=300)
    print(f"Graph image saved as {save_path}")
    plt.close()

nodes, edges = fetch_graph_data()
path = os.path.join("./uploads", "graph_image.png")
plot_graph(nodes, edges, save_path=path)
