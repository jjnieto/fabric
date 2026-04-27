# Día 4 — Smart Contracts, wallets y Solidity básico

---

## Slide 1 — Cotilleos 🗞️

[IMAGEN: Sección de cotilleos divertidos del mundo cripto - formato de periódico sensacionalista]

[NOTA PROFESOR: Buscar 2-3 noticias recientes y curiosas del mundo cripto para compartir con los alumnos como icebreaker. Ejemplos: NFTs absurdos vendidos por millones, tuits de Elon Musk moviendo mercados, hackeos llamativos, etc. Actualizar antes de cada edición del curso.]

---

## Slide 2 — Portada sección

**Blockchain**
Custodial Wallets

---

## Slide 3 — Custodial Wallets

Son wallets de blockchain donde el usuario **no controla las claves privadas**. La custodia la lleva un tercero (normalmente un exchange o proveedor).

**Ventajas:**
- Recuperación de acceso si se pierde la contraseña
- Experiencia de usuario más sencilla
- Integración con compra/venta de cripto con dinero fiat

**Desventajas:**
- El usuario no tiene soberanía total sobre sus fondos
- Riesgo de hackeo del custodio o bloqueo de cuentas
- Posible censura de transacciones
- Dependencia de la honestidad de un tercero

---

## Slide 4 — Debate: Custodial vs Non-Custodial Wallet

Comparar este tipo de wallets con MetaMask.

Recordad los términos:
- **Seguridad**
- **Sencillez**
- **Accesibilidad**
- **Utilidad**
- **Protección ante errores o pérdida de la clave**

---

## Slide 5 — Portada sección

**Blockchain**
Smart Contracts

[IMAGEN: Engranajes digitales dentro de una cadena de bloques]

---

## Slide 6 — El origen de los Smart Contracts

- En 2013, **Vitalik Buterin** publicó un whitepaper proponiendo evolucionar Bitcoin a algo más flexible, capaz de ejecutar pequeños programas a los que llamó "contratos inteligentes"
- La comunidad Bitcoin lo ignoró y él decidió recaudar fondos para crear la red Ethereum junto con Joseph Lubin, Gavin Wood y otros referentes del blockchain
- En 2015 lanzó **Ethereum** y desde entonces ha sido el referente de Smart Contracts y blockchain programable

---

## Slide 7 — Smart Contracts: La idea (I)

- Habíamos visto que los nodos de la red blockchain guardan un ledger en bloques encadenados
- Cada bloque representa un estado del ledger y el último bloque el estado actual
- En cierto modo podemos ver blockchain como una **máquina de estados** en la que todos los nodos acuerdan cuál va a ser el siguiente estado en base a los mecanismos de consenso

[IMAGEN: Diagrama de máquina de estados: Estado N → Transacciones → Estado N+1]

---

## Slide 8 — Smart Contracts: La idea (II)

- La idea de Vitalik fue dotar a cada nodo de la red de una pequeña **máquina virtual** capaz de ejecutar código, además de los algoritmos para validar, minar y gestionar transacciones
- Los datos se almacenan en los bloques igual que los datos del ledger
- Cuando se invoca dicho código, **todos los nodos ejecutan el código** con los datos existentes y actualizan los datos de salida
- Todos los nodos deben tener consenso respecto al nuevo estado de los datos. Es decir, deben dar la misma salida (**por eso no se admiten números aleatorios** en la programación de Ethereum)
- Eso convierte a Ethereum en una especie de **computador mundial** o, mejor dicho, en una máquina de estados descentralizada, pública y confiable

[IMAGEN: Diagrama mostrando un bloque con secciones DATA y CODE, y los nodos ejecutando el mismo código con los mismos datos]

---

## Slide 9 — Smart Contracts: Killer applications

Uno de los primeros usos reales de los Smart Contracts fue permitir crear **tokens fungibles** dentro de Ethereum: los **ERC-20**.

Más adelante se crearon:
- **NFTs** o tokens no fungibles: **ERC-721**
- **Híbridos** mitad fungible mitad no fungible: **ERC-1155**

Por el camino se han creado innumerable cantidad de Smart Contracts que han posibilitado funcionalidades como:
- **DeFi** (finanzas descentralizadas)
- **DAOs** (organizaciones autónomas descentralizadas)
- **Bridges** (puentes entre blockchains)
- **DEX** (exchanges descentralizados)
- La fiebre de las **ICOs** (Initial Coin Offerings)

---

## Slide 10 — Cybercultura: Fit Vitalik

La campaña llamada FitVitalik fue una **parodia de ICO** lanzada en noviembre de 2017 con el fin de recaudar fondos para que Vitalik Buterin "se ponga en forma".

