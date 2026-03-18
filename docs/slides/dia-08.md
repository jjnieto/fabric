# Día 8 — De blockchain público a permissioned: introducción a Hyperledger

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos del mundo cripto y enterprise blockchain - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre adopción empresarial de blockchain, proyectos Hyperledger, o la tensión entre blockchain público y privado. Ejemplos: grandes bancos usando Fabric, nuevas regulaciones cripto en la UE (MiCA), CBDCs, tokenización de activos reales (RWA), etc. Actualizar antes de cada edición del curso.]

---

## Slide 2 — Quiz relámpago: ¿Cuánto recuerdas? ⚡ (Parte 1)

**Repaso general — Días 1 a 7** (10 minutos, 15 preguntas)

Responde individualmente en tu cuaderno. Después corregimos en grupo.

1. ¿Qué función criptográfica convierte cualquier dato en una huella digital de longitud fija?
2. ¿Qué dos claves componen un par de claves asimétricas y cuál se comparte públicamente?
3. ¿Qué estructura de datos encadena los bloques entre sí de forma inmutable?
4. ¿Qué problema resuelve el consenso en una red P2P sin autoridad central?
5. Nombra dos mecanismos de consenso y una diferencia clave entre ellos.

[NOTA PROFESOR: Respuestas esperadas:
1. Función hash (SHA-256, Keccak-256...).
2. Clave pública (se comparte) y clave privada (se guarda en secreto).
3. Cada bloque contiene el hash del bloque anterior, formando una cadena.
4. El problema del doble gasto / cómo ponerse de acuerdo sin confianza mutua.
5. PoW (gasta energía computacional) vs PoS (apuesta tokens como garantía). Otras combinaciones válidas.]

---

## Slide 3 — Quiz relámpago: ¿Cuánto recuerdas? ⚡ (Parte 2)

6. ¿Qué herramienta usamos para interactuar con Ethereum desde el navegador?
7. ¿Qué es el gas en Ethereum y por qué es necesario?
8. ¿Qué lenguaje se usa para escribir smart contracts en la EVM?
9. ¿Qué estándar define un token fungible en Ethereum? ¿Y uno no fungible?
10. ¿Qué significa DeFi y da un ejemplo de protocolo?

[NOTA PROFESOR: Respuestas esperadas:
6. MetaMask (wallet de navegador).
7. Gas = unidad de coste computacional. Necesario para evitar spam y compensar a los validadores.
8. Solidity (también Vyper, pero en el curso usamos Solidity).
9. ERC-20 (fungible) y ERC-721 (NFT).
10. Finanzas descentralizadas. Ejemplos: Uniswap (DEX), Aave (préstamos), MakerDAO (stablecoin DAI).]

---

## Slide 4 — Quiz relámpago: ¿Cuánto recuerdas? ⚡ (Parte 3)

11. ¿Qué es una DAO y qué mecanismo usa para tomar decisiones?
12. ¿Cuál es el trilema de la blockchain? Nombra sus tres vértices.
13. ¿Qué es una dApp y en qué se diferencia de una app web normal?
14. ¿Por qué decimos que Bitcoin es "pseudoanónimo" y no anónimo?
15. **Bonus:** ¿Qué pasaría si una empresa farmacéutica quisiera registrar la trazabilidad de medicamentos en una blockchain pública como Ethereum?

[NOTA PROFESOR: Respuestas esperadas:
11. Organización Autónoma Descentralizada. Usa votación on-chain con tokens de gobernanza.
12. Descentralización, Seguridad, Escalabilidad. Solo puedes optimizar dos a la vez.
13. Una dApp ejecuta su lógica en smart contracts (blockchain), no en servidores centralizados.
14. Las direcciones son públicas pero no llevan nombre. Si se vincula una dirección a una identidad, se pierde el anonimato.
15. Pregunta trampa/puente al tema de hoy. Problemas: datos de pacientes visibles, coste de gas, rendimiento limitado, regulación exige control de acceso. Esto nos lleva a... blockchain permissioned.]

---

## Slide 5 — Treasure Hunt: ¿Quién creó Hyperledger? 🏴‍☠️

