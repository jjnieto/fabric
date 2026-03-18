# Día 1 — El dinero, la crisis y el nacimiento de Bitcoin

---

## Slide 1 — Portada
**Blockchain**
El Dinero

[IMAGEN: Portada visual con monedas antiguas, billetes y bitcoin superpuestos]

---

## Slide 2 — El origen del dinero: El Trueque
- Surgió en las primeras comunidades agrícolas del Neolítico (aprox. 10.000 a.C.)
- Se usaba para intercambiar excedentes de producción: cereales, animales, herramientas
- En Mesopotamia y Egipto, templos y palacios actuaban como centros de intercambio
- El valor de los bienes se establecía por necesidad y acuerdo directo
- **Limitaciones:** requería coincidencia de necesidades y no permitía acumular valor fácilmente
- Persistió incluso tras la aparición del dinero, sobre todo en economías rurales o de escasez

---

## Slide 3 — El origen del dinero: Dinero Commodity
Objetos con valor intrínseco:
- **Sal** (Roma, República temprana, entre los siglos VI y IV a.C.)
- **Conchas de caurí** (África y Asia)
- **Metales preciosos** (Egipto, China, Mesopotamia)
- Hay registros de deudas en plata de hace más de 5.000 años
- La moneda acuñada aparece en el siglo VII a.C. en Lidia (actual Turquía occidental)

---

## Slide 4 — El origen del dinero: Dinero Convertible
Es dinero respaldado por bienes tangibles, normalmente oro:
- Papel moneda en China, siglo IX
- Recibos de orfebres en Europa, siglo XVII
- Billetes bajo patrón oro, siglo XIX

---

## Slide 5 — El origen del dinero: Dinero Fiduciario
Dinero sin respaldo físico. Su valor depende de la confianza en el emisor:
- Lo inició China en el siglo XIII
- Se estableció globalmente en 1971 al suspender Nixon la convertibilidad del dólar en oro

---

## Slide 6 — Nacimiento de la banca: Reserva fraccionaria
- En el siglo XVII, los orfebres observaron que rara vez el depositario retiraba todo el metal precioso
- Les permitía emitir recibos más allá de los depósitos que tenían, realizando préstamos con intereses sobre fondos que no poseían. Nació la **reserva fraccionaria** y el concepto de banca moderna
- Aumentó el dinero en circulación pero generó riesgo de fuga de depósitos (**corridas bancarias**)
- El sistema fue institucionalizado con bancos públicos como el Banco de Ámsterdam (1609) y el Banco de Inglaterra (1694)

---

## Slide 7 — Concepto: Riesgo de contrapartida
**Definición:** Riesgo de que la otra parte de una transacción no cumpla con su obligación.

Es algo cotidiano con lo que lidiamos a diario:
- Hipotecas
- Préstamos al consumo
- Compras online
- Pago por adelantado
- Guardar ahorros en un banco

Todo esto nos lleva a la incómoda revelación de que el dinero se presenta en diferentes tipos y calidades.

---

## Slide 8 — Tipos de dinero

| Tipo | Descripción |
|------|-------------|
| **Dinero commodity** (oro, sal, conchas) | Valor propio, pero difícil de usar y transportar |
| **Dinero fiduciario de banco central** (billetes, efectivo) | Sin respaldo físico, pero máxima confianza institucional |
| **Depósitos bancarios** | Digitales y cómodos, con riesgo de contrapartida bancaria |
| **Dinero privado digital** (cripto, stablecoins) | Sin garantía estatal, riesgo y volatilidad elevados |
| **Dinero digital de banco central** | Las famosas CBDCs (Euro Digital) |

[IMAGEN: Diagrama con los 5 tipos de dinero ordenados de mayor a menor confianza institucional, con iconos representativos]

---

## Slide 9 — El concepto de liquidación o settlement
- El **settlement** o liquidación es la entrega final y confirmada de cualquier activo
- Marca el cierre real de la transacción: ya no hay riesgo pendiente
- En el pasado implicaba intercambio físico de oro o efectivo
- Hoy se hace mediante dinero de banco central (reserva o efectivo)

