# 06 - Operaciones de administracion

## Visión general

Este documento parte de la red montada con Fabric CA en el [doc 05](05-fabric-ca.md). Completamos la red con peers y orderer, desplegamos un chaincode y practicamos las operaciones de administracion mas comunes.

```mermaid
graph TB
    subgraph "Lo que vamos a hacer"
        A["0. Completar la red<br/>(peers + orderer + canal)"]
        B["1. Desplegar un<br/>chaincode"]
        C["2. Anadir organizacion<br/>al canal"]
        D["3. Actualizar config<br/>del canal"]
        E["4. Monitorizacion<br/>y logs"]
        F["5. Backup y<br/>recuperacion"]
        G["6. Rotacion de<br/>certificados"]
    end

    A --> B --> C
    A --> D
    A --> E
    A --> F
    A --> G

    style A fill:#EC0000,color:#fff
    style B fill:#22627E,color:#fff
    style C fill:#22627E,color:#fff
    style D fill:#0D9448,color:#fff
    style E fill:#0D9448,color:#fff
    style F fill:#B45D09,color:#fff
    style G fill:#7C3AED,color:#fff
```

---

## Prerequisitos

Debes haber completado el [doc 05](05-fabric-ca.md) hasta el paso 6 (todas las identidades generadas con Fabric CA). Deberias tener:

```
$HOME/red-con-ca/
├── fabric-ca/
│   ├── org1/        # CA de Org1 + identidades enrolladas
│   ├── org2/        # CA de Org2 + identidades enrolladas
│   └── orderer/     # CA del Orderer + identidades enrolladas
├── organizations/   # MSPs construidos
├── channel-artifacts/
└── docker/
    └── docker-compose-ca.yaml   # Las 3 CAs (ya corriendo)
```

---

## 0. Completar la red: peers, orderer y canal

El doc 05 monto las CAs y genero las identidades. Ahora levantamos los peers y el orderer que usan esos certificados.

### 0.1 Docker Compose para la red

Crea el archivo `docker/docker-compose-net.yaml`:

