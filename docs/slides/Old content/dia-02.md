# Día 2 — Hash, criptografía, redes P2P y encadenado de bloques

---

## Slide 1 — Portada
**Blockchain**
Hash

[IMAGEN: Representación visual de una función hash con datos entrando y un código hexadecimal saliendo]

---

## Slide 2 — ¿Qué es un Hash?
- Un hash es una función de **una sola dirección** que convierte datos de entrada en una salida única de **tamaño fijo**. Se puede ver como una huella digital de los datos
- Es de una sola dirección porque es sencillo generar la salida, pero dada una salida es **imposible*** calcular los datos originales que la generaron
- Las funciones de hash tienen dos características más:
  - Crear el hash dada una entrada es **rápido**
  - No hay **colisiones**: es imposible* que dos entradas diferentes generen la misma salida

*La probabilidad es de 1/10⁷², la misma que la de coger dos veces el mismo electrón en el universo

[IMAGEN: Diagrama mostrando Entrada A → Hash → Salida fija, con flecha de vuelta tachada (irreversible)]

---

## Slide 3 — Actividad: Validar algoritmos de hash
Un hash debe cumplir:
1. Función de una sola dirección
2. Entrada variable, salida de tamaño fijo
3. Rápida y sin colisiones

**Propuesta de algoritmo MyHash:**
- Tomamos un número primo P y el hash es el resto de dividir la entrada entre ese número
- Por ejemplo P=7:
  - MyHash(21) = 0 → 21/7 = 3, resto 0
  - MyHash(33) = 5 → 33/7 = 4, resto 5

**¿Por qué no es válida?**

[NOTA PROFESOR: No cumple "sin colisiones" ni "tamaño fijo proporcional a la seguridad". MyHash(21) = MyHash(14) = MyHash(7) = 0. Hay infinitas colisiones. Además, dado el hash se puede encontrar fácilmente una entrada válida (no es unidireccional en la práctica).]

---

## Slide 4 — Hash en Blockchain
En Blockchain el hash se usa para:
- **Integridad de datos** en el encadenado de bloques
- **Algoritmos de consenso** (Proof of Work)
- **Creación de identificadores únicos**

Hay múltiples funciones matemáticas de hashing:
CRC, MD5, SHA-1, SHA-2, SHA-3, Keccak, SHAKE, KMAC, BLAKE…

| Blockchain | Función de hash |
|------------|----------------|
| Bitcoin | SHA-256 |
| Ethereum | Keccak-256 |

---

## Slide 5 — Práctica: SHA-256 en el navegador
Ir a: https://emn178.github.io/online-tools/sha256.html

- Introducir diferentes textos y observar cómo cambia completamente el hash
- Probar que cambiar un solo carácter produce un hash totalmente distinto
- Verificar que el mismo texto siempre produce el mismo hash

---

## Slide 6 — Portada sección
**Blockchain**
Clave Pública/Privada

[IMAGEN: Candado abierto (clave pública) y llave (clave privada)]

---

## Slide 7 — Claves pública/privada
Son dos números matemáticamente ligados, de forma que de la clave privada se puede calcular la pública fácilmente pero no a la inversa. Cumplen dos propiedades importantes:

**Cifrado:**
- La **clave pública** se comparte libremente. Cualquiera la usa para **cifrar** un mensaje
- La **clave privada** es secreta y permite descifrar lo que fue cifrado con la pública
- Tu clave pública es como un **candado abierto** que regalas a todos. Cualquiera mete un mensaje en una caja y la cierra con ese candado. Solo tú tienes la llave para abrirla

**Firma digital:**
- Con tu **clave privada** puedes, dado un mensaje cualquiera, generar un **código único** que solo esa clave privada puede producir
- Cualquiera que tenga tu **clave pública** puede comprobar:
  - Que la firma proviene de tu clave privada (**autenticidad**)
  - Que el mensaje no fue alterado después (**integridad**)

