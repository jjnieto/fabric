import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

add_title_slide(prs, "Seguridad y Buenas Practicas\nen Chaincodes",
    "Dia 5 - Endorsement avanzado, determinismo, ABAC y auditoria")

add_review_slide(prs, "Repaso del dia anterior", [
    "¿Como se implementa un token fungible en Fabric?",
    "¿Que es una composite key y para que se usa en NFTs?",
    "Describe el flujo de trazabilidad de un lote alimentario",
    "¿Quien puede hacer recall de un lote?",
])

# Treasure Hunt
add_special_slide(prs, "TREASURE HUNT", "The DAO Hack y como Fabric lo previene", [
    "En junio de 2016, 'The DAO' era el mayor crowdfunding de la historia: 150M USD en ETH.",
    "Un atacante exploto un bug de re-entrancy en el smart contract y robo 60M USD.",
    "La comunidad Ethereum hizo un hard fork para revertir el robo -> nacio Ethereum Classic.",
    "",
    "Mision: Investigar y responder:",
    "  1. ¿Que es un ataque de re-entrancy? ¿Como funciona paso a paso?",
    "  2. ¿Es posible un ataque de re-entrancy en Hyperledger Fabric? ¿Por que si o por que no?",
    "  3. ¿Que mecanismo de Fabric impide que un chaincode 'llame a si mismo' de forma recursiva?",
    "  Pista: piensa en las diferencias entre el modelo execute-order de EVM",
    "  y el modelo execute-order-validate de Fabric.",
])

# Endorsement avanzado
add_section_slide(prs, "Politicas de Endorsement\nAvanzadas", "Quien debe aprobar cada transaccion")

add_content_slide(prs, "Politicas de endorsement: repaso", [
    "Una politica de endorsement define que organizaciones deben ejecutar y firmar",
    "Se define al desplegar el chaincode (lifecycle) o por key (state-based)",
    "Expresiones de politica:",
    "La politica por defecto se aplica a todas las keys del chaincode",
    "Pero se puede cambiar por key individual (state-based endorsement)",
],
subbullets={
    2: ["AND('Org1MSP.peer', 'Org2MSP.peer') - ambas deben aprobar",
        "OR('Org1MSP.peer', 'Org2MSP.peer') - basta con una",
        "OutOf(2, 'Org1MSP.peer', 'Org2MSP.peer', 'Org3MSP.peer') - al menos 2 de 3",
        "MAJORITY - mayoria de las organizaciones del canal"],
})

add_content_slide(prs, "State-Based Endorsement", [
    "Permite cambiar la politica de endorsement para una key especifica",
    "Util cuando diferentes activos requieren diferentes aprobaciones",
    "Ejemplo: una propiedad de alto valor requiere 3 orgs, una normal solo 2",
    "Se gestiona desde el chaincode con:",
    "La politica se almacena junto con el state en el World State",
],
subbullets={
    3: ["SetStateValidationParameter(key, policy) - establecer politica",
        "GetStateValidationParameter(key) - leer politica actual"],
})

add_code_slide(prs, "State-Based Endorsement: ejemplo", """
import (
    "github.com/hyperledger/fabric-chaincode-go/pkg/statebased"
)

func (s *SmartContract) SetHighValueEndorsement(
    ctx contractapi.TransactionContextInterface,
    propertyID string) error {

    // Leer propiedad
    property, _ := s.ReadProperty(ctx, propertyID)

    // Si el valor supera 1M, requerir endorsement de 3 orgs
    if property.AppraisalValue > 1000000 {
        policy, err := statebased.NewStateEP(nil)
        if err != nil {
            return err
        }
        // Requiere las tres organizaciones
        policy.AddOrgs(statebased.RoleTypePeer,
            "Org1MSP", "Org2MSP", "Org3MSP")
        policyBytes, _ := policy.Policy()

        return ctx.GetStub().SetStateValidationParameter(
            propertyID, policyBytes)
    }
    return nil
}""", language="go", subtitle="Politica dinamica segun el valor del activo")

