import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# 1. Portada
add_title_slide(prs, "Diseno de Chaincodes:\nPatrones y Arquitectura",
    "Dia 2 - Anatomia, modelado de datos y patrones CRUD")

# 2. Repaso dia anterior
add_review_slide(prs, "Repaso del dia anterior", [
    "¿Cual es la principal diferencia entre tokens en Ethereum y en Fabric?",
    "Nombra las tres formas de implementar tokens en Fabric",
    "¿Que es el modelo UTXO?",
    "¿Por que Fabric no tiene moneda nativa?",
])

# 3. Cultura General: Grace Hopper
add_special_slide(prs, "CULTURA GENERAL", "Grace Hopper: la madre del debugging", [
    "Grace Hopper (1906-1992) fue una pionera de la informatica y contraalmirante de la US Navy.",
    "Desarrollo el primer compilador (A-0) y contribuyo al lenguaje COBOL.",
    "En 1947, su equipo encontro una polilla atrapada en un rele del Mark II.",
    "Pego la polilla en el cuaderno de bitacora con la nota: 'First actual case of bug being found'.",
    "Aunque el termino 'bug' ya existia, este incidente lo popularizo en informatica.",
    "Leccion para el curso: cuando un chaincode no funciona... puede que sea un bug literal.",
    "",
    "¿Sabiais que el USS Hopper (DDG-70), un destructor de la US Navy, lleva su nombre?",
])

# 4. Que es un chaincode
add_content_slide(prs, "¿Que es un chaincode en Fabric?", [
    "Un chaincode es un programa que se ejecuta en los peers de Fabric",
    "Equivalente a un Smart Contract, pero con diferencias importantes:",
    "Un chaincode puede contener MULTIPLES contratos (clases)",
    "Se empaqueta como un contenedor Docker independiente",
    "Se ejecuta en un entorno aislado del peer (sandbox)",
    "Lenguajes soportados: Go, Node.js, Java",
],
subbullets={
    1: ["Se despliega a traves del lifecycle (no con una transaccion como en EVM)",
        "No paga gas: el coste es operativo, no transaccional",
        "Accede al World State via Stub API, no a storage slots"],
})

# 5. Chaincode vs Smart Contract
add_two_column_slide(prs, "Chaincode vs Smart Contract: terminologia",
    "En Ethereum", [
        "1 Smart Contract = 1 direccion",
        "Escrito en Solidity",
        "Desplegado con una transaccion",
        "Ejecutado por todos los nodos",
        "Estado en storage slots (mapping)",
        "Inmutable una vez desplegado",
        "(salvo patron proxy)",
    ],
    "En Fabric", [
        "1 Chaincode = N contratos",
        "Escrito en Go / Node.js / Java",
        "Desplegado via lifecycle (approve + commit)",
        "Ejecutado solo por endorsing peers",
        "Estado en World State (key-value)",
        "Actualizable via lifecycle",
        "(nueva version, misma politica)",
    ])

# 6. Anatomia Go
add_code_slide(prs, "Anatomia de un chaincode en Go", """
package main

import (
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract proporciona las funciones del chaincode
type SmartContract struct {
    contractapi.Contract
}

// InitLedger inicializa el ledger con datos de ejemplo
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
    // Logica de inicializacion aqui
    return nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(&SmartContract{})
    if err != nil {
        panic(err)
    }
    if err := chaincode.Start(); err != nil {
        panic(err)
    }
}""", language="go", subtitle="Estructura basica: struct + Contract API + main()")

# 7. Anatomia Node.js
add_code_slide(prs, "Anatomia de un chaincode en Node.js", """
'use strict';

const { Contract } = require('fabric-contract-api');

class AssetContract extends Contract {

    async InitLedger(ctx) {
        // Logica de inicializacion aqui
        const assets = [
            { ID: 'asset1', Owner: 'Alice', Value: 100 },
            { ID: 'asset2', Owner: 'Bob',   Value: 200 },
        ];
        for (const asset of assets) {
            await ctx.stub.putState(asset.ID,
                Buffer.from(JSON.stringify(asset)));
        }
    }

    async ReadAsset(ctx, id) {
        const assetJSON = await ctx.stub.getState(id);
        if (!assetJSON || assetJSON.length === 0) {
            throw new Error(`Asset ${id} does not exist`);
        }
        return assetJSON.toString();
    }
}

module.exports = AssetContract;""", language="node.js",
    subtitle="Estructura basica: clase que extiende Contract")