```yaml
# docker/docker-compose-net.yaml
version: '3.7'

volumes:
  orderer.example.com:
  peer0.org1.example.com:
  peer0.org2.example.com:

networks:
  fabric-ca-net:
    external: true
    name: fabric-ca-net

services:
  orderer.example.com:
    container_name: orderer.example.com
    image: hyperledger/fabric-orderer:2.5
    environment:
      - FABRIC_LOGGING_SPEC=INFO
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      - ORDERER_GENERAL_TLS_ENABLED=true
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_GENERAL_CLUSTER_CLIENTCERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_CLUSTER_CLIENTPRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_CLUSTER_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_GENERAL_BOOTSTRAPMETHOD=none
      - ORDERER_CHANNELPARTICIPATION_ENABLED=true
      - ORDERER_ADMIN_TLS_ENABLED=true
      - ORDERER_ADMIN_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_ADMIN_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_ADMIN_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_ADMIN_TLS_CLIENTROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
      - ORDERER_ADMIN_LISTENADDRESS=0.0.0.0:7053
      - ORDERER_OPERATIONS_LISTENADDRESS=orderer.example.com:9443
    command: orderer
    volumes:
      - ../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp
      - ../organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls:/var/hyperledger/orderer/tls
      - orderer.example.com:/var/hyperledger/production/orderer
    ports:
      - 7050:7050
      - 7053:7053
      - 9443:9443
    networks:
      - fabric-ca-net

  couchdb.org1:
    container_name: couchdb.org1
    image: couchdb:3.3
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=adminpw
    ports:
      - 5984:5984
    networks:
      - fabric-ca-net

  peer0.org1.example.com:
    container_name: peer0.org1.example.com
    image: hyperledger/fabric-peer:2.5
    environment:
      - FABRIC_LOGGING_SPEC=INFO
      - CORE_PEER_ID=peer0.org1.example.com
      - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
      - CORE_PEER_LISTENADDRESS=0.0.0.0:7051
      - CORE_PEER_CHAINCODEADDRESS=peer0.org1.example.com:7052
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:7052
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.org1.example.com:7051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer0.org1.example.com:7051
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/msp
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric-ca-net
      - CORE_LEDGER_STATE_STATEDATABASE=CouchDB
      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb.org1:5984
      - CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME=admin
      - CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD=adminpw
      - CORE_OPERATIONS_LISTENADDRESS=peer0.org1.example.com:9444
    command: peer node start
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - ../organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp:/etc/hyperledger/fabric/msp
      - ../organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls:/etc/hyperledger/fabric/tls
      - peer0.org1.example.com:/var/hyperledger/production
    ports:
      - 7051:7051
      - 9444:9444
    depends_on:
      - couchdb.org1
    networks:
      - fabric-ca-net

  couchdb.org2:
    container_name: couchdb.org2
    image: couchdb:3.3
    environment:
      - COUCHDB_USER=admin
      - COUCHDB_PASSWORD=adminpw
    ports:
      - 7984:5984
    networks:
      - fabric-ca-net

  peer0.org2.example.com:
    container_name: peer0.org2.example.com
    image: hyperledger/fabric-peer:2.5
    environment:
      - FABRIC_LOGGING_SPEC=INFO
      - CORE_PEER_ID=peer0.org2.example.com
      - CORE_PEER_ADDRESS=peer0.org2.example.com:9051
      - CORE_PEER_LISTENADDRESS=0.0.0.0:9051
      - CORE_PEER_CHAINCODEADDRESS=peer0.org2.example.com:9052
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:9052
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.org2.example.com:9051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer0.org2.example.com:9051
      - CORE_PEER_LOCALMSPID=Org2MSP
      - CORE_PEER_MSPCONFIGPATH=/etc/hyperledger/fabric/msp
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/etc/hyperledger/fabric/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/etc/hyperledger/fabric/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/etc/hyperledger/fabric/tls/ca.crt
      - CORE_VM_ENDPOINT=unix:///host/var/run/docker.sock
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric-ca-net
      - CORE_LEDGER_STATE_STATEDATABASE=CouchDB
      - CORE_LEDGER_STATE_COUCHDBCONFIG_COUCHDBADDRESS=couchdb.org2:5984
      - CORE_LEDGER_STATE_COUCHDBCONFIG_USERNAME=admin
      - CORE_LEDGER_STATE_COUCHDBCONFIG_PASSWORD=adminpw
      - CORE_OPERATIONS_LISTENADDRESS=peer0.org2.example.com:9445
    command: peer node start
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - ../organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/msp:/etc/hyperledger/fabric/msp
      - ../organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls:/etc/hyperledger/fabric/tls
      - peer0.org2.example.com:/var/hyperledger/production
    ports:
      - 9051:9051
      - 9445:9445
    depends_on:
      - couchdb.org2
    networks:
      - fabric-ca-net
```

### 0.2 Levantar la red

```bash
cd $HOME/red-con-ca
docker compose -f docker/docker-compose-net.yaml up -d
```

Verificar (deberias ver 8 contenedores: 3 CAs + orderer + 2 peers + 2 CouchDB):

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### 0.3 Crear canal y unir peers

```bash
# Variables comunes
export FABRIC_CFG_PATH=$PWD
export ORDERER_CA=$PWD/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt
export ORDERER_ADMIN_TLS_CERT=$PWD/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt
export ORDERER_ADMIN_TLS_KEY=$PWD/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.key

# Generar bloque genesis (necesitas un configtx.yaml — ver doc 03 como referencia)
configtxgen -profile TwoOrgsChannel \
  -outputBlock channel-artifacts/mychannel.block \
  -channelID mychannel

# Unir orderer al canal
osnadmin channel join \
  --channelID mychannel \
  --config-block channel-artifacts/mychannel.block \
  -o localhost:7053 \
  --ca-file $ORDERER_CA \
  --client-cert $ORDERER_ADMIN_TLS_CERT \
  --client-key $ORDERER_ADMIN_TLS_KEY

# Unir peer Org1
export FABRIC_CFG_PATH=$HOME/fabric/fabric-samples/config
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=$PWD/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

peer channel join -b channel-artifacts/mychannel.block

# Unir peer Org2
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_TLS_ROOTCERT_FILE=$PWD/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051

peer channel join -b channel-artifacts/mychannel.block
```

