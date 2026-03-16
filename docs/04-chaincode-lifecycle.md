# 04 - Ciclo de vida de un Chaincode (Smart Contract)

En Hyperledger Fabric, desplegar un chaincode no es un solo paso. Requiere un proceso de gobernanza donde **múltiples organizaciones deben aprobar** antes de que el chaincode sea operativo en el canal.

---

## Comparativa rápida: Solidity (EVM) vs Chaincode (Fabric)

| Aspecto | EVM (Ethereum) | Hyperledger Fabric |
|---|---|---|
| Lenguajes | Solidity, Vyper | Go, Node.js, Java |
| Despliegue | Una transacción | 4 pasos (package → install → approve → commit) |
| Quién despliega | Cualquier cuenta | Solo organizaciones autorizadas |
| Actualización | Proxy pattern / nuevo deploy | Incrementar `sequence` + re-aprobar |
| Estado | Mapping en storage | World State (LevelDB o CouchDB) |
| Ejecución | En todos los nodos | Solo en endorsing peers |
| Determinismo | Garantizado por EVM | Responsabilidad del desarrollador |

---

## El flujo de 4 pasos

```
┌──────────┐    ┌──────────┐    ┌─────────────────┐    ┌──────────┐
│ 1.Package│───▶│ 2.Install│───▶│ 3.Approve (x org)│───▶│ 4.Commit │
└──────────┘    └──────────┘    └─────────────────┘    └──────────┘
     │               │                  │                    │
  Crear .tar.gz   Subir a cada     Cada org vota       Se activa en
  con el código   peer que         a favor              el canal
                  endorse
```

---

## Prerequisitos

Estos ejemplos asumen que tienes la red levantada (ver docs anteriores) y las variables de entorno configuradas:

```bash
export PATH=${PWD}/../bin:$PATH
export FABRIC_CFG_PATH=${PWD}/../config/
```

---

## Paso 1: Empaquetar el chaincode

### Go

```bash
# Descargar dependencias del módulo Go
cd ../asset-transfer-basic/chaincode-go
GO111MODULE=on go mod vendor
cd ../../test-network

# Empaquetar
peer lifecycle chaincode package basic.tar.gz \
  --path ../asset-transfer-basic/chaincode-go/ \
  --lang golang \
  --label basic_1.0
```

### Node.js

```bash
cd ../asset-transfer-basic/chaincode-javascript
npm install
cd ../../test-network

peer lifecycle chaincode package basic.tar.gz \
  --path ../asset-transfer-basic/chaincode-javascript/ \
  --lang node \
  --label basic_1.0
```

### Java

```bash
cd ../asset-transfer-basic/chaincode-java
./gradlew installDist
cd ../../test-network

peer lifecycle chaincode package basic.tar.gz \
  --path ../asset-transfer-basic/chaincode-java/ \
  --lang java \
  --label basic_1.0
```

**Resultado:** archivo `basic.tar.gz` en el directorio actual.

**Parámetros:**
| Flag | Descripción |
|---|---|
| `--path` | Ruta al código fuente |
| `--lang` | Lenguaje: `golang`, `node`, `java` |
| `--label` | Etiqueta identificativa (nombre_versión) |

---

## Paso 2: Instalar en los peers

El chaincode debe instalarse en **cada peer que vaya a endosar transacciones**.

### Instalar en peer0.org1

```bash
# Configurar entorno como Org1
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

peer lifecycle chaincode install basic.tar.gz
```

### Instalar en peer0.org2

```bash
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051

peer lifecycle chaincode install basic.tar.gz
```

### Consultar el Package ID (lo necesitarás para aprobar)

```bash
peer lifecycle chaincode queryinstalled
```

Resultado:

```
Installed chaincodes on peer:
Package ID: basic_1.0:abc123def456..., Label: basic_1.0
```

Guardar el Package ID:

```bash
export CC_PACKAGE_ID=basic_1.0:abc123def456...
```

---

## Paso 3: Aprobar el chaincode por organización

**Cada organización** del canal debe aprobar la definición del chaincode. La aprobación se hace con el admin de cada org.

### Aprobar como Org1

```bash
# Asegurarse de estar como Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt

peer lifecycle chaincode approveformyorg \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  --channelID mychannel \
  --name basic \
  --version 1.0 \
  --package-id $CC_PACKAGE_ID \
  --sequence 1
```

