# 03 - Crear una red Hyperledger Fabric personalizada desde cero

En esta guía creamos una red Fabric **sin usar la test-network**, configurando manualmente cada componente. Esto es lo que se haría en un entorno real de producción.

---

## Arquitectura objetivo

```
Red: mi-red
├── OrdererOrg
│   └── orderer.example.com (Raft, 1 nodo para simplificar)
├── Org1
│   └── peer0.org1.example.com
├── Org2
│   └── peer0.org2.example.com
└── Canal: canal-negocio
```

---

## 1. Crear la estructura de directorios

```bash
mkdir -p $HOME/mi-red/{configtx,crypto-config,channel-artifacts,docker,scripts}
cd $HOME/mi-red
```

---

## 2. Generar material criptográfico

### Opción A: Usando cryptogen (desarrollo)

#### 2.1 Crear `crypto-config.yaml`

Crea el archivo `crypto-config.yaml` en el directorio `$HOME/mi-red` con el siguiente contenido:

```yaml
# crypto-config.yaml
OrdererOrgs:
  - Name: Orderer
    Domain: example.com
    EnableNodeOUs: true
    Specs:
      - Hostname: orderer
        SANS:
          - localhost
          - 127.0.0.1

PeerOrgs:
  - Name: Org1
    Domain: org1.example.com
    EnableNodeOUs: true
    Template:
      Count: 1
      SANS:
        - localhost
        - 127.0.0.1
    Users:
      Count: 1

  - Name: Org2
    Domain: org2.example.com
    EnableNodeOUs: true
    Template:
      Count: 1
      SANS:
        - localhost
        - 127.0.0.1
    Users:
      Count: 1
```

> **Nota:** Copia solo el contenido YAML (desde `OrdererOrgs:` hasta el final).
> Puedes crear el archivo con `code crypto-config.yaml` desde la terminal de Ubuntu
> para abrirlo directamente en VS Code.

**Campos clave:**
- `EnableNodeOUs: true` — Habilita clasificación de identidades por tipo (admin, peer, client, orderer)
- `Template.Count` — Número de peers por organización
- `Users.Count` — Número de usuarios (además del Admin que se crea siempre)

#### 2.2 Generar los certificados

```bash
cryptogen generate --config=crypto-config.yaml --output=crypto-config
```

#### 2.3 Verificar la estructura generada

```bash
tree crypto-config --dirsfirst -L 4
```

Estructura resultante (simplificada):

```
crypto-config/
├── ordererOrganizations/
│   └── example.com/
│       ├── ca/                          # CA del orderer
│       ├── msp/                         # MSP de la org orderer
│       ├── orderers/
│       │   └── orderer.example.com/
│       │       ├── msp/                 # MSP del nodo orderer
│       │       └── tls/                 # Certificados TLS
│       ├── tlsca/                       # TLS CA
│       └── users/
│           └── Admin@example.com/
└── peerOrganizations/
    ├── org1.example.com/
    │   ├── ca/
    │   ├── msp/
    │   ├── peers/
    │   │   └── peer0.org1.example.com/
    │   │       ├── msp/
    │   │       └── tls/
    │   ├── tlsca/
    │   └── users/
    │       ├── Admin@org1.example.com/
    │       └── User1@org1.example.com/
    └── org2.example.com/
        └── (misma estructura que org1)
```

### Opción B: Usando Fabric CA (producción)

Ver [04 - Fabric CA en detalle](04-fabric-ca.md) para el flujo completo con CAs.

---

## 3. Configurar la topología de la red (configtx.yaml)

Este es el archivo más importante. Define organizaciones, políticas, orderer y perfiles de canales.

Crea el archivo `configtx.yaml` en el directorio `$HOME/mi-red` con el siguiente contenido:

