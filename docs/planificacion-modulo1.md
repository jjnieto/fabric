# Planificación Módulo 1: Introducción a Blockchain + Hyperledger Fabric

**Duración total:** 11 jornadas (55 horas)
**Estructura de cada jornada:** 5h con pausas (ver ritmo diario más abajo)

---

## Ritmo diario tipo

| Bloque | Duración | Contenido |
|--------|----------|-----------|
| Repaso + conexión | 25 min | Repaso del día anterior, preguntas rápidas |
| Cultura / Treasure Hunt | 15 min | Sección amena (rotativa, no todos los días) |
| Teoría | 55 min | Concepto principal con demos |
| **Pausa** | **15 min** | |
| Práctica guiada | 70 min | Ejercicio paso a paso |
| **Pausa** | **15 min** | |
| Teoría / Debate | 45 min | Segundo bloque conceptual o debate |
| Práctica / Actividad | 45 min | Ejercicio autónomo o actividad grupal |
| Cierre + Repaso | 15 min | Preguntas de repaso del día |

> **Nota:** La Treasure Hunt y la sección de Cultura General se alternan. No todos
> los días tienen ambas — se distribuyen para mantener el ritmo sin saturar.

---

## Día 1 — El dinero, la crisis y el nacimiento de Bitcoin

### Contenido (slides 1-20 de la PPT existente)

**Teoría**
- El origen del dinero: trueque → commodity → convertible → fiduciario
- Reserva fraccionaria y la banca moderna
- Riesgo de contrapartida
- Tipos y calidades del dinero
- Liquidación (settlement): qué es, por qué es complejo

**Actividad: Liquidación simulada** (slides 11-14)
- Tres casos: interna del banco, interbancaria, cross-border
- Grupos simulan los agentes del sistema de pagos

**Teoría**
- La crisis de 2008: causas, colapso, consecuencias
- Satoshi Nakamoto y el whitepaper de Bitcoin
- Del problema a la tecnología: qué propone blockchain

**Debate** (slide 17)
- ¿Qué falló en 2008?
- ¿Qué papel jugaron los reguladores?
- ¿Cuál fue el resultado de la crisis?

**Repaso del día** (slide 36)

---

## Día 2 — Hash, criptografía y redes P2P

### Contenido (slides 23-50 de la PPT)

**Teoría**
- Qué es un hash: propiedades (unidireccional, tamaño fijo, sin colisiones)
- Uso del hash en blockchain

**Actividad: Validar algoritmos de hash** (slide 25)
- ¿Por qué MyHash con módulo primo no es válido?

**Práctica online** (slide 27)
- SHA-256 en navegador

**Teoría**
- Claves pública/privada: cifrado, firma, verificación
- De claves a wallets: cómo se genera una dirección

**Práctica** (slides 30-35)
- RSA: cifrar/descifrar online
- ECDSA: firmar/verificar online
- Generar direcciones Bitcoin y Ethereum

**Teoría**
- Red peer-to-peer: propagación de transacciones
- Encadenado de bloques: hash del bloque anterior

**Actividad de reflexión** (slides 45-50)
- ¿Por qué una red P2P con hashes aún no es suficiente?
- Identificar los problemas que quedan sin resolver

| | |
|---|---|
| **Treasure Hunt** | *Bitcoin Pizza Day* (slide 52): descifrar la contribución de Laszlo Hanyecz usando las pistas con clave privada y RSA/ECB/PKCS1Padding |

**Repaso del día** (slide 74)

---

## Día 3 — Consenso, PoW, trilema y MetaMask

### Contenido (slides 53-121 de la PPT)

**Teoría**
- Problema de los generales bizantinos
- BFT: solución con 2/3 de nodos leales

**Actividad con tarjetas** (slide 59)
- Simular generales leales y traidores en grupos

**Teoría**
- Proof of Work paso a paso (nonce, target, recompensa)
- Forks temporales y regla de la cadena más larga
- Cómo PoW resuelve el doble gasto

**Actividad: encontrar hash con ceros** (slide 66)
- SHA-256 manual buscando nonce

**Actividad: Blockchain humano** (slide 69)
- Grupos de mineros, ledger en pizarra, transacciones reales

**Teoría**
- PoS como alternativa: stake, slashing, comparativa con PoW
- El trilema de blockchain (seguridad, escalabilidad, descentralización)