---

## Slide 8 — Práctica: Cifrado RSA
https://www.devglan.com/online-tools/rsa-encryption-decryption

- Generar un par de claves RSA
- Cifrar un mensaje con la clave pública
- Descifrar con la clave privada
- Intentar descifrar con otra clave privada diferente (no funciona)

---

## Slide 9 — Pregunta para reflexionar
**¿Por qué no puedo usar simplemente una clave privada elegida por mí al azar y un algoritmo de hash para calcular mi clave pública y que cifren con ella?**

Después de todo, la clave pública se calcularía fácilmente desde la privada…

[NOTA PROFESOR: Porque un hash no tiene la propiedad de "trampa" (trapdoor) necesaria para el cifrado asimétrico. Con un hash no puedes descifrar. Se necesita una relación matemática específica (como curvas elípticas o factorización de primos) que permita cifrar con una y descifrar con la otra.]

---

## Slide 10 — Práctica: Firma con ECDSA
https://8gwifi.org/ecsignverify.jsp

- Generar claves con curva elíptica
- Firmar un mensaje
- Verificar la firma
- Alterar el mensaje y verificar de nuevo (falla)

---

## Slide 11 — ¿Para qué se usan las claves en blockchain?
**Respuesta:** Para crear los wallets de los clientes y firmar transacciones con la clave privada asociada a ese wallet. Es una especie de identidad digital pseudónima.

- Cada usuario genera un par de claves: privada (secreta) y pública (se deriva de la privada)
- De la clave pública se calcula una **dirección** aplicando hashes y codificación
  - Ejemplo Bitcoin: SHA-256 → RIPEMD-160 → Base58Check
- Esa dirección es lo que compartes para recibir fondos
- La privada nunca se revela; se usa solo para firmar transacciones

Tu dirección es como tu número de cuenta, tu clave pública la respalda, y tu clave privada es la única forma de mover el dinero. Te identifica de forma pseudónima en esa red.

---

## Slide 12 — Práctica: Generar dirección Bitcoin
https://www.bitaddress.org/

- Generar una dirección Bitcoin
- Identificar la clave privada, la clave pública y la dirección
- Observar cómo la dirección es mucho más corta que la clave pública

---

## Slide 13 — Práctica: Generar dirección Ethereum
https://generate.mitilena.com/en/ethereum/

- Generar una dirección Ethereum
- Comparar el formato con la dirección Bitcoin
- ¿Qué diferencias observas?

---

## Slide 14 — Portada sección
**Blockchain**
Redes P2P

[IMAGEN: Red de nodos interconectados sin servidor central]

---

## Slide 15 — Red peer-to-peer

[IMAGEN: Comparativa entre red cliente-servidor (estrella) y red P2P (malla). En la red P2P todos los nodos son iguales.]

- En una red P2P no hay servidor central
- Todos los nodos son iguales: cada uno es cliente y servidor a la vez
- Ejemplo real: https://geth.ethereum.org/ (nodo de Ethereum)

---

## Slide 16 — Propagación de transacciones en P2P

[IMAGEN: Animación/secuencia de un nodo enviando una transacción y esta propagándose nodo a nodo por toda la red]

- Un nodo recibe una transacción
- Ese nodo la transmite a sus pares, y así se propaga por **toda la red**
- Cada nodo valida la transacción antes de reenviarla

---

## Slide 17 — De transacciones a bloques

[IMAGEN: Secuencia mostrando: transacciones sueltas → agrupadas en un bloque → bloque añadido a la cadena]

- Las transacciones se agrupan en bloques
- Cada nuevo bloque se añade al final de la cadena
- Como contiene el hash del bloque anterior, queda "encadenado"
- Si alguien altera un bloque, toda la secuencia posterior se invalida

---

## Slide 18 — Portada sección
**Blockchain**
Cadena de Bloques

---

## Slide 19 — Encadenado de bloques

