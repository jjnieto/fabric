#!/bin/bash
# stop-network.sh — Para la red conservando datos
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== FidelityChain — Parando red ==="
docker compose -f "$PROJECT_DIR/network/docker/docker-compose.yaml" down
echo "Red parada. Los datos se conservan en los volumenes Docker."
