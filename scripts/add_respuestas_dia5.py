"""
Anade slides de respuestas al dia 5 del Modulo 4.
Abre el pptx existente y anade slides al final SIN tocar las existentes.
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import add_content_slide
from pptx import Presentation

PPTX_PATH = "/mnt/d/Dev/Fabric/docs/slides/Modulo 4/dia_5.pptx"

# IMPORTANTE: abrir presentacion existente, NO regenerar
prs = Presentation(PPTX_PATH)

# Respuestas al debate (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. ¿Quien audita los chaincodes en un consorcio?",
    "2. Bug de determinismo que no falla visiblemente:",
    "3. ¿ABAC suficiente o hace falta RBAC con World State?",
], subbullets={
    0: ["Opcion A: cada org audita por su cuenta (conflicto de intereses).",
        "Opcion B: auditor externo independiente (mas objetivo, mas caro).",
        "Opcion C: mixto — codigo open source + auditoria por org + auditor externo.",
        "En la practica: los consorcios serios pagan una auditoria externa antes de cada release."],
    1: ["Monitorizar tasa de transacciones invalidas (MVCC_READ_CONFLICT, etc.) en metricas.",
        "Alertas cuando esa tasa sube sin causa clara.",
        "Tests de integracion que ejecuten el chaincode en PARALELO en varios peers.",
        "Revisar logs de los peers: buscan 'invalid transactions' en el commit.",
        "Mejor: prevenir en CI con linters que detecten time.Now, rand, map iteration, etc."],
    2: ["ABAC (atributos en cert X.509) es simple pero rigido: el atributo queda fijado al emitir.",
        "RBAC con tabla en World State es flexible: puedes cambiar permisos sin reenroll.",
        "Combinar: ABAC para roles estables (minter, regulator), RBAC para permisos granulares.",
        "Cuidado con RBAC: los permisos son datos normales, necesitan proteccion tambien."],
})

# Respuestas al debate (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. Protecciones si un endorsing peer es comprometido:",
    "5. Rotacion de certificados sin perder acceso:",
], subbullets={
    0: ["La politica de endorsement exige firma de VARIAS orgs — un solo peer comprometido no basta.",
        "El atacante puede emitir endorsements falsos, pero si no hay mayoria, no se commitean.",
        "Detectar: los otros peers ven las propuestas y pueden detectar comportamiento anomalo.",
        "Mitigar: revocar el certificado del peer comprometido y generar uno nuevo.",
        "Proteger los orderers: si hay 3 orderers y 2 estan comprometidos, el atacante controla el bloque."],
    1: ["Los certificados los usa cada org localmente — no afectan a los datos del World State.",
        "Al renovar (reenroll), el nuevo certificado queda asociado al mismo MSPID.",
        "Los datos siguen siendo accesibles porque el control de acceso es por MSPID, no por cert concreto.",
        "El peer/cliente solo tiene que conocer el nuevo cert y la nueva clave.",
        "Proceso: Fabric CA emite nuevo cert -> copiar al peer -> reiniciar peer -> listo."],
})

# Respuestas al repaso (parte 1)
add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Politica de endorsement:",
    "2. State-based endorsement:",
    "3. ABAC en Fabric:",
    "4. 5 errores de determinismo mas comunes:",
], subbullets={
    0: ["Regla que define que organizaciones deben firmar una transaccion para que sea valida.",
        "Ejemplo: AND('Org1MSP.peer','Org2MSP.peer'), OR(...), OutOf(2, ...), MAJORITY.",
        "Se define en approveformyorg / commit (nivel chaincode) o state-based (nivel key)."],
    1: ["Cambiar la politica de endorsement para una KEY concreta del World State.",
        "Permite que diferentes activos tengan diferentes requisitos (ej: alto valor = 3 orgs).",
        "Se gestiona con ctx.GetStub().SetStateValidationParameter(key, policy)."],
    2: ["Attribute-Based Access Control: verificar atributos custom del cert X.509.",
        "Atributos se anaden en Fabric CA al registrar/enrollar.",
        "En el chaincode: ctx.GetClientIdentity().AssertAttributeValue('role', 'admin')."],
    3: ["1) time.Now() en vez de GetTxTimestamp()",
        "2) Iterar mapas sin ordenar",
        "3) Llamadas HTTP/gRPC/filesystem externas",
        "4) math/rand (numeros aleatorios)",
        "5) Variables globales mutables"],
})

# Respuestas al repaso (parte 2)
add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "5. Conflicto MVCC:",
    "6. Actualizar un chaincode:",
    "7. Migrar datos entre versiones:",
    "8. 3 items del checklist de seguridad:",
], subbullets={
    0: ["Multi-Version Concurrency Control.",
        "Ocurre cuando dos transacciones concurrentes modifican las mismas keys.",
        "Fabric verifica en el commit que las versiones leidas siguen siendo las mismas.",
        "Si han cambiado -> transaccion invalidada (MVCC_READ_CONFLICT).",
        "Mitigar: evitar queries amplias en transacciones de escritura."],
    1: ["Empaquetar nueva version con sequence incrementado.",
        "Install en cada peer + approveformyorg en cada org + commit.",
        "El World State se preserva automaticamente entre versiones."],
    2: ["Campos nuevos opcionales (retrocompatibilidad).",
        "Migracion lazy: al leer un dato viejo, aplicar defaults y guardar.",
        "Migracion en bloque: funcion admin que recorre el World State."],
    3: ["Verificar identidad del caller (GetMSPID, ABAC)",
        "No usar time.Now, rand, http, map iteration (determinismo)",
        "Validar inputs (tipos, rangos, longitud)",
        "No loguear datos sensibles",
        "Paginar queries, no devolver miles de registros"],
})

prs.save(PPTX_PATH)
print(f"Anadidas 4 slides al final de {PPTX_PATH}")
print(f"Total slides ahora: {len(prs.slides)}")