---

## Slide 10 — El concepto de liquidación o settlement (II)

[IMAGEN: Diagrama mostrando Central Bank Country A y Central Bank Country B conectados a través de CLS, con las siguientes anotaciones distribuidas alrededor:]

- Autorización, clearing y settlement ocurren en procesos y entidades diferentes
- Fees de las transacciones pagados por los usuarios
- Poca transparencia respecto al estado del pago
- Tiempo de pago poco predecible
- Coste operacional y de cumplimiento elevado
- Excesiva intermediación

---

## Slide 11 — Actividad: Liquidación simulada
Simular tres tipos de transacciones:
1. Interna del mismo banco
2. Transacción intrabancaria (in-border)
3. Transacción transfronteriza (cross-border)

Definir todos los agentes: pagador → banco del pagador → banco corresponsal en origen → banco central → y lo mismo en destino hasta el receptor.

---

## Slide 12 — Actividad: Liquidación simulada (I)
**Caso 1: Transacción interna del mismo banco**

Ejemplo: Cliente A (Banco A) paga a Cliente B (Banco A)

Pasos:
1. Cliente A da la orden de pago de 100 unidades
2. Banco A resta 100 de la cuenta de A y suma 100 a la cuenta de B en su libro interno (no interviene el banco central ni sale dinero real del banco)
3. Banco A informa a ambos clientes

**Conclusión:** Es solo un **asiento contable interno**. No hay movimiento de dinero de banco central.

---

## Slide 13 — Actividad: Liquidación simulada (II)
**Caso 2: Transacción intrabancaria (entre bancos del mismo país)**

Ejemplo: Cliente A (Banco A) paga a Cliente B (Banco B)

Pasos:
1. Cliente A da la orden de pagar 100 unidades
2. Banco A reduce 100 en la cuenta de A
3. Banco A debe transferir 100 a Banco B. Para ello usa sus **reservas** en el Banco Central
4. Banco A resta 100 en su cuenta de reservas en el Banco Central
5. Banco Central suma 100 a la cuenta de reservas de Banco B
6. Banco B acredita 100 a la cuenta de Cliente B
7. Ambos bancos informan a sus clientes

**Conclusión:** El dinero entre bancos se liquida con **dinero de banco central**. El dinero de clientes sigue siendo **dinero de banco comercial**.

---

## Slide 14 — Actividad: Liquidación simulada (III)
**Caso 3: Transacción transfronteriza (entre países distintos)**

Ejemplo: Cliente A (Banco A, País X) paga a Cliente B (Banco B, País Y)

Pasos:
1. Cliente A ordena pagar 100 unidades (en moneda de País Y o divisa)
2. Banco A reduce 100 en la cuenta de A
3. Banco A ordena el pago a través de su **banco corresponsal** en País Y
4. Banco A tiene una cuenta **nostro** en Banco C (corresponsal)
5. Banco C tiene reservas en el Banco Central del País Y
6. Banco C transfiere 100 a Banco B mediante el sistema local del País Y (como en el caso 2)
7. Banco B acredita 100 a Cliente B
8. Si hay cambio de divisa, los bancos centrales pueden intervenir para ajustar reservas internacionales

**Conclusión:** El dinero cruza fronteras mediante relaciones de corresponsalía y reservas en diferentes bancos centrales.

---

## Slide 15 — Los bancos crean dinero
- La reserva fraccionaria permite a las entidades con licencia del Banco Central captar fondos de clientes y crear dinero con un ratio aproximado de 10 a 1
- Es decir, por cada euro que deposita el cliente, el banco puede crear aproximadamente 10, pero debe dedicarlos a préstamos
- Es una manera de multiplicar el dinero que crea el Banco Central y dedicarlo a los proyectos más prometedores, porque no olvidemos que los bancos son muy buenos evaluando el riesgo de crédito…
- … ¿o no?

---

