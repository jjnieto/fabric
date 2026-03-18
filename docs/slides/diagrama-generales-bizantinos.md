# Generales Bizantinos — Diagramas con 4 generales

## Caso 1: El traidor es un teniente

El Comandante es leal y ordena **"Atacar"**. El Teniente 2 es el traidor.

### Ronda 1 — El Comandante envía la orden

```mermaid
graph TD
    C["🟢 COMANDANTE<br/>(leal)<br/>Orden: ATACAR"]
    L1["🟢 Teniente 1<br/>(leal)"]
    L2["🔴 Teniente 2<br/>(TRAIDOR)"]
    L3["🟢 Teniente 3<br/>(leal)"]

    C -->|"Atacar"| L1
    C -->|"Atacar"| L2
    C -->|"Atacar"| L3

    style C fill:#4CAF50,color:#fff
    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#f44336,color:#fff
    style L3 fill:#4CAF50,color:#fff
```

### Ronda 2 — Los tenientes intercambian lo que recibieron

```mermaid
graph LR
    L1["🟢 Teniente 1<br/>(leal)"]
    L2["🔴 Teniente 2<br/>(TRAIDOR)"]
    L3["🟢 Teniente 3<br/>(leal)"]

    L1 -->|"Yo recibí: Atacar"| L2
    L1 -->|"Yo recibí: Atacar"| L3

    L2 -->|"Yo recibí: RETIRARSE ❌"| L1
    L2 -->|"Yo recibí: RETIRARSE ❌"| L3

    L3 -->|"Yo recibí: Atacar"| L1
    L3 -->|"Yo recibí: Atacar"| L2

    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#f44336,color:#fff
    style L3 fill:#4CAF50,color:#fff
```

### Votación por mayoría

```mermaid
graph TD
    subgraph T1["Teniente 1 (leal) — DECIDE"]
        T1a["Del Comandante: Atacar"]
        T1b["Del Teniente 2: Retirarse"]
        T1c["Del Teniente 3: Atacar"]
        T1r["MAYORÍA → ✅ ATACAR<br/>(2 Atacar vs 1 Retirarse)"]
        T1a --> T1r
        T1b --> T1r
        T1c --> T1r
    end

    subgraph T3["Teniente 3 (leal) — DECIDE"]
        T3a["Del Comandante: Atacar"]
        T3b["Del Teniente 1: Atacar"]
        T3c["Del Teniente 2: Retirarse"]
        T3r["MAYORÍA → ✅ ATACAR<br/>(2 Atacar vs 1 Retirarse)"]
        T3a --> T3r
        T3b --> T3r
        T3c --> T3r
    end

    style T1r fill:#4CAF50,color:#fff
    style T3r fill:#4CAF50,color:#fff
```

**Resultado: Ambos tenientes leales deciden ATACAR. Consenso alcanzado.**

---

## Caso 2: El traidor es el Comandante

El Comandante es el traidor. Envía órdenes contradictorias. Los 3 tenientes son leales.

### Ronda 1 — El Comandante (traidor) envía órdenes distintas

```mermaid
graph TD
    C["🔴 COMANDANTE<br/>(TRAIDOR)"]
    L1["🟢 Teniente 1<br/>(leal)"]
    L2["🟢 Teniente 2<br/>(leal)"]
    L3["🟢 Teniente 3<br/>(leal)"]

    C -->|"Atacar"| L1
    C -->|"RETIRARSE ❌"| L2
    C -->|"Atacar"| L3

    style C fill:#f44336,color:#fff
    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#4CAF50,color:#fff
    style L3 fill:#4CAF50,color:#fff
```

### Ronda 2 — Los tenientes intercambian lo que recibieron (todos dicen la verdad)

```mermaid
graph LR
    L1["🟢 Teniente 1"]
    L2["🟢 Teniente 2"]
    L3["🟢 Teniente 3"]

    L1 -->|"Yo recibí: Atacar"| L2
    L1 -->|"Yo recibí: Atacar"| L3

    L2 -->|"Yo recibí: Retirarse"| L1
    L2 -->|"Yo recibí: Retirarse"| L3

    L3 -->|"Yo recibí: Atacar"| L1
    L3 -->|"Yo recibí: Atacar"| L2

    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#4CAF50,color:#fff
    style L3 fill:#4CAF50,color:#fff
```

### Votación por mayoría