```yaml
# configtx.yaml
---
Organizations:
  - &OrdererOrg
    Name: OrdererOrg
    ID: OrdererMSP
    MSPDir: crypto-config/ordererOrganizations/example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('OrdererMSP.member')"
      Writers:
        Type: Signature
        Rule: "OR('OrdererMSP.member')"
      Admins:
        Type: Signature
        Rule: "OR('OrdererMSP.admin')"
    OrdererEndpoints:
      - orderer.example.com:7050

  - &Org1
    Name: Org1MSP
    ID: Org1MSP
    MSPDir: crypto-config/peerOrganizations/org1.example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.peer', 'Org1MSP.client')"
      Writers:
        Type: Signature
        Rule: "OR('Org1MSP.admin', 'Org1MSP.client')"
      Admins:
        Type: Signature
        Rule: "OR('Org1MSP.admin')"
      Endorsement:
        Type: Signature
        Rule: "OR('Org1MSP.peer')"
    AnchorPeers:
      - Host: peer0.org1.example.com
        Port: 7051

  - &Org2
    Name: Org2MSP
    ID: Org2MSP
    MSPDir: crypto-config/peerOrganizations/org2.example.com/msp
    Policies:
      Readers:
        Type: Signature
        Rule: "OR('Org2MSP.admin', 'Org2MSP.peer', 'Org2MSP.client')"
      Writers:
        Type: Signature
        Rule: "OR('Org2MSP.admin', 'Org2MSP.client')"
      Admins:
        Type: Signature
        Rule: "OR('Org2MSP.admin')"
      Endorsement:
        Type: Signature
        Rule: "OR('Org2MSP.peer')"
    AnchorPeers:
      - Host: peer0.org2.example.com
        Port: 9051

Capabilities:
  Channel: &ChannelCapabilities
    V2_0: true
  Orderer: &OrdererCapabilities
    V2_0: true
  Application: &ApplicationCapabilities
    V2_0: true

Application: &ApplicationDefaults
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
    LifecycleEndorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
    Endorsement:
      Type: ImplicitMeta
      Rule: "MAJORITY Endorsement"
  Capabilities:
    <<: *ApplicationCapabilities

Orderer: &OrdererDefaults
  OrdererType: etcdraft
  BatchTimeout: 2s
  BatchSize:
    MaxMessageCount: 10
    AbsoluteMaxBytes: 99 MB
    PreferredMaxBytes: 512 KB
  EtcdRaft:
    Consenters:
      - Host: orderer.example.com
        Port: 7050
        ClientTLSCert: crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt
        ServerTLSCert: crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt
  Organizations:
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
    BlockValidation:
      Type: ImplicitMeta
      Rule: "ANY Writers"
  Capabilities:
    <<: *OrdererCapabilities

Channel: &ChannelDefaults
  Policies:
    Readers:
      Type: ImplicitMeta
      Rule: "ANY Readers"
    Writers:
      Type: ImplicitMeta
      Rule: "ANY Writers"
    Admins:
      Type: ImplicitMeta
      Rule: "MAJORITY Admins"
  Capabilities:
    <<: *ChannelCapabilities

Profiles:
  CanalNegocio:
    <<: *ChannelDefaults
    Orderer:
      <<: *OrdererDefaults
      Organizations:
        - *OrdererOrg
    Application:
      <<: *ApplicationDefaults
      Organizations:
        - *Org1
        - *Org2
```

> **Nota:** Copia solo el contenido YAML (desde `---` hasta el final).
> Puedes crear el archivo con `code configtx.yaml` desde la terminal de Ubuntu.

### Conceptos clave del configtx.yaml

| Sección | Propósito |
|---|---|
| **Organizations** | Define cada organización con su MSP y políticas |
| **Orderer** | Tipo de consenso (Raft), configuración de batches, consenters |
| **Application** | Políticas de aplicación (endorsement, lifecycle) |
| **Channel** | Políticas a nivel de canal |
| **Profiles** | Perfiles reutilizables para crear canales |
| **Capabilities** | Versión de funcionalidades habilitadas |

### Tipos de políticas

- **Signature**: Regla explícita (`OR('Org1MSP.admin')`)
- **ImplicitMeta**: Regla agregada sobre sub-políticas (`MAJORITY Admins` = mayoría de las políticas Admins de las organizaciones miembro)

---

## 4. Generar el bloque génesis del canal

```bash
export FABRIC_CFG_PATH=$PWD

configtxgen -profile CanalNegocio \
  -outputBlock channel-artifacts/canal-negocio.block \
  -channelID canal-negocio
```

Verificar que se generó:

```bash
ls -la channel-artifacts/
```

---

## 5. Configurar Docker Compose

### 5.1 Crear el archivo `docker/docker-compose.yaml`

Crea el archivo `docker/docker-compose.yaml` con el siguiente contenido:

