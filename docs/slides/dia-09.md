# Día 9 — Arquitectura de Hyperledger Fabric en profundidad

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos del mundo enterprise blockchain - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre Hyperledger Fabric o blockchain empresarial. Ejemplos: nuevos miembros del consorcio Hyperledger, casos de uso en producción (trazabilidad, finanzas, sanidad), movimientos de IBM o empresas del ecosistema, adquisiciones, nuevas versiones de Fabric, etc. Actualizar antes de cada edición del curso.]

---

## Slide 2 — Portada sección

**Blockchain**
Cultura general: Los consorcios enterprise blockchain

[IMAGEN: Logos de R3 Corda, Enterprise Ethereum Alliance e Hyperledger sobre un fondo corporativo de rascacielos]

---

## Slide 3 — ¿Por qué las grandes empresas se unieron?

A partir de 2015, las grandes corporaciones vieron el potencial de la tecnología blockchain, pero no encajaban en el modelo público:

- **No querían tokens ni especulación:** su interés era la tecnología, no las criptomonedas
- **Necesitaban privacidad:** no podían poner datos corporativos en una red pública
- **Necesitaban identidad conocida:** regulaciones como KYC/AML exigen saber quién participa
- **Necesitaban rendimiento:** Ethereum hacía 15 TPS; un banco necesita miles
- **Necesitaban gobernanza clara:** ¿quién decide las reglas? En Bitcoin "nadie", pero en un consorcio empresarial necesitan un marco legal

**Solución:** crear consorcios para desarrollar plataformas blockchain permisionadas adaptadas al mundo corporativo.

---

## Slide 4 — Los tres grandes consorcios

| Consorcio | Fundación | Enfoque | Miembros destacados |
|-----------|-----------|---------|---------------------|
| **R3 Corda** | 2014 | Servicios financieros | Barclays, Goldman Sachs, JP Morgan, BBVA |
| **Enterprise Ethereum Alliance (EEA)** | 2017 | Estándares sobre Ethereum para empresas | Microsoft, Intel, Santander, ConsenSys |
| **Hyperledger (Linux Foundation)** | 2015 | Framework modular y agnóstico de industria | IBM, Intel, SAP, Airbus, Walmart, Maersk |

**Dato curioso:** muchas empresas participaban en los tres a la vez, cubriendo apuestas.

[NOTA PROFESOR: Enfatizar que no se trata de competencia directa: R3 Corda se centró en finanzas (trades, derivados), EEA quería estandarizar Ethereum para empresas manteniendo compatibilidad con la red pública, y Hyperledger apostó por modularidad y frameworks agnósticos. Cada uno resolvía necesidades distintas.]

---

## Slide 5 — Hyperledger: el paraguas

Hyperledger **no es una blockchain**. Es un conjunto de proyectos bajo la Linux Foundation:

| Proyecto | Descripción | Estado |
|----------|-------------|--------|
| **Fabric** | Framework de blockchain permisionada modular. El proyecto estrella | Activo, producción |
| **Sawtooth** | Blockchain modular con consenso PoET (Intel) | Mantenimiento |
| **Besu** | Cliente Ethereum en Java (compatible con redes públicas y privadas) | Activo |
| **Iroha** | Blockchain simple orientada a aplicaciones móviles | Mantenimiento |
| **Indy** | Identidad descentralizada (SSI) | Activo |
| **Aries** | Framework para agentes de identidad | Activo |
| **Firefly** | Supernode para conectar múltiples blockchains | Activo |

**Nuestro foco a partir de ahora: Hyperledger Fabric.**

[NOTA PROFESOR: Mencionar que Hyperledger Fabric fue propuesto originalmente por IBM y Digital Asset Holdings. Su primera versión estable (1.0) se lanzó en julio de 2017. La versión actual (2.5.x) incorpora mejoras significativas como ciclo de vida de chaincode descentralizado y gateway service.]

---

## Slide 6 — Portada sección

**Hyperledger Fabric**
Componentes principales

[IMAGEN: Diagrama de alto nivel de una red Fabric con peers, orderers, CAs y clientes conectados entre sí]

---

## Slide 7 — Visión general de los componentes

En Fabric, una red está formada por:

```
┌─────────────────────────────────────────────────┐
│                  RED FABRIC                      │
│                                                  │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│   │  Org 1   │  │  Org 2   │  │  Org 3   │     │
│   │ ┌──────┐ │  │ ┌──────┐ │  │ ┌──────┐ │     │
│   │ │Peer 0│ │  │ │Peer 0│ │  │ │Peer 0│ │     │
│   │ │Peer 1│ │  │ │Peer 0│ │  │ │Peer 1│ │     │
│   │ │ CA   │ │  │ │ CA   │ │  │ │ CA   │ │     │
│   │ └──────┘ │  │ └──────┘ │  │ └──────┘ │     │
│   └──────────┘  └──────────┘  └──────────┘     │
│                                                  │
│        ┌─────────────────────────┐              │
│        │   Ordering Service      │              │
│        │  (Raft: 3 o 5 nodos)   │              │
│        └─────────────────────────┘              │
└─────────────────────────────────────────────────┘
```

