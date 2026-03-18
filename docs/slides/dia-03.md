# Día 3 — Consenso, Proof of Work, trilema y MetaMask

---

## Slide 1 — Portada sección
**Blockchain**
Consenso

[IMAGEN: Generales bizantinos alrededor de una ciudad amurallada]

---

## Slide 2 — Mecanismos de Consenso
- **Objetivo:** lograr que muchos nodos no confiables acuerden una única historia de transacciones
- **Requisito clave:** tolerar fallos y nodos maliciosos sin depender de una autoridad central
- Pero… ¿cómo fiarte de otros pares de los que no puedes fiarte?

---

## Slide 3 — El problema de los generales bizantinos
- Varios generales rodean una ciudad con sus ejércitos y deben decidir si atacar o retirarse
- Uno de ellos es el que debe iniciar la orden de ataque o de retirada
- Se comunican mediante mensajeros
- Tanto los generales como los mensajeros pueden ser **traidores** y dar información falsa
- **Éxito:** se llega a consenso entre todos los generales leales
- **Fracaso:** algunos generales leales atacan y otros se retiran

---

## Slide 4 — Generales bizantinos: con 3 no hay solución

[IMAGEN: Diagrama con 3 generales: 1 traidor y 2 leales. El traidor envía "Atacar" a uno y "Retirarse" al otro. Los leales no pueden distinguir la verdad.]

Con tres generales no hay solución si uno es traidor.

---

## Slide 5 — Generales bizantinos: con 4 sí hay solución (si 3 son leales)

[IMAGEN: Diagrama con 4 generales: 1 traidor y 3 leales. Los leales intercambian mensajes y por mayoría llegan a consenso.]

Con cuatro generales sí hay solución si 3 son leales.

---

## Slide 6 — Generales bizantinos: la regla de los 2/3
Hay solución si **más de dos tercios** de los generales son leales.

[IMAGEN: Diagrama con 8 generales: 6 leales y 2 traidores, mostrando que se alcanza consenso]

---

## Slide 7 — Actividad: Simulación de consenso BFT
- Crear grupos en clase (ideal 5 personas por grupo)
- Cada persona tiene tarjetas suficientes para dar una al resto
- Probar la eficacia con pocos traidores (consenso se alcanza)
- Probar la eficacia con muchos traidores (consenso falla)
- Probar que con muchos traidores puede haber consenso a veces pero no siempre
- Debatir las conclusiones

---

## Slide 8 — Conclusiones: Consenso BFT
- El reto central es acordar un único valor en presencia de nodos que mienten
- Dos propiedades clave: **consistencia** (todos los leales deciden lo mismo) y **validez** (si la fuente leal dice X, se decide X)
- El coste de consenso crece con los fallos y con la latencia; la sincronía de la red importa
- La identidad de los participantes es fija y conocida; el modelo no contempla ataques Sybil
- A continuación veremos las diferencias clave con blockchain:
  - BFT clásico ofrece **finalidad determinista** con validadores conocidos
  - Nakamoto (PoW) ofrece **finalidad probabilística** en red abierta

---

## Slide 9 — Portada sección
**Blockchain**
Proof of Work

[IMAGEN: Pico de minero golpeando un bloque dorado con un hash]

---

## Slide 10 — Consenso Nakamoto: Proof of Work
- Se añade un **coste computacional** obligatorio para proponer un bloque
- Esa dificultad computacional se ajusta según la capacidad de cómputo actual de la red
- Se **recompensa** la creación de bloques correctos, lo que incentiva la honestidad
- Se basa en una **finalidad probabilística**

---

## Slide 11 — Proof of Work paso a paso
Se basa en resolver un puzzle matemático a base de fuerza bruta de computación:
1. El minero recoge transacciones y arma un bloque candidato
2. Al bloque le añade el timestamp, el hash del bloque previo y un número arbitrario llamado **nonce**
3. El minero varía el nonce y recalcula el hash del bloque
4. Repite millones de veces hasta que `hash(bloque) < target`
5. Si encuentra uno válido, lo difunde. Otros nodos verifican rápidamente (hash y transacciones)
6. Si es válido, lo aceptan y se convierte en la punta de la cadena