---

## 1. Desplegar un chaincode

Desplegamos el `asset-transfer-basic` de fabric-samples para tener algo con lo que trabajar.

```mermaid
graph LR
    P["Package"] --> I["Install"] --> A["Approve"] --> C["Commit"] --> T["Test"]
    style P fill:#7C3AED,color:#fff
    style I fill:#22627E,color:#fff
    style A fill:#B45D09,color:#fff
    style C fill:#0D9448,color:#fff
    style T fill:#EC0000,color:#fff
```

### 1.1 Preparar y empaquetar

```bash
cd $HOME/red-con-ca

# Preparar dependencias del chaincode
cd $HOME/fabric/fabric-samples/asset-transfer-basic/chaincode-go
GO111MODULE=on go mod vendor
cd $HOME/red-con-ca

# Empaquetar
peer lifecycle chaincode package basic.tar.gz \
  --path $HOME/fabric/fabric-samples/asset-transfer-basic/chaincode-go/ \
  --lang golang \
  --label basic_1.0
```

### 1.2 Instalar en ambos peers

```bash
# Variables comunes para el orderer
export ORDERER_CA=$PWD/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt
export PEER_ORG1_TLS=$PWD/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export PEER_ORG2_TLS=$PWD/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt

# Instalar en peer Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG1_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

peer lifecycle chaincode install basic.tar.gz

# Instalar en peer Org2
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG2_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp

peer lifecycle chaincode install basic.tar.gz
```

### 1.3 Obtener Package ID

```bash
peer lifecycle chaincode queryinstalled
export CC_PACKAGE_ID=basic_1.0:XXXX...
```

### 1.4 Aprobar como ambas orgs

```bash
# Aprobar como Org2 (ya estamos como Org2)
peer lifecycle chaincode approveformyorg \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  --channelID mychannel --name basic --version 1.0 \
  --package-id $CC_PACKAGE_ID --sequence 1

# Aprobar como Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG1_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

peer lifecycle chaincode approveformyorg \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  --channelID mychannel --name basic --version 1.0 \
  --package-id $CC_PACKAGE_ID --sequence 1
```

### 1.5 Verificar y commit

```bash
# Verificar aprobaciones
peer lifecycle chaincode checkcommitreadiness \
  --channelID mychannel --name basic --version 1.0 --sequence 1 --output json

# Commit
peer lifecycle chaincode commit \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  --channelID mychannel --name basic --version 1.0 --sequence 1 \
  --peerAddresses localhost:7051 --tlsRootCertFiles $PEER_ORG1_TLS \
  --peerAddresses localhost:9051 --tlsRootCertFiles $PEER_ORG2_TLS
```

### 1.6 Probar que funciona

```bash
# Inicializar
peer chaincode invoke \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  -C mychannel -n basic \
  --peerAddresses localhost:7051 --tlsRootCertFiles $PEER_ORG1_TLS \
  --peerAddresses localhost:9051 --tlsRootCertFiles $PEER_ORG2_TLS \
  -c '{"function":"InitLedger","Args":[]}'

# Consultar
peer chaincode query -C mychannel -n basic \
  -c '{"Args":["GetAllAssets"]}'
```

Si ves una lista de activos en JSON, la red esta operativa y el chaincode funciona. Ya podemos practicar las operaciones de administracion.

---

## 2. Añadir una nueva organización al canal

