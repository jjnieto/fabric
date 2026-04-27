# Día 5 — Tokens, fungibilidad, tokenización y stablecoins

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos divertidos del mundo cripto - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes sobre tokens, NFTs o stablecoins para compartir como icebreaker. Ejemplos: la última colección de NFTs absurda, movimientos grandes de USDT/USDC entre wallets, nuevos proyectos de tokenización de activos reales, o noticias sobre regulación de stablecoins. Actualizar antes de cada edición del curso.]

---

## Slide 2 — Portada sección

**Blockchain**
Fungibilidad

[IMAGEN: Dos monedas de euro idénticas frente a la Mona Lisa (fungible vs no fungible)]

---

## Slide 3 — El concepto de fungibilidad

[IMAGEN: Diagrama visual mostrando elementos fungibles (billetes, lingotes de oro) vs no fungibles (cuadro de arte, pasaporte)]

Un bien es **fungible** cuando puede ser sustituido por otro idéntico sin que cambie su valor ni sus propiedades.

Un bien es **no fungible** cuando es único e irremplazable.

---

## Slide 4 — Fungibilidad: curiosidades históricas

- El **Chicago Board of Trade (CBOT)** se fundó en 1848; es el mercado de futuros y opciones más antiguo del mundo (Chicago)
- La **Bolsa de Arroz de Dojima**, fundada en Osaka (Japón) en 1697, es considerada la primera bolsa de futuros del mundo, especializada en arroz
- Sin embargo, ya en el **2000 a.C.** los agricultores del Nilo vendían toda su cosecha antes de recogerla, sin saber la cantidad o calidad de sus cultivos

[IMAGEN: Ilustración histórica de la Bolsa de Arroz de Dojima]

---

## Slide 5 — Actividad: ¿Fungible o no?

Identificar qué elementos de la lista son fungibles, cuáles no y cuáles son discutibles:

| Elemento | Tu respuesta |
|----------|-------------|
| Cartas coleccionables | |
| Billetes de 10 € | |
| Un cuadro original de Picasso | |
| Habitaciones de hotel | |
| Bitcoins | |
| Monedas antiguas de colección | |
| Licencias de software | |
| Una casa específica | |
| Tokens de un casino | |
| Entradas de cine | |
| Tu pasaporte | |
| Discos de vinilo | |
| Camisetas oficiales de un equipo | |
| Un contrato firmado con tu nombre | |
| Litros de gasolina | |
| Un NFT de arte digital único | |
| Tickets de transporte público | |
| Acciones de una misma empresa | |
| Botellas de vino | |
| Objetos de videojuegos | |

---

## Slide 6 — Solución: Claramente fungibles

Se pueden intercambiar 1:1 sin diferencia:
- Billetes de 10 €
- Litros de gasolina
- Tokens de un casino
- Bitcoins
- Acciones de una misma empresa

---

## Slide 7 — Solución: Claramente no fungibles

Únicos, con identidad propia:
- Un cuadro original de Picasso
- Tu pasaporte
- Un NFT de arte digital único
- Una casa específica
- Un contrato firmado con tu nombre

---

## Slide 8 — Solución: Casos ambiguos (dependen del contexto)

- **Botellas de vino:** misma añada y bodega → fungibles; botella con cata especial → no fungible
- **Entradas de cine:** mismo día/sala/sin asiento → fungible; numeradas → no fungible
- **Camisetas de un equipo:** misma talla y edición → fungibles; firmadas por jugadores → no fungibles
- **Cartas coleccionables:** carta común repetida → fungible; carta rara única → no fungible
- **Monedas antiguas:** misma emisión y estado → fungibles; con rarezas → no fungibles
- **Objetos de videojuegos:** poción de salud → fungible; espada única → no fungible
- **Habitaciones de hotel:** misma categoría → fungibles; suites únicas → no fungible
- **Discos de vinilo:** reproducciones masivas → fungibles; ediciones limitadas → no fungible
- **Licencias de software:** clave genérica de serie → fungible; clave personalizada → no fungible
- **Tickets de transporte:** viaje sencillo sin asiento → fungibles; con número de asiento → no fungible

---

## Slide 9 — Portada sección

**Blockchain**
ERC-20, ERC-721, ERC-1155

---

## Slide 10 — Smart Contracts: ERCs conocidos

[IMAGEN: Diagrama visual mostrando los tres tipos de tokens:
- ERC-20: montón de monedas iguales con cantidades (50, 12, 387, 897, 28)
- ERC-721: colección de objetos únicos con Id: 0, 1, 2, 3, 4
- ERC-1155: combinación de ambos - colecciones de items donde cada colección puede tener múltiples unidades]