**Misión de investigación (10 minutos):**

Sigue las pistas para descubrir el origen de Hyperledger:

1. **Pista 1:** Su logo es un pingüino gigante y contribuyó a que Linux sea lo que es hoy. ¿De qué organización hablamos?
2. **Pista 2:** Esta organización anunció un nuevo proyecto blockchain en diciembre de 2015. ¿Cómo se llamó?
3. **Pista 3:** Busca en https://www.hyperledger.org — ¿Cuántos proyectos diferentes hay bajo su paraguas?
4. **Pista 4:** ¿Qué grandes empresas fueron miembros fundadores? (Nombra al menos 5)
5. **Pista 5:** ¿Qué relación tiene con la Linux Foundation? ¿Es un competidor de Ethereum?

[NOTA PROFESOR: Respuestas:
1. La Linux Foundation (Tux es el pingüino mascota de Linux).
2. Hyperledger, anunciado en diciembre de 2015.
3. Múltiples proyectos: Fabric, Besu, Iroha, Sawtooth, Indy, Aries, Caliper, Cacti (Cactus), Firefly, etc. El número exacto varía porque algunos se retiran y otros se añaden.
4. IBM, Intel, SAP, Fujitsu, Cisco, J.P. Morgan, DTCC, entre otros.
5. Hyperledger es un PROYECTO de la Linux Foundation, no una empresa. No compite con Ethereum: son paradigmas distintos (permissioned vs público). Pueden ser complementarios.]

---

## Slide 6 — Portada sección

**De blockchain público a permissioned**
El giro empresarial

[IMAGEN: Una autopista que se bifurca en dos caminos: uno abierto al público con multitud de coches (blockchain público) y otro con una barrera de control de acceso y coches corporativos identificados (blockchain permissioned)]

---

## Slide 7 — El trilema revisitado: ¿dónde encaja la empresa?

[IMAGEN: Triángulo del trilema blockchain (Descentralización, Seguridad, Escalabilidad) con dos zonas marcadas: blockchains públicas cerca del vértice Descentralización-Seguridad, y blockchains empresariales cerca del vértice Seguridad-Escalabilidad]

- Las blockchains **públicas** (Bitcoin, Ethereum) priorizan **descentralización + seguridad**.
- Las blockchains **permissioned** sacrifican descentralización total a cambio de **seguridad + escalabilidad + privacidad**.
- No es "mejor" ni "peor": es un **trade-off** según el caso de uso.

> "No necesitas que 10.000 nodos anónimos validen tu factura entre proveedores."

[NOTA PROFESOR: Clave: el trilema no es una ley física, es un modelo mental. Fabric relaja la descentralización (participantes conocidos) y a cambio gana rendimiento, privacidad y control. Preguntar a los alumnos: ¿tiene sentido que una cadena de suministro entre 5 empresas use PoW con mineros anónimos?]

---

## Slide 8 — Público vs Permissioned vs Privado

| Característica | Público | Permissioned (consorcio) | Privado |
|---|---|---|---|
| **¿Quién puede unirse?** | Cualquiera | Solo miembros autorizados | Una sola organización |
| **¿Quién valida?** | Cualquier nodo (minero/validador) | Nodos seleccionados del consorcio | La propia organización |
| **Identidad** | Pseudoanónima | Conocida y verificada | Totalmente conocida |
| **Transparencia** | Total (todo es público) | Selectiva (canales privados) | Solo interna |
| **Confianza** | En el protocolo (trustless) | En el consorcio + protocolo | En la organización |
| **Rendimiento** | Bajo-medio (~15-100 TPS) | Alto (~1.000-20.000 TPS) | Muy alto |
| **Ejemplos** | Bitcoin, Ethereum | Hyperledger Fabric, R3 Corda | Bases de datos internas |

[NOTA PROFESOR: Enfatizar que "permissioned" no significa "centralizado". Un consorcio de 20 hospitales es descentralizado entre sus miembros, pero no es abierto al mundo. La columna "Privado" a veces se confunde con permissioned — aclara que una blockchain de un solo dueño pierde mucho sentido frente a una base de datos tradicional.]

