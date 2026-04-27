# Ejercicio Dia 2: Registro de Propiedad

## Enunciado

Diseñar el modelo de datos y las claves para un sistema de Registro de Propiedad inmobiliaria, implementar el chaincode CRUD completo y desplegarlo en la test-network.

1. Definir la estructura de datos (Property) con todos los campos necesarios
2. Diseñar el key space: ¿que clave usareis? ¿composite keys?
3. Identificar las queries que necesitareis (por propietario, por zona, por tipo...)
4. Decidir: ¿LevelDB o CouchDB? Justificar
5. Crear el chaincode CRUD completo usando el prompt de IA como base
6. Desplegar en la test-network y probar las operaciones básicas

---

## 1. Estructura de datos (Property)

Analisis: ¿que información necesitamos guardar de una propiedad inmobiliaria?

```go
type Property struct {
    DocType        string `json:"docType"`        // Siempre "property" (para CouchDB queries)
    ID             string `json:"id"`             // Referencia catastral (unico en Espana)
    Address        string `json:"address"`        // Direccion fisica
    Owner          string `json:"owner"`          // DNI del propietario
    OwnerName      string `json:"ownerName"`      // Nombre del propietario
    Area           int    `json:"area"`           // Metros cuadrados
    PropertyType   string `json:"propertyType"`   // apartment | house | land | commercial
    Status         string `json:"status"`         // active | transferring | blocked
    Region         string `json:"region"`         // Comunidad autonoma
    Municipality   string `json:"municipality"`   // Municipio
    AppraisalValue int    `json:"appraisalValue"` // Valor de tasacion en euros
    RegisteredAt   string `json:"registeredAt"`   // Fecha de registro (RFC3339)
    LastModifiedAt string `json:"lastModifiedAt"` // Ultima modificacion
}
```

**Decisiones de diseño:**
- **ID = referencia catastral**: es un identificador único y oficial en España, ya existe fuera de blockchain. No inventamos IDs nuevos.
- **Owner = DNI** (no nombre): el nombre puede repetirse, el DNI es único. Ver por que en el [caso del Módulo 6](../../módulo-6/01-diseño-funcional.md).
- **Status como enum**: `active | transferring | blocked`. Permite máquina de estados clara.
- **Region y Municipality separados**: para poder buscar por zona sin parsear la dirección.
- **docType = "property"**: imprescindible si usamos CouchDB — permite filtrar por tipo de documento en rich queries.

---

## 2. Diseño del key space

### Opcion A: clave simple (no recomendada)

```
Key: <referencia_catastral>
```

Problema: solo se puede buscar por ID exacto. Ineficiente para queries "dame todas las propiedades de Madrid".

### Opcion B: composite key (recomendada)

```
Key: property~<region>~<municipality>~<referencia_catastral>
```

Ventajas:
- Se puede buscar por region: `GetStateByPartialCompositeKey("property", ["Madrid"])`
- Se puede buscar por region + municipio: `GetStateByPartialCompositeKey("property", ["Madrid", "Alcobendas"])`
- Se puede buscar por propiedad exacta con las 3 partes

### Opcion C: clave simple + CouchDB rich queries (mejor)

```
Key: property_<referencia_catastral>
```

Y dejar que CouchDB haga las queries por `region`, `owner`, `propertyType`, etc. gracias al campo `docType` y los índices.

**Nuestra elección: Opcion C** — mas simple de mantener, mas potente para queries complejas.

### Índices de CouchDB

Crear el archivo `META-INF/statedb/couchdb/indexes/indexPropertyType.json` en el paquete del chaincode:

```json
{
  "index": {
    "fields": ["docType", "propertyType"]
  },
  "ddoc": "indexPropertyTypeDoc",
  "name": "indexPropertyType",
  "type": "json"
}
```

Otros índices recomendados:
- `indexOwner`: por `docType` + `owner` (buscar propiedades de un dueño)
- `indexRegion`: por `docType` + `region` (propiedades de una comunidad)
- `indexValue`: por `docType` + `appraisalValue` (ordenar por valor)

---

## 3. Queries necesarias

Antes de elegir tecnología, listar TODO lo que queremos poder hacer:

| Query | Descripcion | Complejidad |
|-------|------------|-------------|
| `GetProperty(id)` | Leer una propiedad por referencia catastral | Baja (clave exacta) |
| `GetPropertiesByOwner(dni)` | Todas las propiedades de un dueño | Media (filtrar por campo) |
| `GetPropertiesByRegion(region)` | Todas las propiedades de Madrid/Cataluña/etc. | Media (filtrar por campo) |
| `GetPropertiesByType(type)` | Todos los pisos, todas las casas... | Media (filtrar por campo) |
| `SearchProperties(minValue, maxValue)` | Propiedades en un rango de precio | Media (filtrar por rango) |
| `GetAllProperties(pageSize, bookmark)` | Listado paginado de todas | Baja (rango de claves) |
| `GetPropertyHistory(id)` | Historial de cambios de una propiedad | Baja (GetHistoryForKey) |

---

## 4. ¿LevelDB o CouchDB?

### LevelDB
- **Pro**: rápido, ligero, sin contenedor adicional
- **Con**: solo busqueda por clave exacta o rango de claves
- **Cuando usar**: si solo necesitas lookups directos (como un key-value store simple)

### CouchDB
- **Pro**: rich queries con sintaxis Mango (JSON), índices, ordenación, paginación
- **Con**: contenedor adicional, algo mas lento, mas memoria
- **Cuando usar**: si necesitas buscar por campos del JSON (no solo por clave)

**Nuestra elección: CouchDB**.

Razón: la mayoria de queries de nuestra tabla anterior necesitan filtrar por campos (`owner`, `region`, `propertyType`, `appraisalValue`). Con LevelDB tendriamos que recorrer TODAS las propiedades en cada query, lo que no escala. Con CouchDB e índices, las queries son eficientes incluso con millones de propiedades.

El coste de un contenedor CouchDB extra es despreciable comparado con el beneficio.

---

## 5. Chaincode CRUD completo

### Estructura

```go
package main

import (
    "encoding/json"
    "fmt"
    "time"

    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type Property struct {
    DocType        string `json:"docType"`
    ID             string `json:"id"`
    Address        string `json:"address"`
    Owner          string `json:"owner"`
    OwnerName      string `json:"ownerName"`
    Area           int    `json:"area"`
    PropertyType   string `json:"propertyType"`
    Status         string `json:"status"`
    Region         string `json:"region"`
    Municipality   string `json:"municipality"`
    AppraisalValue int    `json:"appraisalValue"`
    RegisteredAt   string `json:"registeredAt"`
    LastModifiedAt string `json:"lastModifiedAt"`
}

type SmartContract struct {
    contractapi.Contract
}
```

### CREATE

```go
func (s *SmartContract) CreateProperty(ctx contractapi.TransactionContextInterface,
    id, address, owner, ownerName, propertyType, region, municipality string,
    area, appraisalValue int) error {

    // Validaciones
    if id == "" || owner == "" {
        return fmt.Errorf("id y owner son obligatorios")
    }
    if area <= 0 || appraisalValue <= 0 {
        return fmt.Errorf("area y appraisalValue deben ser positivos")
    }

    // Verificar existencia
    existing, err := ctx.GetStub().GetState("property_" + id)
    if err != nil {
        return fmt.Errorf("error leyendo state: %v", err)
    }
    if existing != nil {
        return fmt.Errorf("la propiedad %s ya existe", id)
    }

    // Timestamp determinista
    txTimestamp, _ := ctx.GetStub().GetTxTimestamp()
    ts := time.Unix(txTimestamp.Seconds, 0).Format(time.RFC3339)

    property := Property{
        DocType:        "property",
        ID:             id,
        Address:        address,
        Owner:          owner,
        OwnerName:      ownerName,
        Area:           area,
        PropertyType:   propertyType,
        Status:         "active",
        Region:         region,
        Municipality:   municipality,
        AppraisalValue: appraisalValue,
        RegisteredAt:   ts,
        LastModifiedAt: ts,
    }

    propertyJSON, _ := json.Marshal(property)
    ctx.GetStub().SetEvent("PropertyCreated", []byte(
        fmt.Sprintf(`{"id":"%s","owner":"%s"}`, id, owner)))
    return ctx.GetStub().PutState("property_"+id, propertyJSON)
}
```

### READ

```go
func (s *SmartContract) ReadProperty(ctx contractapi.TransactionContextInterface,
    id string) (*Property, error) {

    propertyJSON, err := ctx.GetStub().GetState("property_" + id)
    if err != nil {
        return nil, fmt.Errorf("error leyendo state: %v", err)
    }
    if propertyJSON == nil {
        return nil, fmt.Errorf("la propiedad %s no existe", id)
    }

    var property Property
    if err := json.Unmarshal(propertyJSON, &property); err != nil {
        return nil, err
    }
    return &property, nil
}
```

