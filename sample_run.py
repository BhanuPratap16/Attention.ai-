import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import os

# Connect to Neo4j
def get_neo4j_session(uri, user, password,database):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver.session(database=database)

def fetch_graph_data(session):
    query = """
    MATCH (n)-[r]->(m)
    RETURN n.name AS source, m.name AS target, type(r) AS relationship
    """
    results = session.run(query)
    nodes = set()
    edges = []
    
    for record in results:
        source = record["source"]
        target = record["target"]
        
        # Skip any edge where source or target is None
        if source is None or target is None:
            continue
        
        nodes.add(source)
        nodes.add(target)
        edges.append((source, target, record["relationship"]))
    
    return list(nodes), edges

def create_pyvis_graph(nodes, edges):
    net = Network(height="600px", width="100%", notebook=False)
    
    # Ensure that all nodes are strings and non-None
    for node in nodes:
        if node is not None:
            node_id = str(node)
            net.add_node(node_id, label=node_id)
    
    # Add edges with valid nodes
    for source, target, relationship in edges:
        if source is not None and target is not None:
            net.add_edge(source, target, title=relationship)
    
    # Save graph as HTML
    graph_html_path = "graph.html"
    net.write_html(graph_html_path, notebook=False, open_browser=False)
    
    print(f"Graph file will be saved to: {os.path.abspath(graph_html_path)}")
    return graph_html_path

# Streamlit UI
st.title("Relational Graph with Neo4j and Streamlit")

# Connection Details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j1234"

# Dropdown to select database
database_list = ["chatbotdatabase"]  # Replace with your actual database names
selected_database = st.selectbox("Select a Database", database_list)

# Create session
session = get_neo4j_session(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD,selected_database)

# Fetch and Visualize Data
if st.button("Generate Graph"):
    nodes, edges = fetch_graph_data(session)
    graph_html_path = create_pyvis_graph(nodes, edges)
    st.components.v1.html(open(graph_html_path, "r").read(), height=600)