## Slide 16 — La crisis bancaria de 2008: Tormenta perfecta
- **Crédito de mala calidad:** los bancos prestaron a prestatarios muy por encima del nivel de riesgo aceptable
- **Activos de mala calidad:** hipotecas "subprime" empaquetadas en productos financieros que parecían seguros
- **Confianza rota:** cuando los impagos crecieron, se dudó de la solvencia bancaria → riesgo de contrapartida visible
- **Congelación del settlement interbancario:** bancos dejaron de prestarse entre sí porque no confiaban en recibir el pago final
- **Resultado:** corridas bancarias "modernas" (retiros masivos de depósitos y liquidez), necesidad de rescates estatales y de bancos centrales como prestamistas de última instancia

La crisis no fue solo de hipotecas, fue de **confianza en el propio dinero bancario**. La diferencia entre dinero de banco central y dinero privado se volvió evidente.

---

## Slide 17 — Debate: Confianza en el Sistema Financiero
- ¿Qué falló en 2008 para que casi colapsara la economía mundial?
- ¿Qué papel jugaron los reguladores (Bancos Centrales) antes, durante y después de la crisis?
- ¿Cuál crees que fue el resultado de esa crisis?

[NOTA PROFESOR:
- Antes: permitieron una expansión crediticia excesiva y una regulación laxa del riesgo.
- Durante: actuaron como prestamistas de última instancia, inyectando liquidez masiva y rescatando bancos.
- Después: reforzaron la regulación (mayores requisitos de capital, supervisión más estricta) y mantuvieron políticas monetarias expansivas.
- Resultado: surgió desconfianza hacia las instituciones financieras, lo que impulsó la búsqueda de alternativas descentralizadas → Bitcoin.]

---

## Slide 18 — Satoshi Nakamoto y el paper de Bitcoin
- **2008, colapso financiero global:** se evidencian los problemas del dinero bancario: riesgo de contrapartida, falta de transparencia y confianza
- **Octubre 2008:** aparece en internet el whitepaper de Bitcoin, firmado por Satoshi Nakamoto
- **Propuesta clave:** un sistema de dinero digital, descentralizado y sin necesidad de bancos, basado en criptografía y consenso distribuido
- **Mensaje simbólico:** en el primer bloque minado (el genesis block) se incluyó la frase: *"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"*
- Bitcoin nació como respuesta a la crisis y a la dependencia del sistema financiero tradicional

*Repartir el paper entre los alumnos*

---

## Slide 19 — Del problema a la tecnología
- El 2008 mostró los límites del dinero bancario: riesgo, opacidad, rescates
- Bitcoin planteó: ¿es posible tener dinero digital sin depender de bancos?
- Respuesta: una tecnología llamada **blockchain**, que permite registrar transacciones de forma segura, transparente y descentralizada
- A partir de aquí, no solo Bitcoin → toda una revolución tecnológica llamada **Blockchain**

---

## Slide 20 — Qué propone Blockchain
**Dinero digital sin intermediarios:**
- Transferir archivos es trivial (copiar/pegar)
- Pero con dinero no puedes permitir que alguien copie sus monedas y las gaste dos veces
- Antes de Bitcoin, todas las propuestas de dinero digital requerían un **tercero central** que validara operaciones (bancos, PayPal…)

---

## Slide 21 — Qué problemas resuelve Blockchain

| Problema | Descripción |
|----------|-------------|
| **Doble gasto** | Sin un árbitro, ¿cómo evitar que una misma moneda se use dos veces? Si mando una foto, tú la tienes pero yo también. Con dinero eso sería fraude. |
| **Orden de las transacciones** | ¿Quién decide qué transacción ocurrió primero? En un sistema descentralizado, distintos nodos pueden ver mensajes en distinto orden → se necesita un mecanismo compartido de secuencia. |
| **Integridad de registros** | Una vez acordado el orden, ¿cómo garantizar que nadie pueda cambiar el pasado? Si alguien modifica un registro, todo lo posterior debe quedar inválido. |
| **Confianza sin intermediario** | ¿Cómo puedo confiar en que una transacción es válida si no hay un banco central? La red debe verificar de manera colectiva. |

---

