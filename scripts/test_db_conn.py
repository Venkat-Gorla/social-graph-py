"""Quick connection test to Neo4j Aura Free."""
from src.social_graph.db import Neo4jDriver

def main():
    db = Neo4jDriver()
    print("Testing Neo4j connection...")
    result = db.run_query("RETURN 'Connection OK' AS status;")
    print(result[0]["status"])
    db.close()

if __name__ == "__main__":
    main()