Cada organización gestiona sus propios componentes. Nadie controla la red completa.

---

## Slide 8 — Peers: los caballos de batalla

Un **peer** es un nodo que:
- Mantiene una **copia del ledger** (blockchain + world state)
- Ejecuta **chaincodes** (smart contracts)
- Participa en el protocolo de **gossip** para sincronizar datos

**Tipos de peers:**

| Tipo | Función |
|------|---------|
| **Endorsing peer** | Ejecuta el chaincode y firma el resultado (endorsement). Solo lo hace si tiene el chaincode instalado |
| **Committing peer** | Valida los bloques recibidos del orderer y actualiza su ledger. **Todos** los peers son committing peers |
| **Anchor peer** | Punto de contacto conocido para que otras organizaciones descubran peers vía gossip |

[NOTA PROFESOR: Aclarar que un mismo peer puede ser endorsing Y committing. La diferencia es funcional: endorsing = tiene el chaincode instalado y aparece en la política de endorsement. Anchor peer es simplemente un peer cuya dirección se publica en la configuración del canal para facilitar el descubrimiento entre organizaciones.]

---

## Slide 9 — Comparación: Peers en Fabric vs Nodos en Ethereum

| Aspecto | Nodo Ethereum | Peer Fabric |
|---------|--------------|-------------|
| **Identidad** | Anónimo (clave pública) | Identificado por certificado X.509 |
| **Permiso para unirse** | Cualquiera puede ejecutar un nodo | Solo con certificado de una CA autorizada |
| **Ejecución** | Todos ejecutan todas las transacciones | Solo los endorsing peers ejecutan |
| **Datos** | Todos ven todas las transacciones | Solo ven los canales a los que pertenecen |
| **Recompensa** | Validators reciben recompensas en ETH | No hay recompensas; los peers pertenecen a organizaciones con interés en la red |

[IMAGEN: Lado izquierdo: nodo Ethereum anónimo en una nube global. Lado derecho: peer Fabric con certificado dentro de un edificio corporativo]

---

## Slide 10 — Orderers: el servicio de ordenación

Los **orderers** se encargan exclusivamente de:

1. **Recibir** transacciones endorsadas de los clientes
2. **Ordenarlas** en un orden determinista (todos deben estar de acuerdo en el orden)
3. **Empaquetarlas** en bloques
4. **Distribuir** los bloques a los peers del canal

**Lo que los orderers NO hacen:**
- No ejecutan chaincodes
- No validan la lógica de negocio
- No mantienen el world state

**Analogía:** en un tribunal, el juez decide el orden en que se presentan las pruebas, pero no juzga si son verdaderas. Eso lo hacen los peers.

[NOTA PROFESOR: Esta separación de responsabilidades es una decisión de diseño fundamental de Fabric. En Ethereum, los validadores hacen todo: ordenan, ejecutan y validan. En Fabric, cada rol está separado, lo que permite escalar de manera independiente.]

---

## Slide 11 — Consenso Raft en el ordering service

Fabric usa **Raft** como protocolo de consenso para el ordering service. Es un protocolo de **Crash Fault Tolerant (CFT)**.

**¿Cómo funciona Raft?**

1. **Leader election:** un nodo se elige como líder. Los demás son seguidores
2. **Log replication:** el líder recibe las transacciones y las replica a los seguidores
3. **Commit:** cuando la mayoría confirma, la entrada se considera comprometida
4. **Tolerancia a fallos:** si el líder cae, los seguidores eligen uno nuevo automáticamente

**Regla de mayoría:** con N nodos, se toleran (N-1)/2 fallos:
- 3 orderers → tolera 1 fallo
- 5 orderers → tolera 2 fallos
- 7 orderers → tolera 3 fallos

[IMAGEN: Diagrama de Raft con 5 nodos: 1 líder enviando log entries a 4 seguidores, con flechas de heartbeat]

[NOTA PROFESOR: Raft es CFT, no BFT (Byzantine Fault Tolerant). Esto significa que protege contra nodos que se caen, pero NO contra nodos que actúan maliciosamente. Esto es aceptable en Fabric porque todos los participantes son conocidos y han firmado acuerdos legales. Si alguien actúa maliciosamente, hay consecuencias legales fuera de la red. A partir de Fabric 3.x se está explorando soporte para BFT (SmartBFT).]

---

## Slide 12 — Fabric CA: la autoridad de certificación

