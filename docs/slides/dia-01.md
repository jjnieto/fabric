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

### El banco prudente y el banco temerario (30-40 min)

Simulación del sistema bancario con dos bancos que operan de forma muy diferente. Cuando llega la crisis, uno sobrevive y el otro no.

**Preparación (3 min)**

| Rol | Quién |
|-----|-------|
| **Banco Central** | El profesor |
| **Banco Prudente** | 1-2 alumnos voluntarios |
| **Banco Temerario** | 1-2 alumnos voluntarios |
| **Clientes** | El resto de la clase, repartidos entre ambos bancos |

Dibujar en la pizarra dos balances lado a lado:

```
BANCO PRUDENTE                   BANCO TEMERARIO
─────────────────────            ─────────────────────
DEPÓSITOS:   ___€                DEPÓSITOS:   ___€
RESERVAS:    ___€                RESERVAS:    ___€
PRÉSTAMOS:   ___€                PRÉSTAMOS:   ___€
```

Dar a cada alumno-cliente un papelito que dice "100€".

---

**FASE 1 — Los depósitos (3 min)**

El profesor:

> "Soy el Banco Central. He emitido dinero y cada ciudadano tiene 100€. Necesitáis depositarlo en un banco. Elegid libremente a cuál vais."

Los clientes se reparten y depositan. Los bancos anotan. Supongamos que quedan ~6 clientes por banco:

```
BANCO PRUDENTE                   BANCO TEMERARIO
─────────────────────            ─────────────────────
DEPÓSITOS:   600€                DEPÓSITOS:   600€
RESERVAS:    600€                RESERVAS:    600€
PRÉSTAMOS:     0€                PRÉSTAMOS:     0€
```

> "Ambos bancos tienen licencia para operar con reserva fraccionaria al 10%. Solo necesitáis guardar el 10% de los depósitos. El resto lo podéis prestar para ganar intereses. Cuanto más prestéis, más ganáis."

---

**FASE 2 — Cada banco decide su estrategia (5 min)**

El profesor presenta a los dos bancos una lista de solicitudes de crédito. **Los bancos deciden cuáles aceptan.**

| Solicitud | Importe | Perfil del solicitante |
|-----------|---------|----------------------|
| Familia García | 100€ | Matrimonio con empleo estable, quieren reformar la cocina |
| Restaurante "El Buen Gusto" | 150€ | Negocio con 10 años de antigüedad, quiere ampliar terraza |
| StartUp "CryptoMoon" | 200€ | Empresa de 3 meses, sin ingresos, promete un 500% de retorno |
| Familia López | 100€ | Matrimonio con empleo estable, quieren comprar un coche |
| Inmobiliaria "Pisos Fácil" | 250€ | Quiere comprar pisos para revender, lleva 1 año operando |
| Juan, estudiante | 50€ | Sin ingresos, quiere irse de vacaciones |
| Clínica dental | 100€ | Negocio consolidado, necesita nuevo equipo |
| Constructora "Ladrillo de Oro" | 300€ | Quiere construir 50 pisos de lujo en una zona sin demanda |

El profesor dice a cada banco por separado:

> **Al Banco Prudente** (en voz baja): "Vuestro comité de riesgos es estricto. Solo aprobáis créditos a solicitantes con capacidad demostrada de pago. Elegid los que os parezcan seguros."

> **Al Banco Temerario** (en voz baja): "Vuestro objetivo es maximizar beneficios este trimestre. El bonus del director depende del volumen de créditos concedidos. Cuanto más prestéis, más cobráis."

Los bancos eligen y anotan en la pizarra. **Resultado esperado:**

```
BANCO PRUDENTE                   BANCO TEMERARIO
─────────────────────            ─────────────────────
DEPÓSITOS:   600€                DEPÓSITOS:   600€
RESERVAS:    250€                RESERVAS:     60€
PRÉSTAMOS:   350€                PRÉSTAMOS:   540€
  - Fam. García: 100€             - CryptoMoon: 200€
  - Restaurante: 150€             - Pisos Fácil: 250€
  - Fam. López: 100€              - Juan: 50€
                                   - Ladrillo Oro: 300€
                                   (↑ supera lo permitido,
                                    pero "ya se arreglará")
```

[NOTA PROFESOR: No hace falta que los números cuadren exactamente. Lo importante es el contraste: el prudente guarda reservas de sobra y presta a perfiles sólidos; el temerario presta casi todo, incluso a perfiles de alto riesgo. Si el Banco Temerario no es lo bastante agresivo, empújalos: "¿Seguro que no queréis aprobar alguno más? El bonus del director es muy jugoso…"]

---

**FASE 3 — Los buenos tiempos (2 min)**