---

## Slide 12 — Proof of Work: diagrama de flujo

[IMAGEN: Diagrama mostrando el flujo completo:
1) Envío de transacciones
2) La transacción se almacena en el pool de transacciones
3) Mineros arman bloque y calculan nonce
4) Cuando lo encuentran, mandan el bloque a la red
5) La red valida el bloque y lo añade a la cadena
6) Al minero ganador se le recompensa]

---

## Slide 13 — Actividad: Encontrar hash con ceros al final
Ir a: https://emn178.github.io/online-tools/sha256.html

1. Elegir el algoritmo SHA-256
2. Introducir el texto: `Prueba de trabajo`
3. Calcular el hash
4. Añadir números después del texto hasta obtener un hash que acabe con al menos 3 ceros `000`

[NOTA PROFESOR: Una solución es: "Prueba de trabajo138". Animar a los alumnos a competir por quién lo encuentra primero. Esto simula la competición entre mineros.]

---

## Slide 14 — El problema de los forks temporales
- Idealmente todos los nodos se comunican instantáneamente. Sin embargo, en la realidad no es así
- Puede ocurrir que dos mineros en ubicaciones con latencia considerable resuelvan el bloque a la vez, lo envíen a los nodos más cercanos y ambos se validen y añadan a la cadena
- Eso crea una **bifurcación** (fork) en la cadena, lo cual es problemático
- **Solución:** desechar la rama con menos bloques acumulados, revertiendo todas las operaciones como si nunca hubieran existido, y retomar la que más bloques acumula

[IMAGEN: Diagrama de una cadena que se bifurca en dos ramas y luego la más corta se descarta]

---

## Slide 15 — ¿Cómo PoW resuelve los problemas?

| Problema | Cómo lo resuelve PoW |
|----------|---------------------|
| **Doble gasto** | Para reescribir la historia hace falta rehacer PoW de todos los bloques posteriores. Eso exige un gasto enorme de tiempo y energía |
| **Orden único** | La regla "cadena con más trabajo acumulado" sirve como criterio objetivo para escoger la historia |
| **Incentivos** | Los mineros que siguen las reglas reciben recompensas; atacar cuesta más que beneficiarse honestamente (si la mayoría es honesta) |

---

## Slide 16 — Actividad: Blockchain humano
- Pintar un ledger en la pizarra con tres wallets con saldo:
  - Ana: 1000
  - Nuria: 500
  - Ramón: 2500
- Organizar tres o cuatro grupos de mineros
- El profesor hará las veces de usuario solicitando transacciones entre las wallets
- Algoritmo de PoW: encontrar una palabra que empiece por la letra del wallet origen, acabe por la del destino y contenga la primera letra de la cantidad transferida
  - Ejemplo: 20 de Nuria a Ramón -> N...V...R -> "**navegar**" valdría
- Recompensar a los ganadores
- Ver cuánto acumula cada grupo al final de la actividad

---

## Slide 17 — Mecanismos de consenso alternativos: Proof of Stake
- En lugar de gastar energía, los nodos deben bloquear monedas ("**stake**")
- Los validadores son elegidos de forma pseudoaleatoria proporcional a su stake
- **Incentivo:**
  - Si actúan honestamente -> recompensas
  - Si atacan o se equivocan -> pierden parte del stake (**slashing**)

---

## Slide 18 — Comparativa: PoW vs PoS

| Aspecto | Proof of Work | Proof of Stake |
|---------|--------------|----------------|
| Ganancia | Proporcional a la inversión en hardware y consumo eléctrico | Proporcional a la cantidad de moneda bloqueada en el stake |
| Velocidad | Más lento produciendo bloques | Más rápido produciendo bloques |
| Energía | Consume mucha electricidad | Apenas consume electricidad |
| Vector de ataque | Los hackers necesitan el 51 % de la capacidad de cómputo | Los hackers necesitan el 51 % de las monedas de la red |