En Ethereum, tu identidad es una clave privada que generas localmente con MetaMask. Nadie te la emite.

En Fabric, tu identidad es un **certificado X.509** emitido por una **Certificate Authority (CA)** de tu organización.

**Flujo de identidad en Fabric:**

```
1. Admin registra al usuario en la CA (registration)
2. El usuario solicita su certificado (enrollment)
3. La CA emite un certificado X.509 firmado
4. El usuario usa ese certificado para firmar transacciones
5. Los peers verifican el certificado contra la CA de la organización
```

**¿Qué contiene el certificado?**
- Clave pública del usuario
- Nombre de la organización (Org1, Org2...)
- Rol (admin, peer, client, orderer)
- Fecha de expiración
- Firma de la CA que lo emitió

---

## Slide 13 — Comparación: Identidad en MetaMask vs Fabric CA

| Aspecto | MetaMask (Ethereum) | Fabric CA |
|---------|--------------------:|----------:|
| **Creación** | El usuario genera un par de claves localmente | Una CA autorizada emite un certificado |
| **Anonimato** | Seudónimo (dirección 0x...) | Identidad completa conocida |
| **Revocación** | Imposible revocar una dirección | La CA puede revocar certificados (CRL) |
| **Recuperación** | Si pierdes la seed phrase, pierdes todo | La CA puede reemitir certificados |
| **Confianza** | Confías en la criptografía | Confías en la criptografía + en la CA |
| **Regulación** | Difícil de cumplir KYC/AML | Compatible con marcos regulatorios |

[NOTA PROFESOR: Subrayar que esto es una diferencia filosófica fundamental. Las blockchains públicas nacieron para eliminar intermediarios de confianza. Fabric acepta que en el mundo empresarial SÍ hay intermediarios (las organizaciones miembros) y los integra en el diseño. No es mejor ni peor: son modelos para casos de uso distintos.]

---

## Slide 14 — MSP: Membership Service Provider

El **MSP** define **quién pertenece a cada organización** y qué puede hacer.

```
Org1MSP/
├── cacerts/          ← Certificado raíz de la CA de Org1
├── tlscacerts/       ← Certificado TLS de la CA
├── admincerts/       ← Certificados de los administradores
├── config.yaml       ← Configuración de NodeOUs
└── (en el peer)
    ├── signcerts/    ← Certificado del peer
    └── keystore/     ← Clave privada del peer
```

**Cada organización tiene su propio MSP.** Cuando un peer recibe una transacción firmada, verifica:
1. ¿El certificado fue emitido por una CA reconocida en algún MSP?
2. ¿A qué organización pertenece?
3. ¿Tiene el rol adecuado para esta operación?

---

## Slide 15 — MSP: Roles y NodeOUs

Los **NodeOUs** (Organizational Units) permiten clasificar certificados automáticamente según su tipo:

| Rol | NodeOU | Puede hacer |
|-----|--------|-------------|
| **admin** | `OU=admin` | Gestionar la red, instalar chaincodes, crear canales |
| **peer** | `OU=peer` | Mantener el ledger, endorsar transacciones |
| **client** | `OU=client` | Enviar propuestas de transacción, consultar datos |
| **orderer** | `OU=orderer` | Participar en el servicio de ordenación |

**Ventaja:** no necesitas listar explícitamente los certificados de cada admin. Cualquier certificado con `OU=admin` emitido por la CA de la organización es reconocido automáticamente como administrador.

[NOTA PROFESOR: Antes de NodeOUs, los administradores se definían listando sus certificados en la carpeta admincerts del MSP. NodeOUs simplifica enormemente la gestión. Es la configuración recomendada desde Fabric 2.x.]

---

## Slide 16 — Portada sección

**Hyperledger Fabric**
El Ledger

[IMAGEN: Un libro abierto con dos mitades: la izquierda muestra bloques encadenados (blockchain) y la derecha una base de datos con pares clave-valor (world state)]

---

## Slide 17 — El Ledger de Fabric: dos partes

El ledger de Fabric tiene **dos componentes**:

```
┌─────────────────────────────────────────────┐
│                   LEDGER                     │
│                                              │
│  ┌───────────────────┐  ┌────────────────┐  │
│  │    BLOCKCHAIN      │  │  WORLD STATE   │  │
│  │  (inmutable)       │  │  (actual)      │  │
│  │                    │  │                │  │
│  │  Bloque 0 (génesis)│  │  clave → valor │  │
│  │  Bloque 1          │  │  car1 → {blue} │  │
│  │  Bloque 2          │  │  car2 → {red}  │  │
│  │  Bloque 3          │  │  car3 → {white}│  │
│  │  ...               │  │  ...           │  │
│  └───────────────────┘  └────────────────┘  │
└─────────────────────────────────────────────┘
```