# 8. El contexto de transaccion
add_content_slide(prs, "El contexto de transaccion (ctx)", [
    "Cada funcion del chaincode recibe un ctx (TransactionContext)",
    "A traves de ctx accedes a:",
    "ctx es tu puerta de entrada a todo el estado de Fabric",
    "Nunca accedas al filesystem o a la red desde un chaincode",
],
subbullets={
    1: ["ctx.GetStub() - la Stub API para leer/escribir el World State",
        "ctx.GetClientIdentity() - identidad del cliente que invoca (cert X.509)",
        "ctx.GetStub().GetTxID() - ID unico de la transaccion",
        "ctx.GetStub().GetTxTimestamp() - timestamp de la transaccion",
        "ctx.GetStub().SetEvent() - emitir eventos"],
})

# 9. Stub API
add_content_slide(prs, "Stub API: operaciones sobre el World State", [
    "GetState(key) - Leer un valor por su clave",
    "PutState(key, value) - Escribir o actualizar un valor",
    "DelState(key) - Eliminar una clave (borrado logico del state)",
    "GetStateByRange(startKey, endKey) - Rango de claves",
    "GetQueryResult(query) - Rich query (solo CouchDB)",
    "GetStateByPartialCompositeKey(objectType, attrs) - Buscar por clave compuesta",
    "GetHistoryForKey(key) - Historial de cambios de una clave",
    "",
    "Importante: PutState no escribe inmediatamente. Los cambios se aplican",
    "solo si la transaccion es validada y committeada por los peers.",
])

# 10. Composite Keys
add_content_slide(prs, "Composite Keys: claves compuestas", [
    "Permiten crear claves estructuradas para busquedas eficientes",
    "Se construyen con CreateCompositeKey(objectType, attributes[])",
    "El objectType actua como 'tabla' y los attributes como indices",
    "Ejemplo: clave para un activo de un propietario:",
    "Se pueden buscar por prefijo con GetStateByPartialCompositeKey",
    "Muy utiles para relaciones 1:N (propietario -> activos)",
],
subbullets={
    3: ['CreateCompositeKey("asset", []string{"org1", "warehouse", "LOT-001"})',
        'Resultado: \\x00asset\\x00org1\\x00warehouse\\x00LOT-001\\x00'],
})

# 11. Composite Keys ejemplo
add_code_slide(prs, "Composite Keys: ejemplo practico", """
// Crear una clave compuesta para un activo
func (s *SmartContract) CreateAsset(ctx contractapi.TransactionContextInterface,
    owner string, assetType string, id string, value int) error {

    // Clave compuesta: permite buscar por owner o por type
    key, err := ctx.GetStub().CreateCompositeKey("asset",
        []string{owner, assetType, id})
    if err != nil {
        return err
    }

    asset := Asset{ID: id, Owner: owner, Type: assetType, Value: value}
    assetJSON, _ := json.Marshal(asset)
    return ctx.GetStub().PutState(key, assetJSON)
}

// Buscar todos los activos de un propietario
func (s *SmartContract) GetAssetsByOwner(ctx contractapi.TransactionContextInterface,
    owner string) ([]*Asset, error) {

    iterator, err := ctx.GetStub().GetStateByPartialCompositeKey("asset",
        []string{owner})
    // ... iterar sobre resultados
}""", language="go")