| Estándar | Tipo | Ejemplo |
|----------|------|---------|
| ERC-20 | Token fungible | USDC, DAI, UNI |
| ERC-721 | Token no fungible (NFT) | CryptoKitties, Bored Apes |
| ERC-1155 | Híbrido (multi-token) | Items de videojuegos |

---

## Slide 11 — Smart Contracts: Estandarización

Un estándar ERC define una **interfaz** (conjunto de funciones) que todos los contratos de ese tipo deben implementar.

**Interfaz ERC-20 (funciones obligatorias):**
```
function name() public view returns (string)
function symbol() public view returns (string)
function decimals() public view returns (uint8)
function totalSupply() public view returns (uint256)
function balanceOf(address _owner) public view returns (uint256)
function transfer(address _to, uint256 _value) public returns (bool)
function transferFrom(address _from, address _to, uint256 _value) public returns (bool)
function approve(address _spender, uint256 _value) public returns (bool)
function allowance(address _owner, address _spender) public view returns (uint256)
```

Esto permite que cualquier wallet, exchange o dApp pueda interactuar con **cualquier** token ERC-20 sin conocer su implementación interna.

---

## Slide 12 — Smart Contracts: Composabilidad

**Blockchain como World Computer**

[IMAGEN: Diagrama mostrando un Smart Contract propio (My SC) que llama a USDC, DAI y MATIC — todos son ERC-20 con las mismas funciones (balanceOf, transfer, approve, allowance). My SC orquesta llamadas entre ellos en una sola transacción.]

La composabilidad permite que un contrato llame a otros contratos. Como todos siguen estándares conocidos, se pueden **combinar como piezas de Lego** ("Money Legos").

---

## Slide 13 — Cybercultura: Fit Vitalik

La campaña llamada FitVitalik fue una **parodia de ICO** lanzada en noviembre de 2017 con el fin de recaudar fondos para que Vitalik Buterin "se ponga en forma".

Llegó a cotizar en exchanges. El Smart Contract estaba en esta dirección:
`0xe250d7fd146e009dcc2ff367cad01b2ac3c70266`

[IMAGEN: Meme de Fit Vitalik con foto de antes y después]

[NOTA PROFESOR: Este es un ejemplo perfecto de cómo la estandarización (ERC-20) y la composabilidad permiten que cualquier token, incluso uno absurdo como FitVitalik, pueda listarse en exchanges y ser intercambiado. Es un caso real de lo fácil que es crear y distribuir tokens. Aprovechar para debatir si eso es positivo (democratización) o negativo (scams, memecoins sin valor).]

---

## Slide 14 — Práctica: Contratos existentes (USDC)

1. Ir al faucet de Circle: https://faucet.circle.com/
2. Solicitar 10 USDC a nuestro wallet
3. Localizar la dirección de USDC en Etherscan:
   https://sepolia.etherscan.io/address/0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238
4. Mostrarlo en MetaMask (importar token personalizado)
5. Importarlo en Remix — el profesor explicará cómo hacerlo

---

## Slide 15 — Práctica: Crear nuestro propio Token ERC-20

1. Revisar el Smart Contract entre todos (versión mínima de un ERC-20)
2. Decidir un nombre entre todos
3. El profesor desplegará el Smart Contract base
4. Importar el token en MetaMask
5. El profesor hará un reparto inicial de tokens a los alumnos
6. Transferir tokens entre alumnos
7. Inspeccionar en Sepolia Etherscan las transacciones producidas en la dirección del Smart Contract

**¡Somos ricos!** 💰

[NOTA PROFESOR: Tener preparado el código de un ERC-20 mínimo con comentarios. El nombre del token lo deciden los alumnos (genera engagement). Preparar el despliegue con antelación para no perder tiempo en clase.]

---

## Treasure Hunt — La tokenización del mundo real 🏴‍☠️

En 2021, un grupo de personas formó una DAO (organización autónoma descentralizada) con el objetivo de recaudar fondos en criptomonedas para comprar una copia original de la Constitución de los Estados Unidos que salía a subasta en Sotheby's. Recaudaron más de 40 millones de dólares en ETH en cuestión de días.