**Debate en grupos** (slides 77-80)
- Analizar cada combinación del trilema con ejemplos reales

**Práctica: Instalar y usar MetaMask** (slides 87-110)
- Instalar extensión, crear wallet, red Sepolia
- Conseguir ETH de prueba desde faucet
- Enviar ETH entre compañeros
- Explorar gas, fees y nonce

| | |
|---|---|
| **Cultura General** | *Soy Minero* ♫ (slide 82) — momento musical para romper el hielo antes del debate sobre el poder de los mineros |

**Debate: El poder de los mineros** (slides 83-86)
- MEV, front-running, sandwich attacks

**Repaso del día** (slides 121, preguntas de la 1044-1061)

---

## Día 4 — Smart Contracts, wallets y Solidity básico

### Contenido (slides 122-141 de la PPT)

| | |
|---|---|
| **Cotilleos** | Sección de cotilleos (slides 122-123) — paréntesis ameno al inicio |

**Teoría**
- Custodial vs non-custodial wallets
- Ethereum y la idea de Vitalik: máquina de estados + EVM
- Smart contracts: qué son, por qué son inmutables
- ¿Por qué no hay números aleatorios en Solidity?

**Debate: Custodial vs Non-Custodial** (slide 126)
- Seguridad, sencillez, accesibilidad, recuperación

**Práctica: Desplegar la Caja Fuerte en Remix** (slide 140)
- Conectar MetaMask a Remix
- Compilar, desplegar, interactuar con vault.sol
- Bloquear ETH y verificar que no se puede retirar antes de tiempo

**Debate post-práctica** (slide 141)
- Experiencia técnica, riesgos de firmas, contratos maliciosos
- "Deploy once, consume all" — propiedad intelectual, inmutabilidad

| | |
|---|---|
| **Cultura General** | *Alan Turing* (slides 135-137): vida, Enigma, test de Turing, la película |

**Repaso del día** (slide 142)

**Tarea para casa:** Investigar ERC-3643 y preparar una slide

---

## Día 5 — Tokens, fungibilidad y tokenización

### Contenido (slides 146-177 de la PPT)

**Teoría**
- Concepto de fungibilidad con ejemplos cotidianos

**Actividad: ¿Fungible o no?** (slide 152)
- Clasificar 20 elementos en fungibles, no fungibles y discutibles

**Teoría**
- ERC-20, ERC-721, ERC-1155: qué son, cómo funcionan
- Estandarización: interfaces obligatorias
- Composabilidad: "lego" de smart contracts

**Práctica: Obtener USDC y explorar contratos existentes** (slide 159)
- Faucet de Circle, Etherscan, importar en MetaMask

**Práctica: Crear nuestro propio token ERC-20** (slide 160)
- Desplegar, repartir tokens entre alumnos, transferir
- Inspeccionar en Etherscan

**Teoría**
- Tokenización de activos: qué es, qué se puede tokenizar
- Beneficios: propiedad fraccionada, liquidez, programabilidad
- Caso Santander bond 2019, EIB bond 2021

**Teoría**
- Stablecoins: fiat-backed, crypto-backed, algorítmicas
- Caso Terra/Luna: anatomía del colapso

**Caso de estudio en grupo** (slide 175)
- ¿Pueden funcionar las stablecoins algorítmicas sin riesgo?

**Repaso del día** (slides 161 y 177)

---

## Día 6 — CBDCs, Euro Digital y el futuro del dinero

### Contenido (slides 178-211 de la PPT)

**Teoría**
- CBDCs: motivación, ventajas (programabilidad, pagos rápidos, contingencia)
- Euro Digital: fases, requerimientos, modelos (directo, intermediado, tokens)

**Debate** (slide 182)
- ¿Qué motivó a los bancos centrales?
- ¿Qué supone dar acceso directo a dinero de banco central?

**Teoría**
- Yuan Digital: adopción, wallets, KYC, pagos offline
- Fnality: settlement institucional con tokens respaldados por banco central
- Funding, transferencia y defunding en Fnality

**Teoría**
- Tipos de stablecoins: clasificación completa (emisor, colateral, fungibilidad, riesgo, redes, regulación)

**Debate amplio** (slides 209-210)
- Diseñar la stablecoin europea ideal
- Futuro del dinero: convivencia de tipos

**Repaso del día** (slide 211)

