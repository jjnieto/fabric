# Día 7 — dApps, DeFi, DAOs, escalabilidad y casos de uso

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos divertidos del mundo cripto - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre DeFi, DAOs o dApps. Ejemplos: hackeos de protocolos DeFi, récords de TVL, nuevas DAOs curiosas, adopción institucional de blockchain, etc. Actualizar antes de cada edición del curso.]

---

## Mini Treasure Hunt — ¿Cuánto dinero hay en DeFi? 🏴‍☠️

Antes de empezar con la teoría, vamos a investigar el tamaño real de las finanzas descentralizadas.

**Misión rápida (10 minutos):**
1. Ir a https://defillama.com/
2. ¿Cuál es el **TVL (Total Value Locked)** total en DeFi ahora mismo?
3. ¿Cuáles son los **3 protocolos** con mayor TVL?
4. ¿En qué **blockchain** hay más valor bloqueado?
5. Buscar **Uniswap** en DeFiLlama. ¿Cuánto TVL tiene? ¿En cuántas cadenas opera?
6. **Bonus:** ¿Cuál fue el pico máximo histórico de TVL en DeFi y en qué fecha ocurrió?

[NOTA PROFESOR: Respuestas aproximadas (varían con el mercado):
- El TVL total de DeFi suele estar entre 50.000 y 200.000 millones de USD dependiendo del momento del mercado.
- Los protocolos top suelen ser Lido (staking líquido), Aave (préstamos), MakerDAO/Sky (stablecoins) y Uniswap (DEX).
- Ethereum domina con más del 50-60% del TVL total.
- El pico histórico fue en noviembre de 2021, superando los 180.000 millones de USD.
- Esta actividad sirve para que los alumnos dimensionen el ecosistema DeFi antes de estudiarlo en detalle.]

---

## Slide 2 — Portada sección

**Blockchain**
dApps: Aplicaciones Descentralizadas

[IMAGEN: Iconos de aplicaciones dentro de una red descentralizada de nodos]

---

## Slide 3 — ¿Qué es una dApp?

Una **dApp** (Decentralized Application) es una aplicación cuya lógica de negocio se ejecuta en una blockchain a través de smart contracts.

**Diferencias con una app tradicional:**

| Aspecto | App tradicional | dApp |
|---------|----------------|------|
| **Backend** | Servidores centralizados | Smart contracts en blockchain |
| **Datos** | Base de datos privada | Blockchain pública |
| **Control** | La empresa propietaria | Los usuarios/la comunidad |
| **Censura** | Puede ser censurada o cerrada | Resistente a la censura |
| **Autenticación** | Usuario y contraseña | Wallet (clave privada) |

---

## Slide 4 — Categorías de dApps

[IMAGEN: Mapa visual con 4 grandes categorías de dApps y ejemplos de cada una]

- **DeFi** (Finanzas descentralizadas): Uniswap, Aave, MakerDAO, Compound, dYdX
- **NFTs y Metaverso:** OpenSea, Blur, Decentraland, The Sandbox
- **DAOs** (Organizaciones autónomas): MakerDAO, Uniswap DAO, Aave DAO
- **Otras:** juegos (Axie Infinity), identidad digital, cadena de suministro, seguros

---

## Slide 5 — Portada sección

**Blockchain**
Exchanges: CEX vs DEX

[IMAGEN: Dos edificios enfrentados: uno corporativo con logo centralizado y otro hecho de nodos interconectados]

---

## Slide 6 — CEX: Exchanges centralizados

Un **CEX** (Centralized Exchange) es una plataforma gestionada por una empresa que actúa como intermediario entre compradores y vendedores.

**Características:**
- La empresa custodia los fondos del usuario
- Requiere registro con KYC (verificación de identidad)
- Interfaz familiar, similar a un bróker tradicional
- Ofrece soporte al cliente, protección ante errores
- Opera bajo regulación financiera

**Ejemplos:** Coinbase, Binance, Kraken, Bitfinex

**Riesgo:** si el exchange quiebra o es hackeado, los fondos del usuario pueden perderse (caso FTX, 2022)

---

## Slide 7 — DEX: Exchanges descentralizados

Un **DEX** (Decentralized Exchange) es un protocolo que permite intercambiar tokens directamente entre usuarios, sin intermediarios.

**Características:**
- El usuario mantiene la custodia de sus fondos en todo momento
- No requiere registro ni KYC
- Funciona mediante smart contracts y pools de liquidez
- Sin soporte al cliente: el usuario es responsable de sus acciones
- Resistente a la censura

**Ejemplos:** Uniswap, SushiSwap, Curve, PancakeSwap

**Riesgo:** contratos con bugs, tokens fraudulentos (rug pulls), impermanent loss

---

## Slide 8 — CEX vs DEX: Comparativa