### UPDATE (cambiar valor de tasacion)

```go
func (s *SmartContract) UpdateAppraisalValue(ctx contractapi.TransactionContextInterface,
    id string, newValue int) error {

    if newValue <= 0 {
        return fmt.Errorf("el valor debe ser positivo")
    }

    property, err := s.ReadProperty(ctx, id)
    if err != nil {
        return err
    }

    if property.Status != "active" {
        return fmt.Errorf("la propiedad esta en estado %s, no se puede modificar",
            property.Status)
    }

    property.AppraisalValue = newValue
    txTimestamp, _ := ctx.GetStub().GetTxTimestamp()
    property.LastModifiedAt = time.Unix(txTimestamp.Seconds, 0).Format(time.RFC3339)

    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState("property_"+id, propertyJSON)
}
```

### DELETE (borrado lógico)

```go
func (s *SmartContract) DeactivateProperty(ctx contractapi.TransactionContextInterface,
    id string) error {

    property, err := s.ReadProperty(ctx, id)
    if err != nil {
        return err
    }

    property.Status = "inactive"
    txTimestamp, _ := ctx.GetStub().GetTxTimestamp()
    property.LastModifiedAt = time.Unix(txTimestamp.Seconds, 0).Format(time.RFC3339)

    propertyJSON, _ := json.Marshal(property)
    return ctx.GetStub().PutState("property_"+id, propertyJSON)
}
```

### QUERIES (rich queries con CouchDB)

```go
// Buscar propiedades por tipo y rango de valor
func (s *SmartContract) QueryPropertiesByTypeAndValue(
    ctx contractapi.TransactionContextInterface,
    propertyType string, minValue, maxValue int) ([]*Property, error) {

    queryString := fmt.Sprintf(`{
        "selector": {
            "docType": "property",
            "propertyType": "%s",
            "appraisalValue": {"$gte": %d, "$lte": %d}
        },
        "sort": [{"appraisalValue": "desc"}],
        "use_index": "indexPropertyType"
    }`, propertyType, minValue, maxValue)

    return s.executeQuery(ctx, queryString)
}

// Buscar propiedades por propietario
func (s *SmartContract) GetPropertiesByOwner(
    ctx contractapi.TransactionContextInterface,
    owner string) ([]*Property, error) {

    queryString := fmt.Sprintf(`{
        "selector": {
            "docType": "property",
            "owner": "%s"
        },
        "use_index": "indexOwner"
    }`, owner)

    return s.executeQuery(ctx, queryString)
}

// Buscar propiedades por region
func (s *SmartContract) GetPropertiesByRegion(
    ctx contractapi.TransactionContextInterface,
    region string) ([]*Property, error) {

    queryString := fmt.Sprintf(`{
        "selector": {
            "docType": "property",
            "region": "%s"
        },
        "use_index": "indexRegion"
    }`, region)

    return s.executeQuery(ctx, queryString)
}

// Helper comun
func (s *SmartContract) executeQuery(
    ctx contractapi.TransactionContextInterface,
    queryString string) ([]*Property, error) {

    iterator, err := ctx.GetStub().GetQueryResult(queryString)
    if err != nil {
        return nil, err
    }
    defer iterator.Close()

    var properties []*Property
    for iterator.HasNext() {
        result, err := iterator.Next()
        if err != nil {
            return nil, err
        }
        var property Property
        if err := json.Unmarshal(result.Value, &property); err != nil {
            return nil, err
        }
        properties = append(properties, &property)
    }
    return properties, nil
}
```

### GetAll con paginación

```go
type PaginatedResult struct {
    Properties []*Property `json:"properties"`
    Bookmark   string      `json:"bookmark"`
    FetchedCount int32     `json:"fetchedCount"`
}

func (s *SmartContract) GetAllProperties(ctx contractapi.TransactionContextInterface,
    pageSize int32, bookmark string) (*PaginatedResult, error) {

    iterator, metadata, err := ctx.GetStub().GetStateByRangeWithPagination(
        "property_", "property_~", pageSize, bookmark)
    if err != nil {
        return nil, err
    }
    defer iterator.Close()

    var properties []*Property
    for iterator.HasNext() {
        result, err := iterator.Next()
        if err != nil {
            return nil, err
        }
        var property Property
        json.Unmarshal(result.Value, &property)
        properties = append(properties, &property)
    }

    return &PaginatedResult{
        Properties:   properties,
        Bookmark:     metadata.Bookmark,
        FetchedCount: metadata.FetchedRecordsCount,
    }, nil
}
```

