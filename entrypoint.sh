#!/bin/bash
set -e
echo "◈ ALICE GENERAL — V0 PUBLIC NODE"
echo "  Port:     127.0.0.1:${ALICE_PORT:-7781}"
echo "  Role:     ${ALICE_ROLE:-GENERAL}"
echo "  Chain:    ${RPC_URL:-http://127.0.0.1:8545} (ID ${CHAIN_ID:-31337})"
exec python3 -u alice_general.py
