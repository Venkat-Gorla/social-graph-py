# 📌 Social Graph — Async Neo4j + NetworkX Project

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Async](https://img.shields.io/badge/Async-asyncio-4D8C57?logo=python)
![Neo4j](https://img.shields.io/badge/Database-Neo4j%20Aura%20Free-008CC1?logo=neo4j)
![NetworkX](https://img.shields.io/badge/Graph-NetworkX-0C6AA6)
![Tests](https://img.shields.io/badge/Tests-pytest-yellow?logo=pytest)
![Package Manager](https://img.shields.io/badge/uv-package_manager-9cf)
![License](https://img.shields.io/badge/License-MIT-blue)

A fully asynchronous social graph system using Neo4j Aura Free and NetworkX, featuring recommendation algorithms, graph analytics, and a clean modular architecture.

This project uses:

- **Async Python** for non-blocking I/O
- **NetworkX** for local PageRank & community detection
- **Heap-optimized recommendation engine**
- End-to-end integration tests
- Strict, fully mocked unit tests
- Deterministic CLI demos

## 📑 Table of Contents

- [🚀 Features](#-features)
- [🧰 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [📚 Summary / Highlights](#-summary--highlights)
- [🧱 Architecture](#-architecture)
- [🎯 Why This Project?](#-why-this-project)
- [📦 Installation](#-installation)
- [✅ Run the local analytics demo](#-run-the-local-analytics-demo)
- [🧪 Tests in Action](#-tests-in-action)
- [📦 Deployment](#-deployment)
- [🔮 Future Enhancements](#-future-enhancements)
- [🏷️ License](#️-license)

## 🚀 Features

Core capabilities implemented end-to-end using async I/O and Neo4j:

- Create and manage users
- Manage bidirectional friendships
- List direct friends
- Recommend friends (mutual friends & 2nd-degree connections)
- Compute graph metrics (degree, PageRank, communities)
- Uses free, cloud-hosted [Neo4j Aura](https://neo4j.com/cloud/aura-free/) — no local DB install needed

### 🗺️ Sample Social Graph

![Sample social graph](./scripts/analytics-sample-graph.png)

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

    👉 For a deeper explanation of the local NetworkX analytics system, see the dedicated  
    [📊 Analytics Module README](./README_analytics.md).

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

NetworkX Communities (Greedy Modularity):
  Community 1: alice, bob, carol, dave
  Community 2: eve, frank
```

## 🧪 Tests in Action

Run all tests:

```bash
uv run pytest -v
```

**Test Output:**

```
C:\Users\venka\Downloads\Udemy\GitHub\social-graph-py>uv run pytest -v
========================= test session starts =========================
platform win32 -- Python 3.13.1, pytest-8.4.2, pluggy-1.6.0 -- C:\Users\venka\Downloads\Udemy\GitHub\social-graph-py\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\venka\Downloads\Udemy\GitHub\social-graph-py
configfile: pyproject.toml
testpaths: tests
plugins: asyncio-1.2.0, mock-3.15.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 23 items

tests/integration/test_integration_basic.py::test_basic_graph_flow_async PASSED                                                                                      [  4%]
tests/integration/test_recommender_mutuals.py::test_recommender_mutual_friends PASSED                                                                                [  8%]
tests/integration/test_recommender_mutuals.py::test_recommender_suggest_friends PASSED                                                                               [ 13%]
tests/integration/test_recommender_mutuals.py::test_recommender_recommend_top_k PASSED                                                                               [ 17%]
tests/integration/test_recommender_mutuals.py::test_recommender_recommend_top_k_no_candidates PASSED                                                                 [ 21%]
tests/unit/test_analytics_local_unit.py::test_pagerank_local_basic PASSED                                                                                            [ 26%]
tests/unit/test_analytics_local_unit.py::test_guard_blocks_db_access PASSED                                                                                          [ 30%]
tests/unit/test_analytics_local_unit.py::test_detect_communities_local_path_splits_into_two PASSED                                                                   [ 34%]
tests/unit/test_analytics_local_unit.py::test_detect_communities_two_clusters PASSED                                                                                 [ 39%]
tests/unit/test_analytics_local_unit.py::test_detect_communities_local_fully_connected PASSED                                                                        [ 43%]
tests/unit/test_analytics_local_unit.py::test_detect_communities_local_empty_graph PASSED                                                                            [ 47%]
tests/unit/test_recommender_heap_logic_unit.py::test_heap_keeps_top_k_only PASSED                                                                                    [ 52%]
tests/unit/test_recommender_heap_logic_unit.py::test_heap_sorts_ties_by_username PASSED                                                                              [ 56%]
tests/unit/test_recommender_heap_logic_unit.py::test_heap_called_with_exact_k_ordered PASSED                                                                         [ 60%]
tests/unit/test_recommender_mutuals_unit.py::test_mutual_friend_count_positive PASSED                                                                                [ 65%]
tests/unit/test_recommender_mutuals_unit.py::test_mutual_friend_count_zero PASSED                                                                                    [ 69%]
tests/unit/test_recommender_mutuals_unit.py::test_mutual_friend_count_no_result PASSED                                                                               [ 73%]
tests/unit/test_recommender_score_unit.py::test_compute_score_math_only PASSED                                                                                       [ 78%]
tests/unit/test_recommender_score_unit.py::test_compute_score_zero_cases PASSED                                                                                      [ 82%]
tests/unit/test_recommender_top_k_ranking_unit.py::test_recommend_top_k_ranking PASSED                                                                               [ 86%]
tests/unit/test_service_unit.py::test_add_user_with_injected_driver PASSED                                                                                           [ 91%]
tests/unit/test_service_unit.py::test_add_friendship_executes_expected_query PASSED                                                                                  [ 95%]
tests/unit/test_service_unit.py::test_list_friends_returns_sorted_list PASSED                                                                                        [100%]

========================= 23 passed in 11.11s =========================

C:\Users\venka\Downloads\Udemy\GitHub\social-graph-py>
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