### Historial de cambios

```go
func (s *SmartContract) GetPropertyHistory(
    ctx contractapi.TransactionContextInterface,
    id string) ([]map[string]interface{}, error) {

    iterator, err := ctx.GetStub().GetHistoryForKey("property_" + id)
    if err != nil {
        return nil, err
    }
    defer iterator.Close()

    var history []map[string]interface{}
    for iterator.HasNext() {
        record, err := iterator.Next()
        if err != nil {
            return nil, err
        }
        entry := map[string]interface{}{
            "txID":      record.TxId,
            "timestamp": record.Timestamp.AsTime().Format(time.RFC3339),
            "isDelete":  record.IsDelete,
        }
        if !record.IsDelete {
            var property Property
            json.Unmarshal(record.Value, &property)
            entry["value"] = property
        }
        history = append(history, entry)
    }
    return history, nil
}
```

---

## 6. Desplegar en test-network y probar

### Estructura del paquete

```
registro-propiedad/
├── go.mod
├── registro.go
└── META-INF/
    └── statedb/
        └── couchdb/
            └── indexes/
                ├── indexPropertyType.json
                ├── indexOwner.json
                └── indexRegion.json
```

### Levantar la red con CouchDB

```bash
cd $HOME/fabric/fabric-samples/test-network
./network.sh down
./network.sh up createChannel -s couchdb
```

El flag `-s couchdb` es clave — sin el, Fabric usa LevelDB por defecto y las rich queries no funcionan.

### Empaquetar, instalar, aprobar, commit

```bash
cd $HOME/fabric/fabric-samples/test-network

# Empaquetar
peer lifecycle chaincode package registro.tar.gz \
  --path ../registro-propiedad/ \
  --lang golang \
  --label registro_1.0

# (resto del lifecycle igual que en docs/04-chaincode-lifecycle.md)
./network.sh deployCC -ccn registro -ccp ../registro-propiedad -ccl go
```

### Probar

```bash
# Variables (como en el doc 04)
export ORDERER_CA=...
export PEER_ORG1_TLS=...
export PEER_ORG2_TLS=...

# Crear propiedad
peer chaincode invoke \
  -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
  --tls --cafile $ORDERER_CA \
  -C mychannel -n registro \
  --peerAddresses localhost:7051 --tlsRootCertFiles $PEER_ORG1_TLS \
  --peerAddresses localhost:9051 --tlsRootCertFiles $PEER_ORG2_TLS \
  -c '{"function":"CreateProperty","Args":["1234ABC","Calle Mayor 1, Madrid","12345678A","Javier Garcia","apartment","Madrid","Madrid","120","250000"]}'

# Leer propiedad
peer chaincode query -C mychannel -n registro \
  -c '{"Args":["ReadProperty","1234ABC"]}'

# Buscar por tipo y valor
peer chaincode query -C mychannel -n registro \
  -c '{"Args":["QueryPropertiesByTypeAndValue","apartment","100000","500000"]}'

# Buscar por propietario
peer chaincode query -C mychannel -n registro \
  -c '{"Args":["GetPropertiesByOwner","12345678A"]}'

# Buscar por region
peer chaincode query -C mychannel -n registro \
  -c '{"Args":["GetPropertiesByRegion","Madrid"]}'

# Actualizar valor
peer chaincode invoke ... \
  -c '{"function":"UpdateAppraisalValue","Args":["1234ABC","275000"]}'

# Ver historial
peer chaincode query -C mychannel -n registro \
  -c '{"Args":["GetPropertyHistory","1234ABC"]}'
```

---

## Preguntas para la puesta en común

1. ¿Que campos incluyes en `Property` que no estaban en el enunciado? ¿Por que?
2. ¿Que decisiones de key space habeis tomado? ¿Composite keys o no?
3. ¿Habeis elegido LevelDB o CouchDB? ¿Por que?
4. ¿Que queries son las mas útiles para un Registro de Propiedad real?
5. ¿Que pasa si dos personas intentan modificar la misma propiedad a la vez?
6. ¿Como gestionariais una transferencia de propiedad entre personas?
   (Este seria el tema del dia 3)

---

## Referencias

- Slides del dia 2: `docs/slides/Modulo 4/dia_2.pptx`
- Doc Chaincode Lifecycle: `docs/04-chaincode-lifecycle.md`
- Tutorial test-network: `docs/02-test-network.md`
- Ejemplo completo en producción (FidelityChain): `docs/modulo-6/03-chaincode.md`