- **Blockchain:** registro inmutable y secuencial de todas las transacciones. No se puede modificar ni borrar
- **World state:** estado actual de todos los datos. Es la "foto" del momento presente. Se puede reconstruir reproduciendo toda la blockchain

---

## Slide 18 — World state: LevelDB vs CouchDB

| Aspecto | LevelDB | CouchDB |
|---------|---------|---------|
| **Tipo** | Key-value puro | Documentos JSON |
| **Consultas** | Solo por clave exacta o rango de claves | Consultas ricas sobre campos JSON (Mango queries) |
| **Rendimiento** | Más rápido | Algo más lento por la indexación |
| **Caso de uso** | Datos simples, alto rendimiento | Datos complejos que necesitan búsquedas avanzadas |
| **Ejemplo de consulta** | `GetState("car1")` | `{"selector": {"color": "blue", "owner": "Org1"}}` |
| **Configuración** | Por defecto, embebido en el peer | Requiere instancia externa de CouchDB |

[NOTA PROFESOR: En la práctica, la mayoría de proyectos en producción usan CouchDB porque las consultas ricas son muy útiles para las aplicaciones cliente. LevelDB es adecuado para prototipos o cuando el rendimiento es crítico y las consultas son simples.]

---

## Slide 19 — Comparación: Estado en Ethereum vs Fabric

| Aspecto | Ethereum | Fabric |
|---------|----------|--------|
| **Estructura** | Patricia Merkle Trie con storage slots (256 bits) | Pares clave-valor en LevelDB o documentos JSON en CouchDB |
| **Acceso** | Por dirección del contrato + slot | Por clave de string arbitraria |
| **Consultas** | No hay consultas nativas; se usan eventos + indexadores (The Graph) | Consultas directas al world state, incluyendo rich queries con CouchDB |
| **Visibilidad** | Todo público, cualquiera puede leer cualquier storage slot | Solo visible para los peers del canal |
| **Tamaño clave** | Fijo: 32 bytes | Variable: strings arbitrarios |

**En Solidity:**
```solidity
mapping(string => Car) public cars;
cars["car1"] = Car("blue", "Alice");
// Acceso: contract.cars("car1")
```

**En Fabric (chaincode Go):**
```go
car := Car{Color: "blue", Owner: "Alice"}
carJSON, _ := json.Marshal(car)
ctx.GetStub().PutState("car1", carJSON)
// Acceso: ctx.GetStub().GetState("car1")
```

---

## Slide 20 — Portada sección

**Hyperledger Fabric**
Canales y privacidad

[IMAGEN: Varios tubos de colores separados representando canales, cada uno con diferentes organizaciones dentro]

---

## Slide 21 — Canales: redes lógicas aisladas

Un **canal** en Fabric es una sub-red privada con su propio ledger independiente.

```
Red Fabric
├── Canal "comercio-exterior"
│   ├── Org: BancoA
│   ├── Org: BancoB
│   └── Org: Aduana
│   └── Ledger propio
│
├── Canal "seguros"
│   ├── Org: BancoA
│   ├── Org: Aseguradora1
│   └── Org: Aseguradora2
│   └── Ledger propio
│
└── Canal "interbancario"
    ├── Org: BancoA
    ├── Org: BancoB
    └── Ledger propio
```

- BancoA está en los tres canales: ve los datos de los tres
- Aseguradora1 solo está en "seguros": no puede ver nada de los otros canales
- Cada canal tiene su **propia blockchain y world state**

---

## Slide 22 — Canales vs Ethereum: privacidad

| Aspecto | Ethereum | Fabric (canales) |
|---------|----------|-------------------|
| **Visibilidad** | Todas las transacciones son públicas para todos | Solo los miembros del canal ven sus transacciones |
| **Segregación** | No existe. Todo está en la misma red | Canales independientes con ledgers separados |
| **Unirse** | Cualquiera puede leer la blockchain | Se necesita invitación y aprobación del canal |
| **Ejemplo** | Si Santander emite un bono en Ethereum, cualquiera puede ver los detalles | En un canal Fabric, solo los participantes autorizados ven el bono |

**Analogía:** Ethereum es un **tablón de anuncios público** en la plaza del pueblo. Un canal de Fabric es una **sala de reuniones privada** donde solo entran los invitados.

---

## Slide 23 — Private Data Collections

Incluso dentro de un canal, a veces no quieres compartir todo con todos los miembros.

**Private Data Collections** permiten que un subconjunto de organizaciones del canal comparta datos privados:

```
Canal "suministro"
├── Org: Fabricante
├── Org: Distribuidor
├── Org: Minorista
│
├── Collection "precio-fabricante-distribuidor"
│   ├── Datos privados: solo Fabricante y Distribuidor
│   └── En el ledger público: solo un hash de los datos
│
└── Collection "precio-distribuidor-minorista"
    ├── Datos privados: solo Distribuidor y Minorista
    └── En el ledger público: solo un hash de los datos
```