| Aspecto | CEX | DEX |
|---------|-----|-----|
| **Custodia** | El exchange guarda tus fondos | Tú controlas tus fondos |
| **KYC** | Obligatorio | No requerido |
| **Velocidad** | Rápido (base de datos interna) | Depende de la blockchain |
| **Liquidez** | Alta (order books) | Variable (pools de liquidez) |
| **Soporte** | Sí | No |
| **Regulación** | Regulado | No regulado |
| **Riesgo principal** | Quiebra del exchange | Bug en el smart contract |

---

## Slide 9 — Práctica: Explorar Coinbase

1. Ir a https://www.coinbase.com/ (no es necesario crear cuenta)
2. Explorar la interfaz pública: precios, gráficos, mercados disponibles
3. Observar los **pares de trading** disponibles (BTC/USD, ETH/EUR, etc.)
4. Buscar las **comisiones** que cobra Coinbase
5. ¿Qué información pide para registrarte? (KYC)
6. Buscar la sección de "Earn" o "Learn": ¿qué ofrece?

[NOTA PROFESOR: El objetivo es que los alumnos vean cómo funciona un CEX real sin necesidad de crear cuenta ni depositar fondos. Si algún alumno ya tiene cuenta, puede mostrar la interfaz logueada.]

---

## Slide 10 — Práctica: Uniswap con MetaMask (Testnet)

1. Abrir MetaMask y asegurarse de estar en la red **Sepolia**
2. Ir a https://app.uniswap.org/
3. Conectar MetaMask a Uniswap
4. Cambiar a la red de pruebas Sepolia dentro de Uniswap
5. Intentar hacer un **swap** de Sepolia ETH por otro token de prueba
6. Observar:
   - ¿Qué información muestra antes de confirmar?
   - ¿Cuánto gas cuesta la operación?
   - ¿Dónde se ve el slippage (deslizamiento de precio)?
   - ¿Qué pasa al confirmar en MetaMask?

[NOTA PROFESOR: Es posible que los tokens de prueba en Sepolia no siempre estén disponibles en Uniswap. Tener preparada una alternativa: mostrar un swap real en mainnet de Ethereum sin ejecutarlo (solo llegar hasta la pantalla de confirmación para ver los datos). Lo importante es que los alumnos vean la interfaz de un DEX y comparen con Coinbase.]

---

## Slide 11 — Debate: Uniswap vs Coinbase

Después de explorar ambas plataformas, debatir:

1. **Facilidad de uso:** ¿cuál es más intuitiva para alguien sin experiencia?
2. **Control:** ¿en cuál tienes más control sobre tus fondos?
3. **Confianza:** ¿de quién depende que tu dinero esté seguro en cada caso?
4. **Transparencia:** ¿en cuál puedes verificar exactamente qué ocurre con tu transacción?
5. **Adopción masiva:** ¿cuál tiene más probabilidades de llegar al público general?
6. **Escenario:** si mañana Coinbase cierra, ¿qué pasa con tus fondos? ¿Y si Uniswap desaparece como empresa?

[NOTA PROFESOR: Punto clave del debate: si Coinbase cierra, los fondos están en riesgo (caso FTX). Si Uniswap como empresa desaparece, el smart contract sigue funcionando en Ethereum porque es imparable. Pero Uniswap es mucho más difícil de usar para el público general. La pregunta de fondo es: ¿merece la pena la complejidad a cambio de la descentralización?]

---

## Slide 12 — Portada sección

**Blockchain**
DeFi: Finanzas Descentralizadas

[IMAGEN: Edificio bancario tradicional desintegrándose en bloques digitales que forman una red descentralizada]

---

## Slide 13 — DeFi: Principales categorías

Las finanzas descentralizadas replican los servicios financieros tradicionales usando smart contracts:

| Categoría | Servicio tradicional | Equivalente DeFi | Ejemplo |
|-----------|---------------------|-------------------|---------|
| **Préstamos** | Banco te presta dinero | Protocolo de lending | Aave, Compound |
| **Stablecoins** | Banco central emite moneda | Smart contract genera stablecoin | MakerDAO (DAI) |
| **Trading** | Bróker / Exchange | DEX | Uniswap, Curve |
| **Derivados** | Mercado de futuros | Protocolo de derivados | dYdX, GMX |
| **Seguros** | Aseguradora | Protocolo de seguros | Nexus Mutual |
| **Ahorro** | Depósito bancario | Yield farming / Staking | Lido, Yearn |

---

## Slide 14 — DeFi: Préstamos descentralizados

**¿Cómo funciona un préstamo en DeFi?**

1. El **prestamista** deposita sus tokens en un pool de liquidez (por ejemplo, USDC)
2. El **prestatario** deposita un colateral (por ejemplo, ETH) por valor superior al préstamo (sobrecolateralización, típicamente 150%)
3. El prestatario recibe el préstamo (USDC) y paga intereses
4. Si el valor del colateral cae por debajo del umbral, se **liquida automáticamente** para proteger al prestamista

