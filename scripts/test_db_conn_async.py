"""Quick async Neo4j connection test.

Run with, from root folder:
    uv run python scripts/test_db_conn_async.py
"""

import asyncio
from social_graph.db_async import get_driver, close_driver

async def main():
    driver = get_driver()
    print("Testing Neo4j async connection...")
    result = await driver.run_query("RETURN 'Connection OK' AS status;")
    print(result[0]["status"])
    await close_driver()

if __name__ == "__main__":
    asyncio.run(main())
