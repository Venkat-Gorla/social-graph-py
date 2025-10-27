# Social Graph Py — README.md Starter

> **Project:** `social-graph-py`  
> **Description:** Cloud-hosted social graph backend built in Python, demonstrating system design, graph modeling, recommendation algorithms, and analytics using Neo4j Aura Free.

---

## 🧩 Overview
`social-graph-py` is a backend-only project showcasing how to design and build a **scalable social graph system**. It supports user creation, friendship modeling, friend recommendations, and basic analytics — all through a clean Python CLI interface. 

This project highlights strong **system design, algorithmic thinking, and backend architecture** skills suitable for technical interviews and resume portfolios.

---

## 🚀 Features
- Create and manage users
- Create/remove friendships (bidirectional)
- List direct friends
- Recommend friends (mutual friends & 2nd-degree connections)
- Compute graph metrics (degree, PageRank, communities)
- CLI interface built with [Typer](https://typer.tiangolo.com)
- Uses free, cloud-hosted [Neo4j Aura](https://neo4j.com/cloud/aura-free/) — no local DB install needed

---

## 🧱 Tech Stack
| Component | Technology |
|------------|-------------|
| Language | Python 3.11+ |
| Graph Database | Neo4j Aura Free (Cloud) |
| CLI Framework | Typer + Rich |
| Testing | pytest |
| Optional Cloud (Design Notes) | AWS Neptune |

---

## 📦 Quickstart
### 1️⃣ Setup
1. Create a **Neo4j Aura Free** instance: [https://neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free)
2. Note your credentials: `BOLT_URL`, `USERNAME`, `PASSWORD`
3. Create `.env` file:
   ```bash
   NEO4J_URI=bolt://<your-instance>.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=<your-password>
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2️⃣ Run Example Commands
```bash
python -m social_graph.cli create-user --name "Alice" --email alice@example.com
python -m social_graph.cli create-user --name "Bob" --email bob@example.com
python -m social_graph.cli add-friend Alice Bob
python -m social_graph.cli list-friends Alice
python -m social_graph.cli recommend Alice --k 5
```

### 3️⃣ Run Tests
```bash
pytest -q
```

---

## 📁 Project Structure
```
social-graph-py/
├─ src/social_graph/
│  ├─ config.py
│  ├─ db.py
│  ├─ models.py
│  ├─ service.py
│  ├─ recommender.py
│  ├─ analytics.py
│  └─ cli.py
├─ tests/
├─ examples/
│  └─ demo_commands.sh
└─ docs/
   └─ architecture.md
```

---

## 🧮 Example Cypher Queries
- Create User:
  ```cypher
  CREATE (u:User {user_id: $id, name: $name, email: $email, created_at: datetime()}) RETURN u;
  ```
- Add Friendship:
  ```cypher
  MATCH (a:User {user_id:$a}), (b:User {user_id:$b})
  MERGE (a)-[:FRIEND]-(b)
  ON CREATE SET r.since = datetime();
  ```
- Recommend Friends:
  ```cypher
  MATCH (u:User {user_id:$id})-[:FRIEND]->(:User)-[:FRIEND]->(fof:User)
  WHERE NOT (u)-[:FRIEND]-(fof) AND u <> fof
  RETURN fof.user_id, fof.name, count(*) AS mutuals
  ORDER BY mutuals DESC LIMIT $k;
  ```

---

## 📊 Future Enhancements
- Add follower/following relationships
- Integrate Neo4j Graph Data Science (GDS) for real PageRank
- Add REST API wrapper for CLI commands (FastAPI)
- Include Dockerfile for optional container deployment
- Extend design for AWS Neptune serverless

---

## 🧾 Resume Summary Example
> **Designed and implemented a Python-based social graph backend (Neo4j Aura Cloud)** featuring graph schema modeling, recommender algorithms (mutual-friend, 2nd-degree), and CLI-driven analytics. Documented AWS Neptune migration and scalability strategy.

---

## 🏷️ License
MIT License — free to use, modify, and share.

---

## 📚 References
- [Neo4j Aura Free](https://neo4j.com/cloud/aura-free/)
- [Neo4j Python Driver Docs](https://neo4j.com/docs/api/python-driver/current/)
- [AWS Neptune Overview](https://aws.amazon.com/neptune/)
- [Typer Docs](https://typer.tiangolo.com/)