**Diferencias con un banco:**
- No hay aprobación humana ni scoring crediticio
- Todo es automático mediante smart contracts
- Cualquiera puede ser prestamista o prestatario
- Los tipos de interés se ajustan por oferta/demanda en tiempo real

---

## Slide 15 — Portada sección

**Blockchain**
Oráculos

[IMAGEN: Oráculo griego antiguo con datos digitales fluyendo desde el mundo exterior hacia una blockchain]

---

## Slide 16 — ¿Por qué los smart contracts necesitan oráculos?

- Los smart contracts solo pueden acceder a datos **dentro** de la blockchain
- No pueden consultar APIs externas, páginas web o bases de datos
- Pero muchos contratos necesitan datos del mundo real:
  - ¿Cuál es el precio actual de ETH en dólares?
  - ¿Ha llovido más de 50mm en Madrid hoy? (seguros paramétricos)
  - ¿Quién ganó el partido de fútbol? (apuestas)
  - ¿Cuál es el tipo de cambio EUR/USD?

Los **oráculos** son servicios que traen datos del mundo exterior a la blockchain de forma verificable y segura.

[IMAGEN: Diagrama: Mundo real (APIs, sensores, datos) → Oráculo → Blockchain → Smart Contract ejecuta lógica]

---

## Slide 17 — Tipos de oráculos

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Centralizado** | Un único proveedor aporta los datos | API de un exchange |
| **Descentralizado** | Múltiples nodos independientes agregan datos y llegan a consenso | Chainlink |
| **Inbound** | Datos del mundo real → blockchain | Precio de ETH |
| **Outbound** | Blockchain → acciones en el mundo real | Enviar un email al cumplirse una condición |
| **Hardware** | Sensores físicos que alimentan la blockchain | Sensores IoT, lectores RFID |

---

## Slide 18 — Chainlink: El estándar de los oráculos

**Chainlink** es la red de oráculos descentralizados más utilizada en blockchain.

**Servicios principales:**

| Servicio | Descripción |
|----------|-------------|
| **Price Feeds** | Precios de activos actualizados en tiempo real. Usados por Aave, Compound, dYdX y la mayoría de protocolos DeFi |
| **VRF (Verifiable Random Function)** | Generación de números aleatorios verificables on-chain. Usado en juegos, loterías y NFTs |
| **Automation** | Ejecución automática de funciones de smart contracts cuando se cumplen condiciones (reemplaza la necesidad de cron jobs) |
| **CCIP (Cross-Chain Interoperability Protocol)** | Comunicación segura entre diferentes blockchains |

---

## Slide 19 — Chainlink: Slashing y seguridad

¿Cómo garantiza Chainlink que los datos sean correctos?

- Cada nodo operador debe depositar tokens **LINK** como garantía (stake)
- Si un nodo proporciona datos incorrectos o no responde a tiempo, pierde parte de su stake (**slashing**)
- Los datos se agregan de **múltiples nodos independientes** y se calcula la mediana, eliminando valores atípicos
- Los nodos tienen reputación pública verificable on-chain

**Incentivos alineados:** mentir cuesta dinero, ser honesto genera recompensas.

[IMAGEN: Diagrama de nodos Chainlink: múltiples fuentes de datos → múltiples nodos → agregación → resultado final en blockchain]

---

## Slide 20 — Práctica: Aave en testnet

**Aave** es uno de los protocolos de préstamos DeFi más importantes.

1. Ir a https://app.aave.com/
2. Conectar MetaMask (red Sepolia o la testnet disponible en Aave)
3. Obtener tokens de prueba del faucet de Aave (si está disponible)
4. **Depositar** tokens como colateral
5. **Pedir un préstamo** contra ese colateral
6. Observar:
   - ¿Qué tasa de interés te ofrecen?
   - ¿Cuál es el ratio de colateralización?
   - ¿Qué pasa si el colateral baja de valor? (Health Factor)
7. **Devolver el préstamo** y recuperar el colateral

[NOTA PROFESOR: Aave tiene una interfaz de testnet que puede cambiar de URL o red. Verificar antes de clase que la testnet de Aave está operativa. Si no lo está, hacer una demostración en pantalla con la interfaz real en mainnet sin ejecutar transacciones. Lo importante es que los alumnos entiendan el flujo de préstamo/devolución y el concepto de liquidación.]

---

## Slide 21 — Práctica: dYdX en testnet

**dYdX** es un protocolo de derivados descentralizado que permite operar con futuros perpetuos.

1. Ir a https://trade.dydx.exchange/ (testnet si disponible)
2. Conectar wallet
3. Explorar la interfaz:
   - ¿Qué pares de trading están disponibles?
   - ¿Qué apalancamiento máximo ofrecen?
   - ¿Cómo funciona la liquidación?