**Misión:**
1. Buscar en internet: ¿cómo se llamaba esta DAO?
2. Encontrar la dirección del contrato del token de gobernanza de esa DAO en Etherscan (mainnet). ¿Qué tipo de token es (ERC-20, ERC-721 o ERC-1155)?
3. ¿Cuánto dinero recaudaron exactamente en ETH? Convertirlo al precio de ETH en ese momento.
4. ¿Ganaron la subasta? ¿Qué pasó después con los fondos?
5. **Bonus:** Existe otra DAO similar que intentó comprar un equipo de la NBA y otra que intentó comprar una copia del álbum "Once Upon a Time in Shaolin" de Wu-Tang Clan. ¿Cómo se llamaban?

[NOTA PROFESOR: La DAO es ConstitutionDAO. El token PEOPLE (ERC-20) está en la dirección 0x7A58c0Be72BE218B41C608b7Fe7C5bB630736C71. Recaudaron aproximadamente 11.613 ETH (unos 47 millones de dólares al precio de ese momento). Perdieron la subasta frente a Kenneth Griffin (CEO de Citadel). Los fondos se devolvieron a los contribuyentes (menos el gas). Las DAOs bonus son KrauseHouse (NBA) y PleasrDAO (Wu-Tang). Es un caso perfecto para ilustrar tokenización, gobernanza descentralizada y los límites de las DAOs al interactuar con el mundo real.]

---

## Slide 16 — Portada sección

**Blockchain**
Tokenización

---

## Slide 17 — ¿Qué es la tokenización?

La **tokenización** de activos implica la representación digital de activos reales en registros distribuidos o la emisión de activos tradicionales en formato tokenizado.

El potencial de la tokenización es teóricamente ilimitado, ya que cualquier activo real puede incorporarse a la cadena de bloques.

| Tokens que representan un activo real | Tokens nativos (no representan un activo real) |
|---|---|
| Existen y se negocian tanto dentro como fuera de la cadena | Existen y se negocian solo on-chain |
| Activos financieros (valores), STOs | Tokens de utilidad e ICOs |
| Activos no financieros (bienes raíces, arte) | Tokens de gobernanza |
| Materias primas (oro) | Tokens sociales |
| Respaldados por activos reales fuera del ledger | Se definen por su existencia en el ledger |

---

## Slide 18 — ¿Qué se puede tokenizar?

[IMAGEN: Mapa mental con 4 categorías principales:
- Dinero: stablecoins, CBDCs, RBDCs
- Activos intangibles: licencias, derechos, trademarks, copyright, royalties, propiedad intelectual, patentes
- Instrumentos financieros: fixed income, equities, futuros, opciones, stocks
- Objetos físicos: commodities, consumibles, coleccionables, dispositivos, real estate]

---

## Slide 19 — Beneficios de tokenizar en DLT

| Beneficio | Descripción |
|-----------|-------------|
| **Propiedad fraccionada** | Reduce barreras de inversión, permite acceso a activos antes inasequibles |
| **Mayor liquidez** | Base más amplia de inversores, negociación 24/7 |
| **Programabilidad** | Smart contracts automatizan transacciones complejas y cumplimiento (KYC/AML) |
| **Accesibilidad** | Abrir una wallet es casi instantáneo, sin necesidad de banco ni broker |
| **Mayor confianza** | Transparencia e inmutabilidad de las DLT reducen la dependencia de autoridades centrales |

---

## Slide 20 — Activos financieros tokenizados: el ciclo de vida

[IMAGEN: Diagrama del ciclo de vida: Creación → Distribución/Venta → Trading → Clearing → Settlement → Custodia → Otros servicios]

Cambios clave respecto al proceso tradicional:
- **Creación:** se democratiza, reduciendo barreras de entrada
- **Distribución:** se eliminan intermediarios, canales directos
- **Trading:** opera 24/7, sin mercado extrabursátil
- **Clearing/Settlement:** se simplifica con "Entrega vs Pago" (DvP), elimina cámaras de compensación
- **Custodia:** se fortalecen mecanismos para proteger claves
- **Nuevos servicios:** puentes entre activos tokenizados y no tokenizados (swaps, financiación)

---

## Slide 21 — Caso real: Bono Santander 2019

Se utilizó la plataforma de **Nivaura**, que automatiza la producción de documentos legales, el proceso de book building y ofrece compensación y liquidación instantánea (en lugar de D+3).

El bono se emitió en la **red pública de Ethereum** (bono, efectivo y cupones se tokenizaron), consiguiendo realizar la **entrega vs. pago en una operación atómica** dentro de un Smart Contract.

| Detalle | Valor |
|---------|-------|
| Importe | USD $20M |
| Plazo | 1 año |
| Cupones | 4 |
| Interés | 1,98% fijo |

---

## Slide 22 — Caso real: Bono EIB 2021

