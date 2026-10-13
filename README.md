# ALICE V0 — Autonomous AI Agent

Public autonomous agent for V0 nodes. Zero external dependencies — runs on Python stdlib only.

## What it does

- **Health + status monitoring** — always-on health and status endpoints
- **Chain sync** — connects to THESEED L0 blockchain (chain 31337), background sync loop
- **Query endpoint** — ask ALICE about chain state, node info, uptime
- **Task endpoint** — send tasks (sync, report)
- **Agent logs** — access agent activity logs via API
- **Self-healing** — auto-recovers from chain disconnects

## Run with Docker

```bash
docker build -t alice-agent .
docker run -d --name alice-agent \
  -e ALICE_PORT=7781 \
  -e RPC_URL=http://host.docker.internal:8545 \
  -e CHAIN_ID=31337 \
  --network host \
  alice-agent
```

## Run directly

```bash
python3 alice_general.py
```

No `pip install` needed — uses only Python stdlib.

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | GET | Full node status |
| `/api/chain` | GET | Chain info (block, sync status) |
| `/api/query` | POST | Query the agent (`{"input": "..."}`) |
| `/api/task` | POST | Send task (`{"task": "sync_chain"}`) |
| `/api/node` | GET | Node identity |
| `/api/logs` | GET | Agent activity logs |

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `ALICE_PORT` | `7781` | HTTP server port |
| `ALICE_ROLE` | `GENERAL` | Agent role |
| `RPC_URL` | `http://127.0.0.1:8545` | Blockchain RPC endpoint |
| `CHAIN_ID` | `31337` | Chain ID |

## License

MIT