```yaml
# docker/docker-compose.yaml
version: '3.7'

volumes:
  orderer.example.com:
  peer0.org1.example.com:
  peer0.org2.example.com:

networks:
  fabric-net:
    name: fabric-net

services:
  # ============================================================
  # ORDERER
  # ============================================================
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
    working_dir: /root
    command: orderer
    volumes:
      - ../crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/msp:/var/hyperledger/orderer/msp
      - ../crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls:/var/hyperledger/orderer/tls
      - orderer.example.com:/var/hyperledger/production/orderer
    ports:
      - 7050:7050
      - 7053:7053
    networks:
      - fabric-net

  # ============================================================
  # PEER0 ORG1
  # ============================================================
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
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric-net
    working_dir: /root
    command: peer node start
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - ../crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/msp:/etc/hyperledger/fabric/msp
      - ../crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls:/etc/hyperledger/fabric/tls
      - peer0.org1.example.com:/var/hyperledger/production
    ports:
      - 7051:7051
    networks:
      - fabric-net

  # ============================================================
  # PEER0 ORG2
  # ============================================================
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
      - CORE_VM_DOCKER_HOSTCONFIG_NETWORKMODE=fabric-net
    working_dir: /root
    command: peer node start
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - ../crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/msp:/etc/hyperledger/fabric/msp
      - ../crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls:/etc/hyperledger/fabric/tls
      - peer0.org2.example.com:/var/hyperledger/production
    ports:
      - 9051:9051
    networks:
      - fabric-net

  # ============================================================
  # CLI (herramienta para administrar la red)
  # ============================================================
  cli:
    container_name: cli
    image: hyperledger/fabric-tools:2.5
    tty: true
    stdin_open: true
    environment:
      - GOPATH=/opt/gopath
      - FABRIC_LOGGING_SPEC=INFO
      - CORE_PEER_ID=cli
      - CORE_PEER_ADDRESS=peer0.org1.example.com:7051
      - CORE_PEER_LOCALMSPID=Org1MSP
      - CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
      - CORE_PEER_TLS_ENABLED=true
      - CORE_PEER_TLS_CERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.crt
      - CORE_PEER_TLS_KEY_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/server.key
      - CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
    working_dir: /opt/gopath/src/github.com/hyperledger/fabric/peer
    command: /bin/bash
    volumes:
      - ../crypto-config:/opt/gopath/src/github.com/hyperledger/fabric/peer/organizations
      - ../channel-artifacts:/opt/gopath/src/github.com/hyperledger/fabric/peer/channel-artifacts
    networks:
      - fabric-net
    depends_on:
      - orderer.example.com
      - peer0.org1.example.com
      - peer0.org2.example.com
```

> **Nota:** Copia solo el contenido YAML (desde `version: '3.7'` hasta el final).
> Puedes crear el archivo con `code docker/docker-compose.yaml` desde la terminal de Ubuntu.

---

## 6. Levantar la red

```bash
cd $HOME/mi-red
docker compose -f docker/docker-compose.yaml up -d
```

### Verificar que todos los contenedores están corriendo

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Resultado esperado:

```
NAMES                       STATUS
cli                         Up ...
peer0.org1.example.com      Up ...
peer0.org2.example.com      Up ...
orderer.example.com         Up ...
```

### Ver logs de un componente

```bash
docker logs orderer.example.com --tail 50
docker logs peer0.org1.example.com --tail 50
```

---

## 7. Crear el canal

### 7.1 Unir el orderer al canal con osnadmin

```bash
export ORDERER_CA=$HOME/mi-red/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt
export ORDERER_ADMIN_TLS_CERT=$HOME/mi-red/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.crt
export ORDERER_ADMIN_TLS_KEY=$HOME/mi-red/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/server.key

osnadmin channel join \
  --channelID canal-negocio \
  --config-block channel-artifacts/canal-negocio.block \
  -o localhost:7053 \
  --ca-file $ORDERER_CA \
  --client-cert $ORDERER_ADMIN_TLS_CERT \
  --client-key $ORDERER_ADMIN_TLS_KEY
```

### 7.2 Verificar que el canal se creó

```bash
osnadmin channel list \
  -o localhost:7053 \
  --ca-file $ORDERER_CA \
  --client-cert $ORDERER_ADMIN_TLS_CERT \
  --client-key $ORDERER_ADMIN_TLS_KEY
```

---

## 8. Unir los peers al canal

### 8.1 Unir peer0.org1

