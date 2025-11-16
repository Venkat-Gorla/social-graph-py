# 📌 Social Graph — Async Neo4j + NetworkX Project

**vegorla pending: tech stack badge row, merge with analytics Readme**
**Automated tests in action**
**Toc**

A production-quality **social graph system** built in Python, demonstrating scalable system design, graph modeling, recommendation algorithms, and analytics using Neo4j Aura Free.

This project uses:

- **Async Python** for non-blocking I/O
- **NetworkX** for local PageRank & community fallbacks
- **Heap-optimized recommendation engine**
- Strict, fully mocked unit tests
- End-end integration tests
- Deterministic CLI demos

## 🚀 Features

- Create and manage users
- Create/remove friendships (bidirectional)
- List direct friends
- Recommend friends (mutual friends & 2nd-degree connections)
- Compute graph metrics (degree, PageRank, communities)
- Uses free, cloud-hosted [Neo4j Aura](https://neo4j.com/cloud/aura-free/) — no local DB install needed

## 🧱 Tech Stack

| Component                      | Technology              |
| ------------------------------ | ----------------------- |
| Language                       | Python 3.11+            |
| Graph Database                 | Neo4j Aura Free (Cloud) |
| Testing                        | pytest                  |
| Lightweight dependency manager | uv                      |

## 📁 Project Structure

```
social-graph-py/
├─ src/social_graph/
│  ├─ config.py
│  ├─ db.py              # Neo4j driver wrapper
│  ├─ db_async.py        # Async driver wrapper
│  ├─ models.py
│  ├─ service.py         # Neo4j operations for the social graph
│  ├─ service_async.py   # Async Neo4j operations
│  ├─ recommender.py     # Scoring & top-K ranking
│  ├─ analytics.py       # Cypher-based analytics
│  ├─ analytics_local.py # NetworkX PageRank & communities
├─ tests/
│  ├─ integration/
│  ├─ unit/
├─ scripts/
│  ├─ demo_analytics.py
│  ├─ demo_analytics_local.py
```

## Summary / Highlights

- **Asynchronous Neo4j driver wrapper**
  Encapsulates all database access behind a clean `run_query()` API.

- **Dual analytics pipeline**

  - Neo4j Cypher-only MVP for Aura Free
  - **Local NetworkX fallback** (PageRank + Greedy modularity communities)

- **Recommender engine with tunable weighting**

  - Uses mutual friends + degree centrality
  - Stable deterministic ranking
  - Efficient heap-based top-K selection

- **Test-driven, production-style code**

  - End-end integration tests with sample social graphs
  - Unit tests exercise all core logic with in-memory graphs and full mocking of DB access
  - Guard fixtures ensure no accidental network calls

- **Scripted demos**

  - Build a sample graph
  - Print adjacency list
  - Run PageRank + communities
  - Print analytics

- **Clean, modular architecture**

## 🧱 Architecture

```
               ┌─────────────────────┐
               │    Demo Scripts &   │
               │    Automated Tests  │
               └──────────┬──────────┘
                          │
        ┌─────────────────┼───────────────────┐
        │                 │                   │
        ▼                 ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌────────────────┐
│ Recommender  │   │ Analytics NX │   │ Async Neo4j    │
│ Scoring/K    │   │ PageRank/    │   │ Driver Wrapper │
│ Mutuals      │   │ Communities  │   │ run_query()    │
└───────┬──────┘   └───────┬──────┘   └────────┬───────┘
        │                  │                   │
        └──────────────────┴───────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ Neo4j Aura Free Graph  │
              └────────────────────────┘
```

## 🎯 Why This Project?

This codebase demonstrates:

✅ Strong async Python fundamentals  
✅ Clean separation of concerns  
✅ Non-trivial algorithms (PageRank, communities, heaps)  
✅ Realistic data modeling  
✅ Production-grade test practice  
✅ CI-friendly structure  
✅ Readable, maintainable code

## Run the local analytics demo

```
uv run python scripts/demo_analytics_local.py
```

You will see:

```
Input Graph (Adjacency List):
  alice: bob, carol, frank
  ...

Top users by NetworkX PageRank:
  - alice: 0.21
  - dave: 0.21
  ...

NetworkX Communities:
  Community 1: alice, bob, carol, dave
  Community 2: eve, frank
```

## 📦 Deployment

Since all logic is pure Python + async I/O:

- Works on any platform
- No Docker required
- Neo4j Aura Free compatible
- Can run analytics entirely offline using NetworkX mode

## 📊 Future Enhancements

- Add follower/following relationships
- Integrate Neo4j Graph Data Science (GDS)
- Add REST API wrapper (FastAPI)
- Include Dockerfile for optional container deployment
- Extend design for AWS Neptune serverless

## 🏷️ License

MIT License — free to use, modify, and share.