Esta es una de las operaciones mas complejas en Fabric. Un nuevo socio se une al consorcio y necesita participar en un canal existente.

### Flujo general

```mermaid
sequenceDiagram
    participant NewOrg as Nueva Org (Org3)
    participant Admin as Admin existente
    participant Orderer as Orderer
    participant Canal as Canal

    Note over NewOrg: 1. Preparar material criptografico
    NewOrg->>NewOrg: Generar certs con Fabric CA
    NewOrg->>Admin: Entregar MSP de Org3

    Note over Admin,Orderer: 2. Actualizar config del canal
    Admin->>Orderer: Fetch config actual
    Admin->>Admin: Anadir Org3 al JSON de config
    Admin->>Admin: Calcular delta (config update)
    Admin->>Orderer: Enviar config update firmada

    Note over NewOrg,Canal: 3. Unir peer al canal
    NewOrg->>Orderer: Obtener bloque genesis
    NewOrg->>Canal: peer channel join
```

### Paso a paso

#### 2.1 Generar identidades de la nueva org con Fabric CA

Levantar una CA para Org3 (añadir al docker-compose-ca.yaml o crear uno nuevo):

```bash
# Enrollar admin bootstrap de Org3
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/org3/admin
fabric-ca-client enroll \
  -u https://admin:adminpw@localhost:10054 \
  --caname ca-org3 \
  --tls.certfiles $PWD/fabric-ca/org3/tls-cert.pem

# Registrar y enrollar peer de Org3
fabric-ca-client register --caname ca-org3 \
  --id.name peer0 --id.secret peer0pw --id.type peer \
  --tls.certfiles $PWD/fabric-ca/org3/tls-cert.pem

export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/org3/peer0
fabric-ca-client enroll \
  -u https://peer0:peer0pw@localhost:10054 \
  --caname ca-org3 \
  --csr.hosts peer0.org3.example.com,localhost \
  --tls.certfiles $PWD/fabric-ca/org3/tls-cert.pem

# Construir MSP de Org3 (misma estructura que Org1/Org2)
```

#### 2.2 Generar la definición JSON de Org3

Anade Org3 al `configtx.yaml` y genera su definición:

```bash
export FABRIC_CFG_PATH=$PWD
configtxgen -printOrg Org3MSP > channel-artifacts/org3-definition.json
```

#### 2.3 Obtener la config actual del canal

```bash
# Como Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG1_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

peer channel fetch config channel-artifacts/config_block.pb \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  -c mychannel

configtxlator proto_decode --input channel-artifacts/config_block.pb \
  --type common.Block --output channel-artifacts/config_block.json

jq '.data.data[0].payload.data.config' channel-artifacts/config_block.json \
  > channel-artifacts/config.json
```

#### 2.4 Añadir Org3 a la configuración

```bash
jq -s '.[0] * {"channel_group":{"groups":{"Application":{"groups":{
  "Org3MSP":.[1]}}}}}' \
  channel-artifacts/config.json \
  channel-artifacts/org3-definition.json \
  > channel-artifacts/config_modified.json
```

#### 2.5 Calcular el delta

```bash
configtxlator proto_encode --input channel-artifacts/config.json \
  --type common.Config --output channel-artifacts/config.pb
configtxlator proto_encode --input channel-artifacts/config_modified.json \
  --type common.Config --output channel-artifacts/modified_config.pb

configtxlator compute_update --channel_id mychannel \
  --original channel-artifacts/config.pb \
  --updated channel-artifacts/modified_config.pb \
  --output channel-artifacts/config_update.pb

configtxlator proto_decode --input channel-artifacts/config_update.pb \
  --type common.ConfigUpdate --output channel-artifacts/config_update.json

echo '{"payload":{"header":{"channel_header":{
  "channel_id":"mychannel","type":2}},
  "data":{"config_update":'$(cat channel-artifacts/config_update.json)'}}}' | \
  jq . > channel-artifacts/config_update_envelope.json

configtxlator proto_encode --input channel-artifacts/config_update_envelope.json \
  --type common.Envelope --output channel-artifacts/config_update_envelope.pb
```

