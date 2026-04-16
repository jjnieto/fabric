# 05 - Fabric CA: Gestion de identidades en produccion

## Por que Fabric CA

En los documentos anteriores usamos `cryptogen` para generar todos los certificados de golpe. Esto funciona para desarrollo, pero tiene limitaciones serias en produccion:

- **No puedes anadir nuevos usuarios** sin regenerar todo
- **No puedes revocar** un certificado comprometido
- **No puedes renovar** certificados que caducan
- **No hay registro** de quien solicito que certificado y cuando

Fabric CA es una **autoridad certificadora** real que resuelve todos estos problemas. Funciona como un servicio independiente al que las organizaciones envian peticiones para registrar y enrollar identidades.

```mermaid
graph TB
    subgraph "Con cryptogen (desarrollo)"
        CG["cryptogen"] --> |"Genera todo de golpe"| CERTS1["Todos los certs"]
        CERTS1 -. "No se pueden anadir,<br/>revocar ni renovar" .-> X["Limitado"]
    end

    subgraph "Con Fabric CA (produccion)"
        CA["Fabric CA Server"] --> |"register"| ID["Identidad registrada"]
        ID --> |"enroll"| CERT["Certificado emitido"]
        CA --> |"revoke"| REV["Certificado revocado"]
        CA --> |"reenroll"| REN["Certificado renovado"]
    end

    style CG fill:#B45D09,color:#fff
    style X fill:#EC0000,color:#fff
    style CA fill:#0D9448,color:#fff
    style CERT fill:#0D9448,color:#fff
```

> **Analogia:** `cryptogen` es como imprimir todos los DNIs de un pais de golpe el dia de la fundacion. Fabric CA es el registro civil: emite DNIs bajo demanda, los renueva cuando caducan y los invalida si se pierden.

---

## Arquitectura de Fabric CA

En una red real, **cada organizacion tiene su propia Fabric CA**. La CA de Org1 solo emite certificados para miembros de Org1, y la CA de Org2 solo para los suyos.

```mermaid
graph TB
    subgraph "Red Fabric"
        subgraph Org1["Org1"]
            CA1["Fabric CA Org1<br/>Puerto: 7054"]
            CA1 --> P1["peer0.org1<br/>(cert emitido por CA1)"]
            CA1 --> A1["Admin@org1<br/>(cert emitido por CA1)"]
            CA1 --> U1["User1@org1<br/>(cert emitido por CA1)"]
        end

        subgraph Org2["Org2"]
            CA2["Fabric CA Org2<br/>Puerto: 8054"]
            CA2 --> P2["peer0.org2<br/>(cert emitido por CA2)"]
            CA2 --> A2["Admin@org2<br/>(cert emitido por CA2)"]
        end

        subgraph OrdererOrg["OrdererOrg"]
            CA0["Fabric CA Orderer<br/>Puerto: 9054"]
            CA0 --> ORD["orderer<br/>(cert emitido por CA0)"]
        end
    end

    style CA1 fill:#7C3AED,color:#fff
    style CA2 fill:#7C3AED,color:#fff
    style CA0 fill:#7C3AED,color:#fff
```

Fabric CA tiene dos componentes:
- **fabric-ca-server**: el servidor que gestiona las identidades (uno por org)
- **fabric-ca-client**: el CLI que usan los admins para interactuar con el server

---

## Conceptos clave

### Register vs Enroll

Estas son las dos operaciones fundamentales de Fabric CA y es importante no confundirlas:

```mermaid
sequenceDiagram
    participant Admin as Admin de la Org
    participant CA as Fabric CA Server
    participant User as Nuevo usuario

    Note over Admin,CA: REGISTER (crear la identidad)
    Admin->>CA: register --id.name juan --id.secret password123
    CA->>CA: Guarda: juan puede enrollarse
    CA-->>Admin: OK, identidad registrada

    Note over User,CA: ENROLL (obtener el certificado)
    User->>CA: enroll -u https://juan:password123@ca:7054
    CA->>CA: Genera cert X.509 para juan
    CA-->>User: Certificado + clave privada
```

| Operacion | Quien la ejecuta | Que hace | Resultado |
|-----------|-----------------|----------|-----------|
| **register** | Admin de la org | Crea una identidad en la CA | La identidad existe pero aun no tiene certificado |
| **enroll** | El propio usuario | Solicita su certificado a la CA | Obtiene cert X.509 + clave privada |

> **Analogia:** Register es como dar de alta a un ciudadano en el padron. Enroll es cuando ese ciudadano va a la oficina a recoger su DNI.