4. Abrir una posición **long** (apuesta a que el precio sube) con poco capital de prueba
5. Abrir una posición **short** (apuesta a que el precio baja)
6. Observar cómo varía el PnL (beneficio/pérdida) en tiempo real

[NOTA PROFESOR: dYdX migró a su propia cadena basada en Cosmos. La interfaz de testnet puede variar. Si no está disponible, hacer demostración en pantalla. Lo importante es que los alumnos entiendan qué son los futuros perpetuos, el apalancamiento y la liquidación. Advertir que en el mundo real el trading con apalancamiento es extremadamente arriesgado.]

---

## Slide 22 — Portada sección

**Blockchain**
DAOs: Organizaciones Autónomas Descentralizadas

[IMAGEN: Grupo de personas votando digitalmente conectadas por una red blockchain, sin jefe ni oficina central]

---

## Slide 23 — ¿Qué es una DAO?

Una **DAO** (Decentralized Autonomous Organization) es una organización gobernada por smart contracts donde las decisiones se toman mediante votación de sus miembros.

**Características:**
- **Sin jerarquía central:** no hay CEO, consejo de administración ni oficinas
- **Gobernanza on-chain:** las propuestas y votaciones se registran en blockchain
- **Tokens de gobernanza:** los miembros votan proporcionalmente a sus tokens
- **Ejecución automática:** si una propuesta es aprobada, el smart contract la ejecuta sin intermediarios
- **Tesorería transparente:** los fondos de la DAO están en un smart contract visible por todos

---

## Slide 24 — DAOs: Mecanismos de votación

| Mecanismo | Descripción | Ventajas | Desventajas |
|-----------|-------------|----------|-------------|
| **1 token = 1 voto** | Votación proporcional a la cantidad de tokens | Simple, directo | Las ballenas dominan |
| **Votación cuadrática** | El coste de cada voto adicional crece cuadráticamente | Más equitativo | Vulnerable a Sybil attacks |
| **Delegación** | Los usuarios delegan su voto en un representante | Permite participación pasiva | Concentración de poder |
| **Conviction voting** | Los votos ganan peso con el tiempo | Evita decisiones impulsivas | Lento |
| **Multisig** | Se requiere la firma de N de M miembros | Seguro para tesorerías | Menos descentralizado |

---

## Slide 25 — DAOs: Ejemplos reales

| DAO | Propósito | Tesorería aprox. | Tokens de gobernanza |
|-----|-----------|-----------------|---------------------|
| **MakerDAO** | Gestionar el protocolo de DAI | ~5.000M USD | MKR |
| **Uniswap DAO** | Gobernar el protocolo Uniswap | ~3.000M USD | UNI |
| **Aave DAO** | Gobernar el protocolo de préstamos | ~1.000M USD | AAVE |
| **Lido DAO** | Gestionar el staking líquido | ~2.000M USD | LDO |
| **ConstitutionDAO** | Comprar una copia de la Constitución de EEUU | Recaudó 47M USD | PEOPLE |
| **Nouns DAO** | Arte generativo y financiación de proyectos | ~50M USD | NOUN (1 NFT = 1 voto) |

[NOTA PROFESOR: Los valores de tesorería son aproximados y fluctúan con el mercado. ConstitutionDAO es un ejemplo interesante porque aunque fracasó en su objetivo (no ganó la subasta), demostró el poder de coordinación de una DAO.]

---

## Slide 26 — Caso: The DAO Hack (2016)

**The DAO** fue la primera DAO de la historia. Lanzada en abril de 2016, recaudó **150 millones de dólares** en ETH.

**El ataque (junio de 2016):**
- Un atacante encontró una vulnerabilidad de **reentrancy** en el smart contract
- Explotó la función de retirada de fondos para extraer ETH repetidamente antes de que el contrato actualizara el saldo
- Robó **3,6 millones de ETH** (unos 60 millones de USD en ese momento)

**Consecuencias:**
- La comunidad Ethereum se dividió: ¿revertir el robo o respetar el principio de inmutabilidad?
- Se votó hacer un **hard fork** para devolver los fondos a los inversores
- Los que aceptaron el fork siguieron en **Ethereum (ETH)**
- Los que rechazaron el fork crearon **Ethereum Classic (ETC)**

[IMAGEN: Línea temporal del hack de The DAO: lanzamiento → recaudación → ataque → debate → hard fork → ETH / ETC]

---

## Slide 27 — Caso: Beanstalk DAO Attack (2022)

**Beanstalk** era un protocolo de stablecoin algorítmica gobernado por una DAO.

**El ataque (abril de 2022):**
- El atacante pidió un **flash loan** (préstamo instantáneo sin colateral) por valor de ~1.000 millones de USD
- Usó esos fondos para comprar tokens de gobernanza de Beanstalk
- Con la mayoría de votos, **aprobó una propuesta** que transfería todos los fondos de la tesorería a su wallet
- Devolvió el flash loan y se quedó con ~182 millones de USD de beneficio
- Todo en **una sola transacción** que duró unos 13 segundos

