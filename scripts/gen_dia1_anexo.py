import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# 1. Portada
add_title_slide(prs, "Tokenizacion en\nHyperledger Fabric",
    "De tokens EVM a tokens enterprise en Fabric")

# 2. De EVM a Fabric
add_content_slide(prs, "De Ethereum a Fabric: cambio de paradigma", [
    "En Ethereum los tokens son Smart Contracts publicos (ERC-20, ERC-721, ERC-1155)",
    "Cualquiera puede crear, transferir y consultar tokens sin permiso",
    "En Fabric no existen estandares ERC: los tokens se implementan como chaincodes",
    "Fabric es permissioned: solo participantes autorizados operan con tokens",
    "No hay criptomoneda nativa: los tokens representan activos del mundo real",
    "La privacidad es nativa: canales y Private Data Collections",
])

# 3. Comparativa tabla
add_table_slide(prs, "Tokens: Ethereum vs Hyperledger Fabric",
    ["Aspecto", "Ethereum", "Hyperledger Fabric"],
    [
        ["Estandar", "ERC-20, ERC-721, ERC-1155", "No hay estandar oficial, se implementa via chaincode"],
        ["Permiso", "Permissionless: cualquiera puede crear tokens", "Permissioned: solo participantes autorizados"],
        ["Visibilidad", "Publica: todo el mundo ve los balances", "Privada: canales y Private Data"],
        ["Moneda nativa", "ETH para gas", "No hay moneda nativa"],
        ["Lenguaje", "Solidity / Vyper", "Go, Node.js, Java"],
        ["Identidad", "Direccion pseudonima", "Certificado X.509 con nombre y org"],
        ["Interoperabilidad", "Cualquier wallet/DEX", "Solo participantes de la red"],
        ["Caso de uso tipico", "DeFi, NFTs, especulacion", "Supply chain, bonos, fidelizacion"],
    ])

# 4. Tres formas de implementar tokens
add_content_slide(prs, "Tres formas de implementar tokens en Fabric", [
    "1. Chaincode custom: escribir tu propia logica de token desde cero",
    "2. Fabric Token SDK: libreria oficial con modelo UTXO",
    "3. Fabric Samples token-erc20: ejemplo oficial tipo ERC-20 con modelo de cuentas",
],
subbullets={
    0: ["Maximo control y flexibilidad",
        "Requiere implementar mint, transfer, balanceOf, allowance..."],
    1: ["Modelo UTXO similar a Bitcoin",
        "Soporta privacidad con tokens anonimos",
        "Mas complejo de entender pero mas potente"],
    2: ["El mas parecido a un ERC-20 de Ethereum",
        "Buen punto de partida para aprender",
        "Repositorio: fabric-samples/token-erc-20"],
})

# 5. Diagrama: Flujo de un token en Fabric
add_image_placeholder(prs, "Flujo de un token en Fabric",
    "[Diagrama: App cliente -> Gateway -> Peer (chaincode token) -> World State (balances)]",
    "Technical diagram showing token flow in Hyperledger Fabric: client app sends transaction proposal through Fabric Gateway to endorsing peer, chaincode executes token logic, world state updates balances. Clean flat design, dark teal color scheme, labeled arrows between components.")

# 6. Fabric Token SDK
add_content_slide(prs, "Fabric Token SDK: vision general", [
    "Libreria oficial de Hyperledger para gestion de tokens",
    "Modelo UTXO: cada token es una 'moneda' indivisible que se gasta completa",
    "Operaciones principales:",
    "Soporta tokens fungibles y no fungibles",
    "Permite anonimato: el emisor no sabe quien tiene los tokens",
    "Integracion con Fabric CA para identidades",
],
subbullets={
    2: ["Issue: crear nuevos tokens (equivalente a mint)",
        "Transfer: enviar tokens a otro participante",
        "Redeem: destruir tokens (equivalente a burn)",
        "List: consultar tokens propios"],
})

# 7. UTXO vs Account model
add_two_column_slide(prs, "UTXO vs Account Model",
    "Modelo UTXO (Token SDK)", [
        "Cada token es un 'billete' unico",
        "Para pagar, se 'gasta' el billete entero",
        "Si sobra, se crea un 'cambio'",
        "Mejor privacidad (no hay balance visible)",
        "Mas complejo de consultar",
        "",
        "Ejemplo: tienes un token de 100.",
        "Pagas 30 -> se destruye el de 100",
        "Se crean dos: uno de 30 (destino)",
        "y otro de 70 (tu cambio).",
    ],
    "Modelo de Cuentas (ERC-20 like)", [
        "Cada usuario tiene un balance numerico",
        "Transferir = restar de uno, sumar a otro",
        "Mas intuitivo y facil de consultar",
        "Menos privado (balances visibles)",
        "Similar a una cuenta bancaria",
        "",
        "Ejemplo: tienes balance = 100.",
        "Pagas 30 -> tu balance = 70",
        "Destino: su balance += 30",
        "Simple, directo.",
    ])

# 8. Imagen UTXO
add_image_placeholder(prs, "Modelo UTXO visualizado",
    "[Diagrama: Token de 100 se destruye, se crean token de 30 y token de 70]",
    "Clean infographic showing UTXO model: a single token worth 100 units splits into two tokens (30 and 70). Left side shows input token being consumed, right side shows two new output tokens created. Arrows indicate flow. Minimalist flat design, teal and white color scheme.")