# 12. Modelado de datos JSON
add_content_slide(prs, "Modelado de datos: JSON en el World State", [
    "El World State almacena pares clave-valor",
    "El valor tipicamente es un JSON serializado",
    "Disena tus structs/objetos pensando en las queries que necesitaras",
    "Reglas de diseno:",
],
subbullets={
    3: ["Incluye siempre un campo 'docType' para filtrar en CouchDB",
        "Usa IDs deterministas (no UUIDs generados en el chaincode)",
        "Evita objetos anidados profundos: complican las queries",
        "Piensa en el key space: ¿como vas a buscar este dato?",
        "Desnormaliza si es necesario: no hay JOINs en el World State"],
})

# 13. Ejemplo modelo de datos
add_code_slide(prs, "Modelo de datos: Registro de Propiedad", """
// Propiedad inmobiliaria
type Property struct {
    DocType       string `json:"docType"`       // siempre "property"
    ID            string `json:"id"`            // referencia catastral
    Address       string `json:"address"`       // direccion fisica
    Owner         string `json:"owner"`         // ID del propietario (MSP)
    OwnerName     string `json:"ownerName"`     // nombre del propietario
    Area          int    `json:"area"`          // metros cuadrados
    PropertyType  string `json:"propertyType"`  // "apartment"|"house"|"land"
    Status        string `json:"status"`        // "active"|"transferring"|"blocked"
    RegisteredAt  string `json:"registeredAt"`  // fecha de registro
    AppraisalValue int   `json:"appraisalValue"` // valor de tasacion (euros)
}

// Key design: "property" + comunidad + municipio + referencia_catastral
// Permite buscar por comunidad, por municipio, o por referencia exacta""",
    language="go", subtitle="Caso de uso: Registro de Propiedad")

# 14. LevelDB vs CouchDB
add_two_column_slide(prs, "World State: LevelDB vs CouchDB",
    "LevelDB", [
        "Base de datos key-value embebida",
        "Solo soporta queries por clave exacta",
        "y por rango de claves (startKey-endKey)",
        "Mas rapido y ligero",
        "No requiere contenedor adicional",
        "Ideal para: lookups por clave,",
        "modelos simples, alto rendimiento",
    ],
    "CouchDB", [
        "Base de datos documental (JSON)",
        "Soporta rich queries (consultas JSON)",
        "Indices configurables",
        "Requiere contenedor Docker adicional",
        "Algo mas lento pero mucho mas flexible",
        "Ideal para: queries complejas,",
        "reportes, busquedas por atributo",
    ])

# 15. Rich queries CouchDB
add_code_slide(prs, "Rich Queries con CouchDB", """
// Buscar propiedades por tipo y rango de valor
func (s *SmartContract) QueryProperties(ctx contractapi.TransactionContextInterface,
    propertyType string, minValue int) ([]*Property, error) {

    // Mango query (sintaxis CouchDB)
    queryString := fmt.Sprintf(
        `{"selector":{
            "docType": "property",
            "propertyType": "%s",
            "appraisalValue": {"$gte": %d}
        },
        "sort": [{"appraisalValue": "desc"}],
        "use_index": "indexPropertyType"}`,
        propertyType, minValue)

    resultsIterator, err := ctx.GetStub().GetQueryResult(queryString)
    if err != nil {
        return nil, err
    }
    defer resultsIterator.Close()

    // Iterar y deserializar resultados...
}""", language="go", subtitle="Consultas JSON estilo MongoDB sobre el World State")

# 16. Paginacion
add_content_slide(prs, "Paginacion de resultados", [
    "Cuando hay muchos resultados, paginar es esencial",
    "GetStateByRangeWithPagination(startKey, endKey, pageSize, bookmark)",
    "GetQueryResultWithPagination(query, pageSize, bookmark)",
    "El bookmark es un token opaco que identifica la siguiente pagina",
    "Primera llamada: bookmark vacio",
    "Siguientes: usar el bookmark devuelto en la respuesta anterior",
    "",
    "Consejo: limita siempre los resultados. Una query sin limite",
    "puede devolver miles de registros y degradar el rendimiento.",
])