#### 2.6 Firmar y enviar

```bash
# Org1 firma
peer channel signconfigtx -f channel-artifacts/config_update_envelope.pb

# Cambiar a Org2 para enviar (su firma se anade automaticamente)
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_ADDRESS=localhost:9051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG2_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp

peer channel update -f channel-artifacts/config_update_envelope.pb \
  -c mychannel \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA
```

#### 2.7 Unir el peer de Org3

```bash
export CORE_PEER_LOCALMSPID=Org3MSP
export CORE_PEER_ADDRESS=localhost:11051
export CORE_PEER_TLS_ROOTCERT_FILE=$PWD/organizations/peerOrganizations/org3.example.com/peers/peer0.org3.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org3.example.com/users/Admin@org3.example.com/msp

# Obtener bloque genesis
peer channel fetch 0 channel-artifacts/mychannel.block \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  -c mychannel

# Unirse
peer channel join -b channel-artifacts/mychannel.block
```

> **Nota:** Este proceso es complejo a proposito. Fabric requiere gobernanza: no puedes añadir una org sin el consentimiento de las existentes. Es una caracteristica, no un defecto.

---

## 3. Actualizar la configuración del canal

### Que se puede cambiar

| Parametro | Donde | Ejemplo |
|-----------|-------|---------|
| Batch timeout | Orderer | Cambiar de 2s a 1s para mas velocidad |
| Batch size | Orderer | Aumentar MaxMessageCount de 10 a 50 |
| Políticas | Canal/Application/Orderer | Cambiar MAJORITY a ALL |
| Anchor peers | Application.groups.OrgX | Añadir o cambiar anchor peers |
| ACLs | Application | Cambiar permisos de acceso a recursos |
| Capabilities | Canal/Orderer/Application | Habilitar nuevas features de Fabric |

### Proceso general

El patron es siempre el mismo (fetch → decode → modify → compute → submit):

```mermaid
graph LR
    F["1. Fetch config<br/>actual"] --> D["2. Decode<br/>a JSON"]
    D --> M["3. Modificar<br/>el JSON"]
    M --> C["4. Compute<br/>update (delta)"]
    C --> S["5. Sign + Submit<br/>la actualizacion"]

    style F fill:#22627E,color:#fff
    style D fill:#22627E,color:#fff
    style M fill:#B45D09,color:#fff
    style C fill:#22627E,color:#fff
    style S fill:#0D9448,color:#fff
```

### Ejemplo: cambiar el batch timeout

```bash
# Como Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_TLS_ROOTCERT_FILE=$PEER_ORG1_TLS
export CORE_PEER_MSPCONFIGPATH=$PWD/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp

# 1-2. Fetch y decode
peer channel fetch config channel-artifacts/config_block.pb \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA -c mychannel

configtxlator proto_decode --input channel-artifacts/config_block.pb \
  --type common.Block --output channel-artifacts/config_block.json

jq '.data.data[0].payload.data.config' channel-artifacts/config_block.json \
  > channel-artifacts/config.json

# 3. Modificar: batch timeout de 2s a 1s
jq '.channel_group.groups.Orderer.values.BatchTimeout.value.timeout = "1s"' \
  channel-artifacts/config.json > channel-artifacts/config_modified.json

# 4. Compute update
configtxlator proto_encode --input channel-artifacts/config.json \
  --type common.Config --output channel-artifacts/config.pb
configtxlator proto_encode --input channel-artifacts/config_modified.json \
  --type common.Config --output channel-artifacts/modified_config.pb

configtxlator compute_update --channel_id mychannel \
  --original channel-artifacts/config.pb \
  --updated channel-artifacts/modified_config.pb \
  --output channel-artifacts/config_update.pb

configtxlator proto_decode --input channel-artifacts/config_update.pb \
  --type common.ConfigUpdate --output channel-artifacts/config_update.json

echo '{"payload":{"header":{"channel_header":{
  "channel_id":"mychannel","type":2}},
  "data":{"config_update":'$(cat channel-artifacts/config_update.json)'}}}' | \
  jq . > channel-artifacts/config_update_envelope.json

configtxlator proto_encode --input channel-artifacts/config_update_envelope.json \
  --type common.Envelope --output channel-artifacts/config_update_envelope.pb

# 5. Enviar
peer channel update -f channel-artifacts/config_update_envelope.pb \
  -c mychannel \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA
```

