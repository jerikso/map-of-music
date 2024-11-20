from neo4j import GraphDatabase
from dotenv import load_dotenv
import os


load_dotenv()

# Access variables using os.getenv
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Function to create and return the driver
def get_driver():
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        return driver
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        raise

def run_query(driver, query):
    try:
        with driver.session() as session:
            session.run(query)
    except Exception as e:
        print(f"Error running query: {e}")
        raise

def create_node(driver, node_type, properties):
    query = f"""
    MERGE (n:{node_type} {{id: $id}})
    SET n += $properties
    """
    # Extract the "id" property from the dictionary
    node_id = properties["id"]
    
    # Remove "id" from properties to avoid overwriting it
    properties = {k: v for k, v in properties.items() if k != "id"}
    
    with driver.session() as session:
        session.run(query, {"id": node_id, "properties": properties})


def create_relationship(driver, node1_id, node2_id, relationship_type, properties):
    query = f"""
    MATCH (a {{id: $node1_id}}), (b {{id: $node2_id}})
    OPTIONAL MATCH (a)-[r:{relationship_type}]-(b)  // Find any existing relationship, directionless
    DELETE r  // Remove the existing relationship if it exists
    MERGE (a)-[new_r:{relationship_type}]-(b)  // Create the new undirected relationship
    SET new_r += $properties  // Set properties on the new relationship
    """
    
    with driver.session() as session:
        session.run(query, {
            "node1_id": node1_id,
            "node2_id": node2_id,
            "properties": properties
        })
