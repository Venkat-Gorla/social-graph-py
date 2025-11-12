# vegorla: sample graph should be created prior to running the analytics

"""
Demo runner for the Social Graph Analytics MVP.
Executes degree, pagerank, and community detection using the shared async Neo4j driver.
"""

import asyncio
from src.social_graph import analytics
from src.social_graph.db_async import close_driver

async def demo_analytics():
    print("\n=== Running Analytics Demo ===")

    username = "alice"
    print(f"\nDegree for user '{username}':")
    degree = await analytics.degree(username)
    print(f"  -> {degree} connections")

    print("\nTop users by simulated PageRank:")
    ranking = await analytics.pagerank(top_n=5)
    for user, score in ranking:
        print(f"  - {user}: {score}")

    print("\nCommunity detection (mock grouping):")
    communities = await analytics.community_detection()
    for user, group in communities.items():
        print(f"  - {user}: {group}")

    await close_driver()
    print("\nDemo completed successfully.\n")

if __name__ == "__main__":
    asyncio.run(demo_analytics())
