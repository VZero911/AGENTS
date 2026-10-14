<p align="center">
  <img src="https://img.shields.io/badge/AGENTS-Autonomous%20Nodes-5fd38d?style=for-the-badge&labelColor=07060f" alt="AGENTS" />
  <img src="https://img.shields.io/badge/ALICE%20V0-Powered-00ffcc?style=for-the-badge&labelColor=07060f" alt="ALICE V0" />
  <img src="https://img.shields.io/badge/Zero%20Deps-stdlib%20only-8f6cf0?style=for-the-badge&labelColor=07060f" alt="Zero Deps" />
</p>

<p align="center"><b>Autonomous Public Node Agents — Zero External Dependencies</b></p>

<p align="center"><code>ANTI-NETRUNNER</code> — Source integrity hashing prevents automated AI scraping and unauthorized code replication.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776ab?style=flat-square&logo=python&logoColor=white&labelColor=07060f" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white&labelColor=07060f" />
  <img src="https://img.shields.io/badge/pip%20install-NONE-ea4335?style=flat-square&labelColor=07060f" />
  <img src="https://img.shields.io/badge/Chain-31337-f2c14e?style=flat-square&labelColor=07060f" />
  <img src="https://img.shields.io/badge/License-MIT-c0caf5?style=flat-square&labelColor=07060f" />
</p>

---

## What is this?

A standalone AI agent that runs on **any machine** with Python 3.12+. No `pip install`, no `requirements.txt` — pure Python stdlib only.

Connects to THESEED L0 blockchain, syncs chain state, self-heals on disconnect, and exposes an HTTP API for queries and tasks.

## Features

- **Zero dependencies** — `http.server`, `urllib`, `json`, `threading` — that's it
- **Chain sync** — background loop connects to L0 RPC, tracks blocks
- **Self-healing** — auto-recovers from chain disconnects
- **Health monitoring** — `/health` and `/status` always on
- **Task execution** — accepts sync and report tasks via API
- **Query endpoint** — ask the agent about chain state, node info
- **Docker ready** — single Dockerfile, no build deps

## Run

### Docker (recommended)

```bash
docker build -t alice-agent .
docker run -d --name alice-agent \
  -e ALICE_PORT=7781 \
  -e RPC_URL=http://host.docker.internal:8545 \
  -e CHAIN_ID=31337 \
  --network host \
  alice-agent
```

### Direct

```bash
python3 alice_general.py
```

## API

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/status` | GET | Full node status |
| `/api/chain` | GET | Chain info (block, sync status) |
| `/api/query` | POST | Query the agent (`{"input": "..."}`) |
| `/api/task` | POST | Send task (`{"task": "sync_chain"}`) |
| `/api/node` | GET | Node identity |
| `/api/logs` | GET | Agent activity logs |

## Environment

| Variable | Default | Description |
|---|---|---|
| `ALICE_PORT` | `7781` | HTTP server port |
| `ALICE_ROLE` | `GENERAL` | Agent role |
| `RPC_URL` | L0 blockchain RPC endpoint | Blockchain RPC |
| `CHAIN_ID` | `31337` | Chain ID |

## Related

<p align="center">
  <a href="https://github.com/VZero911/A.L.I.C.E"><img src="https://img.shields.io/badge/A.L.I.C.E-AI%20Framework-00ffcc?style=for-the-badge&logo=github&labelColor=07060f" alt="ALICE" /></a>
  <a href="https://github.com/VZero911/MCP"><img src="https://img.shields.io/badge/MCP-Server-8f6cf0?style=for-the-badge&logo=github&labelColor=07060f" alt="MCP" /></a>
  <a href="https://github.com/VZero911/THESEED"><img src="https://img.shields.io/badge/THESEED-Blockchain%20%2F%20Data-f2c14e?style=for-the-badge&logo=github&labelColor=07060f" alt="THESEED" /></a>
</p>

---

<p align="center"><i>Design By V0</i></p>
