"""Quick connection test to Neo4j Aura Free."""

"""
To run this script using uv, from root folder:
uv run python scripts\test_db_conn.py
"""

from social_graph.db import Neo4jDriver

def main():
    db = Neo4jDriver()
    print("Testing Neo4j connection...")
    result = db.run_query("RETURN 'Connection OK' AS status;")
    print(result[0]["status"])
    db.close()

if __name__ == "__main__":
    main()
