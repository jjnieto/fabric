#!/bin/bash
# clean-all.sh — Borra todo y deja el proyecto limpio para empezar de cero
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
NETWORK_DIR="$PROJECT_DIR/network"

echo "=== FidelityChain — Limpieza total ==="

# Parar contenedores y borrar volumenes
echo "Parando contenedores y borrando volumenes..."
docker compose -f "$NETWORK_DIR/docker/docker-compose.yaml" down -v 2>/dev/null || true

# Borrar certificados y artefactos
echo "Borrando certificados y artefactos..."
rm -rf "$NETWORK_DIR/crypto-config"
rm -rf "$NETWORK_DIR/channel-artifacts"
mkdir -p "$NETWORK_DIR/channel-artifacts"

# Borrar paquete de chaincode
rm -f "$PROJECT_DIR/fidelitypoints.tar.gz"

echo ""
echo "=== Limpieza completada. Puedes ejecutar start-network.sh para empezar de cero. ==="