# ABAC
add_content_slide(prs, "ABAC: Attribute-Based Access Control", [
    "ABAC permite control de acceso granular basado en atributos del certificado X.509",
    "Los atributos se anaden al certificado durante el enrollment con Fabric CA:",
    "En el chaincode se verifican con:",
    "Ventajas sobre verificar solo MSPID:",
],
subbullets={
    1: ["fabric-ca-client register --id.attrs 'role=admin,department=legal'",
        "fabric-ca-client enroll --enrollment.attrs 'role,department'"],
    2: ["ctx.GetClientIdentity().GetAttributeValue('role')",
        "ctx.GetClientIdentity().AssertAttributeValue('role', 'admin')"],
    3: ["Multiples roles dentro de la misma organizacion",
        "Permisos granulares: admin, auditor, operador, registrador...",
        "No necesitas crear una org por cada rol",
        "Los atributos viajan en el cert, no se pueden falsificar"],
})

add_code_slide(prs, "ABAC: ejemplo con multiples roles", """
func (s *SmartContract) checkRole(ctx contractapi.TransactionContextInterface,
    requiredRole string) error {

    role, found, err := ctx.GetClientIdentity().GetAttributeValue("role")
    if err != nil {
        return fmt.Errorf("error leyendo atributo role: %v", err)
    }
    if !found {
        return fmt.Errorf("el certificado no tiene atributo 'role'")
    }
    if role != requiredRole {
        return fmt.Errorf("rol requerido: %s, rol actual: %s",
            requiredRole, role)
    }
    return nil
}

// Uso en funciones del chaincode:
func (s *SmartContract) ApproveTransfer(ctx ...) error {
    if err := s.checkRole(ctx, "registrador"); err != nil {
        return err
    }
    // ... logica de aprobacion
}

func (s *SmartContract) FreezeProperty(ctx ...) error {
    if err := s.checkRole(ctx, "autoridad_judicial"); err != nil {
        return err
    }
    // ... logica de bloqueo
}""", language="go", subtitle="Helper reutilizable para verificar roles")

# Determinismo
add_section_slide(prs, "Determinismo en Chaincodes", "Errores que parecen inocentes pero rompen la red")

add_content_slide(prs, "¿Por que importa el determinismo?", [
    "En Fabric, los endorsing peers ejecutan el chaincode ANTES de que se ordene",
    "Todos los endorsers deben obtener el MISMO resultado (read/write set)",
    "Si los resultados difieren, la transaccion se invalida (MVCC conflict)",
    "Por tanto: el chaincode debe ser DETERMINISTA",
    "Esto significa: misma entrada -> siempre mismo resultado, en cualquier peer, en cualquier momento",
])

add_content_slide(prs, "Errores de determinismo: los 5 pecados", [
    "1. Usar timestamps del sistema: time.Now() varia entre peers",
    "2. Iterar mapas (Go): el orden de iteracion en Go maps es aleatorio",
    "3. Llamadas externas: HTTP, gRPC, filesystem... cada peer obtendria distinto resultado",
    "4. Numeros aleatorios: math/rand genera valores distintos en cada peer",
    "5. Variables globales mutables: estado compartido entre invocaciones",
],
subbullets={
    0: ["Solucion: usar ctx.GetStub().GetTxTimestamp() (viene del orderer)"],
    1: ["Solucion: usar slices ordenados o sort.Strings() antes de iterar"],
    2: ["Solucion: los datos externos deben entrar como parametro de la transaccion"],
    3: ["Solucion: si necesitas aleatoriedad, generala fuera y pasala como parametro"],
    4: ["Solucion: todo el estado debe ir en el World State, nunca en memoria global"],
})

add_code_slide(prs, "Determinismo: ejemplos de codigo incorrecto", """
// ERROR 1: Timestamp del sistema
func (s *SmartContract) BadCreate(ctx ...) error {
    asset.CreatedAt = time.Now().String()  // DIFERENTE EN CADA PEER
    // Correcto: asset.CreatedAt = ctx.GetStub().GetTxTimestamp()
}

// ERROR 2: Iterar un mapa en Go (orden aleatorio)
func (s *SmartContract) BadTotals(ctx ...) error {
    totals := map[string]int{"a": 1, "b": 2, "c": 3}
    result := ""
    for k, v := range totals {
        result += fmt.Sprintf("%s:%d,", k, v)
    }
    // result puede ser "a:1,b:2,c:3" o "c:3,a:1,b:2" -> NO DETERMINISTA
}

// ERROR 3: Llamada HTTP externa
func (s *SmartContract) BadPrice(ctx ...) error {
    resp, _ := http.Get("https://api.prices.com/gold")
    // Cada peer puede obtener un precio diferente -> INVALIDA
}

// ERROR 4: Numero aleatorio
func (s *SmartContract) BadRandom(ctx ...) error {
    id := fmt.Sprintf("ASSET-%d", rand.Intn(99999))
    // ID diferente en cada peer -> INVALIDA
}""", language="go", subtitle="Estos errores causan transacciones invalidas silenciosamente")

