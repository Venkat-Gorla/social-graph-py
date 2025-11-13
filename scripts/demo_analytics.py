"""
Demo runner for the Social Graph Analytics MVP.
Executes degree, pagerank, and community detection using the shared async Neo4j driver.
"""

import asyncio
from social_graph import analytics
from social_graph.db_async import close_driver
from social_graph.test_utils import clear_graph, setup_test_graph

async def demo_analytics():
    await setup_demo_graph()
    print("\n=== Running Analytics Demo ===")

    await demo_degree()
    await demo_pagerank()
    await demo_community_detection()

    await close_driver()
    print("\nDemo completed successfully.\n")

async def setup_demo_graph():
    users = ["alice", "bob", "carol", "dave", "eve", "frank"]
    friendships = [
        ("alice", "bob"),
        ("alice", "carol"),
        ("bob", "dave"),
        ("carol", "dave"),
        ("dave", "eve"),
        ("eve", "frank"),
        ("frank", "alice"),
    ]
    await clear_graph()
    await setup_test_graph(users, friendships)

async def demo_degree():
    username = "alice"
    print(f"\nDegree for user '{username}':")
    degree = await analytics.degree(username)
    print(f"  -> {degree} connections")

async def demo_pagerank():
    print("\nTop users by simulated PageRank:")
    ranking = await analytics.pagerank()
    for user, score in ranking:
        print(f"  - {user}: {score}")

async def demo_community_detection():
    print("\nCommunity detection (mock grouping):")
    communities = await analytics.community_detection()
    for user, group in communities.items():
        print(f"  - {user}: {group}")

if __name__ == "__main__":
    asyncio.run(demo_analytics())
