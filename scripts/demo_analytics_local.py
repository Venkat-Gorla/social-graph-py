"""
"""

import asyncio
from social_graph import analytics_local
from social_graph.db_async import close_driver
from social_graph.test_utils import clear_graph, setup_test_graph

async def demo_analytics():
    await setup_demo_graph()
    print("\n=== Running NetworkX Analytics Demo ===")

    await demo_pagerank()
    await demo_communities()

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

async def demo_pagerank():
    print("\nTop users by NetworkX PageRank:")
    ranking = await analytics_local.pagerank_local()
    for user, score in ranking:
        print(f"  - {user}: {score}")

async def demo_communities():
    print("\nNetworkX Communities (Greedy Modularity):")
    communities = await analytics_local.detect_communities_local()
    for idx, group in enumerate(communities, start=1):
        members = ", ".join(sorted(group))
        print(f"  Community {idx}: {members}")

if __name__ == "__main__":
    asyncio.run(demo_analytics())