---

## Slide 9 — ¿Por qué las empresas no usan Ethereum directamente?

[IMAGEN: Ejecutivo mirando una pantalla de Ethereum con cara de preocupación, rodeado de señales de advertencia: privacidad, velocidad, regulación]

**5 razones clave:**

1. **Privacidad** — Todas las transacciones son públicas. ¿Quieres que tu competencia vea tus operaciones?
2. **Rendimiento predecible** — Gas variable, congestión de red, tiempos de bloque no garantizados.
3. **Gobernanza controlada** — ¿Quién decide las reglas? En Ethereum, la comunidad global. Las empresas necesitan acuerdos entre partes conocidas.
4. **Identidad conocida** — La regulación (KYC/AML) exige saber quién participa. Los pseudónimos no sirven.
5. **Cumplimiento normativo** — GDPR (derecho al olvido) vs inmutabilidad total. Datos en servidores en jurisdicciones desconocidas.

[NOTA PROFESOR: No presentar esto como "Ethereum es malo". Ethereum es brillante para lo que fue diseñado. Pero el mundo empresarial tiene requisitos distintos. Preguntar: ¿usarías una plaza pública para una reunión confidencial del consejo de administración? No. Pero la plaza sigue siendo útil para otras cosas.]

---

## Slide 10 — ¿Y Ethereum Layer 2? ¿Y las sidechains?

Pregunta legítima: ¿No resuelven los L2 estos problemas?

| Solución | ¿Resuelve privacidad? | ¿Resuelve identidad? | ¿Resuelve gobernanza? |
|---|---|---|---|
| Rollups (Optimistic/ZK) | Parcialmente | No | No |
| Sidechains | Parcialmente | Parcialmente | Parcialmente |
| Appchains | Sí (con configuración) | Parcialmente | Parcialmente |
| **Blockchain permissioned** | **Sí, por diseño** | **Sí, por diseño** | **Sí, por diseño** |

> La clave: en una blockchain permissioned, la privacidad, identidad y gobernanza **no son parches**, son **decisiones de arquitectura desde el día cero**.

[NOTA PROFESOR: Es importante abordar esto porque los alumnos vienen de 7 días de blockchain público y pueden pensar que L2 resuelve todo. Reconocer que el ecosistema Ethereum está evolucionando (zkEVM, account abstraction, etc.) pero que para muchos casos enterprise, una red permissioned sigue siendo más práctica y directa.]

---

## Slide 11 — Portada sección

**El proyecto Hyperledger**
El paraguas open-source de la Linux Foundation para blockchain empresarial

[IMAGEN: Logo de Hyperledger con el invernadero/greenhouse como metáfora visual, rodeado de logos de los distintos subproyectos]

---

## Slide 12 — Hyperledger: origen y filosofía

- **Fundación:** Diciembre 2015, por la **Linux Foundation**.
- **Objetivo:** Crear tecnologías blockchain **open-source** de grado empresarial.
- **Filosofía:** No hay "una sola blockchain Hyperledger". Es un **invernadero** (greenhouse) de proyectos.
- **Miembros fundadores:** IBM, Intel, SAP, Cisco, Fujitsu, J.P. Morgan, DTCC, entre otros.
- **Modelo de gobernanza:** Meritocracia abierta, como Linux. Contribuyes código, ganas voz.

**Datos clave:**
- +300 organizaciones miembro
- +16.000 participantes en la comunidad
- Proyectos con licencia Apache 2.0 (libre uso comercial)

[NOTA PROFESOR: Hacer la analogía con Linux: así como la Linux Foundation no es "dueña" de Linux sino que coordina su desarrollo colaborativo, Hyperledger coordina múltiples proyectos blockchain. Nadie controla Fabric como IBM no controla Linux (aunque contribuya mucho). Eso da confianza a las empresas para adoptarlo.]

---

## Slide 13 — El ecosistema Hyperledger: no es UNA blockchain

[IMAGEN: Mapa visual del ecosistema Hyperledger como un invernadero con distintas plantas/proyectos, agrupados en categorías: Distributed Ledgers, Libraries, Tools]

