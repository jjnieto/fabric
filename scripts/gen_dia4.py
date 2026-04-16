import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

add_title_slide(prs, "Implementacion de Tokens\nen Fabric",
    "Dia 4 - Tokens fungibles, no fungibles y trazabilidad alimentaria")

add_review_slide(prs, "Repaso del dia anterior", [
    "¿Como se controla el acceso por organizacion en un chaincode?",
    "¿Que es ABAC y como se implementa?",
    "¿Para que sirven las Private Data Collections?",
    "¿Como se emiten eventos desde un chaincode?",
])

# Cultura General
add_special_slide(prs, "CULTURA GENERAL", "Nick Szabo y los Smart Contracts (1994)", [
    "Nick Szabo es un informatico y criptografo que en 1994 propuso el concepto de 'smart contract'.",
    "Su idea: codificar clausulas contractuales en software que se ejecute automaticamente.",
    "El ejemplo que usaba: una maquina expendedora es un smart contract primitivo.",
    "  - Introduces monedas (input), seleccionas producto (condicion), recibes el producto (ejecucion).",
    "  - No necesitas un intermediario: la maquina ejecuta el contrato.",
    "",
    "Szabo tambien propuso 'Bit Gold' en 1998, un precursor de Bitcoin.",
    "Muchos especulan que podria ser Satoshi Nakamoto, aunque el lo ha negado.",
    "",
    "Curiosidad: en Fabric los smart contracts se llaman 'chaincodes',",
    "pero la idea subyacente es la misma que Szabo propuso hace 30 anos.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

# Tokens fungibles
add_section_slide(prs, "Tokens Fungibles en Fabric", "Implementacion tipo ERC-20 con modelo de cuentas")

add_content_slide(prs, "Token fungible: diseno del modelo", [
    "Un token fungible en Fabric se implementa como un chaincode con:",
    "Modelo de datos:",
    "Funciones principales:",
    "Identidad: el propietario se identifica por su certificado X.509, no por una direccion",
],
subbullets={
    1: ["Un balance por cada participante (key: clientID, value: amount)",
        "Un registro de allowances para delegacion (key: owner|spender, value: amount)",
        "Metadata del token: nombre, simbolo, decimales, totalSupply"],
    2: ["Mint(amount) - crear tokens (solo minter autorizado)",
        "Burn(amount) - destruir tokens propios",
        "Transfer(to, amount) - enviar tokens",
        "BalanceOf(owner) - consultar saldo",
        "Approve(spender, amount) + TransferFrom(from, to, amount) - delegacion",
        "TotalSupply() - supply total"],
})

add_code_slide(prs, "Token fungible: Mint", """
func (s *SmartContract) Mint(ctx contractapi.TransactionContextInterface,
    amount int) error {

    // Solo el minter puede crear tokens
    err := ctx.GetClientIdentity().AssertAttributeValue("role", "minter")
    if err != nil {
        return fmt.Errorf("solo el minter puede emitir tokens")
    }

    if amount <= 0 {
        return fmt.Errorf("amount debe ser positivo")
    }

    // Obtener ID del minter
    minterID, _ := ctx.GetClientIdentity().GetID()

    // Actualizar balance
    currentBalance, _ := getBalance(ctx, minterID)
    newBalance := currentBalance + amount
    err = ctx.GetStub().PutState(balanceKey(minterID),
        []byte(strconv.Itoa(newBalance)))

    // Actualizar totalSupply
    supply, _ := getTotalSupply(ctx)
    ctx.GetStub().PutState("totalSupply",
        []byte(strconv.Itoa(supply + amount)))

    // Evento
    ctx.GetStub().SetEvent("Mint",
        []byte(fmt.Sprintf(`{"minter":"%s","amount":%d}`, minterID, amount)))
    return err
}""", language="go", subtitle="Crear tokens: verificar rol, actualizar balance y totalSupply")

add_code_slide(prs, "Token fungible: Transfer", """
func (s *SmartContract) Transfer(ctx contractapi.TransactionContextInterface,
    to string, amount int) error {

    if amount <= 0 {
        return fmt.Errorf("amount debe ser positivo")
    }

    fromID, _ := ctx.GetClientIdentity().GetID()
    if fromID == to {
        return fmt.Errorf("no puedes transferirte a ti mismo")
    }

    // Verificar saldo
    fromBalance, _ := getBalance(ctx, fromID)
    if fromBalance < amount {
        return fmt.Errorf("saldo insuficiente: tiene %d, necesita %d",
            fromBalance, amount)
    }

    // Actualizar balances
    toBalance, _ := getBalance(ctx, to)
    ctx.GetStub().PutState(balanceKey(fromID),
        []byte(strconv.Itoa(fromBalance - amount)))
    ctx.GetStub().PutState(balanceKey(to),
        []byte(strconv.Itoa(toBalance + amount)))

    // Evento
    ctx.GetStub().SetEvent("Transfer",
        []byte(fmt.Sprintf(`{"from":"%s","to":"%s","amount":%d}`,
            fromID, to, amount)))
    return nil
}""", language="go", subtitle="Verificar saldo, restar y sumar atomicamente")

add_code_slide(prs, "Token fungible en Node.js", """
async Transfer(ctx, to, amount) {
    amount = parseInt(amount);
    if (amount <= 0) throw new Error('Amount must be positive');

    const fromID = ctx.clientIdentity.getID();
    if (fromID === to) throw new Error('Cannot transfer to yourself');

    // Read balances
    const fromBalance = await this._getBalance(ctx, fromID);
    if (fromBalance < amount) {
        throw new Error(
            `Insufficient balance: has ${fromBalance}, needs ${amount}`);
    }
    const toBalance = await this._getBalance(ctx, to);

    // Update balances
    await ctx.stub.putState(
        this._balanceKey(fromID),
        Buffer.from((fromBalance - amount).toString()));
    await ctx.stub.putState(
        this._balanceKey(to),
        Buffer.from((toBalance + amount).toString()));

    // Emit event
    ctx.stub.setEvent('Transfer', Buffer.from(JSON.stringify({
        from: fromID, to, amount
    })));
}""", language="node.js", subtitle="Misma logica en JavaScript")

# Tokens no fungibles
add_section_slide(prs, "Tokens No Fungibles en Fabric", "Activos unicos con composite keys")

add_content_slide(prs, "Token no fungible: diseno", [
    "Cada token es un activo unico con su propia identidad",
    "No se divide ni se suma: se transfiere entero",
    "En Fabric se implementa con composite keys:",
    "Funciones tipicas:",
    "Diferencia con ERC-721: en Fabric la identidad es un cert X.509, no una direccion",
],
subbullets={
    2: ["Key: nft~owner~tokenID (permite buscar por owner)",
        "Key: nft~tokenID (permite buscar por ID directo)",
        "Cada token tiene metadata unica (JSON)"],
    3: ["MintNFT(tokenID, metadata) - crear un NFT",
        "TransferNFT(tokenID, newOwner) - transferir",
        "GetNFT(tokenID) - leer metadata",
        "GetNFTsByOwner(owner) - listar NFTs de un propietario"],
})

add_code_slide(prs, "NFT en Fabric: Mint y Transfer", """
type NFT struct {
    DocType     string            `json:"docType"`
    TokenID     string            `json:"tokenID"`
    Owner       string            `json:"owner"`
    Metadata    map[string]string `json:"metadata"`
    CreatedAt   string            `json:"createdAt"`
}

func (s *SmartContract) MintNFT(ctx contractapi.TransactionContextInterface,
    tokenID string, metadataJSON string) error {

    // Verificar que no existe
    existing, _ := ctx.GetStub().GetState("nft_" + tokenID)
    if existing != nil {
        return fmt.Errorf("NFT %s ya existe", tokenID)
    }

    ownerID, _ := ctx.GetClientIdentity().GetID()
    var metadata map[string]string
    json.Unmarshal([]byte(metadataJSON), &metadata)

    nft := NFT{
        DocType: "nft", TokenID: tokenID,
        Owner: ownerID, Metadata: metadata,
    }
    nftJSON, _ := json.Marshal(nft)

    // Guardar por tokenID y crear indice por owner
    ctx.GetStub().PutState("nft_"+tokenID, nftJSON)
    ownerKey, _ := ctx.GetStub().CreateCompositeKey("nftOwner",
        []string{ownerID, tokenID})
    return ctx.GetStub().PutState(ownerKey, []byte{0x00})
}""", language="go")

# Trazabilidad alimentaria
add_section_slide(prs, "Caso practico:\nTrazabilidad Alimentaria", "De la granja a la mesa con tokens en Fabric")

add_content_slide(prs, "Trazabilidad alimentaria: el problema", [
    "Un producto alimentario pasa por multiples etapas y actores:",
    "Problemas actuales:",
    "Blockchain Fabric resuelve:",
],
subbullets={
    0: ["Productor (granja) -> Procesador -> Distribuidor -> Minorista -> Consumidor",
        "Cada actor es una organizacion distinta en la red Fabric"],
    1: ["Falta de visibilidad: ¿de donde viene este producto?",
        "Lentitud en recalls: semanas para rastrear un lote contaminado",
        "Fraude: etiquetas falsas de origen o de organico",
        "Falta de confianza entre actores de la cadena"],
    2: ["Registro inmutable de cada movimiento del lote",
        "Trazabilidad instantanea (caso Walmart: 7 dias -> 2.2 segundos)",
        "Cada organizacion mantiene su peer y valida las transacciones",
        "Private Data para informacion comercial sensible (precios, margenes)"],
})

add_image_placeholder(prs, "Diagrama: Red Fabric para trazabilidad",
    "[Diagrama: 5 organizaciones conectadas via Fabric con un canal compartido]",
    "Network diagram showing 5 organizations in a Hyperledger Fabric network for food traceability: Farm, Processor, Distributor, Retailer, and Regulator. Each with a peer node, connected through a shared channel. Orderer service in the center. Clean flat design, teal color scheme, food supply chain icons.")

add_content_slide(prs, "Modelo de datos: FoodLot (lote alimentario)", [
    "Cada lote de producto es un token no fungible con trazabilidad",
    "Campos del lote:",
    "Key design: lot~productType~origin~lotID",
    "Permite buscar: todos los lotes de un tipo, de un origen, o un lote especifico",
],
subbullets={
    1: ["lotID: identificador unico del lote",
        "productType: tipo de producto (mango, lechuga, pollo...)",
        "origin: pais/region de origen",
        "currentHolder: organizacion que posee el lote actualmente (MSPID)",
        "status: produced | processed | in_transit | delivered | recalled",
        "temperature: ultima temperatura registrada (cold chain)",
        "timestamps: fecha de cada transicion de estado",
        "history: array de {org, action, timestamp} para trazabilidad completa"],
})

add_code_slide(prs, "FoodLot: estructura y creacion", """
type FoodLot struct {
    DocType       string       `json:"docType"`
    LotID         string       `json:"lotID"`
    ProductType   string       `json:"productType"`
    Origin        string       `json:"origin"`
    CurrentHolder string       `json:"currentHolder"`
    Status        string       `json:"status"`
    Temperature   float64      `json:"temperature"`
    Weight        float64      `json:"weight"`
    History       []HistEntry  `json:"history"`
}

type HistEntry struct {
    Org       string `json:"org"`
    Action    string `json:"action"`
    Timestamp string `json:"timestamp"`
    Location  string `json:"location"`
}

func (s *SmartContract) ProduceLot(ctx contractapi.TransactionContextInterface,
    lotID, productType, origin string, weight float64) error {
    producerMSP, _ := ctx.GetClientIdentity().GetMSPID()
    lot := FoodLot{
        DocType: "foodlot", LotID: lotID, ProductType: productType,
        Origin: origin, CurrentHolder: producerMSP, Status: "produced",
        Weight: weight,
        History: []HistEntry{{Org: producerMSP, Action: "produced",
            Timestamp: time.Now().Format(time.RFC3339)}},
    }
    lotJSON, _ := json.Marshal(lot)
    return ctx.GetStub().PutState("lot_"+lotID, lotJSON)
}""", language="go")

add_code_slide(prs, "FoodLot: transferencia entre actores", """
func (s *SmartContract) TransferLot(ctx contractapi.TransactionContextInterface,
    lotID string, newHolder string, location string, temp float64) error {

    lot, err := s.ReadLot(ctx, lotID)
    if err != nil {
        return err
    }

    // Solo el holder actual puede transferir
    callerMSP, _ := ctx.GetClientIdentity().GetMSPID()
    if lot.CurrentHolder != callerMSP {
        return fmt.Errorf("solo %s puede transferir este lote", lot.CurrentHolder)
    }

    // Validar cold chain: alerta si temperatura fuera de rango
    if temp > 8.0 {
        lot.Status = "temp_alert"
        // No se bloquea, pero se registra la alerta
    } else {
        lot.Status = "in_transit"
    }

    // Actualizar holder y registrar en historial
    lot.CurrentHolder = newHolder
    lot.Temperature = temp
    lot.History = append(lot.History, HistEntry{
        Org: callerMSP, Action: "transferred_to_" + newHolder,
        Timestamp: time.Now().Format(time.RFC3339),
        Location: location,
    })

    lotJSON, _ := json.Marshal(lot)
    ctx.GetStub().SetEvent("LotTransferred",
        []byte(fmt.Sprintf(`{"lotID":"%s","to":"%s"}`, lotID, newHolder)))
    return ctx.GetStub().PutState("lot_"+lotID, lotJSON)
}""", language="go", subtitle="Registrar cada movimiento con temperatura y ubicacion")

add_code_slide(prs, "FoodLot: trazabilidad completa", """
// Consultar la trazabilidad completa de un lote
func (s *SmartContract) GetLotHistory(ctx contractapi.TransactionContextInterface,
    lotID string) ([]HistEntry, error) {

    lot, err := s.ReadLot(ctx, lotID)
    if err != nil {
        return nil, err
    }
    return lot.History, nil
}

// Recall: retirar un lote del mercado
func (s *SmartContract) RecallLot(ctx contractapi.TransactionContextInterface,
    lotID string, reason string) error {

    // Solo el regulador puede hacer recall
    err := ctx.GetClientIdentity().AssertAttributeValue("role", "regulador")
    if err != nil {
        return fmt.Errorf("solo el regulador puede retirar lotes")
    }

    lot, err := s.ReadLot(ctx, lotID)
    if err != nil {
        return err
    }
    lot.Status = "recalled"
    lot.History = append(lot.History, HistEntry{
        Org: "Regulador", Action: "recalled: " + reason,
        Timestamp: time.Now().Format(time.RFC3339),
    })

    lotJSON, _ := json.Marshal(lot)
    ctx.GetStub().SetEvent("LotRecalled",
        []byte(fmt.Sprintf(`{"lotID":"%s","reason":"%s"}`, lotID, reason)))
    return ctx.GetStub().PutState("lot_"+lotID, lotJSON)
}""", language="go", subtitle="Historial completo y recall por el regulador")

# Practica
add_activity_slide(prs, "Token de trazabilidad alimentaria", [
    "Objetivo: implementar el chaincode completo de FoodLot",
    "",
    "Organizaciones en la test-network:",
    "  - Org1: Productor (granja)",
    "  - Org2: Distribuidor/Minorista",
    "",
    "Flujo a implementar:",
    "  1. Org1 crea un lote (ProduceLot)",
    "  2. Org1 transfiere a Org2 (TransferLot) con temperatura",
    "  3. Org2 confirma recepcion (UpdateStatus -> delivered)",
    "  4. Consultar trazabilidad completa del lote (GetLotHistory)",
    "  5. [Bonus] Implementar recall y busqueda por productType",
    "",
    "  Usar el prompt de IA para generar la base.",
    "  Tiempo: 90 minutos.",
])

add_prompt_slide(prs, "Prompt IA: Chaincode de trazabilidad alimentaria",
    """Genera un chaincode de Hyperledger Fabric en [Go/Node.js]
para trazabilidad alimentaria con estas especificaciones:

- Modelo FoodLot: lotID, productType, origin, currentHolder,
  status (produced|processed|in_transit|delivered|recalled),
  temperature, weight, history (array de movimientos)
- Funciones: ProduceLot, TransferLot (con temp y location),
  UpdateStatus, GetLotHistory, RecallLot, QueryByProductType
- Control de acceso: solo currentHolder transfiere,
  solo role=regulador puede hacer recall
- Eventos: LotProduced, LotTransferred, LotRecalled
- Validacion de cold chain: alerta si temp > 8 grados
- Rich query CouchDB: buscar por productType y por status
- Incluir comentarios en espanol. Fabric 2.5.x.""")

add_debate_slide(prs, "Trazabilidad en blockchain", [
    "1. ¿Que pasa si alguien introduce datos falsos en el origen (basura in, basura out)?",
    "2. ¿Como combinar Fabric con IoT (sensores de temperatura) para automatizar registros?",
    "3. El consumidor final no tiene peer ni certificado. ¿Como verificaria el origen de su producto?",
    "4. ¿Que datos deberian ser privados (Private Data) y cuales publicos en este caso?",
    "5. ¿Tiene sentido usar tokens fungibles para representar kilos de producto? ¿O solo NFTs por lote?",
])

add_review_slide(prs, "Repaso del dia", [
    "¿Como se implementa un token fungible en Fabric (tipo ERC-20)?",
    "¿Que funciones basicas tiene: Mint, Transfer, BalanceOf...?",
    "¿Como se diferencia un token no fungible de uno fungible en Fabric?",
    "¿Que es una composite key y como ayuda en NFTs?",
    "Describe el flujo de trazabilidad de un lote alimentario",
    "¿Quien puede hacer recall y por que?",
    "¿Como se registra el historial de movimientos de un lote?",
])

prs.save(f"{OUT_DIR}/dia_4.pptx")
print("dia_4.pptx generado OK")