Cada bloque de la cadena contiene dos elementos clave:
- Sus propios datos (transacciones)
- Una marca de tiempo (timestamp)
- El **hash del bloque anterior**

En el ejemplo:
- El Bloque N guarda dentro el hash del Bloque N-1
- El Bloque N+1 guarda dentro el hash del Bloque N

[IMAGEN: Tres bloques encadenados (N-1, N, N+1) con flechas mostrando cómo cada uno contiene el hash del anterior]

Este mecanismo hace que los bloques queden **encadenados criptográficamente:**
- Si alguien modifica un dato en el Bloque N, cambia su hash
- Como ese hash está dentro del Bloque N+1, también se invalida
- El efecto se propaga hasta el final de la cadena

**Consecuencia práctica:** Alterar un solo bloque rompe toda la cadena posterior. Para falsear el ledger habría que rehacer todos los bloques posteriores, algo computacionalmente inviable.

---

## Slide 20 — Actividad: reflexión sobre el encadenado
Hasta ahora tenemos:
1. Un mecanismo que permite **firmar transacciones** con tu identidad
2. Una **red P2P** capaz de recoger esas transacciones, validar que están correctamente firmadas y agregarlas al ledger
3. Un mecanismo que **encadena los hashes** de los bloques impidiendo modificar un bloque sin modificar todos los siguientes

**Pregunta:** ¿Por qué una red así sigue sin ser adecuada para un sistema de transacciones descentralizado?

---

## Slide 21 — Preguntas adecuadas que hacerse

**1. ¿Qué pasa si dos nodos crean bloques distintos al mismo tiempo?**
- Ambos bloques son válidos y contienen transacciones correctas
- La red podría simplemente aceptar los dos
- **Realidad:** Si la red acepta dos cadenas diferentes, ya no existe un único ledger. Los saldos podrían divergir. Se necesita un mecanismo que resuelva qué bloque sobrevive.

**2. ¿Qué impide que alguien manipule su copia del ledger y regenere los hashes?**
- "Las firmas impiden cualquier cambio" → **Falso:** las firmas protegen transacciones, no el hash del bloque
- "Los nodos honestos tienen más potencia" → **Suposición:** si un atacante dispone de recursos superiores, puede inundar la red

**3. ¿Cómo decidimos cuál es la verdadera cadena?**
- "Podríamos votar entre nodos" → **Problema:** los atacantes pueden crear múltiples identidades (**ataque Sybil**) y ganar cualquier votación

---

## Slide 22 — Conclusiones
Falta un **mecanismo de consenso** que ponga de acuerdo a todos los nodos sobre qué bloque es el "oficial" en cada paso.

Dicho mecanismo debe garantizar:
- El **orden único** de las transacciones
- La **prevención del doble gasto** (mismo dinero gastado en dos transacciones)
- La **resistencia a ataques** donde alguien intenta imponer una versión alternativa de la cadena

---

## Treasure Hunt — Bitcoin Pizza Day

En 2010, cuando Bitcoin apenas valía unos céntimos, un programador quiso demostrar que la moneda podía usarse para cosas reales. Ofreció **10.000 bitcoins** a quien le enviara dos pizzas. Un usuario de foros aceptó el trato y pidió las pizzas por teléfono.

A día de hoy, esas dos pizzas habrían costado más de **1.000 millones de dólares**.

Desde entonces, el 22 de mayo se celebra como el **Bitcoin Pizza Day**, un recordatorio humorístico de lo rápido que puede cambiar el valor del dinero digital.

El programador se llamaba Laszlo Hanyecz, y se hizo famoso por ese hecho, pero…

**¿Qué otra gran contribución hizo a la comunidad Bitcoin?**

- Pista 1: ver ficheros 'Private Key.txt' y 'Contribucion del Programador.txt'
- Pista 2: RSA/ECB/PKCS1Padding