# 17-20. Patron CRUD
add_code_slide(prs, "Patron CRUD: Create", """
func (s *SmartContract) CreateProperty(ctx contractapi.TransactionContextInterface,
    id string, address string, owner string, area int,
    propType string, value int) error {

    // Verificar que no existe
    existing, err := ctx.GetStub().GetState(id)
    if err != nil {
        return fmt.Errorf("error reading state: %v", err)
    }
    if existing != nil {
        return fmt.Errorf("property %s already exists", id)
    }

    property := Property{
        DocType:        "property",
        ID:             id,
        Address:        address,
        Owner:          owner,
        Area:           area,
        PropertyType:   propType,
        Status:         "active",
        AppraisalValue: value,
    }

    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState(id, propertyJSON)
}""", language="go", subtitle="Verificar existencia antes de crear")

add_code_slide(prs, "Patron CRUD: Read", """
func (s *SmartContract) ReadProperty(ctx contractapi.TransactionContextInterface,
    id string) (*Property, error) {

    propertyJSON, err := ctx.GetStub().GetState(id)
    if err != nil {
        return nil, fmt.Errorf("failed to read: %v", err)
    }
    if propertyJSON == nil {
        return nil, fmt.Errorf("property %s does not exist", id)
    }

    var property Property
    err = json.Unmarshal(propertyJSON, &property)
    if err != nil {
        return nil, err
    }
    return &property, nil
}

// En Node.js seria:
// async ReadProperty(ctx, id) {
//     const data = await ctx.stub.getState(id);
//     if (!data || data.length === 0) throw new Error('Not found');
//     return JSON.parse(data.toString());
// }""", language="go", subtitle="Leer y deserializar desde el World State")

add_code_slide(prs, "Patron CRUD: Update", """
func (s *SmartContract) UpdatePropertyValue(ctx contractapi.TransactionContextInterface,
    id string, newValue int) error {

    // Leer el activo existente
    property, err := s.ReadProperty(ctx, id)
    if err != nil {
        return err
    }

    // Verificar permisos: solo el owner puede actualizar
    clientMSP, _ := ctx.GetClientIdentity().GetMSPID()
    if property.Owner != clientMSP {
        return fmt.Errorf("only the owner can update this property")
    }

    // Actualizar campo
    property.AppraisalValue = newValue

    // Guardar
    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState(id, propertyJSON)
}""", language="go", subtitle="Leer, verificar permisos, modificar, guardar")

add_code_slide(prs, "Patron CRUD: Delete y GetAll", """
// Delete: borrado logico (cambiar status) vs fisico (DelState)
func (s *SmartContract) DeactivateProperty(ctx contractapi.TransactionContextInterface,
    id string) error {
    property, err := s.ReadProperty(ctx, id)
    if err != nil {
        return err
    }
    property.Status = "inactive"  // borrado logico: mantiene historial
    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState(id, propertyJSON)
}

// GetAll con paginacion
func (s *SmartContract) GetAllProperties(ctx contractapi.TransactionContextInterface,
    pageSize int32, bookmark string) (*PaginatedResult, error) {

    iterator, metadata, err := ctx.GetStub().
        GetStateByRangeWithPagination("", "", pageSize, bookmark)
    if err != nil {
        return nil, err
    }
    defer iterator.Close()
    // ... iterar y construir resultado con metadata.Bookmark
}""", language="go", subtitle="Borrado logico vs fisico + paginacion")

# 21. Prompt IA
add_prompt_slide(prs, "Prompt IA: Generar chaincode CRUD completo",
    """Genera un chaincode de Hyperledger Fabric en [Go/Node.js]
para un sistema de Registro de Propiedad con las siguientes
especificaciones:

- Struct/modelo: Property con campos id, address, owner,
  ownerName, area (int), propertyType (apartment|house|land),
  status (active|transferring|blocked), appraisalValue (int)
- Incluye campo docType="property" para queries CouchDB
- Operaciones CRUD: Create, Read, Update, Delete (logico),
  GetAll con paginacion
- Validaciones: verificar existencia, permisos por MSPID
- Rich query: buscar por propertyType y rango de valor
- Usa la Contract API oficial de Fabric
- Incluye eventos para Create y Transfer
- Anade comentarios explicativos en espanol

Contexto: es para un curso de formacion, debe ser claro
y didactico. Usa Fabric 2.5.x.""",
    notes="Adapta el prompt segun el lenguaje (Go o Node.js) y anade campos extra si lo necesitas")