- El Fabricante no ve el precio que el Distribuidor cobra al Minorista
- El Minorista no ve el precio que el Fabricante cobra al Distribuidor
- Pero **todos pueden verificar** que los datos existen (el hash está en el ledger público del canal)

[NOTA PROFESOR: Este es un caso de uso muy común en supply chain. Cada actor quiere proteger sus márgenes comerciales pero necesita compartir datos de trazabilidad. Las Private Data Collections resuelven exactamente este problema.]

---

## Slide 24 — Portada sección

**Hyperledger Fabric**
Flujo de transacciones (Endorse → Order → Validate)

[IMAGEN: Diagrama con tres fases grandes conectadas por flechas: ENDORSE → ORDER → VALIDATE, con iconos de peers, orderers y checks]

---

## Slide 25 — El concepto más importante de Fabric

En Ethereum, una transacción se ejecuta cuando se incluye en un bloque. Todos los nodos ejecutan la misma transacción y llegan al mismo resultado.

En Fabric, el flujo es radicalmente diferente: **execute-order-validate**.

```
Ethereum:    Order → Execute (todos ejecutan lo mismo)
Fabric:      Execute (simular) → Order → Validate
```

**¿Por qué este cambio?**
- **Rendimiento:** no todos los peers necesitan ejecutar todas las transacciones
- **Confidencialidad:** solo los endorsing peers ven la lógica del chaincode
- **Flexibilidad:** se puede decidir quién debe aprobar cada transacción
- **No-determinismo:** si un chaincode tiene un bug no-determinista, se detecta en la fase de validación en lugar de causar un fork

---

## Slide 26 — Fase 1: ENDORSE (Proponer y simular)

```
┌──────────┐         ┌────────────────────┐
│  Cliente  │────────▶│  Endorsing Peer(s) │
│  (SDK)   │  1.     │  (Org1, Org2...)   │
│          │Propuesta│                    │
│          │         │  2. Ejecuta el     │
│          │◀────────│     chaincode      │
│          │  3.     │  (SIMULACIÓN, no   │
│          │Respuesta│   escribe nada)    │
│          │endorsada│                    │
└──────────┘         └────────────────────┘
```

1. El **cliente** (aplicación) envía una **propuesta de transacción** a los endorsing peers definidos en la política
2. Cada endorsing peer **ejecuta el chaincode** contra su copia del world state. Es una **simulación**: no modifica nada
3. El peer genera un **read-write set**: qué claves leyó y qué valores escribiría
4. Firma el resultado (endorsement) y lo devuelve al cliente

**Clave:** en este momento no se ha modificado ningún ledger. Solo se ha simulado.

---

## Slide 27 — Fase 2: ORDER (Ordenar y empaquetar)

```
┌──────────┐         ┌──────────────────────┐
│  Cliente  │────────▶│  Ordering Service    │
│  (SDK)   │  4.     │  (Raft cluster)      │
│          │Transac- │                      │
│          │ción con │  5. Ordena las       │
│          │endorse- │     transacciones    │
│          │ments    │  6. Empaqueta en     │
│          │         │     bloques          │
└──────────┘         │  7. Distribuye a     │
                     │     todos los peers  │
                     └──────────────────────┘
```

4. El cliente verifica que tiene suficientes endorsements (según la política) y **envía la transacción al orderer**
5. El orderer **ordena** las transacciones recibidas de todos los clientes en un orden determinista
6. Las **empaqueta en un bloque** cuando se cumple alguna condición (timeout, máximo de transacciones o tamaño máximo)
7. **Distribuye** el bloque a todos los peers de todas las organizaciones del canal

**El orderer no mira el contenido de las transacciones.** Solo las ordena.

---

## Slide 28 — Fase 3: VALIDATE (Validar y actualizar)

```
┌────────────────────────────────────────┐
│        Cada peer del canal             │
│                                        │
│  8. Recibe el bloque del orderer       │
│  9. Para cada transacción:             │
│     a) ¿Cumple la endorsement policy?  │
│     b) ¿El read-set sigue siendo       │
│        válido? (MVCC check)            │
│  10. Marca tx como VALID o INVALID     │
│  11. Añade el bloque al blockchain     │
│  12. Actualiza world state (solo VALID)│
└────────────────────────────────────────┘
```

8. Cada peer recibe el bloque del orderer
9. **Valida** cada transacción:
   - **Endorsement policy:** ¿firmaron los peers requeridos?
   - **MVCC (Multi-Version Concurrency Control):** ¿las claves leídas durante la simulación siguen con el mismo valor? Si otra transacción las modificó entre tanto, se marca como INVALID