## Slide 22 — Repaso del Día 1

**Conceptos clave:**
- Riesgo de contrapartida
- Settlement o liquidación
- ¿Por qué el settlement es complejo en las transacciones bancarias?
- ¿Qué propone Blockchain para resolver estos problemas?
- ¿Qué evento histórico motivó la creación de Bitcoin?

---

## Actividad de relleno (si sobra tiempo)

### Simula tu propio banco (30-45 min)

Simulación guiada paso a paso del sistema bancario, la reserva fraccionaria y una crisis de liquidez.

**Preparación (5 min)**

| Rol | Quién | Material |
|-----|-------|----------|
| **Banco Central** | El profesor | Folios en blanco (para "imprimir" dinero) |
| **Banco A** | 2 alumnos (un director y un cajero) | Hoja de balance en la pizarra o papel grande |
| **Banco B** | 2 alumnos (un director y un cajero) | Hoja de balance en la pizarra o papel grande |
| **Clientes** | El resto de la clase (10-15 personas) | Cada uno recibe un sobre con su nombre |

Preparar en la pizarra (o en dos cartulinas) la hoja de balance de cada banco:

```
BANCO A                          BANCO B
─────────────────────            ─────────────────────
RESERVAS:    ___€                RESERVAS:    ___€
PRÉSTAMOS:   ___€                PRÉSTAMOS:   ___€
DEPÓSITOS:   ___€                DEPÓSITOS:   ___€
```

---

**FASE 1 — Los depósitos (5 min)**

El profesor (Banco Central) reparte dinero a los clientes:

> "Soy el Banco Central. Acabo de emitir dinero. Cada uno de vosotros recibe 100€."

Dar a cada cliente un papelito que dice "100€".

> "Ahora necesitáis guardar vuestro dinero. Los que estáis en la fila izquierda, id al Banco A. Los de la fila derecha, al Banco B."

- Los clientes entregan sus 100€ al cajero del banco correspondiente.
- El cajero anota en la hoja de balance: +100€ en RESERVAS y +100€ en DEPÓSITOS por cada cliente.
- **Resultado esperado** (con ~6 clientes por banco):
  - Banco A: Reservas 600€, Depósitos 600€
  - Banco B: Reservas 600€, Depósitos 600€

---

**FASE 2 — La reserva fraccionaria (5 min)**

El profesor explica:

> "Vuestros bancos tienen licencia para operar con reserva fraccionaria del 10%. Eso significa que solo necesitáis mantener el 10% de los depósitos en reserva. El resto lo podéis prestar para ganar intereses."

Instrucciones para los bancos:
- Banco A: reserva 60€ (10%) y puede prestar hasta 540€
- Banco B: reserva 60€ (10%) y puede prestar hasta 540€

---

**FASE 3 — Los préstamos (5 min)**

El profesor asigna préstamos concretos:

> "Cliente 1 (del Banco A): pides un préstamo de 200€ para comprar un coche."

- Banco A entrega 200€ al Cliente 1. Anota: +200€ en PRÉSTAMOS, -200€ en RESERVAS.

> "Cliente 2 (del Banco A): pides un préstamo de 150€ para reformar tu casa."

- Banco A entrega 150€. Anota: +150€ en PRÉSTAMOS, -150€ en RESERVAS.

> "Cliente 7 (del Banco B): pides un préstamo de 300€ para montar un negocio."

- Banco B entrega 300€. Anota: +300€ en PRÉSTAMOS, -300€ en RESERVAS.

> "Cliente 8 (del Banco B): pides 100€ para un viaje."

- Banco B entrega 100€. Anota: +100€ en PRÉSTAMOS, -100€ en RESERVAS.

**Estado de los balances después de los préstamos:**

```
BANCO A                          BANCO B
─────────────────────            ─────────────────────
RESERVAS:    250€                RESERVAS:    200€
PRÉSTAMOS:   350€                PRÉSTAMOS:   400€
DEPÓSITOS:   600€                DEPÓSITOS:   600€
```