---

## Día 7 — dApps, DeFi, DAOs y escalabilidad

### Contenido (slides 212-252 de la PPT)

**Teoría**
- dApps: qué son, categorías (DeFi, NFTs, Metaverso, DAOs)
- Exchanges: CEX vs DEX

**Práctica: Uniswap con MetaMask** (slide 218)
- Conectar, comprar tokens, vender, comparar con Coinbase

**Debate: Uniswap vs Coinbase** (slide 219)

**Teoría**
- DeFi: préstamos, stablecoins, derivados sin intermediarios
- Oráculos: por qué son necesarios, tipos, Chainlink

**Práctica: Aave + dYdX** (slides 222-223)
- Pedir préstamos en testnet, explorar futuros

**Teoría**
- DAOs: gobernanza, mecanismos de votación, ataques (The DAO, Beanstalk)

**Debate: Pros y contras de las DAOs** (slide 236)

**Práctica: Desplegar Mini DAO** (slide 237)
- Votación ponderada por tokens entre alumnos

**Teoría**
- Escalabilidad: rendimiento actual vs VISA
- Soluciones L1 y L2: sharding, state channels, sidechains, rollups

**Debate** (slide 250)
- ¿Por qué blockchain no se usa más? Factores de adopción

| | |
|---|---|
| **Treasure Hunt** | Bonos Santander en Etherscan (slide 251): explorar las transacciones reales del bono en mainnet |

**Práctica grupal: Crear nuestro propio SC** (slide 252)
- Tres grupos, tres ideas, desplegar y probar
- (Esta práctica puede extenderse a las primeras horas del día 8)

---

## Día 8 — Blockchain permissioned y la entrada a Hyperledger

> **Punto de inflexión del curso:** Los días 1-7 han cubierto blockchain público (Bitcoin, Ethereum, EVM). A partir de aquí pivotamos a blockchain empresarial/permissioned.

**Repaso general** (30 min)
- Quiz rápido de todo lo visto: 15 preguntas tipo test en 10 minutos
- Corrección en grupo con debate

| | |
|---|---|
| **Treasure Hunt** | ¿Qué empresa creó Hyperledger? Pista: su logo es un pingüino gigante y contribuyó a que Linux sea lo que es hoy. ¿Qué relación tiene Hyperledger con Linux Foundation? Investigar en la web. |

**Teoría: De público a permissioned** (nuevo contenido)
- Recapitulación del trilema: ¿dónde encaja blockchain empresarial?
- Público vs permissioned vs privado: diferencias clave
- ¿Por qué las empresas no usan Ethereum directamente?
  - Privacidad de transacciones
  - Rendimiento predecible
  - Gobernanza controlada
  - Identidades conocidas (no pseudónimas)
  - Cumplimiento regulatorio

**Teoría: El proyecto Hyperledger**
- Origen: Linux Foundation, 2015
- No es UNA blockchain, es un paraguas de proyectos
- Ecosistema: Fabric, Besu, Iroha, Sawtooth, Indy/Aries, Caliper, Cactus
- Comparativa rápida de los principales proyectos
- Por qué Fabric es el más adoptado en enterprise

**Teoría: Hyperledger Fabric — visión general**
- Diseñado para consorcios empresariales
- Red permissioned: todos los participantes son conocidos
- Arquitectura modular: consenso, identidad, ledger enchufables
- Canales: múltiples ledgers privados en la misma red
- Smart contracts → Chaincodes (Go, Node.js, Java)

**Debate: Ethereum vs Fabric**
- Tabla comparativa interactiva (los alumnos la rellenan)

| Aspecto | Ethereum | Hyperledger Fabric |
|---|---|---|
| Tipo de red | Pública, permissionless | Privada, permissioned |
| Identidad | Pseudónima (wallets) | Conocida (certificados X.509) |
| Consenso | PoS global | Raft por canal (ordering service) |
| Smart Contracts | Solidity | Go, Node.js, Java |
| Visibilidad | Todo es público | Canales y private data |
| Fees | Gas (ETH) | Sin criptomoneda nativa |
| Rendimiento | ~15-20 TPS | ~3000+ TPS |
| Finalidad | Probabilística | Determinista |

**Actividad: Identificar casos de uso**
- Dado un listado de 10 escenarios de negocio, clasificar cuáles se beneficiarían de blockchain público, cuáles de permissioned y cuáles no necesitan blockchain