10. Las transacciones inválidas se **quedan en el bloque** (para auditoría) pero se marcan como inválidas
11. Solo las transacciones **válidas** actualizan el world state

---

## Slide 29 — Flujo completo: visión integrada

[IMAGEN: Diagrama completo del flujo de transacción con las 3 fases: un cliente envía propuesta a endorsing peers de Org1 y Org2, recibe respuestas firmadas, las envía al orderer, el orderer crea un bloque, lo distribuye a todos los peers, y cada peer valida y actualiza su world state]

**Resumen en una frase:**
> En Fabric, la transacción se **ejecuta primero** (endorse), se **ordena después** (order), y se **valida al final** (validate). En Ethereum, se ordena primero y se ejecuta después.

[NOTA PROFESOR: Este es el concepto más importante del día. Dedicar tiempo suficiente a explicarlo paso a paso. Usar el diagrama y recorrerlo varias veces. Preguntar a los alumnos en cada fase: "¿qué pasa si falla aquí?". Ejemplo: si un endorsing peer devuelve un resultado diferente al otro, el cliente detecta la inconsistencia y no envía al orderer. Si el read-set cambia entre endorse y validate, la transacción se marca inválida (MVCC conflict).]

---

## Slide 30 — Actividad: Dibuja el flujo en parejas

**Instrucciones (20 minutos):**

1. Formar **parejas**
2. En un folio grande (o pizarra), dibujar el flujo completo de una transacción en Fabric
3. Incluir:
   - Al menos 2 organizaciones con sus peers
   - Un ordering service con 3 nodos
   - Un cliente que inicia la transacción
   - Flechas numeradas para cada paso
   - Las 3 fases claramente diferenciadas
4. Inventar un caso de uso concreto (ejemplo: "Org1=Fabricante transfiere propiedad del lote 42 a Org2=Distribuidor")
5. Anotar qué pasa en cada paso con los datos del caso concreto

**Después:** un grupo voluntario explica su diagrama al resto de la clase. Los demás hacen preguntas o sugieren correcciones.

[NOTA PROFESOR: Circular entre los grupos durante la actividad para resolver dudas y asegurar que los diagramas son correctos. Los errores más comunes: olvidar que el endorse es una simulación (no escribe), pensar que el orderer ejecuta el chaincode, olvidar la validación MVCC. Dar 5-10 minutos para la presentación del grupo voluntario.]

---

## Slide 31 — Portada sección

**Hyperledger Fabric**
Políticas de endorsement

[IMAGEN: Tres sellos de aprobación de diferentes colores (uno por organización) estampados sobre un documento]

---

## Slide 32 — Endorsement policies: ¿quién debe aprobar?

La **endorsement policy** define qué combinación de organizaciones debe endorsar una transacción para que sea válida.

**Sintaxis:**

| Política | Significado |
|----------|-------------|
| `AND('Org1.peer', 'Org2.peer')` | Org1 **Y** Org2 deben endorsar |
| `OR('Org1.peer', 'Org2.peer')` | Org1 **O** Org2 deben endorsar |
| `OutOf(2, 'Org1.peer', 'Org2.peer', 'Org3.peer')` | Al menos 2 de las 3 deben endorsar |
| `AND('Org1.peer', OR('Org2.peer', 'Org3.peer'))` | Org1 siempre + al menos una de Org2/Org3 |

**Ejemplo real:** en un consorcio bancario para comercio exterior:
- Transferencias < 10.000 EUR: `OR('BancoA.peer', 'BancoB.peer')` → basta con un banco
- Transferencias >= 10.000 EUR: `AND('BancoA.peer', 'BancoB.peer', 'Regulador.peer')` → todos deben aprobar

[NOTA PROFESOR: Las endorsement policies se definen al desplegar o actualizar un chaincode. Desde Fabric 2.x, también se pueden definir a nivel de colección de datos privados o incluso a nivel de clave individual (state-based endorsement). Esto permite una granularidad muy fina.]

---

## Slide 33 — ¿Por qué importan las endorsement policies?

Las endorsement policies implementan **gobernanza descentralizada** dentro de la red permisionada:

1. **Ninguna organización puede actuar sola** si la política requiere múltiples firmas
2. **Protección contra fraude:** un banco no puede fabricar transacciones falsas sin la firma del otro
3. **Cumplimiento regulatorio:** se puede exigir que un regulador endorse ciertas transacciones
4. **Flexibilidad:** diferentes chaincodes pueden tener diferentes políticas en la misma red

**Comparación con Ethereum:**
- En Ethereum, cualquier transacción es válida si tiene gas y firma válida. No hay concepto de "quién debe aprobar"
- En Fabric, la red define explícitamente las reglas de aprobación. Es como pasar de "cualquiera puede operar" a "necesitas las firmas adecuadas"