### Aprobar como Org2

```bash
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt

peer lifecycle chaincode approveformyorg \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  --channelID mychannel \
  --name basic \
  --version 1.0 \
  --package-id $CC_PACKAGE_ID \
  --sequence 1
```

### Verificar quién ha aprobado

```bash
peer lifecycle chaincode checkcommitreadiness \
  --channelID mychannel \
  --name basic \
  --version 1.0 \
  --sequence 1 \
  --output json
```

Resultado:

```json
{
  "approvals": {
    "Org1MSP": true,
    "Org2MSP": true
  }
}
```

---

## Paso 4: Commit (activar en el canal)

Una vez que la **mayoría** de organizaciones han aprobado (según la política de lifecycle), se hace el commit:

```bash
peer lifecycle chaincode commit \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  --channelID mychannel \
  --name basic \
  --version 1.0 \
  --sequence 1 \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
```

### Verificar que el chaincode está activo

```bash
peer lifecycle chaincode querycommitted --channelID mychannel --name basic
```

---

## 5. Invocar y consultar

### Inicializar

```bash
peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel \
  -n basic \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"InitLedger","Args":[]}'
```

### Consultar

```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

### Invocar una función

```bash
peer chaincode invoke \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  -C mychannel \
  -n basic \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
  -c '{"function":"CreateAsset","Args":["asset7","yellow","10","Elena","500"]}'
```

---

## 6. Actualizar un chaincode

Para actualizar un chaincode ya desplegado, repetir el flujo con **sequence incrementado**:

```bash
# 1. Empaquetar nueva versión
peer lifecycle chaincode package basic_2.tar.gz \
  --path ../asset-transfer-basic/chaincode-go/ \
  --lang golang \
  --label basic_2.0

# 2. Instalar en todos los peers
peer lifecycle chaincode install basic_2.tar.gz

# 3. Obtener nuevo Package ID
peer lifecycle chaincode queryinstalled
export CC_PACKAGE_ID=basic_2.0:...

# 4. Aprobar con sequence=2 (cada org)
peer lifecycle chaincode approveformyorg \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  --channelID mychannel \
  --name basic \
  --version 2.0 \
  --package-id $CC_PACKAGE_ID \
  --sequence 2

# 5. Commit con sequence=2
peer lifecycle chaincode commit \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" \
  --channelID mychannel \
  --name basic \
  --version 2.0 \
  --sequence 2 \
  --peerAddresses localhost:7051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
  --peerAddresses localhost:9051 \
  --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt"
```

> **Nota importante:** El world state se **preserva** entre actualizaciones. No se pierden datos.

---

## 7. Políticas de endorsement

Por defecto, se aplica la política `MAJORITY Endorsement` (mayoría de las orgs deben endosar). Se puede personalizar:

### Al aprobar/commit

```bash
# Requiere endorsement de AMBAS orgs
--signature-policy "AND('Org1MSP.peer','Org2MSP.peer')"

# Requiere endorsement de CUALQUIERA
--signature-policy "OR('Org1MSP.peer','Org2MSP.peer')"

# Usar la política por defecto del canal
--channel-config-policy /Channel/Application/Endorsement
```

---

## Resumen de comandos del lifecycle

| Paso | Comando | Quién lo ejecuta |
|---|---|---|
| Empaquetar | `peer lifecycle chaincode package` | Cualquier admin |
| Instalar | `peer lifecycle chaincode install` | Admin de cada org (en su peer) |
| Consultar instalados | `peer lifecycle chaincode queryinstalled` | Admin del peer |
| Aprobar | `peer lifecycle chaincode approveformyorg` | Admin de cada org |
| Verificar aprobaciones | `peer lifecycle chaincode checkcommitreadiness` | Cualquiera |
| Commit | `peer lifecycle chaincode commit` | Cualquier admin (una vez) |
| Consultar committed | `peer lifecycle chaincode querycommitted` | Cualquiera |
| Invocar | `peer chaincode invoke` | Clientes autorizados |
| Consultar | `peer chaincode query` | Clientes autorizados |

---

**Anterior:** [03 - Crear una red personalizada](03-crear-red-personalizada.md)
**Siguiente:** [05 - Desarrollo de chaincodes](05-desarrollo-chaincodes.md)
