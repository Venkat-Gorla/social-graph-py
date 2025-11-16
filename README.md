# 📌 Social Graph — Async Neo4j + NetworkX Project

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Async](https://img.shields.io/badge/Async-asyncio-4D8C57?logo=python)
![Neo4j](https://img.shields.io/badge/Database-Neo4j%20Aura%20Free-008CC1?logo=neo4j)
![NetworkX](https://img.shields.io/badge/Graph-NetworkX-0C6AA6)
![Tests](https://img.shields.io/badge/Tests-pytest-yellow?logo=pytest)
![Package Manager](https://img.shields.io/badge/uv-package_manager-9cf)
![License](https://img.shields.io/badge/License-MIT-blue)

<!-- TODO: Table of Contents -->

A fully asynchronous social graph system using Neo4j Aura Free and NetworkX, featuring recommendation algorithms, graph analytics, and a clean modular architecture.

This project uses:

- **Async Python** for non-blocking I/O
- **NetworkX** for local PageRank & community detection
- **Heap-optimized recommendation engine**
- End-to-end integration tests
- Strict, fully mocked unit tests
- Deterministic CLI demos

## 🚀 Features

Core capabilities implemented end-to-end using async I/O and Neo4j:

- Create and manage users
- Manage bidirectional friendships
- List direct friends
- Recommend friends (mutual friends & 2nd-degree connections)
- Compute graph metrics (degree, PageRank, communities)
- Uses free, cloud-hosted [Neo4j Aura](https://neo4j.com/cloud/aura-free/) — no local DB install needed

## 🧰 Tech Stack

| Component                      | Technology              |
| ------------------------------ | ----------------------- |
| Language                       | Python 3.11+            |
| Graph Database                 | Neo4j Aura Free (Cloud) |
| Testing Framework              | pytest                  |
| Lightweight Dependency Manager | uv                      |

## 📁 Project Structure

Organized into clean modules separating DB access, analytics, and recommendation logic.

> **Note:** The project includes both synchronous (`service.py`, `db.py`) and asynchronous (`service_async.py`, `db_async.py`) implementations.
> The **async versions are the primary, recommended APIs**, and the sync modules are kept for reference and compatibility.

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

## 📚 Summary / Highlights

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

  - End-to-end integration tests with sample social graphs
  - Unit tests exercise all core logic with in-memory graphs and full mocking of DB access
  - Guard fixtures ensure no accidental network calls

- **Scripted demos**

  - Build a sample graph
  - Print adjacency list
  - Run and print analytics

- **Clean, modular architecture**

## 🧱 Architecture

The system is composed of three loosely coupled layers:

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
✅ Readable, maintainable code

## 📦 Installation

```
uv sync
uv run python scripts/demo_analytics.py
```

> Neo4j Aura connection credentials are read from environment variables defined in config.py.

## ✅ Run the local analytics demo

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
- Runs on Neo4j Aura Free (fully managed, cloud-hosted)
- Can run analytics entirely offline using NetworkX mode

## 🔮 Future Enhancements

- Add follower/following relationships
- Integrate Neo4j Graph Data Science (GDS)
- Add REST API wrapper (FastAPI)
- Extend design for AWS Neptune serverless

## 🏷️ License

MIT License — free to use, modify, and share.
