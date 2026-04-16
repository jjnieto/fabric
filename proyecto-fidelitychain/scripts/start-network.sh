#!/bin/bash
# start-network.sh — Levanta la red FidelityChain desde cero
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
NETWORK_DIR="$PROJECT_DIR/network"

echo "=== FidelityChain — Levantar red ==="
echo ""

cd "$NETWORK_DIR"

# 1. Generar certificados
echo "[1/5] Generando certificados..."
cryptogen generate --config=crypto-config.yaml --output=crypto-config
echo "OK"

# 2. Crear directorio de artefactos
mkdir -p channel-artifacts

# 3. Generar bloque genesis
echo "[2/5] Generando bloque genesis del canal..."
export FABRIC_CFG_PATH=$PWD
configtxgen -profile FidelityChannel \
  -outputBlock channel-artifacts/fidelity-channel.block \
  -channelID fidelity-channel
echo "OK"

# 4. Levantar Docker
echo "[3/5] Levantando contenedores Docker..."
docker compose -f docker/docker-compose.yaml up -d
echo "Esperando 5 segundos a que arranquen..."
sleep 5
echo "OK"

# 5. Crear canal (unir orderer)
echo "[4/5] Creando canal fidelity-channel..."
export ORDERER_CA=$NETWORK_DIR/crypto-config/ordererOrganizations/fidelitychain.com/orderers/orderer.fidelitychain.com/tls/ca.crt
export ORDERER_ADMIN_TLS_CERT=$NETWORK_DIR/crypto-config/ordererOrganizations/fidelitychain.com/orderers/orderer.fidelitychain.com/tls/server.crt
export ORDERER_ADMIN_TLS_KEY=$NETWORK_DIR/crypto-config/ordererOrganizations/fidelitychain.com/orderers/orderer.fidelitychain.com/tls/server.key

osnadmin channel join \
  --channelID fidelity-channel \
  --config-block channel-artifacts/fidelity-channel.block \
  -o localhost:7053 \
  --ca-file "$ORDERER_CA" \
  --client-cert "$ORDERER_ADMIN_TLS_CERT" \
  --client-key "$ORDERER_ADMIN_TLS_KEY"
echo "OK"

# 6. Unir peers
echo "[5/5] Uniendo peers al canal..."
export FABRIC_CFG_PATH=$HOME/fabric/fabric-samples/config
export CORE_PEER_TLS_ENABLED=true

# Hotel
export CORE_PEER_LOCALMSPID=HotelMSP
export CORE_PEER_TLS_ROOTCERT_FILE=$NETWORK_DIR/crypto-config/peerOrganizations/hotel.fidelitychain.com/peers/peer0.hotel.fidelitychain.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$NETWORK_DIR/crypto-config/peerOrganizations/hotel.fidelitychain.com/users/Admin@hotel.fidelitychain.com/msp
export CORE_PEER_ADDRESS=localhost:7051
peer channel join -b channel-artifacts/fidelity-channel.block
echo "  Hotel unido al canal"

# Cafeteria
export CORE_PEER_LOCALMSPID=CafeteriaMSP
export CORE_PEER_TLS_ROOTCERT_FILE=$NETWORK_DIR/crypto-config/peerOrganizations/cafeteria.fidelitychain.com/peers/peer0.cafeteria.fidelitychain.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$NETWORK_DIR/crypto-config/peerOrganizations/cafeteria.fidelitychain.com/users/Admin@cafeteria.fidelitychain.com/msp
export CORE_PEER_ADDRESS=localhost:9051
peer channel join -b channel-artifacts/fidelity-channel.block
echo "  Cafeteria unida al canal"

echo ""
echo "=== Red FidelityChain levantada ==="
echo ""
docker ps --format "table {{.Names}}\t{{.Status}}"
