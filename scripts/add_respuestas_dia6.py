"""
Anade slides de respuestas al dia 6 del Modulo 4.
Abre el pptx existente y anade slides al final SIN tocar las existentes.
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import add_content_slide
from pptx import Presentation

PPTX_PATH = "/mnt/d/Dev/Fabric/docs/slides/Modulo 4/dia_6.pptx"

prs = Presentation(PPTX_PATH)

# Respuestas al debate de cierre (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. Lo mas complejo / lo mas util del modulo:",
    "2. Aplicacion real en vuestro sector:",
    "3. ¿Que echais en falta en Fabric vs Ethereum (y al reves)?",
], subbullets={
    0: ["Complejo: el lifecycle de chaincodes (4 pasos) y el determinismo (errores silenciosos).",
        "Util: la capacidad de razonar sobre permisos antes de tocar codigo (MSPID/ABAC).",
        "No hay respuesta unica — depende del background (EVM vs Fabric).",
        "La mayoria coincide: los conceptos son simples, la operacion es donde esta la dificultad."],
    1: ["Depende del sector: trazabilidad, KYC compartido, tokenizacion B2B, registros regulados.",
        "Regla de oro: hay multiples orgs con desconfianza mutua + necesidad de auditoria.",
        "Si un solo actor es suficiente, una base de datos normal es mejor opcion."],
    2: ["Lo que Fabric NO tiene vs Ethereum: ecosistema DeFi, liquidez, interoperabilidad publica,",
        "  wallets universales, stablecoins establecidas, herramientas DevTools maduras.",
        "Lo que Fabric SI tiene vs Ethereum: privacidad nativa, rendimiento, gobernanza controlada,",
        "  identidades reales, integracion con sistemas legacy, cumplimiento regulatorio.",
        "Conclusion: son para casos de uso distintos, no compiten directamente."],
})

# Respuestas al debate de cierre (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. Arquitectura para un proyecto real manana:",
    "5. Papel de la IA en el desarrollo de chaincodes:",
], subbullets={
    0: ["Empezar pequeno: MVP con 2 orgs, 1 canal, 1 chaincode simple.",
        "Cryptogen para desarrollo, Fabric CA para produccion.",
        "CouchDB si necesitas rich queries (la mayoria de casos).",
        "Gateway SDK en el cliente (ya no se usa el SDK antiguo).",
        "Monitorizacion desde el dia 1: Prometheus + Grafana.",
        "Gobernanza clara ANTES de la tecnologia: ¿quien decide? ¿quien paga?"],
    1: ["Generacion de chaincode basico desde especificacion (prompts -> codigo).",
        "Auditoria automatica: detectar errores de determinismo, validaciones faltantes.",
        "Tests generados automaticamente a partir del codigo.",
        "Documentacion y diagramas generados.",
        "Riesgos: la IA no entiende el contexto de negocio, puede generar codigo plausible pero",
        "  incorrecto. Siempre revisar manualmente, especialmente validaciones y control de acceso."],
})

# Respuestas al repaso (parte 1)
add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Tokenizacion Fabric vs Ethereum:",
    "2. Tres formas de implementar tokens en Fabric:",
    "3. Anatomia de un chaincode:",
    "4. CRUD + modelado de datos:",
    "5. Control de acceso (MSPID + ABAC):",
], subbullets={
    0: ["Ethereum: ERC-20/721/1155 estandar, publico, anyone-can-deploy.",
        "Fabric: sin estandar (aun), permissioned, identidades con certificado."],
    1: ["Chaincode custom desde cero (maximo control).",
        "Fabric Token SDK (UTXO, mejor privacidad).",
        "fabric-samples/token-erc-20 (modelo de cuentas, mas simple)."],
    2: ["Struct con contractapi.Contract embebido (Go) o clase que extiende Contract (Node.js).",
        "Funciones reciben ctx: TransactionContextInterface (da acceso al Stub e Identity).",
        "Stub API: GetState, PutState, DelState, GetQueryResult, SetEvent, etc."],
    3: ["CRUD = Create, Read, Update, Delete (logico).",
        "Usar docType en JSON para queries CouchDB.",
        "Composite keys cuando necesitas indices secundarios.",
        "Paginar queries grandes con GetStateByRangeWithPagination."],
    4: ["MSPID: que organizacion llama (HotelMSP, CafeteriaMSP).",
        "ABAC: atributos custom del certificado X.509 (role=minter, etc.).",
        "MSPID para separar orgs, ABAC para separar roles dentro de una org."],
})

# Respuestas al repaso (parte 2)
add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "6. Private Data Collections:",
    "7. Tokens fungibles vs NFT en Fabric:",
    "8. Seguridad (determinismo, MVCC, checklist):",
    "9. Gateway SDK:",
    "10. Testing con mocks:",
], subbullets={
    0: ["Compartir datos entre un subconjunto de orgs (no todo el canal).",
        "Definidas en collections_config.json: nombre, policy, blockToLive.",
        "Datos reales en la BD privada del peer, hash en el ledger publico."],
    1: ["Fungible: balance por cuenta, tipo ERC-20.",
        "NFT: cada token unico con tokenID y metadata, composite keys por owner."],
    2: ["Determinismo: no usar time.Now, rand, http, map iteration.",
        "MVCC: conflicto cuando 2 transacciones tocan las mismas keys.",
        "Checklist: verificar identidad, validar inputs, paginar queries, no loguear secretos."],
    3: ["Libreria cliente para conectar apps con la red Fabric.",
        "Flujo: wallet -> gateway -> peer -> chaincode.",
        "submitTransaction (escritura) vs evaluateTransaction (lectura)."],
    4: ["Mockear ctx, stub e clientIdentity con sinon/testify.",
        "Configurar respuestas esperadas: getState.resolves(...), etc.",
        "Verificar que se llamaron las funciones correctas (putState, setEvent)."],
})

prs.save(PPTX_PATH)
print(f"Anadidas 4 slides al final de {PPTX_PATH}")
print(f"Total slides ahora: {len(prs.slides)}")
