"""
Anade slides de respuestas al dia1_anexo.pptx del Modulo 4.
Abre el pptx existente y anade slides al final SIN tocar las existentes.
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import add_content_slide
from pptx import Presentation

PPTX_PATH = "/mnt/d/Dev/Fabric/docs/slides/Modulo 4/dia1_anexo.pptx"

prs = Presentation(PPTX_PATH)

# Respuestas al debate (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. Permisionado vs libre creacion: ¿ventaja o limitacion?",
    "2. Activos que se benefician de tokenizacion permissioned:",
    "3. UTXO o modelo de cuentas: ¿cual elegir?",
], subbullets={
    0: ["Depende del caso: en un consorcio empresarial es VENTAJA (evita spam y estafas).",
        "En un ecosistema abierto y con innovacion rapida es LIMITACION (frena la creatividad).",
        "Fabric esta pensado para entornos regulados donde se exige control y responsabilidad.",
        "El 99% de ICO fraudulentas de 2017-2018 no podrian haber ocurrido en Fabric."],
    1: ["Titulos de propiedad inmobiliaria (registros oficiales con multiples partes).",
        "Bonos y valores tokenizados entre bancos.",
        "Certificados de origen (vinos, diamantes, commodities).",
        "Puntos de fidelizacion entre empresas del mismo consorcio.",
        "Creditos de carbono con auditoria regulatoria.",
        "Cualquier activo con valor y necesidad de trazabilidad y auditoria."],
    2: ["Cuentas (ERC-20 like): mas simple, mas intuitivo, consulta de saldo directa.",
        "UTXO (Token SDK): mejor privacidad (tokens anonimos), mas complejo.",
        "Cuentas para: puntos de fidelizacion, creditos, casos con balances consultables.",
        "UTXO para: monedas corporativas con privacidad, tokens de valor sensible.",
        "Regla practica: empezar con cuentas (mas simple); migrar a UTXO si la privacidad es critica."],
})

# Respuestas al debate (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. ¿Pierde sentido la tokenizacion sin mercado secundario?",
    "5. ¿Como afecta la privacidad de Fabric al diseño de un token enterprise?",
], subbullets={
    0: ["Depende del caso de uso. Hay tres tipos:",
        "  a) Token que representa valor transferible libremente (SI necesita mercado).",
        "  b) Token que representa algo trazable (trazabilidad, certificaciones) — NO necesita mercado.",
        "  c) Token que representa un derecho (acceso, fidelizacion, voto) — NO necesita mercado.",
        "Muchas aplicaciones enterprise encajan en b) y c): el valor esta en la trazabilidad/control,",
        "  no en la especulacion o el trading.",
        "Ademas, nada impide crear mercados secundarios INTERNOS al consorcio (OTC, subastas)."],
    1: ["Canales: permiten separar tokens por grupo de orgs (no todos ven todos los tokens).",
        "Private Data Collections: ocultar importes y detalles entre partes del contrato.",
        "Zero-Knowledge Proofs (via Token SDK): probar propiedad sin revelar cantidad.",
        "Efecto practico: puedes tener un token cuyo propietario es publico pero el balance es privado.",
        "Tradeoff: mas privacidad = mas complejidad operativa.",
        "Regla: empezar simple (todo publico en el canal), anadir privacidad solo cuando sea critico."],
})

# Respuestas al repaso (parte 1)
add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Diferencia principal entre tokens Ethereum y Fabric:",
    "2. Tres formas de implementar tokens en Fabric:",
    "3. Modelo UTXO vs modelo de cuentas:",
    "4. Operaciones del Fabric Token SDK:",
], subbullets={
    0: ["Ethereum: cualquiera despliega tokens (ERC-20/721/1155), permissionless, identidad pseudonima.",
        "Fabric: solo entidades autorizadas (permissioned), identidad real con certificado X.509,",
        "  sin moneda nativa, flexibilidad total en el diseño del token."],
    1: ["Chaincode custom desde cero (maximo control, mas trabajo).",
        "Fabric Token SDK (modelo UTXO, privacidad avanzada, curva de aprendizaje).",
        "Fabric Samples token-erc-20 (modelo de cuentas tipo ERC-20, mas didactico)."],
    2: ["UTXO: cada token es un 'billete' unico e indivisible. Transferir = consumir unos y crear otros.",
        "  Ejemplo: Bitcoin — la privacidad es mayor porque no hay balance visible publico.",
        "Cuentas: balance numerico por usuario. Transferir = restar de uno, sumar a otro.",
        "  Ejemplo: Ethereum — mas intuitivo pero el balance queda expuesto."],
    3: ["Issue (crear): emitir nuevos tokens, equivalente al Mint.",
        "Transfer: enviar tokens de un propietario a otro.",
        "Redeem (destruir): equivalente al Burn.",
        "List: consultar los tokens propios.",
        "Soporta tokens fungibles y no fungibles con la misma infraestructura."],
})

# Respuestas al repaso (parte 2)
add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "5. ¿Por que Fabric no tiene moneda nativa?",
    "6. Ejemplo de token enterprise con sentido en Fabric:",
    "7. Ventaja de la privacidad de Fabric para tokens enterprise:",
], subbullets={
    0: ["Fabric es una plataforma permissioned: ya conoces a todos los participantes.",
        "No hace falta incentivar a mineros desconocidos (como ETH incentiva a los mineros Ethereum).",
        "Los costes operativos los asumen las orgs del consorcio directamente.",
        "Sin gas = sin mercado especulativo sobre la capacidad de red.",
        "Ventaja: las transacciones no tienen coste por-operacion para los usuarios."],
    1: ["Hotel + Cafeteria compartiendo puntos de fidelizacion (caso del Modulo 6).",
        "Bancos europeos tokenizando bonos corporativos (Santander, EIB).",
        "Trazabilidad de lotes alimentarios (Walmart Food Trust).",
        "Certificados de formacion entre universidades y empresas.",
        "Creditos de carbono verificables entre emisores y auditores."],
    2: ["Canales: segregar mercados internos (p.ej., tokens de fidelizacion por region).",
        "Private Data Collections: importes y terminos comerciales visibles solo entre partes.",
        "Cumplimiento GDPR: datos personales off-chain, solo hashes on-chain.",
        "Confidencialidad competitiva: los competidores en la red no ven los datos sensibles.",
        "Respeto a secretos comerciales: tarifas, margenes, clientes finales no expuestos."],
})

prs.save(PPTX_PATH)
print(f"Anadidas 4 slides al final de {PPTX_PATH}")
print(f"Total slides ahora: {len(prs.slides)}")