**Lección:** el mecanismo de "1 token = 1 voto" es vulnerable si alguien puede adquirir temporalmente una mayoría de tokens.

[NOTA PROFESOR: Este caso es perfecto para debatir los riesgos de la gobernanza on-chain. Los flash loans permiten acumular poder de voto instantáneamente. Soluciones propuestas: timelocks (retrasar la ejecución de propuestas), requisitos de snapshot del balance previo, períodos de votación más largos.]

---

## Slide 28 — Debate: Pros y contras de las DAOs

**A favor:**
- Transparencia total: todo está on-chain
- Participación global sin barreras geográficas
- Resistencia a la censura
- Alineación de incentivos entre participantes

**En contra:**
- Baja participación en votaciones (fatiga de gobernanza)
- Las ballenas dominan las decisiones
- Vulnerables a ataques (flash loans, Sybil)
- Lentitud en la toma de decisiones
- Responsabilidad legal difusa

**Preguntas para debatir:**
1. ¿Podría una empresa real gobernarse como una DAO?
2. ¿Deberían las DAOs tener personalidad jurídica?
3. ¿Es el modelo "1 token = 1 voto" democrático o plutocrático?

---

## Slide 29 — Práctica: Desplegar una Mini DAO

Vamos a crear un smart contract de gobernanza básico en Remix.

**Funcionalidades de la Mini DAO:**
- Los miembros pueden **crear propuestas** (texto descriptivo)
- Los miembros pueden **votar** a favor o en contra
- Cada dirección solo puede votar **una vez** por propuesta
- Si una propuesta alcanza un mínimo de votos a favor, se marca como **aprobada**
- El creador del contrato puede **añadir miembros** con derecho a voto

**Pasos:**
1. Abrir Remix y crear un fichero `MiniDAO.sol`
2. Pegar el código proporcionado por el profesor
3. Compilar y desplegar en Sepolia
4. Añadir las direcciones de los compañeros como miembros
5. Crear una propuesta (por ejemplo: "¿Debería la clase tener un descanso extra?")
6. Votar entre todos y ver el resultado on-chain

[NOTA PROFESOR: Tener preparado el código de MiniDAO.sol con comentarios didácticos. El contrato debe ser lo más sencillo posible: un mapping de propuestas, un mapping de votos por propuesta/dirección, y funciones para proponer, votar y consultar resultados. Preparar también una dirección de contrato ya desplegada como plan B.]

---

## Slide 30 — Portada sección

**Blockchain**
Escalabilidad

[IMAGEN: Autopista congestionada transformándose en una autopista de múltiples niveles con tráfico fluido]

---

## Slide 31 — El problema de la escalabilidad

**Rendimiento actual vs demanda real:**

| Red | Transacciones por segundo (TPS) | Tiempo de bloque |
|-----|--------------------------------|-----------------|
| **Bitcoin** | ~7 TPS | ~10 minutos |
| **Ethereum** | ~15-30 TPS | ~12 segundos |
| **Solana** | ~400-700 TPS (teórico: 65.000) | ~0,4 segundos |
| **VISA** | ~65.000 TPS (pico) | Instantáneo |
| **Mastercard** | ~5.000 TPS (media) | Instantáneo |

**Conclusión:** las blockchains públicas más utilizadas están muy lejos del rendimiento de los sistemas de pago tradicionales.

---

## Slide 32 — Soluciones de escalabilidad: Layer 1

Mejoras **directas** en la blockchain principal:

| Solución | Descripción | Ejemplo |
|----------|-------------|---------|
| **Bloques más grandes** | Más transacciones por bloque, pero mayor coste de nodo | Bitcoin Cash |
| **Consenso más rápido** | Cambiar PoW por PoS u otros mecanismos más eficientes | Ethereum (The Merge) |
| **Sharding** | Dividir la red en fragmentos (shards) que procesan transacciones en paralelo | Ethereum (roadmap) |
| **Diseño nativo** | Blockchains diseñadas desde cero para alto rendimiento | Solana, Avalanche, Aptos |

**Limitación:** las mejoras en L1 siempre están sujetas al trilema de blockchain.

---

## Slide 33 — Soluciones de escalabilidad: Layer 2

Protocolos que operan **encima** de la blockchain principal, procesando transacciones fuera de la cadena y publicando solo el resultado final:

| Solución | Descripción | Ejemplo |
|----------|-------------|---------|
| **Optimistic Rollups** | Ejecutan transacciones off-chain y las publican en L1. Se asume que son válidas salvo que alguien demuestre fraude (periodo de disputa de ~7 días) | Optimism, Arbitrum, Base |
| **ZK-Rollups** | Ejecutan off-chain y publican una prueba criptográfica (zero-knowledge proof) que demuestra la validez | zkSync, StarkNet, Polygon zkEVM |
| **State Channels** | Dos partes abren un canal, hacen múltiples transacciones off-chain y solo publican el resultado final | Lightning Network (Bitcoin) |
| **Sidechains** | Blockchains independientes conectadas a la principal mediante un bridge | Polygon PoS |