### Atributos y tipos

Al registrar una identidad se puede especificar:
- **Tipo**: `client`, `peer`, `orderer`, `admin`
- **Atributos personalizados**: `role=auditor`, `department=legal`, etc.
- **Afiliacion**: la posicion en la jerarquia de la org (`org1.department1`)

Estos atributos quedan embebidos en el certificado X.509 y pueden usarse para control de acceso en los chaincodes (ABAC).

---

## Despliegue de Fabric CA con Docker

### Docker Compose para una CA

```yaml
# Ejemplo: CA para la organizacion Hotel
ca.hotel.fidelitychain.com:
  container_name: ca.hotel.fidelitychain.com
  image: hyperledger/fabric-ca:1.5
  environment:
    - FABRIC_CA_HOME=/etc/hyperledger/fabric-ca-server
    - FABRIC_CA_SERVER_CA_NAME=ca-hotel
    - FABRIC_CA_SERVER_TLS_ENABLED=true
    - FABRIC_CA_SERVER_PORT=7054
    - FABRIC_CA_SERVER_OPERATIONS_LISTENADDRESS=0.0.0.0:17054
  ports:
    - 7054:7054
    - 17054:17054
  command: sh -c 'fabric-ca-server start -b admin:adminpw -d'
  volumes:
    - ./fabric-ca/hotel:/etc/hyperledger/fabric-ca-server
```

El flag `-b admin:adminpw` crea el usuario bootstrap (el primer admin que puede registrar a los demas). En produccion se usaria una contrasena segura.

### Verificar que la CA esta corriendo

```bash
# Debe responder con info de la CA
curl -k https://localhost:7054/cainfo
```

---

## Flujo completo: registrar identidades con Fabric CA

### Paso 1: Enrollar al admin bootstrap

El admin bootstrap es el primer usuario de la CA. Se creo al arrancar el server con `-b admin:adminpw`.

```bash
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/hotel/admin

fabric-ca-client enroll \
  -u https://admin:adminpw@localhost:7054 \
  --caname ca-hotel \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

Esto genera:
```
fabric-ca/hotel/admin/
├── msp/
│   ├── cacerts/          # Certificado raiz de la CA
│   ├── keystore/         # Clave privada del admin
│   ├── signcerts/        # Certificado del admin
│   └── IssuerPublicKey
└── fabric-ca-client-config.yaml
```

### Paso 2: Registrar un peer

```bash
fabric-ca-client register \
  --caname ca-hotel \
  --id.name peer0 \
  --id.secret peer0pw \
  --id.type peer \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

### Paso 3: Registrar un usuario

```bash
fabric-ca-client register \
  --caname ca-hotel \
  --id.name user1 \
  --id.secret user1pw \
  --id.type client \
  --id.attrs '"role=operator,department=reception"' \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

Los atributos `role=operator` y `department=reception` quedaran embebidos en el certificado de user1 y podran verificarse desde un chaincode con `GetAttributeValue("role")`.

### Paso 4: Enrollar el peer

```bash
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/hotel/peer0

fabric-ca-client enroll \
  -u https://peer0:peer0pw@localhost:7054 \
  --caname ca-hotel \
  --csr.hosts peer0.hotel.fidelitychain.com,localhost \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

El flag `--csr.hosts` anade SANs al certificado (equivalente a lo que haciamos con `SANS` en `crypto-config.yaml`).

### Paso 5: Enrollar al usuario

```bash
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/hotel/user1

fabric-ca-client enroll \
  -u https://user1:user1pw@localhost:7054 \
  --caname ca-hotel \
  --enrollment.attrs "role,department" \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

El flag `--enrollment.attrs` indica que atributos incluir en el certificado.

---

## Diagrama del flujo completo

```mermaid
sequenceDiagram
    participant CA as Fabric CA Server
    participant Admin as Admin bootstrap
    participant Peer as peer0
    participant User as user1

    Admin->>CA: enroll (admin:adminpw)
    CA-->>Admin: Cert admin

    Admin->>CA: register peer0 (type=peer)
    CA-->>Admin: OK

    Admin->>CA: register user1 (type=client, role=operator)
    CA-->>Admin: OK

    Peer->>CA: enroll (peer0:peer0pw)
    CA-->>Peer: Cert peer0

    User->>CA: enroll (user1:user1pw)
    CA-->>User: Cert user1 (con role=operator)
```

---

## Revocar un certificado

Cuando un certificado se ve comprometido o un empleado deja la organizacion, hay que revocarlo.

```bash
# Revocar el certificado de user1
fabric-ca-client revoke \
  --caname ca-hotel \
  -e user1 \
  -r "affiliationchange" \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