El profesor narra:

> "Pasan unos meses. La economía va bien. Los préstamos generan intereses. El Banco Temerario presume de beneficios récord en la prensa. El Banco Prudente gana menos, pero duerme tranquilo."

> "El director del Banco Temerario se compra un Porsche. El del Banco Prudente se compra un Seat."

(Risas. Es intencional.)

---

**FASE 4 — La crisis (10 min)**

El profesor cambia de tono:

> "ÚLTIMA HORA: Llega una recesión económica."

Va leyendo los desenlaces uno a uno:

> "**CryptoMoon** ha quebrado. Los 200€ que le prestó el Banco Temerario son irrecuperables."

Banco Temerario tacha 200€ de sus préstamos. Eso es dinero perdido.

> "**Pisos Fácil** no puede vender los pisos que compró. No puede devolver los 250€."

Banco Temerario tacha otros 250€.

> "**Ladrillo de Oro** ha parado la obra. Los 300€ están congelados. Puede que devuelvan algo… o puede que no."

> "**Juan** no devuelve los 50€. Se fue de vacaciones y ahora está en paro."

El profesor actualiza la pizarra:

```
BANCO PRUDENTE                   BANCO TEMERARIO
─────────────────────            ─────────────────────
DEPÓSITOS:   600€                DEPÓSITOS:   600€
RESERVAS:    250€                RESERVAS:     60€
PRÉSTAMOS:   350€ (sanos)        PRÉSTAMOS:   540€
                                   - Perdidos: 500€
                                   - Dudosos: 300€
                                 AGUJERO:    ~500€
```

> "Mientras tanto, los clientes del Banco Prudente están tranquilos. Sus préstamos (familias con empleo, negocios consolidados) siguen pagando sin problemas."

Ahora el profesor deja caer la bomba:

> "Un periódico publica que el Banco Temerario tiene un agujero de 500€ y solo 60€ en caja. Los clientes del Banco Temerario, empezáis a poneros nerviosos. ¿Queréis retirar vuestro dinero?"

Los clientes del Banco Temerario hacen cola. El primero retira 60€. **El segundo ya no puede.**

> "El rumor se extiende. Algunos clientes del Banco Prudente también se asustan. ¿Y si les pasa lo mismo?"

Uno o dos clientes del Banco Prudente piden retirar. **El Banco Prudente puede pagar sin problema** (tiene 250€ en reservas).

> "¿Veis la diferencia?"

---

**FASE 5 — El Banco Central al rescate (5 min)**

El profesor coge folios en blanco. Escribe "500€" en uno y lo entrega al Banco Temerario:

> "Soy el Banco Central. No puedo dejar que el sistema colapse, porque si el Banco Temerario cae, sus clientes pierden todo y la desconfianza se contagia. Así que le presto 500€ de emergencia."

El profesor escribe el dinero delante de todos — literalmente lo crea de la nada.

> "Pregunta: ¿De dónde sale este dinero?"

Dejar que contesten. Luego:

> "Lo acabo de inventar. Es dinero nuevo que no existía. ¿Quién creéis que paga las consecuencias de que haya más dinero en circulación sin que haya más riqueza real?"

(Respuesta: todos, vía inflación.)

> "Y ahora la pregunta del millón: **¿Es justo rescatar al banco que se portó mal con el dinero de todos, mientras el banco que fue prudente no recibe nada?**"

---

**FASE 6 — Debate de cierre (5 min)**

1. ¿Por qué el Banco Temerario prestó tanto? (Incentivos perversos: bonus por volumen)
2. ¿Debería haber un regulador que limite cuánto puede prestar un banco? (Spoiler: lo hay, pero en 2008 falló)
3. ¿Es justo el rescate? ¿Y si dejamos caer al banco? (Riesgo sistémico)
4. Los clientes del Banco Temerario, ¿tenían manera de saber que su banco era imprudente? (Opacidad)
5. ¿Y si existiera un sistema donde **no haga falta confiar** en que un banco sea prudente?

> *"Esto es exactamente lo que pasó en 2008. Bancos prestando a lo loco, crisis, rescates con dinero público. Tres meses después del colapso, Satoshi Nakamoto publicó el whitepaper de Bitcoin."*

[NOTA PROFESOR: La clave de esta versión es el contraste entre los dos bancos. No necesitas microgestionar cada préstamo — deja que los propios alumnos-banqueros decidan, pero empuja al Temerario a ser agresivo. Si el Temerario es demasiado prudente por su cuenta, recuérdale: "Tu bonus depende del volumen". La escena del Banco Central escribiendo dinero en un folio en blanco es el momento más impactante — hazlo teatral.]