---

## Slide 34 — Comparativa: L1 vs L2

| Aspecto | Layer 1 | Layer 2 |
|---------|---------|---------|
| **Seguridad** | Propia de la cadena | Hereda la seguridad de L1 |
| **Velocidad** | Limitada por el diseño | Mucho más rápida |
| **Coste** | Gas alto en redes congestionadas | Gas significativamente menor |
| **Descentralización** | Alta (en redes públicas) | Variable según el diseño |
| **Complejidad** | Menor para el usuario | Mayor (bridges, retiradas lentas) |
| **Ejemplo de coste** | Swap en Ethereum: ~5-50 USD | Swap en Arbitrum: ~0,10-0,50 USD |

---

## Slide 35 — Debate: ¿Por qué blockchain no se usa más?

Si blockchain es tan revolucionaria, ¿por qué no se usa masivamente?

**Puntos para debatir:**
1. **Experiencia de usuario:** ¿es razonable pedir a un usuario que gestione claves privadas y pague gas?
2. **Escalabilidad:** ¿puede una red de 15 TPS competir con VISA?
3. **Regulación:** ¿la incertidumbre regulatoria frena la adopción empresarial?
4. **Volatilidad:** ¿quién quiere cobrar su salario en ETH si mañana puede valer la mitad?
5. **Eficiencia:** ¿necesita realmente cada aplicación una blockchain, o basta con una base de datos?
6. **Percepción:** ¿cómo afectan los hackeos, estafas y la asociación con el crimen a la adopción?

[NOTA PROFESOR: Guiar el debate hacia la conclusión de que blockchain resuelve un problema específico (confianza entre partes que no se conocen) y no es la solución universal para todo. Muchas aplicaciones no necesitan descentralización. La clave es identificar los casos de uso donde blockchain aporta valor real frente a soluciones centralizadas.]

---

## Slide 36 — Portada sección

**Blockchain**
Otros casos de uso

[IMAGEN: Mosaico de iconos representando identidad digital, cadena de suministro, tokenización e IoT]

---

## Slide 37 — Identidad digital descentralizada

**Problema:** nuestra identidad digital está fragmentada entre decenas de plataformas que controlan nuestros datos.

**Solución blockchain:**
- **Identidad autogestionada (SSI):** el usuario controla sus datos de identidad en un wallet
- **Credenciales verificables:** títulos, certificados, permisos emitidos como tokens verificables on-chain
- **Sin intermediarios:** no necesitas que Google o Facebook confirmen quién eres
- **Estándares:** W3C DID (Decentralized Identifiers), ERC-735, ERC-3643

**Ejemplos reales:**
- **European Blockchain Services Infrastructure (EBSI):** identidad digital para ciudadanos de la UE
- **ION (Microsoft):** red de identidad descentralizada sobre Bitcoin
- **Worldcoin:** identidad biométrica mediante escaneo de iris (controvertido)

---

## Slide 38 — Cadena de suministro

**Problema:** falta de trazabilidad y transparencia en las cadenas de suministro globales.

**Solución blockchain:**
- Cada producto se registra en blockchain desde su origen hasta el consumidor final
- Cada participante (fabricante, transportista, distribuidor, minorista) añade su registro
- El consumidor puede verificar el origen y recorrido del producto

**Ejemplos reales:**
- **IBM Food Trust:** Walmart rastrea productos alimentarios (de 7 días a 2,2 segundos para trazar un mango)
- **TradeLens (Maersk + IBM):** seguimiento de contenedores de transporte marítimo (cerrado en 2022)
- **De Beers (Tracr):** trazabilidad de diamantes desde la mina hasta la joyería
- **VeChain:** autenticación de productos de lujo

[NOTA PROFESOR: El caso de TradeLens es interesante porque, a pesar de ser un proyecto con respaldo de dos gigantes (Maersk + IBM), cerró en 2022 por falta de adopción. Esto muestra que la tecnología sola no garantiza el éxito: se necesita que todos los actores de la cadena participen.]

---

## Slide 39 — Tokenización de activos

**Concepto:** representar activos del mundo real (Real World Assets / RWA) como tokens en blockchain.

| Activo | Ejemplo de tokenización | Beneficio |
|--------|------------------------|-----------|
| **Inmobiliario** | Fraccionar un edificio en 10.000 tokens | Inversión accesible desde cantidades pequeñas |
| **Arte** | Tokenizar un Picasso para vender participaciones | Liquidez para activos tradicionalmente ilíquidos |
| **Bonos** | Emitir deuda como tokens ERC-3643 | Settlement instantáneo, reducción de intermediarios |
| **Acciones** | Representar participaciones de empresa como tokens | Trading 24/7, sin horarios de bolsa |
| **Materias primas** | Tokens respaldados por oro (PAXG) | Propiedad verificable de oro físico custodiado |