Despues de revocar, hay que **generar una nueva CRL** (Certificate Revocation List) y distribuirla a los peers:

```bash
# Generar CRL actualizada
fabric-ca-client gencrl \
  --caname ca-hotel \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

La CRL se coloca en el MSP de la organizacion (`msp/crls/`) y los peers la consultan para rechazar certificados revocados.

```mermaid
graph LR
    REV["Admin revoca cert"] --> CRL["Genera nueva CRL"]
    CRL --> MSP["Actualiza MSP<br/>de la org"]
    MSP --> PEERS["Peers rechazan<br/>cert revocado"]

    style REV fill:#EC0000,color:#fff
    style CRL fill:#B45D09,color:#fff
    style PEERS fill:#0D9448,color:#fff
```

> **Importante:** La revocacion no es instantanea. Los peers solo la aplican cuando se actualiza la CRL en su MSP. En produccion, automatizar este proceso es critico.

---

## Renovar un certificado (reenroll)

Los certificados tienen fecha de caducidad. Antes de que caduquen, el titular puede solicitar uno nuevo:

```bash
export FABRIC_CA_CLIENT_HOME=$PWD/fabric-ca/hotel/user1

fabric-ca-client reenroll \
  --caname ca-hotel \
  --tls.certfiles $PWD/fabric-ca/hotel/tls-cert.pem
```

El reenroll genera un nuevo certificado con la misma identidad y atributos, pero con nueva fecha de validez y nueva clave privada.

---

## Estructura del MSP con Fabric CA

Cuando usas Fabric CA, la estructura del MSP es la misma que con cryptogen, pero la gestionas tu:

```
msp/
├── cacerts/              # Certificado raiz de la CA de la org
│   └── ca-cert.pem
├── keystore/             # Clave privada de esta identidad
│   └── priv_sk
├── signcerts/            # Certificado de esta identidad
│   └── cert.pem
├── tlscacerts/           # Certificado raiz de la TLS CA
│   └── tlsca-cert.pem
├── crls/                 # Certificate Revocation Lists (opcional)
│   └── crl.pem
└── config.yaml           # Configuracion NodeOUs
```

El archivo `config.yaml` habilita NodeOUs para distinguir tipos de identidad:

```yaml
NodeOUs:
  Enable: true
  ClientOUIdentifier:
    Certificate: cacerts/ca-cert.pem
    OrganizationalUnitIdentifier: client
  PeerOUIdentifier:
    Certificate: cacerts/ca-cert.pem
    OrganizationalUnitIdentifier: peer
  AdminOUIdentifier:
    Certificate: cacerts/ca-cert.pem
    OrganizationalUnitIdentifier: admin
  OrdererOUIdentifier:
    Certificate: cacerts/ca-cert.pem
    OrganizationalUnitIdentifier: orderer
```

---

## cryptogen vs Fabric CA: cuando usar cada uno

| Aspecto | cryptogen | Fabric CA |
|---------|-----------|-----------|
| Uso | Desarrollo y testing | Produccion |
| Generacion | Todo de golpe | Bajo demanda |
| Anadir usuarios | Regenerar todo | `register` + `enroll` |
| Revocar | No es posible | `revoke` + `gencrl` |
| Renovar | No es posible | `reenroll` |
| Atributos custom | No | Si (`--id.attrs`) |
| Complejidad | Minima | Mayor (server + client) |
| Auditoria | No hay registro | Log completo de operaciones |

> **Regla practica:** Usa `cryptogen` para aprender y prototipar. Usa Fabric CA para cualquier cosa que se parezca a produccion.

---

## Troubleshooting

| Error | Causa | Solucion |
|-------|-------|----------|
| `Authorization failure` | El admin no esta enrollado o el token expiro | Re-enrollar al admin |
| `Identity already registered` | Ya existe un registro con ese nombre | Usar otro nombre o eliminar el existente |
| `Failed to connect to CA` | CA no esta corriendo o puerto incorrecto | Verificar con `docker ps` y `curl -k https://localhost:7054/cainfo` |
| `Certificate has expired` | El cert caduco | `reenroll` para obtener uno nuevo |
| `Certificate is revoked` | El cert esta en la CRL | Emitir una nueva identidad |

---

**Anterior:** [04 - Chaincode Lifecycle](04-chaincode-lifecycle.md)
**Siguiente:** [06 - Operaciones de administracion](06-operaciones-administracion.md)