Llegó a cotizar en exchanges. El Smart Contract estaba en esta dirección:
`0xe250d7fd146e009dcc2ff367cad01b2ac3c70266`

[IMAGEN: Meme de Fit Vitalik con foto de antes y después]

---

## Slide 11 — Smart Contracts: ¿Qué son?

- Son pequeños programas que se despliegan en la red blockchain y guardan ahí sus datos
- Al estar desplegados en blockchain, **nadie puede alterar su código**
- Al ser ejecutados por todos los nodos, los datos de salida se graban permanentemente en la red
- Esto permite ejecutar un código conocido por todos de forma **segura y descentralizada**

---

## Slide 12 — No me he olvidado…

**¿Por qué no hay números aleatorios en el lenguaje de programación de los Smart Contracts?**

[NOTA PROFESOR: Porque si cada nodo generara un número aleatorio diferente, producirían resultados distintos al ejecutar el mismo contrato. No habría consenso sobre el nuevo estado. La aleatoriedad rompe el determinismo necesario para que todos los nodos lleguen al mismo resultado.]

---

## Treasure Hunt — El contrato misterioso 🏴‍☠️

En Ethereum hay un contrato desplegado en la dirección:
`0x06012c8cf97BEaD5deAe237070F9587f8E7A266d`

**Misión:**
1. Buscar esa dirección en https://etherscan.io/
2. Averiguar qué proyecto famoso es (pista: tiene que ver con gatos)
3. ¿Cuántas transacciones ha procesado ese contrato?
4. ¿Cuándo se desplegó?
5. Encontrar la transacción más cara jamás realizada en ese contrato
6. **Bonus:** Ese proyecto causó la primera congestión grave de Ethereum. ¿En qué fecha y cuánto subieron las fees?

[NOTA PROFESOR: Es CryptoKitties, uno de los primeros NFTs (ERC-721). Se desplegó el 23 de noviembre de 2017. Causó tal congestión en la red Ethereum en diciembre de 2017 que las fees se dispararon y muchas transacciones quedaron pendientes durante horas. La transacción más cara fue la venta del gatito "Dragon" por 600 ETH (~170.000$ en ese momento). Es un caso perfecto para ilustrar el trilema de blockchain y la importancia de la escalabilidad.]

---

## Slide 13 — Cultura General

**Alan Turing (1912 – 1954)**

[IMAGEN: Foto de Alan Turing]

- Matemático, lógico y criptógrafo británico
- Propuso en 1936 la **máquina de Turing**, base teórica de los computadores modernos
- Durante la Segunda Guerra Mundial dirigió el equipo que **rompió el código Enigma**, acortando la guerra en años
- En 1950 planteó el **Test de Turing**, primer intento formal de medir inteligencia artificial
- Fue perseguido por su homosexualidad y murió en 1954
- Hoy es considerado el **padre de la computación y la IA**

---

## Slide 14 — Descifrando Enigma (película)

Biopic sobre el matemático británico Alan Turing, famoso por haber descifrado los códigos secretos nazis contenidos en la máquina Enigma, lo cual determinó el devenir de la II Guerra Mundial (1939-1945) en favor de los Aliados.

Lejos de ser admirado como un héroe, Turing fue acusado y juzgado por su condición de homosexual en 1952.

[IMAGEN: Póster de la película "The Imitation Game" (Descifrando Enigma)]

---

## Slide 15 — Portada sección

**Blockchain**
Práctica de Smart Contracts

---

## Slide 16 — Smart Contracts: Ejemplo sencillo - Caja Fuerte

**Caja fuerte (Vault):**
- Permite a cualquier usuario enviar ethers al contrato indicando una cantidad de tiempo durante la que quedarán bloqueados
- No tiene una utilidad práctica directa, pero sirve para ejemplificar el uso de un Smart Contract con código sencillo

---

## Slide 17 — Práctica: Desplegar Caja Fuerte

1. Acceder a Remix: https://remix.ethereum.org/
2. Borrar los contratos de ejemplo que trae por defecto
3. Conectar la billetera MetaMask
4. Crear nuevo fichero `vault.sol` y pegar el código
5. Compilar y verificar que no hay errores
6. (Opcional) Desplegar el código en la red Sepolia, o bien usar la dirección de un contrato ya desplegado
7. Bloquear una pequeña cantidad y verificar que no puedes recuperarla hasta pasado el tiempo de lock

[NOTA PROFESOR: Tener preparado el código de vault.sol y la dirección de un contrato ya desplegado como plan B si algún alumno tiene problemas con el despliegue. Preparar el código con comentarios didácticos línea a línea.]