```mermaid
graph TD
    subgraph T1["Teniente 1 (leal) — DECIDE"]
        T1a["Del Comandante: Atacar"]
        T1b["Del Teniente 2: Retirarse"]
        T1c["Del Teniente 3: Atacar"]
        T1r["MAYORÍA → ✅ ATACAR<br/>(2 Atacar vs 1 Retirarse)"]
        T1a --> T1r
        T1b --> T1r
        T1c --> T1r
    end

    subgraph T2["Teniente 2 (leal) — DECIDE"]
        T2a["Del Comandante: Retirarse"]
        T2b["Del Teniente 1: Atacar"]
        T2c["Del Teniente 3: Atacar"]
        T2r["MAYORÍA → ✅ ATACAR<br/>(2 Atacar vs 1 Retirarse)"]
        T2a --> T2r
        T2b --> T2r
        T2c --> T2r
    end

    subgraph T3["Teniente 3 (leal) — DECIDE"]
        T3a["Del Comandante: Atacar"]
        T3b["Del Teniente 1: Atacar"]
        T3c["Del Teniente 2: Retirarse"]
        T3r["MAYORÍA → ✅ ATACAR<br/>(2 Atacar vs 1 Retirarse)"]
        T3a --> T3r
        T3b --> T3r
        T3c --> T3r
    end

    style T1r fill:#4CAF50,color:#fff
    style T2r fill:#4CAF50,color:#fff
    style T3r fill:#4CAF50,color:#fff
```

**Resultado: Los 3 tenientes leales deciden ATACAR. Consenso alcanzado.**

El Teniente 2 recibió "Retirarse" del comandante traidor, pero al contrastar con los otros dos tenientes, descubre que la mayoría dice "Atacar" → se alinea con la mayoría.

---

## Caso 3 (fallo): Solo 3 generales con 1 traidor

Con 3 generales no se puede resolver. Ejemplo: Comandante traidor.

### Ronda 1

```mermaid
graph TD
    C["🔴 COMANDANTE<br/>(TRAIDOR)"]
    L1["🟢 Teniente 1<br/>(leal)"]
    L2["🟢 Teniente 2<br/>(leal)"]

    C -->|"Atacar"| L1
    C -->|"RETIRARSE ❌"| L2

    style C fill:#f44336,color:#fff
    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#4CAF50,color:#fff
```

### Ronda 2

```mermaid
graph LR
    L1["🟢 Teniente 1"]
    L2["🟢 Teniente 2"]

    L1 -->|"Yo recibí: Atacar"| L2
    L2 -->|"Yo recibí: Retirarse"| L1

    style L1 fill:#4CAF50,color:#fff
    style L2 fill:#4CAF50,color:#fff
```

### Votación

```mermaid
graph TD
    subgraph T1["Teniente 1 — DECIDE"]
        T1a["Del Comandante: Atacar"]
        T1b["Del Teniente 2: Retirarse"]
        T1r["EMPATE ❌<br/>(1 Atacar vs 1 Retirarse)<br/>NO HAY MAYORÍA"]
        T1a --> T1r
        T1b --> T1r
    end

    subgraph T2["Teniente 2 — DECIDE"]
        T2a["Del Comandante: Retirarse"]
        T2b["Del Teniente 1: Atacar"]
        T2r["EMPATE ❌<br/>(1 Atacar vs 1 Retirarse)<br/>NO HAY MAYORÍA"]
        T2a --> T2r
        T2b --> T2r
    end

    style T1r fill:#FF9800,color:#fff
    style T2r fill:#FF9800,color:#fff
```

**Resultado: Empate. Cada teniente tiene 1 voto de cada tipo. No pueden distinguir quién miente. NO hay consenso posible.**

---

## Resumen visual de la regla

```mermaid
graph LR
    subgraph FALLA["❌ NO FUNCIONA"]
        F1["3 generales<br/>1 traidor<br/>(33% traidores)"]
    end

    subgraph FUNCIONA["✅ FUNCIONA"]
        F2["4 generales<br/>1 traidor<br/>(25% traidores)"]
        F3["7 generales<br/>2 traidores<br/>(28% traidores)"]
        F4["10 generales<br/>3 traidores<br/>(30% traidores)"]
    end

    R["REGLA: n ≥ 3f + 1<br/>Máximo 1/3 de traidores"]

    style FALLA fill:#ffcdd2
    style FUNCIONA fill:#c8e6c9
    style R fill:#2196F3,color:#fff
```

**Fórmula:** Para tolerar **f** traidores, necesitas al menos **3f + 1** generales.

| Traidores (f) | Generales necesarios (3f+1) | Leales mínimos |
|---|---|---|
| 1 | 4 | 3 |
| 2 | 7 | 5 |
| 3 | 10 | 7 |
| 10 | 31 | 21 |
