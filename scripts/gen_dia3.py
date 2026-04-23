import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

add_title_slide(prs, "Desarrollo de Chaincodes:\nLogica de Negocio",
    "Dia 3 - Validaciones, control de acceso, Private Data y eventos")

add_review_slide(prs, "Repaso del dia anterior", [
    "¿Que operaciones ofrece la Stub API?",
    "¿Para que sirven las Composite Keys?",
    "¿Cuando usarias CouchDB en vez de LevelDB?",
    "¿Que es una rich query?",
])

# Treasure Hunt
add_special_slide(prs, "TREASURE HUNT", "Walmart y la trazabilidad alimentaria", [
    "En 2018, Walmart implemento un sistema de trazabilidad basado en Hyperledger Fabric.",
    "El objetivo: rastrear el origen de productos frescos (especialmente mangos y cerdo).",
    "Antes: rastrear un mango desde la tienda hasta la granja tardaba 7 dias.",
    "Con Fabric: el mismo rastreo tardo 2.2 segundos.",
    "",
    "Mision: Investigar y responder:",
    "  1. ¿Que empresa de tecnologia colaboro con Walmart en este proyecto?",
    "  2. ¿Cuantos proveedores de hoja verde tiene Walmart en este sistema?",
    "  3. ¿Por que eligieron Fabric y no Ethereum para este caso?",
    "  Pista: La empresa colaboradora creo una plataforma que se llamaba 'Food Trust'.",
])

add_content_slide(prs, "Validaciones en el chaincode", [
    "El chaincode es la ultima linea de defensa antes de escribir en el ledger",
    "Toda validacion critica debe estar en el chaincode, no solo en la app cliente",
    "Tipos de validaciones:",
],
subbullets={
    2: ["Existencia: ¿el activo existe o no antes de operar?",
        "Permisos: ¿quien invoca tiene derecho a hacer esta operacion?",
        "Estado: ¿el activo esta en un estado valido para esta transicion?",
        "Formato: ¿los datos de entrada son validos (tipos, rangos, longitud)?",
        "Reglas de negocio: ¿se cumplen las condiciones de la logica de negocio?"],
})

add_content_slide(prs, "Control de acceso: GetClientIdentity", [
    "Cada invocacion lleva la identidad X.509 del cliente",
    "ctx.GetClientIdentity() expone:",
    "Patron comun: verificar MSPID al inicio de cada funcion",
    "Mas granular: verificar atributos custom del certificado (ABAC)",
],
subbullets={
    1: ["GetID() - identidad completa (CN + emisor del cert)",
        "GetMSPID() - organizacion a la que pertenece (Org1MSP, Org2MSP...)",
        "GetAttributeValue(attrName) - atributos custom del cert X.509",
        "AssertAttributeValue(attrName, value) - verificar atributo directamente"],
})

add_code_slide(prs, "Control de acceso por organizacion", """
func (s *SmartContract) TransferProperty(ctx contractapi.TransactionContextInterface,
    id string, newOwner string) error {

    // Leer propiedad
    property, err := s.ReadProperty(ctx, id)
    if err != nil {
        return err
    }

    // Verificar: solo el propietario actual puede transferir
    clientMSP, _ := ctx.GetClientIdentity().GetMSPID()
    if property.Owner != clientMSP {
        return fmt.Errorf("solo el propietario actual (%s) puede transferir",
            property.Owner)
    }

    // Verificar: la propiedad debe estar en estado 'active'
    if property.Status != "active" {
        return fmt.Errorf("la propiedad esta en estado '%s', no se puede transferir",
            property.Status)
    }

    // Transferir
    property.Owner = newOwner
    property.Status = "active"
    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState(id, propertyJSON)
}""", language="go", subtitle="Verificar MSPID y estado antes de operar")

add_code_slide(prs, "Control de acceso por atributo (ABAC)", """
// Solo un usuario con rol "registrador" puede registrar propiedades
func (s *SmartContract) RegisterProperty(ctx contractapi.TransactionContextInterface,
    id string, address string, owner string) error {

    // Verificar atributo "role" en el certificado X.509
    err := ctx.GetClientIdentity().AssertAttributeValue("role", "registrador")
    if err != nil {
        return fmt.Errorf("solo registradores pueden crear propiedades: %v", err)
    }

    // El atributo se anade al certificado durante el enrollment con Fabric CA:
    //   fabric-ca-client enroll ... --enrollment.attrs "role=registrador"

    property := Property{
        DocType: "property", ID: id, Address: address,
        Owner: owner, Status: "active",
    }
    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState(id, propertyJSON)
}""", language="go", subtitle="Atributos custom en certificados X.509")