---

## Slide 19 — Vídeo: Blockchain explicado visualmente
https://www.youtube.com/watch?v=mhE_vvwAiRc

*Mostrar vídeo*

---

## Treasure Hunt — El código del Emperador

En el año 44 a.C., Julio César usaba un método de cifrado para comunicarse con sus generales: desplazaba cada letra del alfabeto un número fijo de posiciones. Este método se conoce como el **Cifrado César**.

El siguiente mensaje está cifrado con un desplazamiento de 13 posiciones (ROT13):

**`Ry cevzre oybdhr qr Ovgpbva fr yynzn Trarfvf Oybpx l shé zvanqb cbe Fngbfuv Anxnzbgb ry 3 qr rarer qr 2009`**

**Misión:**
1. Descifrar el mensaje (podéis usar https://rot13.com/ o hacerlo a mano)
2. Una vez descifrado: ¿qué mensaje dejó Satoshi dentro de ese bloque y por qué es simbólico?
3. Encontrar el bloque génesis de Bitcoin en un explorador público y verificar el mensaje

[NOTA PROFESOR: El mensaje descifrado es: "El primer bloque de Bitcoin se llama Genesis Block y fue minado por Satoshi Nakamoto el 3 de enero de 2009". El mensaje dentro del bloque génesis es: "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks". Es simbólico porque referencia directamente la crisis bancaria que motivó la creación de Bitcoin. Los alumnos pueden verificarlo en https://blockchair.com/bitcoin/block/0]

---

## Slide 20 — Portada sección
**Blockchain**
Trilema de Blockchain

---

## Slide 21 — El trilema de Blockchain
¿Qué es el trilema de Blockchain?
- Propuesto por **Vitalik Buterin** (Ethereum)
- Una blockchain busca tres propiedades:
  - **Seguridad** -> resistente a ataques y fallos
  - **Escalabilidad** -> procesar muchas transacciones rápido y barato
  - **Descentralización** -> que cualquiera pueda participar como nodo sin barreras
- **Problema:** en la práctica es muy difícil optimizar las tres al mismo tiempo

[IMAGEN: Triángulo con Seguridad, Escalabilidad y Descentralización en cada vértice]

---

## Slide 22 — Actividad: Trilema de Blockchain
Debatir entre los alumnos por qué si optimizas dos propiedades la otra decae:
- Alta descentralización + alta seguridad -> **Baja escalabilidad**
- Alta descentralización + alta escalabilidad -> **Baja seguridad**
- Alta seguridad + alta escalabilidad -> **Baja descentralización**

---

## Slide 23 — Trilema: Descentralización + Seguridad = Baja escalabilidad
- **Validación redundante y pesada:** en una red muy descentralizada cada nodo completo valida todas las transacciones. Máxima seguridad, pero la velocidad está limitada por el nodo más lento. Pocas transacciones por segundo.
- **Bloques pequeños y tiempos largos:** para que cualquier nodo (incluso con conexión débil) participe, los bloques deben ser pequeños y espaciados.
- **Coste de sincronización:** miles de nodos repartidos por el mundo necesitan recibir y verificar cada bloque.
- **Ejemplo:** Bitcoin (~7 TPS, bloques cada 10 minutos). Ethereum y Bitcoin han necesitado sidechains o Layer 2 para agilizar.

---

## Slide 24 — Trilema: Descentralización + Escalabilidad = Baja seguridad
- **Muchos nodos pequeños y rápidos -> difícil coordinar seguridad:** si cualquiera puede montar un nodo con pocos recursos y la red procesa miles de TPS, cada nodo valida muy rápido con poco coste. Resultado: validaciones menos rigurosas.
- **Hardware ligero -> nodos vulnerables:** al relajar requisitos, basta comprometer pocos nodos "fuertes" para manipular la red.
- **Ejemplo:** Solana (2021) buscaba escalabilidad alta y muchos nodos. Sufrió caídas de seguridad por saturación durante 17 horas al no poder eliminar un fork.

---

## Slide 25 — Trilema: Seguridad + Escalabilidad = Baja descentralización
- **Hardware exigente:** para procesar miles de TPS de forma segura, cada nodo necesita gran capacidad de cómputo y ancho de banda. Solo unos pocos actores pueden ser validadores.
- **Coste de entrada alto:** cuanto más compleja la validación, mayor el coste. Esto excluye a nodos pequeños.
- **Riesgo de concentración:** aunque la red sea segura y rápida, si solo un grupo reducido controla el proceso, se compromete la descentralización.
- **Ejemplo:** Redes permissioned (empresariales): muy rápidas y seguras, pero solo un conjunto limitado de nodos autorizados participa.

---

## Slide 26 — Conclusiones del trilema

| Combinación | Resumen |
|-------------|---------|
| Descentralización + Seguridad | "Cuando muchos nodos verifican cada detalle con máxima seguridad, la red se vuelve lenta y cara" |
| Descentralización + Escalabilidad | "Si abres demasiado la red y la haces muy rápida, la validación se debilita y la seguridad baja" |
| Seguridad + Escalabilidad | "Si quieres seguridad fuerte y miles de TPS, necesitas nodos potentes y caros, lo que concentra el control en pocos actores" |

---

## Slide 27 — Soy Minero

[IMAGEN: Minero con pico y casco, pero en lugar de rocas, está minando bloques digitales]

*Momento musical para romper el hielo antes del debate sobre el poder de los mineros*

---

## Slide 28 — Debate: El poder de los mineros
En Ethereum (y otras cadenas), los mineros o validadores deciden qué transacciones incluir en cada bloque y en qué orden. Ese orden puede alterar el resultado económico de operaciones automatizadas (DeFi).

- ¿Qué poder real tienen los mineros?
- ¿Cómo se podría ganar dinero con ese poder?
- Si los mercados financieros tradicionales migran a blockchain... ¿podría esto crear formas nuevas de manipulación o arbitraje?

---

## Slide 29 — El poder real de los mineros

[NOTA PROFESOR: Guiar el debate hacia estas conclusiones:]

- Pueden ver todas las transacciones pendientes en el **mempool** antes de que se confirmen
- Deciden qué transacciones incluir o excluir en cada bloque
- Eligen el **orden exacto** en que se ejecutarán dentro del bloque
- Pueden retrasar, priorizar o reemplazar transacciones según sus propios intereses, obviando las tarifas ofrecidas

---

## Slide 30 — ¿Cómo ganar dinero con ello?
- **Front-running:** adelantar una transacción propia justo antes de una grande para aprovechar un cambio de precio
- **Back-running:** colocar una transacción justo después de otra que moverá el mercado
- **Sandwich attack:** comprar antes y vender justo después de una transacción grande, extrayendo beneficio sin riesgo

Todo esto forma parte del fenómeno conocido como **MEV (Maximal Extractable Value)**.

---

## Slide 31 — Mercados tradicionales en blockchain

[NOTA PROFESOR:
- El control del orden podría permitir formas nuevas de manipulación similares al high-frequency trading
- Los mineros con acceso privilegiado podrían influir en precios o retrasar órdenes
- Surgiría la necesidad de regulación y transparencia]

---

## Slide 32 — Portada sección
**Blockchain**
MetaMask

[IMAGEN: Logo de MetaMask (zorro naranja)]

---

## Slide 33 — MetaMask: Instalar la extensión
- Ir a extensiones del navegador y buscar **MetaMask**
- Click en Obtener -> Agregar extensión
- Desplegar las extensiones existentes y dejar fija MetaMask por comodidad

[IMAGEN: Captura de la tienda de extensiones de Chrome con MetaMask]

---

## Slide 34 — MetaMask: Crear wallet
- Aceptar términos y crear un monedero nuevo
- Elegir una contraseña y **no olvidarla**
- Elegir proteger el monedero, copiar las 12 palabras y **NO PERDERLAS**

[IMAGEN: Pantalla de MetaMask mostrando las 12 palabras de recuperación]

---

## Slide 35 — MetaMask: Configurar red de pruebas
- Desplegar el menú de redes
- Marcar "Mostrar redes de prueba"
- Seleccionar **Sepolia**

[IMAGEN: MetaMask con el selector de redes abierto mostrando Sepolia]

---

## Slide 36 — MetaMask: Conseguir ETH de prueba
- Ir a un faucet: https://cloud.google.com/application/web3/faucet/ethereum/sepolia
- Copiar nuestra dirección de MetaMask
- Pegar en el campo 'Wallet Address' y pulsar 'Receive 0.05 Sepolia ETH'
- Si no tienes cuenta de Google, indicar al profesor para que envíe 0.05 ETH
- Registrar todas las direcciones en un fichero de la carpeta compartida

[NOTA PROFESOR: Tener preparada una wallet con suficientes Sepolia ETH para enviar a alumnos que no puedan usar el faucet. Unos 2 ETH deberían ser suficientes para toda la clase.]

---

## Slide 37 — MetaMask: Enviar ETH a un compañero
1. Pedir a un compañero su dirección y copiarla al portapapeles
2. Pulsar 'Enviar'
3. Pegar su dirección en el campo 'Para'
4. Indicar la cantidad (por ejemplo 0.001)
5. Dar continuar
6. Verificar que todo es correcto y pulsar 'Confirmar'
7. La transacción aparecerá como pendiente
8. Finalmente aparecerá un pop-up avisando de que se ha finalizado
9. El cambio de saldo se verá reflejado en ambas billeteras

---

## Slide 38 — MetaMask: Cambiar Fees
- Hacer otra transacción
- Al revisar los datos, pulsar sobre el icono del lápiz junto a 'Tarifa de red'
- Revisar las opciones existentes
- Ir a 'Avanzado' y revisar las opciones

---

## Slide 39 — Introducción al Gas
- **¿Qué es la 'Tarifa base mínima' (Max Base Fee)?**
  - Es la cantidad máxima de gas (en GWEI) que estás dispuesto a pagar por unidad de gas para cubrir la tarifa base dinámica de la red
  - La red Ethereum ajusta una "base fee" automáticamente en cada bloque
  - Si la base real es menor que tu máximo, te devuelven la diferencia

- **¿Y la 'Tarifa de prioridad' (Priority Fee)?**
  - Es la propina que ofreces al validador para que priorice tu transacción
  - Cuanto mayor es, antes se confirma

---

## Slide 40 — Unidades en Ethereum

[IMAGEN: Tabla de unidades de Ethereum: Wei, Gwei, Finney, Ether con sus equivalencias numéricas]

| Unidad | Valor en Wei | Uso típico |
|--------|-------------|------------|
| Wei | 1 | Unidad mínima |
| Gwei | 10^9 Wei | Tarifas de gas |
| Ether | 10^18 Wei | Transferencias |

---

## Slide 41 — Discusión: ¿Qué pasa con un fee muy bajo?
**¿Qué pasa si mando una transacción con un fee muy bajo?**

[NOTA PROFESOR:
- La transacción entra al mempool pero los validadores la ignoran si otras pagan más, quedando "pendiente" indefinidamente
- Puede sufrir inanición para siempre si las tarifas no bajan
- Mientras esté pendiente, bloquea las siguientes transacciones de esa cuenta ya que cada transacción lleva un número de secuencia (nonce)]

---

## Slide 42 — Nonce de Ethereum
**¿Qué es el nonce en Ethereum?**
- Número secuencial que identifica cada transacción enviada por una cuenta

**Propósito:**
- Garantiza el **orden exacto** de las transacciones
- Evita **repeticiones o duplicados** (ataques de replay)

**Reglas clave:**
- Cada cuenta empieza en nonce = 0
- Cada nueva transacción incrementa el nonce en +1
- Las transacciones deben minarse **en orden**
- Si se salta un número, las siguientes quedan **pendientes** hasta que la anterior se confirme

**No confundir** con el nonce del bloque (PoW). En Ethereum, "nonce" se usa para dos cosas distintas.

---

## Slide 43 — Pregunta: Desbloquear transacción atascada
**Si he mandado una transacción con un fee muy bajo y lleva atascada mucho tiempo (horas/días/meses), ¿cómo la desbloqueo?**

[NOTA PROFESOR:
1. Identificar el nonce bloqueado (Etherscan o MetaMask Configuración avanzada)
2. Reenviar (replace): crear nueva transacción con el MISMO nonce, mismo destino o tu propia dirección, con gas más alto. Esto sustituye la anterior ("Replace-by-fee")
3. Cancelar: enviar transacción vacía (0 ETH a ti mismo) con el mismo nonce y gas alto
4. Resultado: la nueva transacción sobrescribe la antigua y la cola vuelve a fluir]

---

## Slide 44 — MetaMask: ¿Dónde está el nonce?
- Al llegar a la pantalla de 'Confirmar', pulsar sobre el icono de 'settings' (diales) arriba a la derecha
- Aparecerá un campo editable con el nonce de la transacción a enviar

[IMAGEN: Captura de MetaMask mostrando el campo de nonce editable en la configuración avanzada de la transacción]

---

## Slide 45 — Debate: Conclusiones de MetaMask
¿Qué conclusiones sacáis del uso de MetaMask?

Considerar estos términos:
- **Seguridad**
- **Sencillez**
- **Accesibilidad**
- **Utilidad**
- **Protección ante errores o pérdida de la clave**

---

## Slide 46 — Repaso del Día 3

**Preguntas:**
1. El trilema de blockchain dice que solo podemos optimizar dos de estas tres características: seguridad, escalabilidad y privacidad. ¿Cierto o falso? Razona la respuesta.
2. El nonce, en una transacción Ethereum, es el número aleatorio que se añade para conseguir un hash con varios ceros. ¿Cierto o falso?
3. El nonce, en una transacción Ethereum, lo asigna la red para evitar duplicidad de transacciones. ¿Cierto o falso?
4. El gas es el coste que pagan los mineros para poder hacer staking. ¿Cierto o falso?
5. Si mando varias transacciones a la vez con el mismo nonce y el mismo gas, ¿cuál se incluirá en el bloque?
6. Y si mando de nuevo varias con el mismo nonce pero una tiene un poco más de gas, ¿tengo la certeza de que esa se incluirá?
7. ¿Cómo acelero una transacción atascada por emplear poco gas?
8. ¿Cómo elimino una transacción atascada?
9. Las 12 palabras son una representación nemotécnica de mi clave privada. ¿Cierto o falso?
10. ¿Por qué una red muy segura con rendimiento elevado tendrá poca descentralización?
11. Se dice que Blockchain es muy segura porque ofrece total privacidad en las transacciones. ¿Cierto o falso?
12. EVM significa Encrypted Vault Mechanism y es lo que usa MetaMask para guardar mi clave privada. ¿Cierto o falso?
13. MetaMask es un programa web que ofrece Google para gestionar nuestros wallets en sus servidores. ¿Cierto o falso?
14. El Wei es el lenguaje de programación de las redes EVM. ¿Cierto o falso?
15. MetaMask guarda la clave privada cifrada en el ordenador en el que está instalado; su uso está restringido a ese ordenador. ¿Cierto o falso?

[NOTA PROFESOR: Varias de estas preguntas son "trampas" intencionadas para que los alumnos piensen críticamente. Por ejemplo: la pregunta 1 dice "privacidad" en lugar de "descentralización" (falso), la pregunta 12 inventa un significado para EVM (falso: es Ethereum Virtual Machine).]