**Plataformas blockchain (Distributed Ledgers):**
- **Fabric** — Blockchain modular para consorcios. El más adoptado.
- **Besu** — Cliente Ethereum en Java. Soporta redes públicas y permissioned.
- **Iroha** — Diseñado para móvil e IoT. Simple y ligero.
- **Sawtooth** — Arquitectura modular de Intel. Consenso PoET.

**Identidad y credenciales:**
- **Indy** — Identidad descentralizada (SSI).
- **Aries** — Framework de agentes para credenciales verificables.
- **AnonCreds** — Credenciales anónimas.

**Herramientas:**
- **Caliper** — Benchmarking de rendimiento para blockchains.
- **Cacti** (antes Cactus) — Interoperabilidad entre blockchains.
- **Firefly** — Supernode para construir apps Web3 empresariales.

---

## Slide 14 — Comparativa rápida de los proyectos principales

| Proyecto | Tipo de red | Consenso | Smart Contracts | Caso de uso ideal |
|---|---|---|---|---|
| **Fabric** | Permissioned | Pluggable (Raft, BFT) | Chaincode (Go, Node, Java) | Consorcios multi-empresa |
| **Besu** | Pública o permissioned | PoS, IBFT 2.0, QBFT, Clique | Solidity (EVM) | Empresas que quieren compatibilidad EVM |
| **Iroha** | Permissioned | YAC (BFT) | Comandos integrados | IoT, banca móvil |
| **Sawtooth** | Permissioned | PoET, PBFT, Raft | Transaction Families | Cadena de suministro, IoT |

[NOTA PROFESOR: Destacar que Besu es interesante como puente: los alumnos ya conocen la EVM y Solidity, y Besu permite usar esa tecnología en redes permissioned. Pero Fabric es el que estudiaremos en profundidad porque tiene la arquitectura más diferenciada y la mayor adopción enterprise. Mencionar que algunos proyectos como Sawtooth han reducido su actividad.]

---

## Slide 15 — ¿Por qué Fabric es el más adoptado en enterprise?

[IMAGEN: Gráfico de barras mostrando adopción relativa de plataformas enterprise blockchain, con Fabric destacado claramente]

**Razones de la adopción de Fabric:**

1. **Arquitectura modular** — Puedes cambiar consenso, identidad, base de datos sin reescribir la app.
2. **Canales privados** — Múltiples "subredes" dentro de la misma red. Datos aislados entre canales.
3. **Identidad real** — Cada participante tiene certificados X.509 emitidos por una CA (Certificate Authority).
4. **Sin criptomoneda** — No necesitas tokens para operar. Sin volatilidad, sin especulación.
5. **Execute-Order-Validate** — Arquitectura única que mejora rendimiento y privacidad.
6. **Madurez y comunidad** — +5 años en producción, miles de despliegues reales.
7. **Soporte multi-lenguaje** — Chaincodes en Go, Node.js o Java.

---

## Slide 16 — Portada sección

**Hyperledger Fabric: visión general**
La arquitectura que estudiaremos las próximas semanas

[IMAGEN: Diagrama simplificado de una red Fabric con organizaciones, peers, orderers y un canal conectándolos]

---

## Slide 17 — Fabric en una frase

> **Hyperledger Fabric** es una plataforma de blockchain permissioned, modular y de código abierto, diseñada para que consorcios de organizaciones compartan datos y lógica de negocio con **privacidad, rendimiento y control de acceso**.

**Conceptos clave que iremos desgranando:**

- **Permissioned** — Todos los participantes están identificados.
- **Modular** — Cada componente se puede reemplazar.
- **Consorcio** — La red es gobernada por un grupo de organizaciones.
- **Canales** — Sub-redes privadas dentro de la misma infraestructura.
- **Chaincode** — El equivalente a los smart contracts.

[NOTA PROFESOR: No intentar explicar todo hoy. El objetivo es que los alumnos entiendan el QUÉ y el POR QUÉ. El CÓMO vendrá en los días 9 en adelante. Ir colocando los términos para que cuando los vean en profundidad ya suenen familiares.]

---

## Slide 18 — Red permissioned: todos se conocen