```bash
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/mi-red/crypto-config/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/mi-red/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

peer channel join -b channel-artifacts/canal-negocio.block
```

### 8.2 Unir peer0.org2

```bash
export CORE_PEER_LOCALMSPID=Org2MSP
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/mi-red/crypto-config/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=$HOME/mi-red/crypto-config/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp
export CORE_PEER_ADDRESS=localhost:9051

peer channel join -b channel-artifacts/canal-negocio.block
```

### 8.3 Verificar que los peers se unieron

```bash
# Desde Org1
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_ADDRESS=localhost:7051
export CORE_PEER_MSPCONFIGPATH=$HOME/mi-red/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
peer channel list
```

Resultado: `canal-negocio`

---

## 9. Configurar anchor peers

Los anchor peers permiten el descubrimiento entre organizaciones (gossip inter-org).

### 9.1 Obtener la configuración actual del canal

```bash
peer channel fetch config channel-artifacts/config_block.pb \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile $HOME/mi-red/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt \
  -c canal-negocio

# Decodificar
configtxlator proto_decode --input channel-artifacts/config_block.pb \
  --type common.Block --output channel-artifacts/config_block.json

# Extraer la config
jq '.data.data[0].payload.data.config' channel-artifacts/config_block.json > channel-artifacts/config.json
```

### 9.2 Añadir anchor peer para Org1

```bash
# Copia de la config
cp channel-artifacts/config.json channel-artifacts/config_modified.json

# Añadir anchor peer (usando jq)
jq '.channel_group.groups.Application.groups.Org1MSP.values += {
  "AnchorPeers": {
    "mod_policy": "Admins",
    "value": {
      "anchor_peers": [{"host": "peer0.org1.example.com", "port": 7051}]
    },
    "version": "0"
  }
}' channel-artifacts/config.json > channel-artifacts/config_modified.json

# Codificar ambas configs
configtxlator proto_encode --input channel-artifacts/config.json \
  --type common.Config --output channel-artifacts/config.pb
configtxlator proto_encode --input channel-artifacts/config_modified.json \
  --type common.Config --output channel-artifacts/modified_config.pb

# Calcular el delta
configtxlator compute_update --channel_id canal-negocio \
  --original channel-artifacts/config.pb \
  --updated channel-artifacts/modified_config.pb \
  --output channel-artifacts/config_update.pb

# Envolver en envelope
configtxlator proto_decode --input channel-artifacts/config_update.pb \
  --type common.ConfigUpdate --output channel-artifacts/config_update.json

echo '{"payload":{"header":{"channel_header":{"channel_id":"canal-negocio","type":2}},"data":{"config_update":'$(cat channel-artifacts/config_update.json)'}}}' | \
  jq . > channel-artifacts/config_update_in_envelope.json

configtxlator proto_encode --input channel-artifacts/config_update_in_envelope.json \
  --type common.Envelope --output channel-artifacts/config_update_in_envelope.pb

# Enviar la actualización
peer channel update -f channel-artifacts/config_update_in_envelope.pb \
  -c canal-negocio \
  -o localhost:7050 \
  --ordererTLSHostnameOverride orderer.example.com \
  --tls \
  --cafile $HOME/mi-red/crypto-config/ordererOrganizations/example.com/orderers/orderer.example.com/tls/ca.crt
```

> Repetir el proceso análogo para Org2 (cambiando Org1MSP por Org2MSP y el puerto a 9051).

---

## 10. Apagar y limpiar

### Apagar la red (conservando datos)

```bash
docker compose -f docker/docker-compose.yaml down
```

### Apagar y eliminar todo (volúmenes incluidos)

```bash
docker compose -f docker/docker-compose.yaml down -v
rm -rf crypto-config channel-artifacts/*.block channel-artifacts/*.pb channel-artifacts/*.json
```

---

## Resumen del flujo completo

```
1. crypto-config.yaml          → cryptogen generate     → Certificados
2. configtx.yaml               → configtxgen            → Bloque génesis del canal
3. docker-compose.yaml         → docker compose up      → Nodos corriendo
4. osnadmin channel join       →                        → Orderer en el canal
5. peer channel join           →                        → Peers en el canal
6. Configurar anchor peers     →                        → Gossip inter-org
```

---

**Anterior:** [02 - Test Network](02-test-network.md)
**Siguiente:** [04 - Fabric CA: gestión de identidades](04-fabric-ca.md)