---

## Día 9 — Arquitectura de Hyperledger Fabric en profundidad

| | |
|---|---|
| **Cultura General** | Breve historia de los consorcios blockchain empresariales: R3 Corda, Enterprise Ethereum Alliance, Hyperledger. ¿Por qué las grandes empresas se agruparon para crear estándares? |

**Teoría: Componentes principales de Fabric**
- **Peers**: ejecutan chaincodes y mantienen el ledger
  - Endorsing peers vs committing peers
- **Orderers**: servicio de ordenación (Raft)
  - No ejecutan chaincodes, solo ordenan transacciones
- **Fabric CA**: autoridad certificadora
  - Certificados X.509, enrollment, registro
  - Comparar con MetaMask: allí la identidad era una clave privada local, aquí es un certificado emitido por una CA
- **MSP (Membership Service Provider)**: define quién pertenece a cada organización
  - Roles: admin, peer, client, orderer

**Teoría: El ledger de Fabric**
- Dos partes: blockchain (bloques inmutables) + world state (estado actual)
- World state: LevelDB (key-value) o CouchDB (JSON, consultas ricas)
- Comparar con EVM: en Ethereum el estado está en storage slots, en Fabric en key-value pairs

**Teoría: Canales**
- Un canal = una red lógica con su propio ledger
- Privacidad entre organizaciones: solo ven las transacciones del canal al que pertenecen
- Comparar con Ethereum: allí todo es público, aquí puedes segregar

**Teoría: Flujo de una transacción en Fabric**
- Las 3 fases: Endorse → Order → Validate
  1. El cliente propone la transacción a los endorsing peers
  2. Los endorsing peers ejecutan el chaincode y firman el resultado (endorsement)
  3. El cliente envía las respuestas endorsadas al ordering service
  4. El orderer empaqueta en bloque y distribuye
  5. Los peers validan y actualizan el world state
- Comparar con EVM: en Ethereum la transacción se ejecuta en el momento de incluirla en un bloque; en Fabric primero se simula (endorse) y luego se valida

**Actividad: Dibujar el flujo**
- Por parejas, dibujar en papel el flujo completo de una transacción incluyendo todos los componentes
- Puesta en común: un grupo lo explica al resto

**Teoría: Políticas de endorsement**
- Quién debe aprobar: `AND('Org1.peer','Org2.peer')`, `OR(...)`, `MAJORITY`
- Por qué importa: gobernanza descentralizada sin que una sola org controle

---

## Día 10 — Criptografía en Fabric y herramientas

| | |
|---|---|
| **Treasure Hunt** | El primer despliegue de Hyperledger Fabric fue la versión 0.6 en 2016. Fue contribuido inicialmente por una gran empresa tecnológica. ¿Cuál? Pista: su fundador inventó la máquina que hizo obsoletos los registros en papel de las oficinas. |

**Teoría: Identidades y certificados en Fabric**
- De claves pública/privada (que ya conocen) a certificados X.509
- PKI: Certificate Authority → certificados → MSP
- Fabric CA: enroll, register, revoke
- Comparativa directa:

| EVM | Fabric |
|---|---|
| Clave privada en MetaMask | Clave privada + certificado X.509 |
| Dirección = hash de clave pública | Identidad = certificado emitido por CA |
| Pseudónima | Identificada (nombre, org, rol) |
| Sin revocación posible | Revocación mediante CRL |

**Teoría: Criptografía específica de Fabric**
- ECDSA (curva P-256) para firmas
- TLS mutuo entre componentes
- MSP: carpetas de certificados (cacerts, signcerts, keystore, tlscacerts)

**Práctica: Explorar los certificados**
- Examinar la estructura de crypto-config generada por cryptogen
- Abrir un certificado X.509 con openssl y entender los campos
- Comparar con una dirección de Ethereum

**Teoría: Herramientas del ecosistema Fabric**
- `peer` CLI: gestión de canales, chaincodes, ledger
- `orderer`: nodo de ordenación
- `configtxgen`: generar configuración de canales
- `configtxlator`: traducir entre protobuf y JSON
- `cryptogen`: generar material criptográfico (solo desarrollo)
- `fabric-ca-client` / `fabric-ca-server`: gestión de identidades
- `osnadmin`: gestión de canales en el ordering service