El profesor pregunta: *"¿Os dais cuenta de que los depósitos siguen siendo 600€ pero las reservas son mucho menores? ¿Qué pasa si todos los clientes vienen a retirar su dinero a la vez?"*

---

**FASE 4 — Los préstamos interbancarios (3 min)**

> "El Banco A necesita más liquidez para conceder otro préstamo. Le pide prestados 100€ al Banco B."

- Banco B transfiere 100€ al Banco A. Ambos anotan la operación.

```
BANCO A                          BANCO B
─────────────────────            ─────────────────────
RESERVAS:    350€                RESERVAS:    100€
PRÉSTAMOS:   350€                PRÉSTAMOS:   400€
DEPÓSITOS:   600€                DEPÓSITOS:   600€
DEUDA CON B: 100€                B A DEBE:    100€
```

---

**FASE 5 — La crisis (10 min)**

El profesor anuncia con tono dramático:

> "ÚLTIMA HORA: Un periódico publica que el Banco B ha concedido préstamos de mala calidad. El Cliente 7, al que le prestaron 300€ para un negocio, ha quebrado y no va a devolver el dinero."

Pausa. Dejar que los alumnos procesen.

> "Clientes del Banco B: tenéis miedo de perder vuestro dinero. Hacéis cola para retirarlo. Cliente 9, ve al Banco B y retira tus 100€."

- Banco B entrega 100€. Reservas bajan a 0€.

> "Cliente 10, ve al Banco B y retira tus 100€."

- **El Banco B no puede.** Solo tiene 0€ en reservas. El dinero está prestado.

El cajero del Banco B debe decir: *"Lo siento, no tenemos fondos disponibles en este momento."*

> "El rumor se extiende. Ahora los clientes del Banco A también tienen miedo, porque saben que el Banco A le prestó 100€ al Banco B. ¿Y si el Banco B no puede devolvérselos?"

> "Cliente 3, ve al Banco A y retira tus 100€."

- Banco A entrega 100€. Reservas bajan a 250€.

> "Cliente 4, Cliente 5 y Cliente 6: id todos a la vez al Banco A."

- Banco A necesita 300€ pero solo tiene 250€. **No puede pagar a todos.**

**Los dos bancos están en crisis.**

---

**FASE 6 — El rescate del Banco Central (5 min)**

El profesor (Banco Central) interviene:

> "Soy el Banco Central. Para evitar que el sistema colapse, voy a actuar como prestamista de última instancia."

El profesor coge folios en blanco, escribe "200€" en cada uno y los entrega a los bancos:

> "Banco B, te presto 400€ de emergencia para que puedas devolver los depósitos. Banco A, te presto 200€."

- Los bancos pueden ahora pagar a los clientes que esperaban.

El profesor pregunta:

> "¿De dónde ha salido ese dinero? Lo acabo de crear. Literalmente lo he escrito en un papel. ¿Qué consecuencias tiene eso?"

---

**FASE 7 — Debate de cierre (5 min)**

Preguntas para la clase:
1. ¿Fue justo que los bancos prestaran el dinero de los depositantes?
2. ¿Fue justo que el Banco Central "imprimiera" dinero para rescatar a los bancos?
3. ¿Quién paga realmente ese rescate? (inflación → todos los ciudadanos)
4. ¿Y si no hubiera un Banco Central? ¿Qué pasaría?
5. ¿Entendéis ahora por qué alguien propuso un sistema donde no haga falta confiar en bancos?

> *"Esto es exactamente lo que pasó en 2008. Y exactamente por esto, tres meses después, Satoshi Nakamoto publicó el whitepaper de Bitcoin."*

[NOTA PROFESOR: Los números están calibrados para que la crisis sea inevitable con 6 clientes por banco. Si tienes más o menos alumnos, ajusta las cantidades proporcionalmente manteniendo la reserva fraccionaria al 10%. Lo importante es que los bancos NO puedan devolver todos los depósitos cuando llega la crisis. Ten preparados los folios para el "rescate" — el gesto de escribir dinero en un papel en blanco y entregarlo es muy visual y genera reacciones.]