# Maquina de estados
add_content_slide(prs, "Logica de negocio: maquina de estados", [
    "Muchos activos del mundo real siguen un ciclo de vida con estados",
    "El chaincode debe validar que las transiciones son correctas",
    "Ejemplo: estados de una propiedad inmobiliaria",
    "Cada transicion requiere permisos distintos:",
],
subbullets={
    2: ["active -> transferring (propietario inicia transferencia)",
        "transferring -> active (registrador confirma la transferencia)",
        "transferring -> active (propietario cancela la transferencia)",
        "active -> blocked (autoridad judicial bloquea)",
        "blocked -> active (autoridad judicial desbloquea)"],
    3: ["active -> transferring: requiere Owner",
        "transferring -> active (confirmar): requiere role=registrador",
        "active -> blocked: requiere role=autoridad_judicial"],
})

add_image_placeholder(prs, "Diagrama: estados de una propiedad",
    "[Diagrama de estados: active <-> transferring, active <-> blocked]",
    "State machine diagram for a property asset: three states (active in green, transferring in yellow, blocked in red) connected by labeled arrows showing transitions and required roles. Clean flat design, teal and white color scheme, clear labels on each transition.")

add_code_slide(prs, "Maquina de estados en codigo", """
// Mapa de transiciones validas
var validTransitions = map[string][]string{
    "active":       {"transferring", "blocked"},
    "transferring": {"active"},
    "blocked":      {"active"},
}

func isValidTransition(currentStatus, newStatus string) bool {
    allowed, exists := validTransitions[currentStatus]
    if !exists {
        return false
    }
    for _, s := range allowed {
        if s == newStatus {
            return true
        }
    }
    return false
}

// Uso en una funcion del chaincode:
if !isValidTransition(property.Status, newStatus) {
    return fmt.Errorf("transicion no permitida: %s -> %s",
        property.Status, newStatus)
}""", language="go")

# Private Data Collections
add_section_slide(prs, "Private Data Collections", "Datos confidenciales entre subconjuntos de organizaciones")

add_content_slide(prs, "Private Data Collections: concepto", [
    "No todos los datos deben ser visibles para todas las organizaciones del canal",
    "Private Data Collections permiten compartir datos solo entre orgs seleccionadas",
    "En el ledger publico solo se guarda un hash de los datos privados",
    "Los datos reales se almacenan en una base de datos privada en los peers autorizados",
    "Ejemplo: en una transferencia de propiedad,",
],
subbullets={
    4: ["El precio de venta solo lo ven comprador y vendedor",
        "El resto de organizaciones ven que hubo una transferencia, pero no el precio",
        "El hash en el ledger publico garantiza la integridad"],
})

add_code_slide(prs, "Private Data: configuracion", """
// collections_config.json - se pasa al desplegar el chaincode
[
    {
        "name": "privatePropertyDetails",
        "policy": "OR('Org1MSP.member', 'Org2MSP.member')",
        "requiredPeerCount": 1,
        "maxPeerCount": 2,
        "blockToLive": 0,
        "memberOnlyRead": true,
        "memberOnlyWrite": true
    },
    {
        "name": "priceAgreement",
        "policy": "AND('Org1MSP.member', 'Org2MSP.member')",
        "requiredPeerCount": 1,
        "maxPeerCount": 2,
        "blockToLive": 100,
        "memberOnlyRead": true
    }
]""", language="json", subtitle="Definir quien puede leer/escribir cada coleccion")

add_code_slide(prs, "Private Data: leer y escribir", """
// Escribir en una Private Data Collection
func (s *SmartContract) SetPrivatePrice(ctx contractapi.TransactionContextInterface,
    propertyID string) error {

    // Los datos privados vienen en transient data (no en el ledger)
    transientMap, err := ctx.GetStub().GetTransient()
    if err != nil {
        return err
    }
    priceData := transientMap["price"]

    // Guardar en la coleccion privada
    return ctx.GetStub().PutPrivateData("priceAgreement",
        propertyID, priceData)
}

// Leer de una Private Data Collection
func (s *SmartContract) GetPrivatePrice(ctx contractapi.TransactionContextInterface,
    propertyID string) (string, error) {

    priceData, err := ctx.GetStub().GetPrivateData("priceAgreement",
        propertyID)
    if err != nil {
        return "", err
    }
    return string(priceData), nil
}""", language="go", subtitle="Transient data + PutPrivateData / GetPrivateData")

# Eventos
add_content_slide(prs, "Eventos de chaincode", [
    "Los chaincodes pueden emitir eventos que las aplicaciones cliente reciben",
    "Utiles para: notificaciones, integraciones, audit logs",
    "Se emiten con ctx.GetStub().SetEvent(name, payload)",
    "Solo se emite UN evento por transaccion (el ultimo SetEvent gana)",
    "El cliente se suscribe con el Gateway SDK:",
],
subbullets={
    4: ["contract.RegisterEvent() en Go",
        "network.addBlockListener() / contract.addContractListener() en Node.js"],
})