[NOTA PROFESOR: Conectar con el ERC-3643 que los alumnos investigaron como tarea. Es el estándar para tokenizar activos regulados en EVM con controles de identidad y permisos.]

---

## Slide 40 — IoT y blockchain

**Problema:** miles de millones de dispositivos IoT generan datos que necesitan ser confiables, verificables e inalterables.

**Solución blockchain:**
- Los dispositivos registran datos directamente en blockchain
- Se garantiza la **integridad** y la **inmutabilidad** de los datos
- Los dispositivos pueden realizar **micropagos** entre ellos (machine-to-machine economy)

**Ejemplos:**
- **IOTA:** blockchain sin fees diseñada para micropagos IoT (usa un DAG en lugar de blockchain tradicional)
- **Helium:** red descentralizada de puntos de acceso WiFi/5G donde los operadores cobran en tokens
- **Energy Web:** mercado descentralizado de energía donde productores y consumidores negocian directamente

---

## Treasure Hunt — Los bonos de Santander en Ethereum 🏴‍☠️

En septiembre de 2019, **Banco Santander** emitió un bono de **20 millones de dólares** directamente en la blockchain pública de Ethereum. Fue la primera emisión de bonos de principio a fin en una blockchain pública por parte de un gran banco.

**Misión:**
1. Buscar en https://etherscan.io/ la dirección del contrato del bono de Santander. Pista: buscar "Santander bond" o investigar noticias de septiembre de 2019
2. ¿Qué tipo de token es? ¿ERC-20, ERC-721 u otro?
3. ¿Cuántas transacciones ha tenido el contrato?
4. ¿Quién desplegó el contrato? ¿Se puede identificar?
5. ¿Cómo se pagaron los cupones del bono?
6. **Bonus:** Santander luego redimió (recompró) ese bono. ¿Podéis encontrar la transacción de redención?

[NOTA PROFESOR: El bono fue emitido en la blockchain pública de Ethereum, con la estructura completa gestionada on-chain: emisión, pago de cupones trimestrales y redención. La dirección del contrato se puede encontrar a través de noticias de prensa. Fue un hito para la adopción institucional de blockchain pública. El bono se redimió completamente en diciembre de 2019.]

---

## Slide 41 — Portada sección

**Blockchain**
Práctica grupal: Crea tu propio Smart Contract

---

## Slide 42 — Práctica grupal: 3 equipos, 3 ideas

**Instrucciones:**
- Dividir la clase en **3 grupos**
- Cada grupo debe idear y diseñar un smart contract original
- No es necesario programarlo completo, pero sí definir:
  1. **¿Qué problema resuelve?** (descripción en una frase)
  2. **¿Quiénes son los actores?** (usuarios, roles)
  3. **¿Qué datos almacena?** (variables de estado)
  4. **¿Qué funciones tiene?** (qué puede hacer cada actor)
  5. **¿Qué eventos emite?** (qué notificaciones genera)
  6. **¿Necesita oráculos?** ¿Para qué?
  7. **¿Tiene token de gobernanza?** ¿Cómo se gobierna?

**Ideas sugeridas** (o inventar las propias):
- Sistema de votación para la comunidad de vecinos
- Plataforma de crowdfunding con devolución automática si no se alcanza el objetivo
- Certificados de asistencia a un curso (tipo NFT)
- Mercado de predicciones deportivas
- Sistema de fidelización con puntos tokenizados
- Seguro paramétrico que paga automáticamente si llueve X días

---

## Slide 43 — Práctica grupal: Presentación

Cada grupo presenta su idea al resto de la clase (5-10 minutos por grupo).

**Criterios de evaluación:**
- **Originalidad:** ¿es una idea interesante?
- **Viabilidad técnica:** ¿se puede implementar con smart contracts?
- **Utilidad real:** ¿resuelve un problema que justifique usar blockchain?
- **Identificación de riesgos:** ¿qué podría salir mal?

**Feedback cruzado:** cada grupo evalúa las presentaciones de los otros dos.

[NOTA PROFESOR: Dar flexibilidad creativa a los grupos. Si algún grupo es más técnico y quiere escribir pseudocódigo o incluso Solidity real, animarles a hacerlo. Si algún grupo es más conceptual, está bien con un diagrama y una descripción. Lo importante es que piensen en los requisitos, actores y riesgos de un sistema descentralizado.]

---

## Slide 44 — Portada sección

**Blockchain**
Repaso y preguntas

---

## Slide 45 — Repaso del Día 7