[IMAGEN: Comparativa visual: a la izquierda, red P2P con nodos anónimos y signos de interrogación; a la derecha, red donde cada nodo tiene un nombre, un logo corporativo y un certificado digital]

**En Ethereum:**
- Cualquiera puede unirse con un nodo anónimo.
- La identidad es una dirección hexadecimal (0x...).
- No sabes quién valida tu transacción.

**En Fabric:**
- Para unirte necesitas un **certificado digital** emitido por una **CA** (Autoridad de Certificación).
- Cada organización gestiona su propia CA.
- Sabes exactamente **quién propone, quién valida y quién ordena**.
- Las políticas definen **quién puede hacer qué** (endorsement policies).

---

## Slide 19 — Arquitectura modular: piezas intercambiables

[IMAGEN: Diagrama tipo Lego donde cada pieza tiene un nombre: Consenso, Identidad (MSP), Ledger, Smart Contract, Comunicación — las piezas se pueden desmontar y sustituir]

| Componente | Función | Opciones |
|---|---|---|
| **Consenso** | Ordenar transacciones | Raft (CFT), BFT (nuevo en v3.0) |
| **Identidad (MSP)** | Gestionar quién es quién | x.509 con Fabric CA, LDAP externo |
| **Base de datos del estado** | Almacenar estado actual | LevelDB (key-value), CouchDB (JSON queries) |
| **Chaincode** | Lógica de negocio | Go, Node.js, Java |
| **Comunicación** | Protocolos de red | gRPC |

> "Modular" significa que puedes sustituir piezas sin rehacer toda la red. Como cambiar el motor de un coche sin cambiar la carrocería.

[NOTA PROFESOR: No profundizar en cada componente. El objetivo es que vean que Fabric no es monolítico. En días posteriores entraremos en detalle en MSP, ordenadores, peers, etc. Si preguntan por BFT, explicar que es Byzantine Fault Tolerant — resiste nodos maliciosos, a diferencia de Raft que solo tolera nodos caídos (crash).]

---

## Slide 20 — Canales: múltiples ledgers privados

[IMAGEN: Diagrama de una red Fabric con 4 organizaciones (Org1, Org2, Org3, Org4). Canal A conecta Org1+Org2, Canal B conecta Org2+Org3+Org4. Las organizaciones que no están en un canal NO ven esos datos]

**¿Qué es un canal?**
- Una **sub-red privada** dentro de la red Fabric.
- Cada canal tiene su **propio ledger** (cadena de bloques + estado).
- Solo los miembros del canal ven las transacciones de ese canal.
- Una organización puede participar en **múltiples canales** simultáneamente.

**Ejemplo real:**
- **Canal "Farmacéuticas":** Hospital A + Laboratorio X + Distribuidor Y → trazabilidad de medicamentos.
- **Canal "Seguros":** Hospital A + Aseguradora Z → liquidación de pólizas.
- El Hospital A está en ambos canales, pero el Laboratorio X no ve nada del canal de seguros.

[NOTA PROFESOR: Los canales son un concepto clave y diferenciador de Fabric. No existe un equivalente directo en Ethereum (lo más parecido serían las rollups o sidechains, pero no es lo mismo). Enfatizar que esto resuelve el problema de privacidad de forma nativa.]

---

## Slide 21 — Chaincode: los smart contracts de Fabric

[IMAGEN: Código fuente simplificado de un chaincode en Go al lado de un código Solidity, ambos resaltando una función de transferencia — mostrando las similitudes conceptuales]

| Concepto | Ethereum | Fabric |
|---|---|---|
| **Nombre** | Smart contract | Chaincode |
| **Lenguaje** | Solidity, Vyper | Go, Node.js, Java |
| **Ejecución** | EVM (máquina virtual) | Contenedor Docker aislado |
| **Despliegue** | Cualquiera puede desplegar | Requiere aprobación del consorcio (lifecycle) |
| **Actualización** | Proxy patterns, complicado | Proceso formal de actualización con votación |
| **Estado** | Almacenado en la EVM | Base de datos separada (LevelDB/CouchDB) |