add_code_slide(prs, "Eventos: ejemplo completo", """
// En el chaincode: emitir evento al transferir
type TransferEvent struct {
    PropertyID string `json:"propertyID"`
    From       string `json:"from"`
    To         string `json:"to"`
    Timestamp  string `json:"timestamp"`
}

func (s *SmartContract) TransferProperty(ctx contractapi.TransactionContextInterface,
    id string, newOwner string) error {
    // ... logica de transferencia ...

    event := TransferEvent{
        PropertyID: id,
        From:       property.Owner,
        To:         newOwner,
    }
    eventJSON, _ := json.Marshal(event)
    ctx.GetStub().SetEvent("PropertyTransferred", eventJSON)
    return nil
}

// En el cliente Node.js: escuchar eventos
// const listener = async (event) => {
//     const payload = JSON.parse(event.payload.toString());
//     console.log('Transferencia:', payload.propertyID);
// };
// contract.addContractListener(listener);""", language="go")

# Practica
add_activity_slide(prs, "Chaincode de Registro de Propiedad", [
    "Objetivo: implementar un chaincode completo con logica de negocio",
    "",
    "Requisitos del chaincode:",
    "  1. CRUD de propiedades (reutilizar el modelo del dia anterior)",
    "  2. Maquina de estados: active / transferring / blocked",
    "  3. Control de acceso: solo el owner puede iniciar transferencia",
    "  4. Rol registrador (ABAC) para confirmar transferencias",
    "  5. Private Data: precio de venta solo visible para comprador y vendedor",
    "  6. Evento PropertyTransferred al completar una transferencia",
    "",
    "  Usar el prompt de IA para generar la base y luego adaptar.",
    "  Desplegar en la test-network y probar todos los flujos.",
    "",
    "Trabajar en parejas. Tiempo estimado: 90 minutos.",
])

add_prompt_slide(prs, "Prompt IA: Chaincode con logica de negocio",
    """Genera un chaincode de Hyperledger Fabric en [Go/Node.js]
para un Registro de Propiedad con estas funcionalidades:

1. CRUD completo de Property (id, address, owner, area,
   propertyType, status, appraisalValue)
2. Maquina de estados con transiciones validadas:
   active <-> transferring, active <-> blocked
3. Control de acceso por MSPID (solo el owner opera)
   y por atributo "role=registrador" para confirmar
4. Private Data Collection "priceAgreement" para el
   precio de venta (solo comprador y vendedor)
5. Eventos: PropertyCreated, PropertyTransferred
6. Rich queries con CouchDB: buscar por tipo, por owner

Incluye el collections_config.json y comentarios en espanol.
Fabric 2.5.x con Contract API.""")

add_debate_slide(prs, "Logica de negocio en chaincodes", [
    "1. ¿Cuanta logica debe ir en el chaincode vs en la app cliente?",
    "2. ¿Que pasa si necesitas cambiar la maquina de estados despues del despliegue?",
    "3. Private Data: ¿es suficiente para cumplir GDPR? ¿Que limitaciones tiene?",
    "4. ¿Que ocurre si un registrador malicioso confirma transferencias falsas?",
    "5. ¿Como gestionariais los roles (registrador, autoridad) en un consorcio real?",
])

# Respuestas al debate (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. Logica en chaincode vs app cliente:",
    "2. Cambiar la maquina de estados despues del despliegue:",
    "3. Private Data y GDPR:",
],
subbullets={
    0: ["En el chaincode: reglas de negocio inmutables (saldos, permisos, transiciones validas).",
        "En el cliente: UI, orquestacion, validaciones de formato, UX.",
        "Regla: si se puede saltar desde otro cliente, NO es regla de negocio real.",
        "Si la regla afecta al ledger (consistencia entre todos los peers) -> chaincode."],
    1: ["Se despliega una nueva version del chaincode con sequence incrementado.",
        "El World State se preserva — los datos antiguos siguen ahi.",
        "Estrategias: anadir estados nuevos sin romper los antiguos (retrocompatibilidad).",
        "Si la transicion cambia radicalmente: migracion perezosa en cada lectura.",
        "Cuidado: nunca cambies el significado de un estado existente, crea uno nuevo."],
    2: ["Private Data ayuda pero NO cumple GDPR por si solo.",
        "El hash queda on-chain para siempre (inmutable) — potencialmente trazable.",
        "blockToLive permite caducar datos privados, pero el hash sigue.",
        "Mejor practica: datos personales OFF-CHAIN, solo hash/referencia on-chain.",
        "Cuando borras el dato off-chain, el hash on-chain queda huerfano (pseudonimizacion efectiva)."],
})