**Preguntas:**
1. Una dApp es cualquier aplicación móvil que utilice internet para funcionar. ¿Verdadero o falso? Razona la respuesta.
2. ¿Cuál es la diferencia fundamental entre un CEX y un DEX en cuanto a la custodia de fondos?
3. Si Uniswap (la empresa) desaparece mañana, ¿deja de funcionar el protocolo? ¿Por qué?
4. En un préstamo DeFi, ¿por qué se exige sobrecolateralización?
5. ¿Por qué los smart contracts no pueden acceder directamente a datos del mundo real?
6. ¿Qué es el slashing en el contexto de Chainlink?
7. Explica qué es un flash loan y por qué es peligroso para las DAOs.
8. ¿En qué consiste un ataque de reentrancy como el que sufrió The DAO?
9. ¿Qué diferencia hay entre un Optimistic Rollup y un ZK-Rollup?
10. Ethereum procesa unas 15-30 transacciones por segundo. VISA procesa unas 65.000. ¿Cómo pueden las soluciones Layer 2 cerrar esa brecha?
11. ¿Qué es la tokenización de activos y por qué el ERC-3643 es relevante?
12. ¿Es blockchain la solución para todo? ¿Cuándo tiene sentido usar una base de datos centralizada?
13. ¿Qué problema concreto resolvió IBM Food Trust en la cadena de suministro de Walmart?
14. ¿Por qué el modelo "1 token = 1 voto" puede ser problemático en una DAO?
15. ¿Qué conclusiones sacas de que Santander emitiese un bono en la blockchain pública de Ethereum?

[NOTA PROFESOR: Respuestas clave:
1. Falso: una dApp ejecuta su backend en smart contracts sobre blockchain, no en servidores centralizados.
3. El protocolo sigue funcionando porque los smart contracts están desplegados en Ethereum y son imparables. La web (frontend) podría caer, pero cualquiera puede interactuar directamente con el contrato.
4. Porque no hay verificación de identidad ni historial crediticio. El colateral es la única garantía de que el prestatario devolverá el préstamo.
5. Por diseño: los smart contracts deben ser deterministas (todos los nodos deben llegar al mismo resultado). Acceder a internet introduciría resultados diferentes en cada nodo.
7. Un flash loan permite pedir prestada una cantidad enorme sin colateral, usarla para acumular votos y aprobar propuestas maliciosas, todo en una sola transacción.
8. El contrato llamaba a una función externa antes de actualizar el saldo interno, permitiendo al atacante llamar recursivamente a la función de retirada.
12. Blockchain tiene sentido cuando hay desconfianza entre las partes, necesidad de transparencia y auditoría, o cuando se quiere eliminar intermediarios. Si hay una autoridad central de confianza, una base de datos es más eficiente.]

---

## Slide 46 — Tarea para casa

**Investigar un caso real de uso de blockchain en una empresa española o europea:**
- ¿Qué empresa es y en qué sector opera?
- ¿Qué problema resuelve con blockchain?
- ¿Qué tipo de blockchain usa (pública, privada, consorcio)?
- ¿Ha tenido éxito o ha fracasado? ¿Por qué?

Preparar una presentación breve (3-5 minutos) con las conclusiones.

*Presentar el próximo día al inicio de clase.*

[NOTA PROFESOR: Ejemplos que los alumnos podrían encontrar: Santander (bonos en Ethereum), BBVA (préstamos tokenizados), Iberdrola (certificados de energía renovable), Correos (sellos NFT), Telefónica (identidad digital), Repsol (trazabilidad), We.trade (financiación comercial europea, cerrada en 2022). Fomentar que busquen tanto éxitos como fracasos para tener una visión equilibrada.]

---

## Actividad de relleno (si sobra tiempo)

### Hackathon relámpago: mejora tu Smart Contract (45-60 min)

- Los grupos que crearon su Smart Contract en la práctica del día extienden su proyecto:
- Retos opcionales (elegir al menos 2):
  1. **Añadir un evento (event):** que el contrato emita un evento cada vez que se ejecute una acción importante. Verificar en Etherscan que el evento aparece en los logs.
  2. **Añadir control de acceso:** que solo el creador del contrato pueda ejecutar ciertas funciones (modifier `onlyOwner`).
  3. **Añadir una función de emergencia:** un "botón de pánico" que permita al owner pausar el contrato.
  4. **Conectar dos contratos:** que tu contrato llame a una función del contrato de otro grupo (composabilidad real).
  5. **Frontend básico:** usando Remix + MetaMask, crear una página HTML mínima que interactúe con el contrato (el profesor proporciona una plantilla con ethers.js).
- Al final, cada grupo demo su mejora al resto.

[NOTA PROFESOR: Tener preparadas plantillas de código para cada reto (modifier onlyOwner, patrón Pausable, plantilla HTML con ethers.js). Los alumnos que van más rápido pueden intentar varios retos. Los que van más lentos, con hacer uno ya es suficiente.]