# 22. Practica
add_activity_slide(prs, "Disenar modelo de datos: Registro de Propiedad", [
    "Objetivo: disenar el modelo de datos y las claves para un Registro de Propiedad",
    "",
    "1. Definir la estructura de datos (Property) con todos los campos necesarios",
    "2. Disenar el key space: ¿que clave usareis? ¿composite keys?",
    "3. Identificar las queries que necesitareis (por propietario, por zona, por tipo...)",
    "4. Decidir: ¿LevelDB o CouchDB? Justificar",
    "5. Crear el chaincode CRUD completo usando el prompt de IA como base",
    "6. Desplegar en la test-network y probar las operaciones basicas",
    "",
    "Trabajar en parejas. Tiempo estimado: 70 minutos.",
    "Puesta en comun al final: cada pareja explica sus decisiones de diseno.",
])

# 23. Debate
add_debate_slide(prs, "Decisiones de diseno", [
    "1. ¿LevelDB o CouchDB para un Registro de Propiedad? ¿Y para un sistema de pagos?",
    "2. ¿Borrado fisico (DelState) o logico (status=inactive)? ¿Cuando usar cada uno?",
    "3. ¿Composite keys o rich queries? ¿Se pueden combinar?",
    "4. ¿Cuanta logica de negocio debe ir en el chaincode vs en la aplicacion cliente?",
    "5. ¿Que pasa si el modelo de datos necesita cambiar despues del despliegue?",
])

# 23b. Respuestas (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. LevelDB o CouchDB?",
    "2. Borrado fisico vs logico?",
    "3. Composite keys vs rich queries?",
],
subbullets={
    0: ["Registro de Propiedad: CouchDB. Necesitas filtrar por dueno, zona, tipo, valor.",
        "Sistema de pagos: LevelDB. Solo lookup por ID de transaccion, maximo rendimiento.",
        "Regla: si solo buscas por clave exacta, LevelDB. Si necesitas rich queries, CouchDB."],
    1: ["Borrado fisico (DelState): cuando el dato ya no tiene valor ni legal ni historico.",
        "Borrado logico (status=inactive): para regulacion, auditoria, trazabilidad.",
        "En blockchain se recomienda logico: el historial queda intacto y es mas seguro.",
        "DelState marca la key como borrada pero la historia sigue en GetHistoryForKey."],
    2: ["No son excluyentes. Se usan juntas en muchos casos reales.",
        "Composite keys: indexacion estructurada por prefijo (eficiente, determinista).",
        "Rich queries: flexibilidad para filtrar por cualquier campo (requiere CouchDB).",
        "Combinacion habitual: composite keys para lookups frecuentes + rich queries para reportes."],
})

# 23c. Respuestas (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. Logica de negocio: chaincode vs aplicacion cliente?",
    "5. ¿Que pasa si el modelo de datos cambia despues del despliegue?",
],
subbullets={
    0: ["En el chaincode: reglas de negocio CRITICAS e INMUTABLES. Las que deben cumplirse siempre.",
        "En la aplicacion cliente: UI, orquestacion, validaciones de formato, preferencias del usuario.",
        "Regla: si se puede saltar desde otro cliente, NO es una regla de negocio real.",
        "Ejemplo: validar saldo suficiente -> chaincode. Mostrar mensaje bonito de error -> app."],
    1: ["Fabric permite actualizar chaincodes con nuevas versiones (secuencia incrementada).",
        "El World State se preserva — los datos antiguos siguen ahi con el formato viejo.",
        "Estrategias para cambiar el modelo:",
        "  a) Campos nuevos opcionales: los datos viejos siguen funcionando (recomendado).",
        "  b) Migracion perezosa: la primera vez que lees un registro, lo actualizas al formato nuevo.",
        "  c) Migracion en bloque: funcion admin que recorre todos los datos y los actualiza.",
        "Nunca: borrar campos en uso sin migrar antes. Nunca: cambiar el significado de un campo."],
})