**En Fabric, para desplegar un chaincode necesitas:**
1. Que varias organizaciones lo **aprueben** (endorsement policy).
2. Que se **instale** en los peers de cada organización.
3. Que se **confirme** (commit) en el canal.

---

## Slide 22 — Sin criptomoneda nativa

[IMAGEN: Dos balanzas: una con el símbolo ETH (tiene coste de gas) y otra con el logo de Fabric (sin coste de transacción). La balanza de Fabric tiene "0 gas fees"]

**En Ethereum:**
- Cada transacción cuesta **gas** (pagado en ETH).
- El gas fluctúa según la congestión de la red.
- Necesitas ETH para operar → dependes de un activo volátil.

**En Fabric:**
- **No hay criptomoneda nativa**. No hay gas fees.
- El coste de operar es el **coste de infraestructura** (servidores, cloud).
- Las organizaciones del consorcio acuerdan cómo repartir esos costes.
- Se **puede** crear un token si se necesita (pero no es obligatorio).

> Esto elimina la barrera de entrada para empresas que no quieren exposición a criptomonedas.

[NOTA PROFESOR: Para muchas empresas, el tema cripto es un obstáculo legal o reputacional. Fabric elimina esa fricción. Pero aclarar que si el caso de uso necesita un token (programa de fidelidad, créditos de carbono, etc.), se puede implementar como chaincode.]

---

## Slide 23 — Portada sección

**Debate interactivo**
Ethereum vs Hyperledger Fabric: cara a cara

[IMAGEN: Ring de boxeo con los logos de Ethereum y Hyperledger Fabric en esquinas opuestas, pero con guantes de espuma (debate amistoso, no guerra)]

---

## Slide 24 — Actividad: completa la tabla Ethereum vs Fabric

**En parejas (10 minutos):** Rellena esta tabla con lo que sabes. Después ponemos en común.

| Aspecto | Ethereum | Hyperledger Fabric |
|---|---|---|
| **Tipo de red** | | |
| **Identidad** | | |
| **Consenso** | | |
| **Smart contracts** | | |
| **Visibilidad de datos** | | |
| **Coste por transacción** | | |
| **Rendimiento (TPS)** | | |
| **Finalidad** | | |
| **Gobernanza** | | |
| **Caso de uso ideal** | | |

[NOTA PROFESOR: Respuestas esperadas:
- Tipo de red: Público vs Permissioned.
- Identidad: Pseudoanónima (dirección 0x) vs Certificados X.509 (identidad real).
- Consenso: PoS (validators) vs Raft/BFT (orderers del consorcio).
- Smart contracts: Solidity en EVM vs Chaincode en Go/Node/Java en Docker.
- Visibilidad: Todo público en el ledger vs Solo los miembros del canal.
- Coste: Gas en ETH (variable) vs Sin criptomoneda (coste de infra).
- Rendimiento: ~15-100 TPS (L1) vs ~1.000-3.000+ TPS.
- Finalidad: Probabilística (~12 min BTC, ~12 seg ETH) vs Determinista (segundos).
- Gobernanza: Comunidad abierta (EIPs) vs Consorcio con políticas definidas.
- Caso de uso: Apps públicas, DeFi, NFTs vs Consorcios empresariales, cadena de suministro, banca.]

---

## Slide 25 — Debate: ¿son rivales o complementarios?

[IMAGEN: Diagrama de Venn donde un círculo es "Blockchain público" y el otro es "Blockchain permissioned", con una zona de intersección etiquetada "casos híbridos"]

**Argumentos para "son rivales":**
- Compiten por el mismo presupuesto enterprise.
- Ethereum L2 + privacidad (zkEVM) se acerca al terreno de Fabric.
- Besu permite usar Ethereum en modo permissioned.

**Argumentos para "son complementarios":**
- Resuelven problemas distintos con distintos trade-offs.
- Una empresa puede usar Fabric internamente y anclar pruebas en Ethereum público.
- Los puentes cross-chain (como Cacti de Hyperledger) los conectan.
- Un consorcio puede tokenizar activos en Fabric y comercializarlos en un mercado público.

> **No hay una blockchain que sirva para todo. Hay la blockchain adecuada para cada problema.**