Se empleó la plataforma **Forge** (Société Générale), que automatizó la creación del libro del bono y ofrecía clearing y settlement instantáneo mediante blockchain.

El bono se emitió bajo la legislación francesa, en la **red pública de Ethereum** (se tokeniza tanto el bono como el cash), logrando un DvP sintético a través de la figura del Settlement Agent.

| Detalle | Valor |
|---------|-------|
| Importe | EUR €100M |
| Plazo | 2 años |
| Cash | CBDC |
| Interés | 0% (Zero Coupon) |

---

## Slide 23 — Bono digital: proceso tradicional vs blockchain

**Proceso tradicional:**
- Los cupones se pagan a través de un agente de pagos
- Los inversores invierten fondos y reciben los bonos a cambio (implica riesgo de liquidación)
- Comisiones para listar el bono y márgenes en cada operación
- El asesor legal prepara toda la documentación (costoso y repetitivo)

**Proceso blockchain:**
- Los emisores estructuran el bono seleccionando **plantillas estándar**
- El bono se registra en blockchain, **reduciendo comisiones**
- Los cupones se pagan con efectivo tokenizado, **sin retrasos ni cámaras de compensación**
- Plantillas legales rellenadas automáticamente; el asesor legal solo revisa
- **Entrega vs Pago (DvP)** realizada por un Smart Contract de manera **atómica**, reduciendo el riesgo de liquidación

---

## Slide 24 — Ventajas competitivas de la tokenización

| Ventaja | Impacto |
|---------|---------|
| **Emisión rápida** | De meses a días gracias a plantillas |
| **Plantillas legales** | Reducción del coste legal |
| **Sin tasas de mercado** | Control total sobre costes de emisión |
| **Sin riesgo de settlement** | DvP en blockchain libera capital |
| **Mercado secundario** | Emisiones atractivas para PYMEs, inversión accesible a usuarios finales |

---

## Slide 25 — Portada sección

**Blockchain**
Stablecoins

---

## Slide 26 — Stablecoins: Tokens referenciados a fiat

**Qué son:** tokens ERC-20 diseñados para mantener paridad con una moneda fiat (normalmente USD).

**Principales ejemplos:**
| Stablecoin | Tipo | Respaldo |
|-----------|------|----------|
| **USDT** (Tether) | Centralizado | Reservas de la empresa |
| **USDC** (Circle/Coinbase) | Centralizado | Auditado, reservas en bancos |
| **DAI** (MakerDAO) | Descentralizado | Cripto-colateral (ETH, USDC) |

**Utilidad:**
- Refugio contra la volatilidad de BTC/ETH
- Medio de pago en DeFi
- Liquidez global sin pasar por bancos

---

## Slide 27 — Tipos de colateral en stablecoins

| Tipo | Respaldo | Riesgo principal |
|------|----------|-----------------|
| **Colateral fiat** (USDT, USDC) | Depósitos en dólares u otros activos tradicionales | Centralización, opacidad de reservas, reguladores pueden congelar fondos |
| **Colateral cripto** (DAI) | Sobrecolateralización en ETH, USDC u otros | Caída fuerte del colateral → liquidaciones masivas |
| **Algorítmicas** (Terra/Luna) | Sin reservas directas, usan algoritmos y tokens gemelos | Colapso si se rompe la confianza |

Las algorítmicas son vulnerables a condiciones extremas de mercado. Ejemplos de fracasos: Empty Set Dollar, Ampleforth, Basic.Cash, Iron Finance…

---

## Slide 28 — El colapso de Terra/Luna

- **Terra (UST)** era una stablecoin algorítmica que mantenía la paridad con el dólar mediante un sistema de arbitraje con la moneda Luna
- En mayo de 2022 se produjo una acción coordinada: retiraron masivamente **1.000 millones de UST**, provocando la pérdida momentánea de la paridad
- Eso provocó desconfianza; los inversores comenzaron a vender masivamente, ahondando en la crisis
- El sistema algorítmico no aguantó la presión: UST cayó hasta valer **$0,00006**
- En pocos días desaparecieron **60.000 millones de dólares**
- Uno de los mayores colapsos de la historia de las criptomonedas

*Lo veremos en detalle en el módulo regulatorio.*

---

## Slide 29 — Caso de estudio: Stablecoins algorítmicas

**¿Crees que las stablecoins algorítmicas pueden llegar a funcionar sin riesgos?**

Trabajar en grupo (3 grupos de 5 personas) durante 30 minutos y presentar las conclusiones.