**Práctica: Instalar y verificar el entorno** (referencia a docs/01)
- Verificar Docker, Go, binarios de Fabric
- Descargar fabric-samples si no se ha hecho
- Ejecutar `peer version`, `configtxgen -version`

---

## Día 11 — Test Network: primera red Fabric en acción

**Práctica completa: Levantar la test-network** (referencia a docs/02)

1. `./network.sh down` + `./network.sh up createChannel`
2. Explorar los contenedores Docker que se han creado
3. Comparar con lo visto en teoría: identificar peers, orderer, canal

**Práctica: Desplegar y usar un chaincode**
1. `./network.sh deployCC` con asset-transfer-basic
2. Configurar variables de entorno para Org1 y Org2
3. `InitLedger` → `GetAllAssets` → `TransferAsset`
4. Cambiar de organización y verificar el estado

**Actividad: Romper cosas a propósito**
- ¿Qué pasa si intento hacer invoke sin endorsement de las dos orgs?
- ¿Qué pasa si el orderer está caído?
- ¿Qué pasa si uso un certificado de una org para operar como otra?

**Debate de cierre del módulo 1**
- ¿Qué ha sido lo más sorprendente comparando EVM con Fabric?
- ¿Qué os parece más complejo?
- ¿Dónde veis más potencial para vuestra empresa/sector?

**Repaso general del módulo 1**
- Quiz final de 20 preguntas (10 blockchain genérico + 10 Fabric)
- Resolución en grupo

---

## Resumen: distribución de contenido

| Día | Tema principal | Base |
|-----|---------------|------|
| 1 | Dinero, crisis 2008, Bitcoin | PPT existente |
| 2 | Hash, criptografía, P2P, bloques | PPT existente |
| 3 | Consenso, PoW/PoS, trilema, MetaMask | PPT existente |
| 4 | Wallets, Smart Contracts, Remix | PPT existente |
| 5 | Tokens, fungibilidad, tokenización | PPT existente |
| 6 | CBDCs, Euro Digital, stablecoins | PPT existente |
| 7 | dApps, DeFi, DAOs, escalabilidad | PPT existente |
| **8** | **Blockchain permissioned, intro Hyperledger** | **Nuevo** |
| **9** | **Arquitectura Fabric en profundidad** | **Nuevo** |
| **10** | **Criptografía en Fabric, herramientas** | **Nuevo** |
| **11** | **Test Network: práctica completa** | **Nuevo** |

---

## Distribución de secciones especiales

| Día | Treasure Hunt | Cultura General |
|-----|---------------|-----------------|
| 1 | — | — (el contenido histórico del dinero ya cumple este rol) |
| 2 | Bitcoin Pizza Day (slide 52) | — |
| 3 | — | Soy Minero ♫ (slide 82) |
| 4 | — | Alan Turing (slides 135-137) |
| 5 | — | Fit Vitalik / ICO paródica (slide 132) |
| 6 | — | — (el Yuan Digital y sus tarjetas LCD ya es cultura) |
| 7 | Bonos Santander en Etherscan (slide 251) | — |
| 8 | ¿Quién creó Hyperledger? | — |
| 9 | — | Consorcios blockchain empresariales |
| 10 | ¿Quién contribuyó Fabric 0.6? (IBM) | — |
| 11 | — | — (día 100% práctico) |

---

## Notas para el instructor

1. **Los días 1-7 ya tienen slides.** Solo necesitas adaptar formato y corregir las erratas que hay en la PPT original.

2. **Los días 8-11 necesitan slides nuevas.** Son 4 jornadas de contenido nuevo, aproximadamente 80-100 slides.

3. **El día 7 es el más denso.** Tiene dApps + DeFi + DAOs + escalabilidad + práctica grupal. Si se queda corto, la práctica grupal de crear un SC puede iniciarse el día 7 y presentarse al inicio del día 8 como transición.

4. **El día 11 es 100% práctico.** Es la primera vez que tocan Fabric de verdad. Que sea una experiencia positiva — ten el entorno pre-probado.

5. **El puente del día 7 al 8 es crítico.** Pasar de "todo es público y permissionless" a "todo es privado y permissioned" requiere re-contextualizar varios conceptos. La tabla comparativa Ethereum vs Fabric del día 8 es el ejercicio más importante de toda la transición.