# Phantom reads y MVCC
add_content_slide(prs, "Phantom Reads y conflictos MVCC", [
    "MVCC: Multi-Version Concurrency Control",
    "Fabric usa un read/write set para validar transacciones:",
    "Phantom read: cuando una query devuelve resultados diferentes entre endorse y commit",
    "Causa tipica: dos transacciones concurrentes modifican keys del mismo rango",
    "Solucion: disenar el key space para minimizar colisiones",
],
subbullets={
    1: ["En el endorse: se registra que keys se leyeron y sus versiones",
        "En el commit: se verifica que esas versiones no cambiaron",
        "Si cambiaron -> transaccion MVCC_READ_CONFLICT -> se descarta"],
    4: ["Evitar GetStateByRange amplio en transacciones de escritura",
        "Usar keys especificas en vez de queries amplias",
        "Si necesitas leer muchos datos, hacerlo en query (solo lectura)"],
})

# Upgrades
add_section_slide(prs, "Gestion de Upgrades", "Versionado, migracion y compatibilidad")

add_content_slide(prs, "Actualizacion de chaincodes", [
    "A diferencia de Ethereum, los chaincodes en Fabric SE PUEDEN actualizar",
    "El lifecycle de Fabric permite desplegar nuevas versiones:",
    "Consideraciones al actualizar:",
],
subbullets={
    1: ["1. Empaquetar nueva version del chaincode",
        "2. Instalar en todos los peers",
        "3. Cada org aprueba la nueva definicion (approveformyorg)",
        "4. Commit de la nueva definicion (commit)"],
    2: ["El World State se mantiene: los datos NO se borran al actualizar",
        "Los datos antiguos deben ser compatibles con el nuevo codigo",
        "Estrategia: leer dato -> si falta campo nuevo, aplicar default -> guardar",
        "Nunca cambiar el formato de las keys existentes sin migracion"],
})

add_code_slide(prs, "Migracion de datos: compatibilidad hacia atras", """
// Version 1 del modelo
type PropertyV1 struct {
    ID      string `json:"id"`
    Owner   string `json:"owner"`
    Address string `json:"address"`
}

// Version 2: nuevos campos
type PropertyV2 struct {
    ID             string `json:"id"`
    Owner          string `json:"owner"`
    Address        string `json:"address"`
    PropertyType   string `json:"propertyType"`   // NUEVO
    AppraisalValue int    `json:"appraisalValue"` // NUEVO
    Version        int    `json:"version"`        // NUEVO: control de version
}

// Leer con compatibilidad: si faltan campos, aplicar defaults
func (s *SmartContract) ReadProperty(ctx ..., id string) (*PropertyV2, error) {
    data, _ := ctx.GetStub().GetState(id)
    var prop PropertyV2
    json.Unmarshal(data, &prop)

    // Migracion lazy: si es version antigua, aplicar defaults
    if prop.Version < 2 {
        if prop.PropertyType == "" { prop.PropertyType = "unknown" }
        prop.Version = 2
        // Guardar migrado (opcional: hacerlo on-read o con funcion de migracion)
    }
    return &prop, nil
}""", language="go", subtitle="Migracion lazy: migrar datos al leerlos")

# Checklist seguridad
add_content_slide(prs, "Checklist de seguridad para chaincodes", [
    "Verificar identidad: ¿quien invoca? (GetMSPID, GetID, ABAC)",
    "Verificar existencia: ¿el activo existe/no existe antes de operar?",
    "Verificar estado: ¿la transicion de estado es valida?",
    "Determinismo: ¿no uso time.Now, rand, http, map iteration?",
    "Validar inputs: ¿los parametros son validos (tipos, rangos, longitud)?",
    "No loguear datos sensibles: precios, datos personales, claves",
    "Private Data: ¿los datos confidenciales van por transient data?",
    "Eventos: ¿no incluyo datos sensibles en los payloads de eventos?",
    "Endorsement: ¿la politica es suficiente para el valor del activo?",
    "Paginacion: ¿limito los resultados de las queries?",
])

