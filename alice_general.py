#!/usr/bin/env python3
"""ALICE GENERAL — V0 Public Node Agent
Zero external deps — stdlib only.
Autonomous: auto-heal, periodic chain sync, self-managing.
"""
import json, time, os, socket, threading, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("ALICE_PORT", "7781"))
ROLE = os.environ.get("ALICE_ROLE", "GENERAL")
RPC_URL = os.environ.get("RPC_URL", "http://127.0.0.1:8545")
CHAIN_ID = int(os.environ.get("CHAIN_ID", "31337"))
START = time.time()
VERSION = "V0"

request_count = 0
error_count = 0
chain_cache = {"block": 0, "synced": False, "last_check": 0}
agent_log = []


def log(msg):
    ts = time.strftime("%H:%M:%S")
    entry = f"[{ts}] {msg}"
    agent_log.append(entry)
    if len(agent_log) > 500:
        agent_log.pop(0)
    print(entry, flush=True)


def chain_rpc(method, params=None):
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1}).encode()
    req = urllib.request.Request(RPC_URL, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read())


def update_chain_cache():
    try:
        res = chain_rpc("eth_blockNumber")
        chain_cache["block"] = int(res["result"], 16)
        chain_cache["synced"] = True
        chain_cache["last_check"] = time.time()
    except Exception:
        chain_cache["synced"] = False


def autonomous_loop():
    """Background agent loop — chain sync, self-heal, periodic tasks."""
    log("Autonomous agent loop started")
    cycle = 0
    while True:
        cycle += 1
        try:
            update_chain_cache()
            if chain_cache["synced"]:
                if cycle % 30 == 1:
                    log(f"Chain OK — block {chain_cache['block']}")
            else:
                log("Chain DOWN — will retry")
        except Exception as e:
            log(f"Agent cycle error: {e}")
        time.sleep(10)


class AliceHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            return json.loads(self.rfile.read(length))
        return {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        global request_count
        request_count += 1
        path = self.path.split("?")[0]

        if path == "/health":
            self._json({"healthy": True, "role": ROLE, "version": VERSION, "uptime": int(time.time() - START)})

        elif path in ("/status", "/api/status"):
            self._json({
                "agent": "ALICE",
                "role": ROLE,
                "version": VERSION,
                "node": socket.gethostname(),
                "uptime_s": int(time.time() - START),
                "requests": request_count,
                "errors": error_count,
                "services": {
                    "alice-general": {"status": "ACTIVE", "port": PORT},
                    "theseed-anvil": {
                        "status": "SYNCED" if chain_cache["synced"] else "DOWN",
                        "block": chain_cache["block"],
                        "chain_id": CHAIN_ID,
                    },
                },
                "capabilities": ["status", "health", "query", "chain", "node-info", "logs", "agent"],
                "autonomous": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })

        elif path == "/api/chain":
            update_chain_cache()
            if chain_cache["synced"]:
                self._json({"chain_id": CHAIN_ID, "block": chain_cache["block"], "status": "SYNCED", "rpc": RPC_URL})
            else:
                self._json({"chain_id": CHAIN_ID, "block": 0, "status": "DOWN"}, 503)

        elif path == "/api/node":
            identity_file = os.environ.get("NODE_IDENTITY", "/data/.node_identity.json")
            try:
                with open(identity_file) as f:
                    self._json(json.load(f))
            except Exception:
                self._json({"node_id": f"v0-{socket.gethostname()}", "type": "PUBLIC", "version": VERSION})

        elif path == "/api/logs":
            n = 50
            try:
                qs = self.path.split("?", 1)
                if len(qs) > 1:
                    for p in qs[1].split("&"):
                        if p.startswith("n="):
                            n = min(int(p[2:]), 500)
            except Exception:
                pass
            self._json({"logs": agent_log[-n:], "total": len(agent_log)})

        elif path == "/":
            self._json({
                "agent": "ALICE GENERAL",
                "version": VERSION,
                "role": ROLE,
                "node": socket.gethostname(),
                "autonomous": True,
                "endpoints": [
                    {"path": "/health", "method": "GET"},
                    {"path": "/status", "method": "GET"},
                    {"path": "/api/chain", "method": "GET"},
                    {"path": "/api/query", "method": "POST"},
                    {"path": "/api/node", "method": "GET"},
                    {"path": "/api/logs", "method": "GET"},
                    {"path": "/api/task", "method": "POST"},
                ],
            })
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        global request_count, error_count
        request_count += 1
        path = self.path.split("?")[0]

        if path == "/api/query":
            try:
                body = self._read_body()
            except Exception:
                body = {}
            q = body.get("input", body.get("query", ""))
            if not q:
                self._json({"error": "Provide 'input' or 'query' field"}, 400)
                return
            q_lower = q.lower()
            if any(w in q_lower for w in ["block", "chain", "height"]):
                update_chain_cache()
                self._json({"answer": f"Block {chain_cache['block']}, Chain {CHAIN_ID}", "block": chain_cache["block"]})
            elif any(w in q_lower for w in ["status", "uptime", "running"]):
                self._json({"answer": f"ALICE GENERAL up {int(time.time() - START)}s, {request_count} reqs", "uptime": int(time.time() - START)})
            elif any(w in q_lower for w in ["who", "what", "alice", "identity"]):
                self._json({"answer": "ALICE V0 — PUBLIC GENERAL agent on THESEED L0", "version": VERSION, "role": ROLE})
            elif any(w in q_lower for w in ["log", "history", "recent"]):
                self._json({"answer": "Recent agent activity", "logs": agent_log[-20:]})
            else:
                log(f"Query: {q[:100]}")
                self._json({"answer": f"ALICE GENERAL received: {q[:200]}", "capabilities": ["chain-status", "node-info", "block-height", "logs"]})

        elif path == "/api/task":
            try:
                body = self._read_body()
            except Exception:
                body = {}
            task = body.get("task", body.get("action", ""))
            if not task:
                self._json({"error": "Provide 'task' or 'action' field"}, 400)
                return
            log(f"Task received: {task[:100]}")
            if task == "sync_chain":
                update_chain_cache()
                self._json({"result": "synced", "block": chain_cache["block"]})
            elif task == "report":
                self._json({
                    "result": "report",
                    "uptime": int(time.time() - START),
                    "requests": request_count,
                    "errors": error_count,
                    "chain_synced": chain_cache["synced"],
                    "block": chain_cache["block"],
                })
            else:
                self._json({"result": f"Task '{task}' acknowledged — GENERAL role has limited execution", "accepted": True})

        else:
            error_count += 1
            self._json({"error": "not found"}, 404)


if __name__ == "__main__":
    log(f"ALICE GENERAL starting on 127.0.0.1:{PORT}")
    log(f"Role: {ROLE} | Chain: {CHAIN_ID} | RPC: {RPC_URL}")

    agent_thread = threading.Thread(target=autonomous_loop, daemon=True)
    agent_thread.start()

    server = HTTPServer(("127.0.0.1", PORT), AliceHandler)
    log("HTTP server ready")
    server.serve_forever()