---

## 4. Monitorización y logs

### Logs de los contenedores

```bash
# Ver logs en tiempo real
docker logs -f peer0.org1.example.com
docker logs -f orderer.example.com

# Ultimas 100 lineas
docker logs --tail 100 peer0.org1.example.com

# Filtrar por nivel
docker logs peer0.org1.example.com 2>&1 | grep -i error
```

### Niveles de log

Se controlan con la variable `FABRIC_LOGGING_SPEC`:

```bash
# En docker-compose: FABRIC_LOGGING_SPEC=INFO
# Mas detalle:       FABRIC_LOGGING_SPEC=DEBUG
# Solo un modulo:    FABRIC_LOGGING_SPEC=INFO:gossip=DEBUG:msp=DEBUG

# Cambiar en caliente (sin reiniciar el contenedor)
docker exec peer0.org1.example.com \
  peer node logsetlevel gossip DEBUG
```

| Nivel | Cuando usarlo |
|-------|--------------|
| `ERROR` | Producción (solo errores críticos) |
| `WARNING` | Producción (errores + advertencias) |
| `INFO` | Normal (operaciones principales) |
| `DEBUG` | Diagnostico (muy verboso, solo temporal) |

### Métricas con Operations API

Los peers y el orderer exponen métricas en sus puertos de operaciones (configurados en el docker-compose):

```bash
# Health check del peer Org1 (puerto 9444)
curl -s http://localhost:9444/healthz

# Health check del orderer (puerto 9443)
curl -s http://localhost:9443/healthz

# Metricas en formato Prometheus
curl -s http://localhost:9444/metrics | head -20
```

Métricas útiles:

| Métrica | Que indica |
|---------|-----------|
| `endorser_proposal_duration` | Tiempo de endorsement |
| `ledger_block_processing_time` | Tiempo de procesado de bloque |
| `ledger_blockchain_height` | Número de bloques en el ledger |
| `gossip_state_height` | Altura del state según gossip |
| `chaincode_launch_duration` | Tiempo de arranque del chaincode |

```mermaid
graph LR
    P["Peers<br/>:9444, :9445"] --> |"/metrics"| PROM["Prometheus<br/>(recolecta metricas)"]
    O["Orderer<br/>:9443"] --> |"/metrics"| PROM
    PROM --> GRAF["Grafana<br/>(dashboards)"]

    style PROM fill:#B45D09,color:#fff
    style GRAF fill:#0D9448,color:#fff
```

> En producción se configura Prometheus para recolectar métricas y Grafana para visualizarlas.

---

## 5. Backup y recuperacion

### Que hay que respaldar

```mermaid
graph TB
    subgraph "Datos criticos a respaldar"
        A["Ledger<br/>(bloques + world state)"]
        B["Material criptografico<br/>(certs + claves)"]
        C["Configuracion<br/>(yaml, docker-compose)"]
    end

    A --> |"Volumen Docker:<br/>/var/hyperledger/production"| BA["Backup del volumen"]
    B --> |"Directorio:<br/>organizations/ + fabric-ca/"| BB["Backup del directorio"]
    C --> |"Archivos yaml"| BC["Backup en git"]

    style A fill:#EC0000,color:#fff
    style B fill:#EC0000,color:#fff
    style C fill:#B45D09,color:#fff
```

