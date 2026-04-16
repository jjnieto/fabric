#!/bin/bash
# deploy-chaincode.sh — Despliega el chaincode fidelitypoints
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
NETWORK_DIR="$PROJECT_DIR/network"

echo "=== FidelityChain — Desplegar chaincode ==="
echo ""

cd "$PROJECT_DIR"

export FABRIC_CFG_PATH=$HOME/fabric/fabric-samples/config
export CORE_PEER_TLS_ENABLED=true

ORDERER_CA=$NETWORK_DIR/crypto-config/ordererOrganizations/fidelitychain.com/orderers/orderer.fidelitychain.com/msp/tlscacerts/tlsca.fidelitychain.com-cert.pem
PEER_HOTEL_TLS=$NETWORK_DIR/crypto-config/peerOrganizations/hotel.fidelitychain.com/peers/peer0.hotel.fidelitychain.com/tls/ca.crt
PEER_CAFE_TLS=$NETWORK_DIR/crypto-config/peerOrganizations/cafeteria.fidelitychain.com/peers/peer0.cafeteria.fidelitychain.com/tls/ca.crt

# 1. Empaquetar
echo "[1/6] Empaquetando chaincode..."
peer lifecycle chaincode package fidelitypoints.tar.gz \
  --path ./chaincode/chaincode-go/ \
  --lang golang \
  --label fidelitypoints_1.0
echo "OK"

# 2. Instalar en Hotel
echo "[2/6] Instalando en peer del Hotel..."
export CORE_PEER_LOCALMSPID=HotelMSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_HOTEL_TLS
export CORE_PEER_MSPCONFIGPATH=$NETWORK_DIR/crypto-config/peerOrganizations/hotel.fidelitychain.com/users/Admin@hotel.fidelitychain.com/msp
peer lifecycle chaincode install fidelitypoints.tar.gz
echo "OK"

# 3. Instalar en Cafeteria
echo "[3/6] Instalando en peer de la Cafeteria..."
export CORE_PEER_LOCALMSPID=CafeteriaMSP
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_CAFE_TLS
export CORE_PEER_MSPCONFIGPATH=$NETWORK_DIR/crypto-config/peerOrganizations/cafeteria.fidelitychain.com/users/Admin@cafeteria.fidelitychain.com/msp
peer lifecycle chaincode install fidelitypoints.tar.gz
echo "OK"

# 4. Obtener Package ID
echo "[4/6] Obteniendo Package ID..."
CC_PACKAGE_ID=$(peer lifecycle chaincode queryinstalled --output json | jq -r '.installed_chaincodes[0].package_id')
echo "  Package ID: $CC_PACKAGE_ID"

# 5. Aprobar
echo "[5/6] Aprobando chaincode..."

# Aprobar como Cafeteria (ya estamos como Cafeteria)
peer lifecycle chaincode approveformyorg \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.fidelitychain.com \
  --tls --cafile "$ORDERER_CA" \
  --channelID fidelity-channel \
  --name fidelitypoints --version 1.0 \
  --package-id "$CC_PACKAGE_ID" --sequence 1
echo "  Cafeteria aprobada"

# Aprobar como Hotel
export CORE_PEER_LOCALMSPID=HotelMSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_HOTEL_TLS
export CORE_PEER_MSPCONFIGPATH=$NETWORK_DIR/crypto-config/peerOrganizations/hotel.fidelitychain.com/users/Admin@hotel.fidelitychain.com/msp

peer lifecycle chaincode approveformyorg \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.fidelitychain.com \
  --tls --cafile "$ORDERER_CA" \
  --channelID fidelity-channel \
  --name fidelitypoints --version 1.0 \
  --package-id "$CC_PACKAGE_ID" --sequence 1
echo "  Hotel aprobado"

# Verificar
echo "  Verificando aprobaciones..."
peer lifecycle chaincode checkcommitreadiness \
  --channelID fidelity-channel \
  --name fidelitypoints --version 1.0 --sequence 1 --output json

# 6. Commit
echo "[6/6] Commit del chaincode..."
peer lifecycle chaincode commit \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.fidelitychain.com \
  --tls --cafile "$ORDERER_CA" \
  --channelID fidelity-channel \
  --name fidelitypoints --version 1.0 --sequence 1 \
  --peerAddresses localhost:7051 --tlsRootCertFiles "$PEER_HOTEL_TLS" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "$PEER_CAFE_TLS"
echo "OK"

# Verificar
echo ""
echo "Chaincode desplegado:"
peer lifecycle chaincode querycommitted --channelID fidelity-channel --name fidelitypoints

# Inicializar
echo ""
echo "Inicializando token..."
peer chaincode invoke \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.fidelitychain.com \
  --tls --cafile "$ORDERER_CA" \
  -C fidelity-channel -n fidelitypoints \
  --peerAddresses localhost:7051 --tlsRootCertFiles "$PEER_HOTEL_TLS" \
  --peerAddresses localhost:9051 --tlsRootCertFiles "$PEER_CAFE_TLS" \
  -c '{"function":"InitLedger","Args":[]}'

echo ""
echo "=== Chaincode fidelitypoints desplegado y listo ==="

# Limpiar
rm -f fidelitypoints.tar.gz
