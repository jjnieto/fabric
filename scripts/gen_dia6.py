import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

add_title_slide(prs, "Integracion y\nProyecto Final",
    "Dia 6 - Fabric Gateway SDK, testing y proyecto de trazabilidad")

add_review_slide(prs, "Repaso del dia anterior", [
    "¿Que es una politica de endorsement state-based?",
    "Nombra 3 errores de determinismo en chaincodes",
    "¿Que es un conflicto MVCC?",
    "¿Como se migran datos al actualizar un chaincode?",
])

# Cultura General
add_special_slide(prs, "CULTURA GENERAL", "Tim Berners-Lee y la descentralizacion", [
    "Tim Berners-Lee invento la World Wide Web en 1989 en el CERN.",
    "Su vision original era una web descentralizada donde cada persona controlara sus datos.",
    "30 anos despues, la web esta dominada por unos pocos gigantes (Google, Meta, Amazon).",
    "",
    "En 2018, Berners-Lee lanzo Solid, un proyecto para devolver el control de los datos",
    "a los usuarios, usando 'pods' personales de datos.",
    "",
    "Conexion con Fabric: la idea de que los participantes controlen sus propios datos",
    "sin depender de un intermediario central es la misma que motiva blockchain enterprise.",
    "Fabric va un paso mas alla: no solo controlas tus datos, sino que puedes verificar",
    "criptograficamente que los datos de los demas son correctos.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

# Gateway SDK
add_section_slide(prs, "Fabric Gateway SDK", "Conectar aplicaciones cliente con la red Fabric")

add_content_slide(prs, "Fabric Gateway SDK: vision general", [
    "El Gateway SDK es la forma estandar de conectar una app con Fabric",
    "Disponible en Node.js, Go y Java",
    "Reemplaza al antiguo Fabric SDK (mucho mas complejo)",
    "Flujo simplificado:",
    "El Gateway se encarga de: descubrimiento de peers, endorsement, ordering y commit",
],
subbullets={
    3: ["1. Cargar identidad (certificado + clave privada) desde wallet",
        "2. Conectar al Gateway (apuntando a un peer de tu org)",
        "3. Obtener referencia al canal y al contrato",
        "4. Invocar funciones: submit (escritura) o evaluate (lectura)",
        "5. Desconectar"],
})

add_code_slide(prs, "Gateway SDK: conexion en Node.js", """
const { Gateway, Wallets } = require('fabric-network');
const path = require('path');
const fs = require('fs');

async function main() {
    // 1. Cargar connection profile
    const ccpPath = path.resolve(__dirname, 'connection-org1.json');
    const ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));

    // 2. Cargar identidad desde wallet
    const walletPath = path.join(__dirname, 'wallet');
    const wallet = await Wallets.newFileSystemWallet(walletPath);

    // 3. Conectar al Gateway
    const gateway = new Gateway();
    await gateway.connect(ccp, {
        wallet,
        identity: 'appUser',
        discovery: { enabled: true, asLocalhost: true }
    });

    // 4. Obtener canal y contrato
    const network = await gateway.getNetwork('mychannel');
    const contract = network.getContract('foodtrace');

    // 5. Invocar funciones
    const result = await contract.evaluateTransaction('GetAllLots');
    console.log(JSON.parse(result.toString()));

    gateway.disconnect();
}""", language="node.js", subtitle="Conexion completa: wallet -> gateway -> contrato")

add_code_slide(prs, "Gateway SDK: submit vs evaluate", """
// EVALUATE: solo lectura, no genera transaccion en el ledger
// Se ejecuta en UN solo peer (rapido)
const result = await contract.evaluateTransaction('ReadProperty', 'PROP001');
const property = JSON.parse(result.toString());
console.log(property);

// SUBMIT: escritura, genera transaccion completa
// Endorse -> Order -> Commit (mas lento, modifica el ledger)
await contract.submitTransaction('CreateProperty',
    'PROP002', 'Calle Mayor 1', 'Org1MSP', '120', 'apartment', '250000');

// SUBMIT con transient data (para Private Data)
const transientData = {
    price: Buffer.from(JSON.stringify({ amount: 350000, currency: 'EUR' }))
};
await contract.createTransaction('SetPrivatePrice')
    .setTransient(transientData)
    .submit('PROP001');

// Escuchar eventos
await contract.addContractListener(async (event) => {
    console.log(`Evento: ${event.eventName}`);
    console.log(`Payload: ${event.payload.toString()}`);
});""", language="node.js", subtitle="Lectura (evaluate) vs escritura (submit) + eventos")

add_code_slide(prs, "Gateway SDK: conexion en Go", """
package main

import (
    "github.com/hyperledger/fabric-gateway/pkg/client"
    "google.golang.org/grpc"
    "crypto/x509"
)

func main() {
    // 1. Conexion gRPC al peer
    clientConnection, _ := grpc.NewClient("localhost:7051", grpc.WithTransportCredentials(...))
    defer clientConnection.Close()

    // 2. Crear identidad
    id := client.NewX509Identity("Org1MSP", certificate)
    sign, _ := client.NewSign(privateKey)

    // 3. Conectar al Gateway
    gw, _ := client.Connect(id, client.WithSign(sign),
        client.WithClientConnection(clientConnection))
    defer gw.Close()

    // 4. Obtener canal y contrato
    network := gw.GetNetwork("mychannel")
    contract := network.GetContract("foodtrace")

    // 5. Evaluar (lectura)
    result, _ := contract.EvaluateTransaction("GetAllLots")

    // 6. Submit (escritura)
    _, err := contract.SubmitTransaction("ProduceLot",
        "LOT-001", "mango", "Spain", "500.0")
}""", language="go", subtitle="Misma estructura: conectar, obtener contrato, invocar")

# Identity wallet
add_content_slide(prs, "Identity Wallet: gestion de identidades", [
    "La wallet almacena las identidades (cert + clave privada) de los usuarios",
    "Tipos de wallet en el SDK:",
    "En produccion: usar HSM o sistema de gestion de secretos (Vault)",
    "En desarrollo: FileSystemWallet es suficiente",
    "Importante: la wallet NO es como MetaMask",
],
subbullets={
    1: ["FileSystemWallet: archivos en disco (desarrollo)",
        "InMemoryWallet: en memoria (testing)",
        "CouchDBWallet: en CouchDB (produccion ligera)",
        "HSMWallet: Hardware Security Module (produccion enterprise)"],
    4: ["En EVM, la wallet tiene una clave privada que genera una direccion",
        "En Fabric, la wallet tiene un certificado X.509 emitido por una CA",
        "El certificado contiene: nombre, organizacion, rol, atributos"],
})

add_image_placeholder(prs, "Diagrama: Flujo completo de una app Fabric",
    "[Diagrama: App -> Wallet -> Gateway -> Peer -> Chaincode -> World State]",
    "Architecture diagram showing complete Fabric application flow: Client App loads identity from Wallet, connects through Gateway to Peer node, Peer executes Chaincode which reads/writes World State. Include Orderer for transaction ordering. Clean flat design, teal color scheme, labeled arrows showing data flow.")

# Testing
add_section_slide(prs, "Testing de Chaincodes", "Unit tests, mocks y tests de integracion")

add_content_slide(prs, "Estrategia de testing", [
    "Tres niveles de testing para chaincodes:",
    "En el curso nos centramos en unit tests e integracion basica",
    "Herramientas:",
],
subbullets={
    0: ["Unit tests: probar funciones individuales con mocks del stub",
        "Integration tests: probar contra una red real (test-network)",
        "End-to-end: probar la app completa (cliente + chaincode + red)"],
    2: ["Go: testing package + mockery/counterfeiter para generar mocks",
        "Node.js: Jest/Mocha + sinon para mocks",
        "Fabric: fabric-samples tiene ejemplos de tests en ambos lenguajes"],
})

add_code_slide(prs, "Unit test con mock del Stub (Go)", """
func TestCreateProperty(t *testing.T) {
    // Crear mock del TransactionContext y del Stub
    mockCtx := new(mocks.TransactionContext)
    mockStub := new(mocks.ChaincodeStub)
    mockIdentity := new(mocks.ClientIdentity)

    mockCtx.On("GetStub").Return(mockStub)
    mockCtx.On("GetClientIdentity").Return(mockIdentity)
    mockIdentity.On("GetMSPID").Return("Org1MSP", nil)
    mockIdentity.On("AssertAttributeValue", "role", "registrador").
        Return(nil)

    // GetState devuelve nil (propiedad no existe)
    mockStub.On("GetState", "PROP001").Return(nil, nil)
    // PutState acepta cualquier valor
    mockStub.On("PutState", "PROP001", mock.Anything).Return(nil)

    // Ejecutar
    contract := SmartContract{}
    err := contract.CreateProperty(mockCtx,
        "PROP001", "Calle Mayor 1", "Org1MSP", 120, "apartment", 250000)

    // Verificar
    assert.NoError(t, err)
    mockStub.AssertCalled(t, "PutState", "PROP001", mock.Anything)
}""", language="go", subtitle="Mockear Stub, Identity y verificar llamadas")

add_code_slide(prs, "Unit test con mock (Node.js)", """
const { expect } = require('chai');
const sinon = require('sinon');
const { AssetContract } = require('../lib/assetContract');

describe('AssetContract', () => {
    let contract;
    let ctx;

    beforeEach(() => {
        contract = new AssetContract();
        ctx = {
            stub: {
                getState: sinon.stub(),
                putState: sinon.stub(),
                setEvent: sinon.stub(),
            },
            clientIdentity: {
                getMSPID: sinon.stub().returns('Org1MSP'),
                getID: sinon.stub().returns('user1'),
                getAttributeValue: sinon.stub().returns(['registrador', true]),
            },
        };
    });

    it('should create a property', async () => {
        ctx.stub.getState.resolves(null); // No existe
        await contract.CreateProperty(ctx,
            'PROP001', 'Calle Mayor 1', 'Org1MSP', '120', 'apartment', '250000');

        expect(ctx.stub.putState.calledOnce).to.be.true;
        const savedData = JSON.parse(ctx.stub.putState.firstCall.args[1]);
        expect(savedData.id).to.equal('PROP001');
    });
});""", language="node.js", subtitle="Sinon para mocks, Chai para assertions")

add_prompt_slide(prs, "Prompt IA: Generar tests para un chaincode",
    """Genera una suite de unit tests para el siguiente chaincode
de Hyperledger Fabric en [Go/Node.js].

El chaincode tiene las funciones:
- CreateProperty(id, address, owner, area, propertyType, value)
- ReadProperty(id)
- TransferProperty(id, newOwner)
- UpdatePropertyValue(id, newValue)
- GetAllProperties(pageSize, bookmark)

Para cada funcion genera tests que cubran:
1. Caso exitoso (happy path)
2. Caso de error: activo no existe
3. Caso de error: permisos insuficientes
4. Caso de error: inputs invalidos

Usa mocks para el Stub y ClientIdentity.
[Go: mockery/testify] [Node.js: sinon/chai]

[Pegar aqui el codigo del chaincode]""")

# Proyecto final
add_section_slide(prs, "Proyecto Final:\nTrazabilidad Alimentaria", "Integrando todo lo aprendido en el modulo")

add_content_slide(prs, "Proyecto final: alcance", [
    "Objetivo: construir un sistema completo de trazabilidad alimentaria",
    "Componentes a entregar:",
    "Organizaciones:",
    "Tiempo: resto de la sesion + presentacion al final",
],
subbullets={
    1: ["1. Chaincode de FoodLot (Go o Node.js) - desarrollado en dia 4",
        "2. App cliente con Gateway SDK (Node.js o Go)",
        "3. Tests unitarios para las funciones principales",
        "4. Despliegue en test-network funcionando",
        "5. Demo de trazabilidad completa de un lote"],
    2: ["Org1: Productor (crea lotes, registra origen)",
        "Org2: Distribuidor (recibe lotes, registra transporte)"],
})

add_activity_slide(prs, "Proyecto: setup y desarrollo", [
    "Paso 1: Preparar el chaincode (15 min)",
    "  - Partir del chaincode FoodLot del dia 4",
    "  - Anadir funciones que falten: QueryByProduct, GetHistory",
    "  - Verificar checklist de seguridad del dia 5",
    "",
    "Paso 2: Desplegar en test-network (15 min)",
    "  - ./network.sh up createChannel",
    "  - Desplegar chaincode con lifecycle",
    "  - Verificar con peer chaincode invoke",
    "",
    "Paso 3: Crear app cliente (45 min)",
    "  - Usar Gateway SDK para conectar al chaincode",
    "  - Implementar flujo: crear lote -> transferir -> consultar historial",
    "  - Escuchar eventos de transferencia",
])

add_activity_slide(prs, "Proyecto: testing y demo", [
    "Paso 4: Tests unitarios (20 min)",
    "  - Crear tests para ProduceLot, TransferLot, GetHistory",
    "  - Al menos un test de permisos (solo holder transfiere)",
    "",
    "Paso 5: Demo de trazabilidad completa (15 min por pareja)",
    "  - Mostrar el flujo completo:",
    "    1. Org1 crea lote de mangos de Malaga",
    "    2. Org1 transfiere a Org2 con temperatura 4C",
    "    3. Org2 confirma recepcion",
    "    4. Consultar trazabilidad: se ve todo el historial",
    "    5. [Bonus] Org2 reporta alerta de temperatura",
    "    6. [Bonus] Regulador hace recall del lote",
    "",
    "  Presentar: decisiones de diseno, problemas encontrados, soluciones.",
])

add_prompt_slide(prs, "Prompt IA: App cliente con Gateway SDK",
    """Genera una aplicacion cliente Node.js para Hyperledger Fabric
que se conecte a un chaincode de trazabilidad alimentaria
llamado 'foodtrace' en el canal 'mychannel'.

La aplicacion debe:
1. Conectar al Gateway usando connection profile de Org1
2. Cargar identidad desde wallet (FileSystemWallet)
3. Implementar funciones para:
   - Crear un lote (ProduceLot)
   - Transferir un lote (TransferLot)
   - Consultar historial (GetLotHistory)
   - Listar todos los lotes (GetAllLots)
4. Escuchar eventos de LotTransferred
5. Mostrar resultados por consola de forma legible

Usa fabric-network SDK. El connection profile esta en
test-network/organizations/peerOrganizations/.
Incluye comentarios en espanol.""")

# Debate de cierre
add_debate_slide(prs, "Cierre del Modulo 4", [
    "1. ¿Que ha sido lo mas complejo de este modulo? ¿Y lo mas util?",
    "2. ¿Veis aplicacion real en vuestro sector para los tokens en Fabric?",
    "3. ¿Que echais en falta en Fabric comparado con Ethereum? ¿Y al reves?",
    "4. Si tuvierais que empezar un proyecto real manana, ¿que arquitectura elegiriais?",
    "5. ¿Que papel creeis que jugara la IA en el desarrollo de chaincodes?",
])

# Repaso del modulo
add_review_slide(prs, "Repaso del Modulo 4", [
    "Tokenizacion en Fabric vs Ethereum: principales diferencias",
    "Tres formas de implementar tokens en Fabric",
    "Anatomia de un chaincode: struct, Contract API, Stub",
    "Patron CRUD y modelado de datos (JSON, composite keys)",
    "Control de acceso: MSPID y ABAC",
    "Private Data Collections: concepto y uso",
    "Tokens fungibles (tipo ERC-20) y no fungibles en Fabric",
    "Seguridad: determinismo, MVCC, checklist",
    "Gateway SDK: conectar apps con la red",
    "Testing: unit tests con mocks",
])

prs.save(f"{OUT_DIR}/dia_6.pptx")
print("dia_6.pptx generado OK")