[NOTA PROFESOR: Fomentar un debate real. Dividir la clase en dos equipos: Team Ethereum y Team Fabric. Cada uno defiende su postura durante 5 minutos. Después, pedir a cada equipo que reconozca una ventaja del otro. El mensaje final es que son herramientas complementarias.]

---

## Slide 26 — Portada sección

**Actividad práctica**
¿Blockchain público, permissioned, o nada de blockchain?

[IMAGEN: Tres puertas etiquetadas: Puerta 1 "Blockchain público", Puerta 2 "Blockchain permissioned", Puerta 3 "No necesitas blockchain" — un personaje pensativo delante de las tres]

---

## Slide 27 — Actividad: clasifica estos 10 escenarios

**En grupos de 3-4 (15 minutos).** Para cada escenario, decide: **Público, Permissioned, o No necesita blockchain.** Justifica tu respuesta.

1. **Sistema de votación** para las elecciones generales de un país.
2. **Trazabilidad de atún** desde el barco pesquero hasta el supermercado, entre 8 empresas.
3. **Programa de puntos de fidelidad** de una sola cadena de supermercados.
4. **Mercado de arte digital (NFTs)** abierto a cualquier artista del mundo.
5. **Liquidación de pagos interbancarios** entre 12 bancos de la zona euro.

---

## Slide 28 — Actividad: clasifica estos 10 escenarios (continuación)

6. **Registro de notas académicas** entre 50 universidades de un país.
7. **Crowdfunding descentralizado** donde cualquiera puede crear y financiar proyectos.
8. **Inventario interno** de una empresa con 3 almacenes.
9. **Créditos de carbono** que empresas compran y venden en un mercado regulado.
10. **Identidad digital auto-soberana** para refugiados sin documentación.

[NOTA PROFESOR: Respuestas orientativas (hay debate legítimo en varias):
1. Público (o permissioned con auditoría pública). Necesita transparencia y resistencia a censura. Debate: ¿quién controla los nodos?
2. Permissioned (Fabric). Participantes conocidos, datos comerciales sensibles, número limitado de actores.
3. No necesita blockchain. Un solo actor = base de datos centralizada es más eficiente.
4. Público. Abierto a cualquiera, sin permisos, mercado global.
5. Permissioned. Participantes regulados, alta velocidad, privacidad entre bancos.
6. Permissioned. Universidades identificadas, datos personales (GDPR), consorcio definido.
7. Público. Abierto, sin censura, cualquiera participa.
8. No necesita blockchain. Una sola empresa = base de datos interna.
9. Permissioned (posiblemente con puente a público para transparencia). Regulado pero necesita confianza entre partes.
10. Público + identidad descentralizada (Indy/Aries). No depende de ningún gobierno. Debate interesante sobre privacidad.
Aceptar respuestas bien argumentadas aunque difieran. Lo importante es el razonamiento.]

---

## Slide 29 — El test del "¿necesitas blockchain?"

[IMAGEN: Diagrama de flujo / árbol de decisión con preguntas tipo sí/no que lleva a tres conclusiones: "Usa blockchain público", "Usa blockchain permissioned", "No necesitas blockchain"]

**Preguntas clave:**

1. ¿Hay **múltiples partes** que necesitan compartir datos? → Si no → **No necesitas blockchain**.
2. ¿Esas partes **no confían plenamente** entre sí? → Si no → **Base de datos compartida**.
3. ¿Necesitas un **registro inmutable y auditable**? → Si no → **Base de datos compartida**.
4. ¿Los participantes son **conocidos y regulados**? → Si sí → **Permissioned**. Si no → continuar.
5. ¿Necesitas que **cualquiera pueda participar** sin permiso? → Si sí → **Público**.

> "La mejor blockchain es la que no usas cuando no la necesitas."

[NOTA PROFESOR: Este árbol de decisión es una simplificación, pero funciona como herramienta mental. En la vida real hay más matices: requisitos legales, costes de desarrollo, madurez del equipo técnico, etc. Pero el punto clave es: blockchain no es la solución a todo. Es una herramienta más.]

---