**Analogía:** en un banco, un cajero puede aprobar una transferencia pequeña, pero para una grande se necesita la firma del director y del departamento de cumplimiento. Fabric implementa esto a nivel de protocolo.

---

## Slide 34 — Treasure Hunt: Investigación forense de logs de Fabric 🏴‍☠️

**Escenario:** eres auditor de una red Fabric de comercio exterior con 3 organizaciones (BancoAlfa, BancoBeta y Aduana). Has recibido estos fragmentos de log y debes reconstruir qué ocurrió.

**Log 1 — Peer0 de BancoAlfa:**
```
[endorser] ProcessProposal -> INFO  Channel [comercio]: txid [a]
  chaincode: transferencia, proposal from: BancoAlfaMSP/client
  Simulation: ReadSet{lote42: v3}, WriteSet{lote42.owner: BancoBeta}
  Endorsement: SIGNED by BancoAlfa
```

**Log 2 — Peer0 de BancoBeta:**
```
[endorser] ProcessProposal -> INFO  Channel [comercio]: txid [a]
  chaincode: transferencia, proposal from: BancoAlfaMSP/client
  Simulation: ReadSet{lote42: v3}, WriteSet{lote42.owner: BancoBeta}
  Endorsement: SIGNED by BancoBeta
```

**Log 3 — Orderer (Raft leader):**
```
[orderer] Broadcast -> INFO  Channel [comercio]: received txid [a]
  Endorsements: BancoAlfa, BancoBeta
  Block 47: [txid_a, txid_b, txid_c]
  Distributed to: Peer0.BancoAlfa, Peer0.BancoBeta, Peer0.Aduana
```

**Log 4 — Peer0 de Aduana:**
```
[committer] ValidateBlock -> INFO  Block 47, Channel [comercio]
  txid [a]: endorsement policy AND('BancoAlfa','BancoBeta','Aduana') -> INVALID
    reason: missing endorsement from AduanaMSP
  txid [b]: endorsement policy OR('BancoAlfa','BancoBeta') -> VALID
  txid [c]: MVCC conflict on key [lote42] (read v3, current v4) -> INVALID
```

---

## Slide 35 — Treasure Hunt: Preguntas

**Misión (25 minutos, en grupos de 3-4):**

1. ¿Qué intentaba hacer la transacción `txid [a]`? ¿Quién la inició?
2. ¿Qué organizaciones endorsaron `txid [a]`? ¿Fue suficiente?
3. ¿Por qué fue marcada como INVALID la `txid [a]`? ¿Qué debería haber hecho el cliente para que fuese válida?
4. El orderer distribuyó `txid [a]` sin problemas. ¿Por qué no la rechazó si le faltaba un endorsement?
5. La `txid [c]` también fue INVALID. ¿Por qué? Explica qué es un conflicto MVCC con tus propias palabras.
6. ¿La `txid [a]` desaparece del bloque 47 al ser inválida? ¿Por qué sí o por qué no?
7. **Bonus:** si la `txid [c]` leía `lote42` en versión v3, pero la versión actual es v4, ¿qué transacción pudo haber cambiado `lote42` de v3 a v4? ¿Podría haber sido `txid [a]`?

[NOTA PROFESOR: Respuestas:
1. Transferir la propiedad del lote42 a BancoBeta. La inició un cliente de BancoAlfa.
2. BancoAlfa y BancoBeta endorsaron. No fue suficiente: la política era AND de las 3 orgs incluyendo Aduana.
3. Faltaba el endorsement de Aduana. El cliente debería haber enviado la propuesta también al peer de Aduana.
4. El orderer NO evalúa las endorsement policies. Solo ordena. La validación la hacen los peers.
5. MVCC: durante el endorse, txid_c leyó lote42 con valor v3. Pero entre el endorse y el validate, otra transacción cambió lote42 a v4. El dato ya no es consistente, así que se invalida.
6. No desaparece. Las transacciones inválidas permanecen en el bloque para auditoría, pero se marcan como INVALID y no modifican el world state.
7. No puede haber sido txid_a porque fue INVALID (no modifica world state). Probablemente fue txid_b u otra transacción de un bloque anterior.]

---

## Slide 36 — Portada sección

**Hyperledger Fabric**
Repaso y preguntas

[IMAGEN: Cerebro con piezas de puzzle de Fabric encajando: peers, orderers, canales, endorsement]

---

## Slide 37 — Preguntas de repaso: EVM vs Fabric

1. En Ethereum, cualquiera puede unirse a la red ejecutando un nodo. ¿Qué necesita un participante para unirse a una red Fabric?

2. En Ethereum, todos los nodos ejecutan todas las transacciones. ¿Quién ejecuta las transacciones en Fabric? ¿Todos los peers?