# Respuestas al debate (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. Registrador malicioso confirma transferencias falsas:",
    "5. Gestion de roles (registrador, autoridad) en un consorcio real:",
],
subbullets={
    0: ["El chaincode por si solo no lo evita — solo valida que tiene el atributo 'role=registrador'.",
        "Mitigaciones en capas:",
        "  a) Multi-firma: transferencias criticas requieren N de M registradores (endorsement policy).",
        "  b) Auditoria externa: un rol 'auditor' revisa transacciones periodicamente.",
        "  c) Jurisdiccion legal: el certificado identifica a la persona, responsabilidad penal.",
        "  d) Revocacion rapida del certificado si se detecta fraude + CRL actualizada.",
        "Ningun sistema es 100% a prueba de insider malicioso; blockchain reduce pero no elimina."],
    1: ["Registrar los roles como atributos del certificado X.509 via Fabric CA.",
        "Separacion de funciones: quien otorga el rol NO puede usarlo.",
        "Rotacion de roles: no dejar eternamente al mismo usuario con privilegios.",
        "Gobernanza clara: documento del consorcio define quien puede asignar cada rol.",
        "Logs de auditoria: cada emisin/revocacion de rol queda registrada en Fabric CA.",
        "Reglas en el chaincode: un rol solo puede hacer ciertas operaciones (ABAC)."],
})

add_review_slide(prs, "Repaso del dia", [
    "¿Como se verifica la identidad del cliente en un chaincode?",
    "¿Que diferencia hay entre GetMSPID() y AssertAttributeValue()?",
    "¿Que es una maquina de estados y por que es util en chaincodes?",
    "¿Que son las Private Data Collections?",
    "¿Donde se almacenan los datos privados vs el hash?",
    "¿Como se emite un evento desde un chaincode?",
    "¿Cuantos eventos se pueden emitir por transaccion?",
])

# Respuestas al repaso (parte 1)
add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Verificacion de identidad en un chaincode:",
    "2. GetMSPID() vs AssertAttributeValue():",
    "3. Maquina de estados en chaincodes:",
],
subbullets={
    0: ["A traves de ctx.GetClientIdentity(), que devuelve datos del certificado X.509 del caller.",
        "Metodos principales: GetID, GetMSPID, GetAttributeValue, AssertAttributeValue.",
        "El peer YA ha validado el certificado antes de llamar al chaincode (no tienes que validarlo tu).",
        "Tu trabajo es decidir si ese cert autenticado puede hacer lo que pide (autorizacion)."],
    1: ["GetMSPID(): devuelve la organizacion del caller ('Org1MSP', 'HotelMSP'...).",
        "AssertAttributeValue(attr, value): comprueba un atributo custom del cert (devuelve error si no coincide).",
        "GetMSPID: para controlar QUE ORG llama (Hotel vs Cafeteria).",
        "AssertAttributeValue: para controlar QUE ROL tiene (registrador, auditor, admin)."],
    2: ["Conjunto de estados validos y transiciones permitidas entre ellos.",
        "Ejemplo propiedad: active -> transferring -> active | blocked.",
        "Util para: evitar estados imposibles, forzar orden correcto, claridad del dominio.",
        "Implementacion: validar en cada funcion 'if currentStatus != X return error'."],
})

# Respuestas al repaso (parte 2)
add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "4. Private Data Collections:",
    "5. Donde se almacenan datos privados vs hash:",
    "6. Emitir un evento desde chaincode:",
    "7. Cuantos eventos por transaccion:",
],
subbullets={
    0: ["Mecanismo para compartir datos solo entre un subconjunto de orgs del canal.",
        "Se definen en collections_config.json: nombre, policy, blockToLive, miembros.",
        "Ejemplo: priceAgreement visible solo entre comprador y vendedor, no otras orgs."],
    1: ["Datos privados: base de datos privada de cada peer autorizado (LevelDB/CouchDB del peer).",
        "Hash: en el ledger publico del canal, visible para TODAS las orgs.",
        "El hash garantiza integridad sin revelar el contenido."],
    2: ["ctx.GetStub().SetEvent(nombreEvento, payloadBytes).",
        "Ejemplo: ctx.GetStub().SetEvent('PropertyTransferred', eventJSON).",
        "Los clientes se suscriben con contract.addContractListener() o peer channel events."],
    3: ["SOLO UNO por transaccion. Si llamas SetEvent dos veces, solo el ultimo prevalece.",
        "Si necesitas notificar varias cosas, usa un JSON con multiples campos en el payload.",
        "Alternativa: emitir un evento generico con 'type' dentro que indique que ha pasado."],
})

prs.save(f"{OUT_DIR}/dia_3.pptx")
print("dia_3.pptx generado OK")