## Slide 30 — Preguntas de repaso del Día 8

**Responde individualmente:**

1. ¿Qué es Hyperledger y qué relación tiene con la Linux Foundation?
2. Nombra tres diferencias fundamentales entre una blockchain pública y una permissioned.
3. ¿Por qué las empresas suelen preferir blockchain permissioned sobre público? Da dos razones.
4. ¿Qué es un canal en Hyperledger Fabric y qué problema resuelve?
5. ¿Por qué decimos que Fabric tiene arquitectura "modular"? Da un ejemplo.
6. ¿En qué lenguajes se pueden escribir chaincodes en Fabric?
7. ¿Por qué Fabric no tiene criptomoneda nativa? ¿Es eso una ventaja o desventaja?
8. Describe un caso de uso donde blockchain permissioned sea mejor opción que público, y explica por qué.

[NOTA PROFESOR: Estas preguntas pueden servir como tarea para casa o como cierre rápido en los últimos 10 minutos. Las preguntas 7 y 8 son abiertas a propósito para fomentar el pensamiento crítico. No hay respuesta única correcta en la 7.]

---

## Slide 31 — Resumen del Día 8

**Hoy hemos aprendido:**

- Las blockchains públicas y permissioned resuelven **problemas diferentes** con **trade-offs diferentes**.
- **Hyperledger** es un paraguas de proyectos open-source de la Linux Foundation, no una sola blockchain.
- **Hyperledger Fabric** es el proyecto más adoptado para consorcios empresariales.
- Fabric es **permissioned** (identidades reales), **modular** (piezas intercambiables) y usa **canales** (privacidad nativa).
- Los smart contracts en Fabric se llaman **chaincodes** y se escriben en Go, Node.js o Java.
- No toda solución necesita blockchain. Y no toda blockchain necesita ser pública.

**A partir de mañana:** nos sumergimos de lleno en la arquitectura de Fabric — peers, orderers, MSP, ledger, y el flujo completo de una transacción.

[IMAGEN: Mapa de ruta del curso mostrando los días 1-7 (blockchain público) completados y el día 8 como puente, con los días 9+ (Hyperledger Fabric en profundidad) por delante]

[NOTA PROFESOR: Cerrar con entusiasmo: "Ya tenéis las bases de blockchain público. A partir de ahora, entramos en el mundo enterprise con Fabric. Todo lo que aprendisteis sobre hashes, criptografía, consenso y smart contracts sigue siendo válido — pero aplicado de forma diferente." Si hay tiempo, preguntar: ¿qué es lo que más os ha sorprendido de las diferencias entre público y permissioned?]

---

## Actividad de relleno (si sobra tiempo)

### El juicio a Blockchain (30-45 min)

- Simulación de un juicio donde Blockchain está siendo juzgada por "no cumplir sus promesas".
- Roles:
  - **Fiscal** (1 grupo): argumenta que blockchain ha fracasado. Puede usar: bajo rendimiento, hackeos, Terra/Luna, proyectos abandonados (TradeLens de Maersk), consumo energético, complejidad, falta de adopción real.
  - **Defensa** (1 grupo): argumenta que blockchain está transformando industrias. Puede usar: tokenización de bonos, DeFi, identidad digital, CBDCs, transparencia, reducción de intermediarios.
  - **Jurado** (resto de la clase): escucha ambos lados y vota culpable o inocente.
  - **Juez** (profesor): modera y asegura que los argumentos son técnicamente correctos.
- Preparación: 10 minutos para que fiscal y defensa armen sus argumentos.
- Juicio: 5 minutos fiscal, 5 minutos defensa, 5 minutos de réplicas cruzadas.
- Deliberación del jurado: 5 minutos.
- Veredicto y debate abierto.

[NOTA PROFESOR: Esta actividad funciona muy bien como cierre del bloque "blockchain genérico" antes de entrar en Fabric. Obliga a los alumnos a sintetizar todo lo aprendido en 7 días y defenderlo con argumentos. El fiscal tiene argumentos legítimos — es importante que los alumnos reconozcan las limitaciones reales. Lo ideal es que el veredicto sea "inocente con matices".]