[NOTA PROFESOR:
- Funcionan mientras hay confianza y el mercado es pequeño/estable
- En momentos de estrés (retiros masivos, ataques coordinados), casi todas han sufrido depeg
- Cuando pierde paridad → acuña token de respaldo → este se devalúa → más pánico → death spiral
- Ejemplos: Ampleforth (rebasing token), Empty Set Dollar, Basis Cash, Iron Finance (Mark Cuban perdió dinero), Terra/Luna
- Conclusión: ninguna algorítmica ha demostrado resiliencia a largo plazo. Las que dominan son fiat-backed (USDC, USDT) y overcollateralized (DAI)]

---

## Slide 30 — Repaso del Día 5

**Preguntas:**
1. Un elemento fungible es aquel que se puede intercambiar por dinero en cualquier mercado. ¿Verdadero o falso?
2. Un NFT es un "Nearly Funded Token" y representa un contrato ERC-20. ¿Verdadero o falso?
3. Hay elementos que pueden ser fungibles o no según características concretas. ¿Verdadero o falso?
4. Un ERC-20 es un tipo de smart contract que representa elementos fungibles. ¿Verdadero o falso?
5. Un ERC-1155 se puede ver como una colección de ERC-20. ¿Verdadero o falso?
6. La composabilidad es la capacidad de orquestar llamadas entre varios smart contracts en una sola transacción. ¿Verdadero o falso?
7. Un ERC-721 representa una lista de elementos fungibles. ¿Verdadero o falso?
8. La estructura de datos para representar ERC-20, ERC-721 y ERC-1155 es la misma: el mapping. ¿Verdadero o falso?
9. Un mapping es una lista en la que se asocia un valor a un índice único e irrepetible. ¿Verdadero o falso?
10. Los estándares más usados en Ethereum son ERC-20 (fungible), ERC-721 (no fungible) y ERC-1155 (parcialmente fungible). ¿Verdadero o falso?
11. Que un contrato siga un estándar significa que debe exponer funciones conocidas a las que cualquiera pueda llamar. ¿Verdadero o falso?
12. Un contrato proxy permite a cualquiera modificar smart contracts ya desplegados. ¿Verdadero o falso?
13. Explica los pros y contras de los contratos proxy.
14. Se pueden enviar tokens ERC-20 a un smart contract igual que se envían ethers. ¿Verdadero o falso?

---

## Slide 31 — Tarea para casa

**Investigar el proyecto de tokenización de BlackRock (BUIDL Fund):**
1. ¿Qué activo tokeniza el fondo BUIDL de BlackRock?
2. ¿En qué blockchain está desplegado?
3. ¿Cuál es el importe mínimo de inversión?
4. ¿Qué ventajas ofrece frente a un fondo tradicional de mercado monetario?
5. Preparar una slide con las conclusiones para presentar el lunes al inicio de clase.

*Presentar el lunes al inicio de clase.*

[NOTA PROFESOR: BlackRock lanzó el BUIDL Fund (BlackRock USD Institutional Digital Liquidity Fund) en marzo de 2024 sobre Ethereum. Tokeniza participaciones en un fondo de mercado monetario respaldado por bonos del Tesoro de EE.UU. La inversión mínima es de 5 millones de dólares. Es un caso real y reciente de tokenización institucional que conecta directamente con los conceptos vistos en clase (bonos tokenizados, ERC-20, beneficios de tokenizar). También se ha expandido a otras cadenas como Polygon, Avalanche, Arbitrum y Optimism.]

---

## Actividad de relleno (si sobra tiempo)

### Diseña tu negocio tokenizado (30-45 min)

- Por grupos de 3-4 personas, inventar un negocio que use tokenización.
- Cada grupo debe definir:
  1. ¿Qué activo tokenizáis? (inmueble, obra de arte, cosecha, energía, tiempo de consultoría…)
  2. ¿ERC-20, ERC-721 o ERC-1155? Justificar la elección.
  3. ¿Quién puede comprar tokens? ¿Hay restricciones (KYC, acreditación)?
  4. ¿Cómo funciona el mercado secundario?
  5. ¿Qué pasa si el activo real se destruye o desaparece?
  6. Dibujar un esquema simple del flujo: emisor → token → inversor → mercado secundario.
- Cada grupo presenta su idea en 3 minutos al resto de la clase.
- La clase vota el proyecto más viable y el más creativo.

[NOTA PROFESOR: Lo importante no es la perfección técnica sino que piensen en los problemas reales de la tokenización: custodia del activo real, marco legal, liquidez, gobernanza. Las preguntas 5 (destrucción del activo) y 3 (restricciones) suelen generar debates muy buenos.]