# 24. Repaso
add_review_slide(prs, "Repaso del dia", [
    "¿Que diferencia hay entre un chaincode y un Smart Contract de Ethereum?",
    "¿Que es la Stub API y que operaciones principales ofrece?",
    "¿Para que sirven las Composite Keys?",
    "¿Cual es la diferencia entre LevelDB y CouchDB?",
    "¿Que es una rich query y cuando la usarias?",
    "¿Por que es importante incluir un campo docType en los datos?",
    "¿Que ventaja tiene el borrado logico sobre DelState?",
])

# 25. Respuestas al repaso (parte 1)
add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Chaincode vs Smart Contract de Ethereum:",
    "2. Que es la Stub API y que ofrece:",
    "3. Para que sirven las Composite Keys:",
],
subbullets={
    0: ["Lenguajes: Fabric usa Go, Node.js, Java; Ethereum usa Solidity o Vyper.",
        "Fabric es permissioned (identidades conocidas); Ethereum es permissionless.",
        "Fabric separa endorse-order-validate; Ethereum ejecuta todo en el bloque.",
        "Fabric no tiene gas nativo; Ethereum requiere pagar ETH por cada transaccion."],
    1: ["Stub API es la interfaz del chaincode con el ledger (ctx.GetStub()).",
        "Operaciones clave: GetState, PutState, DelState (CRUD basico).",
        "GetStateByRange, GetQueryResult, GetHistoryForKey (consultas avanzadas).",
        "CreateCompositeKey, SplitCompositeKey (gestion de claves compuestas).",
        "SetEvent (eventos), GetTxTimestamp, GetTxID (metadatos de la transaccion)."],
    2: ["Son claves estructuradas que combinan un objectType con varios atributos.",
        "Ejemplo: 'property~region~municipality~id' permite buscar por prefijo.",
        "Sirven para crear indices secundarios en LevelDB (sin CouchDB).",
        "Permiten lookups eficientes por 'primer atributo' sin escanear todo.",
        "Alternativa a las rich queries cuando necesitas rendimiento."],
})

# 26. Respuestas al repaso (parte 2)
add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "4. Diferencia entre LevelDB y CouchDB:",
    "5. Que es una rich query y cuando usarla:",
    "6. Por que incluir docType:",
    "7. Ventaja del borrado logico sobre DelState:",
],
subbullets={
    0: ["LevelDB: key-value simple, rapido, embebido en el peer.",
        "CouchDB: base de datos documental JSON, soporta rich queries.",
        "LevelDB: solo busqueda por clave o rango. CouchDB: por cualquier campo."],
    1: ["Consulta JSON estilo MongoDB sobre el contenido de los documentos (Mango).",
        "Ejemplo: {'selector':{'docType':'property','region':'Madrid'}}.",
        "Usar cuando: necesitas filtrar por campos, ordenar, paginar reportes.",
        "No usar en transacciones de escritura (causa phantom reads y conflictos MVCC)."],
    2: ["Sin docType, no puedes distinguir tipos de documentos en rich queries.",
        "Con docType puedes crear indices CouchDB eficientes.",
        "Convencion universal en Hyperledger: todos los ejemplos oficiales lo usan.",
        "Inutil con LevelDB, pero es buena practica por si migras a CouchDB."],
    3: ["Mantiene el historial completo del activo (compliance, auditoria).",
        "Permite 'reactivar' un registro si fue un error.",
        "Mejor para regulacion (GDPR excepto 'derecho al olvido').",
        "DelState es irreversible; con logico siempre puedes volver atras."],
})

prs.save(f"{OUT_DIR}/dia_2.pptx")
print("dia_2.pptx generado OK")