# Practica: auditar chaincode
add_activity_slide(prs, "Auditar un chaincode con fallos de seguridad", [
    "Objetivo: encontrar y corregir los fallos de seguridad en un chaincode",
    "",
    "Se os proporcionara un chaincode con 8 fallos de seguridad intencionados:",
    "  - Falta de verificacion de identidad",
    "  - Uso de time.Now() (no determinista)",
    "  - Iteracion de mapa sin ordenar",
    "  - Datos sensibles en logs y eventos",
    "  - Falta de validacion de inputs",
    "  - Query sin paginacion",
    "  - Transiciones de estado no validadas",
    "  - Acceso a Private Data sin verificar coleccion",
    "",
    "  Trabajar en parejas: encontrar los 8 fallos, explicar el riesgo,",
    "  y proponer la correccion. Tiempo: 60 minutos.",
    "  Puesta en comun: cada pareja presenta 2 fallos.",
])

add_prompt_slide(prs, "Prompt IA: Generar chaincode con fallos para auditar",
    """Genera un chaincode de Hyperledger Fabric en Go que tenga
8 fallos de seguridad intencionados para un ejercicio de
auditoria en un curso de formacion.

El chaincode debe ser un sistema de gestion de propiedades
con funciones Create, Read, Transfer y Query.

Fallos a incluir (pero sin comentarios que los senalen):
1. Una funcion sin verificacion de MSPID ni rol
2. Uso de time.Now() en vez de GetTxTimestamp()
3. Iteracion de un mapa de Go sin ordenar antes de escribir
4. Un fmt.Println que loguea el precio de venta
5. Falta de validacion en un parametro numerico (acepta negativos)
6. GetQueryResult sin paginacion
7. Transicion de estado invalida no verificada
8. PutPrivateData sin verificar que el caller pertenece
   a la coleccion

El codigo debe parecer plausible y funcional, solo con errores
sutiles. Anade un comentario al final del fichero con la lista
de fallos (para el instructor).""")

add_prompt_slide(prs, "Prompt IA: Auditar un chaincode existente",
    """Actua como auditor de seguridad de Hyperledger Fabric.
Revisa el siguiente chaincode y genera un informe con:

1. Lista de vulnerabilidades encontradas, clasificadas por
   severidad (critica, alta, media, baja)
2. Para cada vulnerabilidad:
   - Descripcion del problema
   - Linea o funcion afectada
   - Impacto potencial
   - Codigo corregido
3. Verificacion de determinismo
4. Verificacion de control de acceso
5. Verificacion de validacion de inputs
6. Recomendaciones generales

[Pegar aqui el codigo del chaincode a auditar]""",
    notes="Este prompt se puede usar para auditar cualquier chaincode, no solo el del ejercicio")

add_debate_slide(prs, "Seguridad en chaincodes", [
    "1. ¿Quien deberia auditar los chaincodes en un consorcio? ¿Cada org por separado o un auditor externo?",
    "2. Un chaincode con un bug de determinismo no falla visiblemente: las transacciones simplemente se invalidan. ¿Como detectarias este problema en produccion?",
    "3. ¿Es ABAC suficiente o necesitariamos algo como RBAC con una tabla de permisos en el World State?",
    "4. Si un endorsing peer es comprometido, ¿que protecciones tiene Fabric?",
    "5. ¿Como gestionariais la rotacion de certificados sin perder el acceso a los datos del World State?",
])

add_review_slide(prs, "Repaso del dia", [
    "¿Que es una politica de endorsement y como se define?",
    "¿Que es state-based endorsement?",
    "¿Que es ABAC y como se implementa en Fabric?",
    "Nombra los 5 errores de determinismo mas comunes",
    "¿Que es un conflicto MVCC y cuando ocurre?",
    "¿Como se actualiza un chaincode en Fabric?",
    "¿Que estrategia usarias para migrar datos entre versiones?",
    "Di 3 items del checklist de seguridad de chaincodes",
])

prs.save(f"{OUT_DIR}/dia_5.pptx")
print("dia_5.pptx generado OK")
