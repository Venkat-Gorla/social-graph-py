## 🧮 Analytics Module (MVP)

### Overview

This module provides lightweight, Cypher-only analytics for the Social Graph Resume Project.
It demonstrates graph insight capabilities (connection count, influence ranking, and community grouping) while staying fully compatible with **Neo4j Aura Free**.

### Location

`src/social_graph/analytics.py`

### Features

| Function                | Purpose                                               | Implementation                |
| ----------------------- | ----------------------------------------------------- | ----------------------------- |
| `degree(username)`      | Counts number of direct friendships                   | Simple Cypher query           |
| `pagerank(top_n)`       | Ranks users by connection count (simulated influence) | Degree-based approximation    |
| `community_detection()` | Groups users into placeholder “communities”           | Deterministic hash-based mock |

### Example Usage

```python
from src.social_graph import analytics

degree = await analytics.degree("alice")
ranking = await analytics.pagerank(top_n=5)
communities = await analytics.community_detection()

print(degree, ranking, communities)
```

### Design Notes

- **Asynchronous architecture:**
  Uses the shared async Neo4j driver (`get_driver()`) defined in `db_async.py`.
  No new connection logic — consistent with the rest of the project.
- **Neo4j-first design:**
  Queries run entirely inside the database; no data export or local traversal.
- **Minimalism for MVP:**
  Focused on working examples that convey graph analytics understanding, without GDS/APOC or NetworkX.

### Trade-offs and Future Work

| Limitation                                 | Reason                         | Future Upgrade                                         |
| ------------------------------------------ | ------------------------------ | ------------------------------------------------------ |
| No PageRank, Louvain, or Label Propagation | GDS not supported on Aura Free | Add when migrating to Aura DS or Enterprise            |
| No local analytics fallback                | Out of MVP scope               | Add optional NetworkX fallback                         |
| Mock community grouping                    | Keeps MVP lightweight          | Replace with real community detection algorithms later |

### Learning Outcomes

This MVP demonstrates:

- Understanding of **graph metrics** (degree, influence, communities).
- Ability to design **async data pipelines** with Neo4j.
- Awareness of **trade-offs** between free-tier limitations and scalable analytics.

## 🎓 What I Learned — Analytics Module

Building this analytics component gave me hands-on experience with **practical graph analysis** in Neo4j using **pure Cypher**.

Key takeaways:

- **Graph Query Thinking:** Learned to design and query relationships directly, focusing on connections and influence, not just tabular data.
- **Async Architecture:** Integrated Neo4j with asynchronous Python workflows, ensuring scalability and clean concurrency.
- **Design Trade-offs:** Understood the balance between free-tier constraints (Aura Free) and advanced analytics (APOC / GDS).
- **Progressive Enhancement Mindset:** Built a working MVP first, documented clear upgrade paths (e.g., real PageRank, Louvain).
- **Software Craftsmanship:** Practiced maintainable modular code — clean, typed, and consistent with the rest of the project.

This module represents a **bridge between theory and practice**: I implemented essential analytics features that _work today_, while designing an architecture that can scale into more sophisticated graph intelligence tomorrow.