[NOTA PROFESOR: Laszlo Hanyecz fue el primero en implementar la minería de Bitcoin con GPU (tarjetas gráficas), multiplicando la velocidad de minado. Los alumnos deben descifrar el fichero 'Contribucion del Programador.txt' usando la clave privada del fichero 'Private Key.txt' con el algoritmo RSA/ECB/PKCS1Padding para descubrir la respuesta.]

---

## Slide 23 — Práctica: Red peer-to-peer con geth
- Descargar el software geth (1.11 o anterior) e instalarlo en `c:\geth`
- Crear bloque génesis en `c:\geth\mychaindata`
- Inicializar la red:
```
geth --datadir mychaindata init ./mychaindata/genesis.json
```
- Verificar cómo se han creado la keystore y el chaindata
- Arrancar el nodo:
```
geth --datadir ./mychaindata --networkid 15 --http --http.addr "localhost" --http.port 8552 --http.api "personal,eth,net,web3,miner,txpool" console
```
- Verificar cómo se crean el ledger (ficheros log, ldb, etc.)

---

## Slide 24 — Repaso del Día 2

**Preguntas:**
1. El hash se usa en blockchain para reducir el tamaño de la firma de las transacciones. ¿Verdadero o falso? Razona la respuesta.
2. La clave privada cifra los hashes de cada bloque para que nadie pueda alterarlos. ¿Verdadero o falso? Razona la respuesta.
3. En un servicio de red tradicional (por ejemplo, Gmail), Google ofrece el servicio y los usuarios lo consumen. En una red P2P, ¿quién es el cliente y quién el servidor?
4. ¿Quién firma las transacciones que se envían a la red blockchain y quién firma cada bloque?
5. ¿Qué es el pool de transacciones?
6. Describe el flujo de trabajo de una red blockchain, desde el envío de una transacción firmada hasta la adición de un nuevo bloque.
7. Proof of Stake cambia el gasto en energía eléctrica por gasto en equipos caros. ¿Verdadero o falso? Razona la respuesta.
8. El algoritmo de consenso sirve para solucionar el problema del orden de bloques y los ataques maliciosos de alteración de la cadena. ¿Verdadero o falso? Razona la respuesta.
9. Nombra, al menos, tres algoritmos de consenso y explica en qué se basan.
10. En una red que usa Proof of Authority, cualquiera puede conectarse y minar bloques. ¿Verdadero o falso? Razona la respuesta.

[NOTA PROFESOR: Las preguntas 7-10 anticipan contenido del día 3 (consenso). Es intencional: sirven como gancho para el día siguiente. No esperar respuestas correctas, sino que empiecen a reflexionar.]

---

## Actividad de relleno (si sobra tiempo)

### Mensajes secretos entre compañeros (30-45 min)

- Por parejas, los alumnos se envían mensajes cifrados usando las herramientas vistas en clase.
- Ronda 1 — Cifrado simétrico: acordar una clave secreta y usar https://aesencryption.net/ para cifrar y descifrar mensajes. El reto: enviar el mensaje cifrado por el chat de clase y que SOLO tu pareja lo pueda leer.
- Ronda 2 — Cifrado asimétrico: usar la herramienta RSA vista en clase. Uno genera el par de claves, comparte la pública, y el otro cifra un mensaje que solo el dueño de la privada puede leer.
- Ronda 3 — Firma digital: firmar un mensaje con tu clave privada y que tu compañero verifique que fuiste tú quien lo escribió.
- Bonus: ¿Puedes interceptar el mensaje de otra pareja? (No deberías poder, pero intentarlo genera aprendizaje.)

[NOTA PROFESOR: Esta actividad refuerza de forma práctica los tres pilares: confidencialidad (cifrado), autenticidad (firma) e integridad (verificación). Si hay alumnos avanzados, pueden intentar un man-in-the-middle attack en la ronda 2 para demostrar por qué se necesitan certificados (que verán en los días de Fabric).]
