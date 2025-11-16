# 📊 Analytics Module (Local NetworkX Fallback)

The project includes a lightweight analytics layer designed for environments where Neo4j Aura Free does not support APOC or Graph Data Science (GDS).
It provides **pure Cypher + local Python analytics**, and all logic is fully asynchronous.

This module acts as a **local analytics fallback** when Neo4j Aura Free cannot run server-side graph algorithms.

## ✨ Features

- **Local graph construction** using data fetched from Neo4j (mocked during tests)
- **PageRank (NetworkX)** for ranking influential users
- **Community detection** using greedy modularity
- **Degree + simple structural metrics** used by the Recommender
- **Graph debugging helper**: adjacency-list printing for demos and CLI visibility

## 🧪 Unit-Test Friendly

Analytics functions are written to be fully testable without Neo4j:

- All DB access is mockable
- Unit tests enforce **zero live database calls**
- NetworkX algorithms run entirely in memory
- Deterministic, reproducible results in all tests

## 🧱 Example Outputs

From the included demo:

```
Input Graph (Adjacency List):
  alice: bob, carol, frank
  bob: alice, dave
  carol: alice, dave
  dave: bob, carol, eve
  eve: dave, frank
  frank: alice, eve

Top users by NetworkX PageRank:
  - alice: 0.21
  - dave: 0.21
  - eve: 0.147
  - frank: 0.147
  - bob: 0.144
  - carol: 0.144

NetworkX Communities (Greedy Modularity):
  Community 1: alice, bob, carol, dave
  Community 2: eve, frank
```

### 🗺️ Input Social Graph

![Sample social graph](./scripts/analytics-sample-graph.png)

## 📁 Code Location

```
src/social_graph/analytics_local.py
scripts/demo_analytics_local.py
tests/unit/test_analytics_local_unit.py
```