3. En Ethereum, el estado se almacena en un Patricia Merkle Trie con storage slots de 256 bits. ¿Cómo se almacena el estado en Fabric?

4. En Ethereum, todas las transacciones son visibles para todos. ¿Cómo consigue Fabric la privacidad entre organizaciones?

5. Si un endorsing peer de Org1 y un endorsing peer de Org2 ejecutan el mismo chaincode pero obtienen resultados diferentes, ¿qué ocurre?

6. ¿El orderer ejecuta el chaincode? ¿Valida las endorsement policies? ¿Qué hace exactamente?

7. ¿Qué es un conflicto MVCC y en qué fase del flujo de transacción se detecta?

8. ¿Puede una transacción inválida aparecer en un bloque de Fabric? ¿Y en Ethereum?

9. Si MetaMask es la "identidad" en Ethereum, ¿cuál es el equivalente en Fabric?

10. ¿Por qué Raft (CFT) es suficiente para Fabric pero no lo sería para Ethereum?

---

## Slide 38 — Respuestas de repaso

[NOTA PROFESOR: Respuestas clave:
1. Un certificado X.509 emitido por la CA de una organización que sea miembro de la red.
2. Solo los endorsing peers (los que tienen el chaincode instalado y están en la política de endorsement). No todos los peers ejecutan.
3. En pares clave-valor, usando LevelDB (key-value simple) o CouchDB (documentos JSON con consultas ricas).
4. Canales (ledgers separados) y Private Data Collections (datos privados dentro de un canal, con solo el hash en el ledger público).
5. El cliente detecta la inconsistencia y no envía la transacción al orderer. La transacción no progresa.
6. No ejecuta chaincode ni valida endorsements. Solo recibe transacciones, las ordena, las empaqueta en bloques y los distribuye.
7. Es cuando una clave leída durante el endorse fue modificada por otra transacción antes de la validación. Se detecta en la fase VALIDATE.
8. Sí, en Fabric las transacciones inválidas permanecen en el bloque marcadas como INVALID. En Ethereum, las transacciones inválidas no se incluyen en bloques (un validador no las incluiría porque no obtendría fees).
9. Un certificado X.509 emitido por la Fabric CA de la organización, gestionado a través del MSP.
10. Porque en Fabric todos los participantes son conocidos e identificados; si actúan maliciosamente hay consecuencias legales. En Ethereum, los nodos son anónimos y se necesita BFT (tolerancia a fallos bizantinos) porque no puedes confiar en que no habrá actores maliciosos.]

---

## Slide 39 — Resumen del día

| Concepto | Idea clave |
|----------|------------|
| **Consorcios** | Las empresas crearon R3, EEA e Hyperledger para adaptar blockchain a sus necesidades |
| **Peers** | Mantienen el ledger y ejecutan chaincodes. Tipos: endorsing, committing, anchor |
| **Orderers** | Ordenan transacciones y crean bloques. No ejecutan chaincodes. Usan Raft |
| **Fabric CA** | Emite certificados X.509. En Fabric la identidad la da una CA, no una clave local |
| **MSP** | Define quién pertenece a cada organización y sus roles |
| **Ledger** | Blockchain (inmutable) + World State (LevelDB o CouchDB) |
| **Canales** | Redes lógicas aisladas con ledgers independientes. Privacidad entre organizaciones |
| **Private Data** | Datos privados dentro de un canal. Solo un hash en el ledger público |
| **Flujo tx** | Endorse → Order → Validate. Diferente a Ethereum (Order → Execute) |
| **Endorsement** | Políticas que definen qué organizaciones deben aprobar una transacción |

---

## Slide 40 — Tarea para casa

**Tarea 1 — Mapa conceptual:**
Crear un mapa conceptual (en papel o con herramienta digital) que conecte todos los componentes de Fabric vistos hoy: peers, orderers, CA, MSP, canales, ledger, world state, endorsement policies. Cada conexión debe incluir una frase que explique la relación (ejemplo: "El peer → mantiene → el ledger").

**Tarea 2 — Investigación:**
Buscar un caso de uso real de Hyperledger Fabric en producción (no un prototipo) y responder:
- ¿Qué empresa o consorcio lo usa?
- ¿Cuántas organizaciones participan?
- ¿Qué problema resuelve?
- ¿Por qué eligieron Fabric y no una blockchain pública?

*Presentar ambas tareas al inicio de la próxima clase.*

[NOTA PROFESOR: Ejemplos de casos reales en producción: Walmart (trazabilidad alimentaria con IBM Food Trust), Maersk (TradeLens, aunque cerró en 2022), Everledger (diamantes), We.trade (financiación comercial, cerró en 2022), GSMA (telecomunicaciones), Change Healthcare (sanidad en EEUU). Los casos de fracaso (TradeLens, We.trade) son igual de valiosos para aprender.]