| Que | Donde esta | Frecuencia | Criticidad |
|-----|-----------|-----------|------------|
| **Claves privadas** | `organizations/*/keystore/` y `fabric-ca/*/` | Una vez (no cambian) | **CRITICA** |
| **Certificados** | `organizations/*/signcerts/` | Al renovar | Alta |
| **Ledger** | Volumen Docker del peer | Periodica | Alta (se reconstruye desde otros peers) |
| **World State** | Volumen Docker (CouchDB) | Periodica | Media (se reconstruye desde bloques) |
| **Configuración** | Archivos yaml | En cada cambio | Alta (tener en git) |
| **Fabric CA database** | `fabric-ca/*/fabric-ca-server.db` | Periodica | **CRITICA** (registro de identidades) |

### Backup del ledger

```bash
# Opcion A: parar y copiar
docker stop peer0.org1.example.com
docker cp peer0.org1.example.com:/var/hyperledger/production ./backup-peer0-org1
docker start peer0.org1.example.com

# Opcion B: snapshot sin parar (Fabric 2.5+)
peer snapshot submitrequest \
  -c mychannel \
  --peerAddress localhost:7051 \
  --tlsRootCertFiles $PEER_ORG1_TLS
```

### Recuperacion

```mermaid
graph TB
    LOST["Peer perdido"] --> A["Opcion A:<br/>Restaurar backup"]
    LOST --> B["Opcion B:<br/>Unirse desde cero"]

    A --> A1["Restaurar volumen → arrancar → sincroniza bloques faltantes"]
    B --> B1["Arrancar limpio → peer channel join → descarga TODO"]

    style A fill:#0D9448,color:#fff
    style B fill:#B45D09,color:#fff
```

---

## 6. Rotación de certificados TLS

Usando la Fabric CA del doc 05, renovar certificados es sencillo:

```bash
# 1. Reenrollar el peer con nuevos certs
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/org1/peer0

fabric-ca-client reenroll \
  --caname ca-org1 \
  --csr.hosts peer0.org1.example.com,localhost \
  --tls.certfiles $PWD/fabric-ca/org1/tls-cert.pem

# 2. Copiar los nuevos certs al MSP del peer
cp $FABRIC_CA_CLIENT_HOME/msp/signcerts/cert.pem \
   $PWD/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt
cp $FABRIC_CA_CLIENT_HOME/msp/keystore/*_sk \
   $PWD/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key

# 3. Reiniciar el peer
docker restart peer0.org1.example.com

# 4. Verificar que sigue funcionando
peer channel list
```

### Calendario de rotación

| Componente | Frecuencia | Impacto |
|-----------|-----------|---------|
| TLS de peers | Cada 12 meses | Reinicio del peer (segundos) |
| TLS de orderers | Cada 12 meses | Coordinar con cluster Raft |
| Enrollment certs | Según política | Sin reinicio |
| CA root cert | Cada 5-10 años | Renovación completa |

---

## Resumen de comandos de administracion

| Operación | Comando |
|-----------|---------|
| Ver canales de un peer | `peer channel list` |
| Info de un canal | `peer channel getinfo -c mychannel` |
| Fetch config | `peer channel fetch config` |
| Actualizar config | `configtxlator compute_update` + `peer channel update` |
| Ver chaincodes instalados | `peer lifecycle chaincode queryinstalled` |
| Ver chaincodes activos | `peer lifecycle chaincode querycommitted` |
| Cambiar log level en caliente | `docker exec <peer> peer node logsetlevel <modulo> <NIVEL>` |
| Health check | `curl http://localhost:9444/healthz` |
| Métricas Prometheus | `curl http://localhost:9444/metrics` |
| Listar canales del orderer | `osnadmin channel list` |
| Snapshot | `peer snapshot submitrequest` |
| Revocar certificado | `fabric-ca-client revoke` |
| Renovar certificado | `fabric-ca-client reenroll` |

---

**Anterior:** [05 - Fabric CA](05-fabric-ca.md)