# 9. Casos de uso enterprise
add_content_slide(prs, "Casos de uso: tokens enterprise en Fabric", [
    "Fidelizacion: puntos de un consorcio de empresas (aeroloineas, retail)",
    "Bonos tokenizados: emision, custodia y liquidacion entre bancos",
    "Supply chain: tokens que representan lotes de producto en transito",
    "Carbon credits: tokens que representan derechos de emision",
    "Pagos interbancarios: settlement instantaneo entre participantes",
    "Propiedad inmobiliaria: fracciones de un activo tokenizado",
])

# 10. Ejemplo: token de fidelizacion
add_content_slide(prs, "Ejemplo: Token de fidelizacion entre empresas", [
    "Escenario: tres empresas (hotel, aerolinea, tienda) comparten puntos",
    "Cada empresa es una organizacion en Fabric con su propio peer",
    "Un canal compartido con un chaincode de token fungible",
    "El hotel emite puntos al cliente por cada estancia",
    "El cliente gasta puntos en la tienda o en vuelos",
    "El chaincode valida: saldo suficiente, org autorizada, limites",
    "Liquidacion mensual entre empresas via el ledger compartido",
])

# 11. Ejemplo: bonos tokenizados
add_content_slide(prs, "Ejemplo: Bonos tokenizados en Fabric", [
    "Escenario: emision de un bono entre emisor, agente y custodios",
    "Cada participante es una org en Fabric",
    "Private Data: solo el emisor y el custodio ven los detalles del inversor",
    "Token no fungible: cada bono tiene numero serie, nominal, cupon, vencimiento",
    "Chaincode gestiona: emision, transferencia, pago de cupones, amortizacion",
    "Auditores acceden via canal separado con vista de solo lectura",
],
subbullets={
    4: ["Comparar con el bono Santander 2019 y EIB 2021 vistos en la sesion anterior"],
})

# 12. Fabric Samples: token-erc-20
add_content_slide(prs, "Fabric Samples: token-erc-20", [
    "Repositorio oficial: fabric-samples/token-erc-20",
    "Implementacion tipo ERC-20 adaptada a Fabric",
    "Funciones disponibles:",
    "Usa certificados X.509 para identificar al propietario (no direcciones)",
    "El minter se define por atributo en el certificado",
    "Ideal como punto de partida para tokens fungibles en Fabric",
],
subbullets={
    2: ["Mint(amount) - crear tokens (solo minter autorizado)",
        "Transfer(to, amount) - transferir tokens",
        "BalanceOf(account) - consultar saldo",
        "Approve(spender, amount) + TransferFrom - delegacion",
        "TotalSupply() - supply total emitido"],
})

# 13. Snippet ERC-20 en Fabric
add_code_slide(prs, "Token ERC-20 en Fabric: snippet", """
// Transfer moves tokens from caller to recipient
func (s *SmartContract) Transfer(ctx contractapi.TransactionContextInterface,
    recipient string, amount int) error {

    clientID, err := ctx.GetClientIdentity().GetID()
    if err != nil {
        return fmt.Errorf("failed to get client identity: %v", err)
    }

    err = transferHelper(ctx, clientID, recipient, amount)
    if err != nil {
        return fmt.Errorf("failed to transfer: %v", err)
    }

    // Emit Transfer event
    transferEvent := TransferEvent{From: clientID, To: recipient, Value: amount}
    eventJSON, _ := json.Marshal(transferEvent)
    ctx.GetStub().SetEvent("Transfer", eventJSON)

    return nil
}""", language="go", subtitle="Funcion Transfer del token-erc-20 oficial de Fabric Samples")

# 14. Debate
add_debate_slide(prs, "Tokenizacion en Fabric", [
    "1. En Ethereum cualquiera puede crear un token. En Fabric solo los autorizados. ¿Es esto una ventaja o una limitacion?",
    "2. ¿Que tipo de activos de vuestra empresa/sector se beneficiarian de la tokenizacion en una red permissioned?",
    "3. ¿Modelo UTXO o modelo de cuentas? ¿Cual elegiriais para vuestro caso de uso y por que?",
    "4. Los tokens en Fabric no cotizan en exchanges. ¿Pierde sentido la tokenizacion sin mercado secundario?",
    "5. ¿Como afecta la privacidad de Fabric (canales, Private Data) al diseno de un token enterprise?",
])

# 15. Repaso
add_review_slide(prs, "Repaso del dia", [
    "¿Cual es la principal diferencia entre tokens en Ethereum y en Fabric?",
    "Nombra tres formas de implementar tokens en Fabric",
    "¿Que es el modelo UTXO y en que se diferencia del modelo de cuentas?",
    "¿Que operaciones soporta el Fabric Token SDK?",
    "¿Por que Fabric no tiene moneda nativa como ETH?",
    "Da un ejemplo de token enterprise que tenga sentido en Fabric",
    "¿Que ventaja ofrece la privacidad de Fabric para tokens enterprise?",
])

prs.save(f"{OUT_DIR}/dia1_anexo.pptx")
print("dia1_anexo.pptx generado OK")