---

## Slide 18 — Debate: Desplegar la Caja Fuerte

**Experiencia técnica y de usuario:**
- ¿Qué te ha parecido el uso de MetaMask para conectarte a Remix?
- ¿Es intuitivo o complejo el proceso de firmar transacciones?
- ¿Qué riesgos ves en que el usuario tenga que aprobar cada interacción manualmente?
- ¿Podría un contrato malicioso aprovechar una firma descuidada?
- ¿Qué aprendiste sobre la relación entre frontend (Remix) y backend (blockchain)?

**Accesibilidad y permanencia:**
- Un contrato desplegado es visible y accesible por cualquiera: ¿qué ventajas e inconvenientes tiene?
- Si cualquiera puede invocar tu contrato, ¿cómo se garantiza la seguridad?
- ¿Qué implica el principio "deploy once, consume all" en términos de propiedad intelectual y responsabilidad?
- ¿Qué tan difícil sería ocultar información sensible en un contrato público?
- ¿Debería existir un modo de retirar o modificar un contrato una vez desplegado?

---

## Slide 19 — Práctica: Usar Etherscan

- Entrar en https://sepolia.etherscan.io/
- Buscar el Smart Contract de la Caja Fuerte
- Ver todas las interacciones que ha habido
- Identificar: quién desplegó, quién bloqueó fondos, quién retiró

---

## Slide 20 — Repaso del Día 4

**Preguntas:**
1. Las custodial wallets son más seguras porque permiten recuperar la clave con 12 palabras. ¿Verdadero o falso? Razona la respuesta.
2. La non-custodial wallet elimina la intermediación de cualquier tercero y hace al usuario final responsable de todos los movimientos. ¿Verdadero o falso?
3. Un smart contract es un programa que envía transacciones a la red blockchain. ¿Verdadero o falso?
4. ¿Qué papel cumplen los mineros en la ejecución de un smart contract?
5. ¿Por qué Ethereum se considera pionera en smart contracts?
6. ¿Qué condiciones deben cumplirse para que un smart contract se ejecute automáticamente?
7. ¿Qué ocurre si un smart contract tiene un error en el código?
8. ¿Por qué la transparencia puede ser a la vez una fortaleza y una debilidad?
9. ¿Puede un smart contract llamar a otro smart contract?
10. ¿Qué papel cumplen los **oráculos** en los smart contracts?
11. ¿Dónde se guarda la clave privada de la dirección en la que se despliega un smart contract?
12. ¿Qué pasa si se pierde la clave privada del propietario del smart contract?
13. ¿Por qué los smart contracts no pueden acceder directamente a internet?
14. ¿Qué ventajas tiene probar un contrato en una red de test como Sepolia antes del despliegue real?
15. ¿Cómo garantizan los oráculos descentralizados (como Chainlink) la fiabilidad de los datos?

---

## Slide 21 — Tarea para casa

**Buscar información sobre el ERC-3643** en internet y preparar una slide en la que se describan sus principales características.

*Presentar el lunes al inicio de clase.*

[NOTA PROFESOR: ERC-3643 es un estándar de "permissioned tokens" para tokenizar RWA (Real World Assets) y valores regulados en EVM. Controla quién puede poseer y transferir. Usa identidades on-chain y claims verificables para KYC/AML. Es un puente perfecto hacia el tema de blockchain permissioned que se verá más adelante con Hyperledger Fabric.]

---

## Actividad de relleno (si sobra tiempo)

### Hackea el contrato (30-45 min)

- El profesor despliega un Smart Contract con un bug intencionado en Sepolia (o usa Remix en modo local).
- El contrato es un "banco simple": permite depositar ETH y retirar.
- Pero tiene una vulnerabilidad: no actualiza el saldo antes de enviar los fondos (reentrancy clásica, como The DAO).
- Reto: los alumnos, en parejas, deben:
  1. Leer el código del contrato en Remix
  2. Identificar la vulnerabilidad
  3. Explicar cómo la explotarían (no hace falta escribir el exploit, solo describirlo)
  4. Proponer cómo arreglarla
- Bonus para los más avanzados: escribir un contrato atacante que explote la vulnerabilidad en Remix (modo local).

[NOTA PROFESOR: Preparar un contrato sencillo tipo:
```solidity
mapping(address => uint) public balances;
function withdraw() public {
    uint amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0; // ← BUG: debería ir ANTES del call
}
```
La vulnerabilidad es que el saldo se pone a 0 DESPUÉS de enviar los fondos. Un contrato atacante puede llamar withdraw() recursivamente desde su función receive(). Conectar con el caso The DAO del día 7.]
