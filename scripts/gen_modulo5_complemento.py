import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# ============================================================
# PORTADA
# ============================================================
add_title_slide(prs, "Identidad Digital:\nAlastria, EBSI y\nArquitecturas Hibridas",
    "Ecosistemas reales, integracion empresarial y conexion con Hyperledger Fabric",
    module="Modulo 5: Identidad Digital (parte 2)")

# ============================================================
# SECCION 1: EBSI
# ============================================================
add_section_slide(prs, "EBSI\nEuropean Blockchain\nServices Infrastructure",
    "La infraestructura blockchain de la Union Europea")

add_content_slide(prs, "¿Que es EBSI?", [
    "European Blockchain Services Infrastructure: infraestructura blockchain de la UE",
    "Impulsada por la Comision Europea y la European Blockchain Partnership (EBP)",
    "27 estados miembros + Noruega y Liechtenstein participan",
    "Objetivo: ofrecer servicios publicos transfronterizos basados en blockchain",
    "Casos de uso principales:",
],
subbullets={
    4: ["Diplomas y credenciales educativas verificables (EBSI Diplomas)",
        "Identidad digital autosoberana (EBSI DID Registry)",
        "Trazabilidad de documentos oficiales",
        "Intercambio seguro de datos entre administraciones publicas",
        "Registro de auditoria para cumplimiento normativo"],
})

add_content_slide(prs, "EBSI: arquitectura tecnica", [
    "Red blockchain permissioned basada en Hyperledger Besu (compatible EVM)",
    "Cada estado miembro opera al menos un nodo validador",
    "Capa de identidad basada en DIDs y Verifiable Credentials (W3C)",
    "APIs publicas para resolver DIDs e interactuar con el registro:",
    "Relacion con eIDAS 2: EBSI es la infraestructura tecnica que da soporte al marco regulatorio europeo",
],
subbullets={
    3: ["DID Registry API: registrar y resolver DIDs",
        "Trusted Issuers Registry: lista de emisores de confianza",
        "Trusted Schemas Registry: esquemas de credenciales validados",
        "Timestamp API: sellado temporal de documentos"],
})

add_image_placeholder(prs, "Arquitectura EBSI",
    "[Diagrama: nodos validadores por pais conectados a APIs publicas, capa DID/VC encima]",
    "Architecture diagram of EBSI: network of validator nodes from EU member states connected to public APIs (DID Registry, Trusted Issuers, Schemas, Timestamp). Layer on top shows DID/VC ecosystem with issuers, holders and verifiers. Clean flat design, EU blue color scheme.")

add_content_slide(prs, "EBSI vs otras redes de identidad", [
    "EBSI no es la unica red de identidad descentralizada en Europa",
    "Cada una tiene su enfoque y tecnologia:",
],
subbullets={
    1: ["EBSI: institucional (UE), Hyperledger Besu, foco en servicios publicos",
        "Alastria: consorcio espanol, multitecnologia, foco en identidad y regulacion",
        "IOTA/Tangle: red publica, sin fees, foco en IoT e identidad",
        "Sovrin: red publica permissioned, Hyperledger Indy, foco SSI puro",
        "Polygon ID: red publica, zero-knowledge proofs, foco en privacidad"],
})

# ============================================================
# SECCION 2: ALASTRIA
# ============================================================
add_section_slide(prs, "Alastria\nEl ecosistema blockchain\nespanol", "Identidad, regulacion y redes enterprise")

add_content_slide(prs, "¿Que es Alastria?", [
    "Consorcio blockchain sin animo de lucro fundado en 2017 en Espana",
    "Mas de 500 entidades miembro: bancos, telcos, energeticas, universidades, AAPP",
    "Objetivo: crear una infraestructura blockchain regulada para Espana",
    "No es UNA blockchain: es un ecosistema con multiples redes e iniciativas",
    "Miembros destacados:",
],
subbullets={
    4: ["Banca: Santander, BBVA, CaixaBank, Bankia",
        "Telco: Telefonica, Vodafone",
        "Energia: Iberdrola, Repsol, Endesa",
        "Consultoras: Everis/NTT Data, Accenture, Deloitte",
        "Universidades: UPM, UC3M, UPC, URJC",
        "AAPP: Red.es, FNMT"],
})

add_content_slide(prs, "Redes de Alastria", [
    "Alastria opera varias redes blockchain en paralelo:",
    "Red T (Quorum/GoQuorum):",
    "Red B (Hyperledger Besu):",
    "Ambas redes son permissioned y compatibles con EVM (Solidity)",
],
subbullets={
    1: ["Primera red del consorcio, basada en Quorum (fork de Ethereum por JP Morgan)",
        "Usada para los primeros pilotos de Alastria ID",
        "En proceso de migracion hacia Red B"],
    2: ["Red actual de referencia, basada en Hyperledger Besu",
        "Compatible con la vision de EBSI (misma tecnologia base)",
        "Mayor rendimiento y mejor soporte a largo plazo",
        "Nodos operados por los miembros del consorcio"],
})

add_image_placeholder(prs, "Mapa del ecosistema Alastria",
    "[Diagrama: Red T y Red B como infraestructura, Alastria ID como capa de identidad, miembros conectados]",
    "Ecosystem diagram of Alastria consortium: two blockchain networks (Red T based on Quorum, Red B based on Hyperledger Besu) as infrastructure layer. Alastria ID as identity layer on top. Member organizations (banks, telcos, energy companies, universities) connected around the edges. Clean corporate style, Spanish flag colors accent.")

add_content_slide(prs, "Alastria ID: el modelo de identidad", [
    "Alastria ID es el sistema de identidad digital descentralizada del consorcio",
    "Basado en el modelo W3C: DIDs + Verifiable Credentials",
    "Componentes:",
    "El ciudadano/empresa controla su identidad sin depender de un unico intermediario",
    "Diferencia clave con identidad en Fabric: Alastria ID es interoperable entre redes y organizaciones",
],
subbullets={
    2: ["DID Alastria: did:ala:<network>:<identifier>",
        "Alastria ID Smart Contracts: gestion de DIDs on-chain",
        "Credential Registry: registro de credenciales emitidas/revocadas",
        "Presentation Registry: registro de presentaciones realizadas",
        "Trusted Service Providers: lista de emisores de confianza"],
})

add_content_slide(prs, "Alastria ID: flujo completo", [
    "1. Registro: la entidad crea un DID en la red Alastria y lo asocia a su clave publica",
    "2. Emision: un Trusted Issuer (universidad, banco, AAPP) emite una VC al titular",
    "3. Almacenamiento: el titular guarda la VC en su wallet (movil)",
    "4. Presentacion: el titular crea una VP y la comparte con el verificador",
    "5. Verificacion: el verificador comprueba la firma del issuer en la red Alastria",
    "6. Revocacion: el issuer puede revocar la VC en cualquier momento via el registry",
])

add_content_slide(prs, "Alastria: casos de uso reales", [
    "Identidad digital para ciudadanos (onboarding KYC bancario)",
    "Titulos universitarios verificables (universidades espanolas)",
    "Certificados de formacion profesional",
    "Credenciales de empleado para acceso a servicios entre empresas",
    "Recetas electronicas verificables entre comunidades autonomas",
    "Certificados de eficiencia energetica de inmuebles",
    "",
    "La mayoria estan en fase piloto o pre-produccion,",
    "pero demuestran la viabilidad tecnica del modelo",
])

# Treasure Hunt
add_special_slide(prs, "TREASURE HUNT", "¿Quien fundo Alastria?", [
    "Alastria se fundo en 2017, pero la idea surgio un ano antes.",
    "",
    "Mision: Investigar y responder:",
    "  1. ¿Quien fue el impulsor principal de la creacion de Alastria?",
    "     Pista: es un reconocido experto en blockchain que fue CTO de una gran consultora espanola.",
    "  2. ¿En que evento se presento Alastria por primera vez?",
    "  3. ¿Cuantos miembros fundadores tenia Alastria? ¿Y cuantos tiene ahora?",
    "  4. ¿Que relacion tiene Alastria con la European Blockchain Partnership?",
    "",
    "Tiempo: 10 minutos. Se puede buscar en internet.",
])

# Respuestas del Treasure Hunt
add_content_slide(prs, "Treasure Hunt: respuestas", [
    "1. Alex Puig, CTO de Everis (ahora NTT Data) y primer presidente de Alastria.",
    "   Impulso la creacion del consorcio junto con otros directivos del sector fintech y blockchain espanol.",
    "",
    "2. Se presento en el Mobile World Congress (MWC) de Barcelona en 2017.",
    "",
    "3. Alastria se fundo con 70 miembros fundadores en 2017.",
    "   Actualmente cuenta con mas de 500 entidades miembro.",
    "",
    "4. Espana, a traves de Alastria y otros actores, es miembro de la",
    "   European Blockchain Partnership (EBP) desde 2018. Alastria colabora",
    "   con EBSI compartiendo estandares de identidad (DID/VC) y participando",
    "   en los pilotos europeos. La Red B (Hyperledger Besu) esta alineada",
    "   tecnologicamente con EBSI para facilitar la interoperabilidad.",
])

# ============================================================
# SECCION 3: INTEGRACION EMPRESARIAL
# ============================================================
add_section_slide(prs, "Integracion de DID/VC\nen Soluciones Empresariales",
    "De la teoria a la practica: como se usa la identidad descentralizada")

add_content_slide(prs, "Caso 1: Onboarding KYC bancario con VCs", [
    "Problema: cada banco repite el proceso KYC (Know Your Customer) desde cero",
    "Solucion con VCs: el cliente hace KYC una vez y obtiene una VC reutilizable",
    "Flujo:",
],
subbullets={
    2: ["1. El cliente completa KYC en el Banco A (presenta DNI, justificante, etc.)",
        "2. El Banco A emite una VC de tipo 'KYC verificado' al cliente",
        "3. El cliente quiere abrir cuenta en el Banco B",
        "4. Presenta la VC de KYC del Banco A al Banco B",
        "5. El Banco B verifica la firma del Banco A en la red (Alastria/EBSI)",
        "6. Si es valida, acepta el KYC sin repetir el proceso",
        "7. Ahorro: semanas de tramites reducidas a segundos"],
})

add_content_slide(prs, "Caso 2: Titulos universitarios verificables", [
    "Problema: verificar un titulo universitario requiere contactar a la universidad emisora",
    "Solucion con VCs: la universidad emite el titulo como una Verifiable Credential",
    "Flujo:",
    "Implementacion real: universidades espanolas en Alastria + proyecto EBSI Diplomas",
],
subbullets={
    2: ["1. El alumno se gradua y la universidad emite una VC con el titulo",
        "2. El alumno guarda la VC en su wallet",
        "3. Una empresa quiere verificar el titulo del candidato",
        "4. El candidato presenta una VP con la VC del titulo",
        "5. La empresa verifica la firma de la universidad en la red",
        "6. Resultado instantaneo: titulo autentico o falso"],
})

add_content_slide(prs, "Caso 3: Acceso a servicios entre empresas", [
    "Problema: un empleado de la Empresa A necesita acceder a un sistema de la Empresa B",
    "Hoy: se crea una cuenta en el sistema de B, con su propio usuario/password",
    "Con VCs: la Empresa A emite una credencial de empleado como VC",
    "Flujo:",
    "Ventaja: cuando el empleado deja la Empresa A, se revoca la VC y pierde acceso en B automaticamente",
],
subbullets={
    3: ["1. Empresa A emite VC: 'Juan es empleado con rol=auditor'",
        "2. Juan presenta la VC al sistema de Empresa B",
        "3. Empresa B verifica la VC y da acceso segun el rol",
        "4. No hay cuenta en B: la identidad viene de A"],
})

# Debate
add_debate_slide(prs, "Identidad digital en la empresa", [
    "1. ¿Que ventajas reales tiene la identidad descentralizada frente a un SSO corporativo (Okta, Azure AD)?",
    "2. ¿Quien deberia ser el 'trusted issuer' para credenciales profesionales? ¿La empresa, un colegio profesional, el Estado?",
    "3. Si un empleado tiene una VC de 'ingeniero certificado' y la empresa que la emitio cierra, ¿sigue siendo valida?",
    "4. ¿Como afecta el GDPR al almacenamiento de datos personales en una VC? ¿Y si la VC esta en blockchain?",
    "5. ¿Veis aplicacion en vuestro sector para las VCs?",
])

# ============================================================
# SECCION 4: ARQUITECTURAS HIBRIDAS
# ============================================================
add_section_slide(prs, "Arquitecturas Hibridas\ncon Multiples Redes",
    "Identidad en una red, negocio en otra")

add_content_slide(prs, "¿Por que arquitecturas hibridas?", [
    "En el mundo real, una sola blockchain no resuelve todo",
    "Cada red tiene su fortaleza:",
    "La arquitectura hibrida combina lo mejor de cada una:",
    "Ejemplo: Alastria para identidad + Fabric para logica de negocio",
],
subbullets={
    1: ["Red publica (EBSI, Alastria): identidad, credenciales, confianza",
        "Red privada (Fabric): logica de negocio, transacciones, datos confidenciales",
        "Cada una gobernada por distintos actores con distintas reglas"],
    2: ["Identidad: interoperable, verificable por cualquiera, en red publica/consorcio",
        "Negocio: privado, rapido, solo entre los participantes, en Fabric"],
})

add_image_placeholder(prs, "Arquitectura hibrida: Alastria + Fabric",
    "[Diagrama: Red Alastria (identidad, DIDs, VCs) conectada con Red Fabric (canales, chaincodes, ledger)]",
    "Split architecture diagram: left side shows Alastria network with DID Registry and VC issuance (blue tones), right side shows Hyperledger Fabric network with channels, chaincodes, and private ledger (green tones). Bridge in the middle showing identity verification flow. Clean corporate style.")

add_content_slide(prs, "Patron: verificar identidad externa en Fabric", [
    "El cliente presenta una VP (Verifiable Presentation) a la aplicacion",
    "La aplicacion verifica la VP contra la red de identidad (Alastria/EBSI)",
    "Si la VP es valida, la aplicacion invoca el chaincode en Fabric",
    "El chaincode puede registrar el DID del cliente como referencia",
    "Flujo:",
],
subbullets={
    4: ["1. Cliente -> App: presenta VP con VC de KYC",
        "2. App -> Alastria: ¿es valida esta VP? ¿el issuer es de confianza?",
        "3. Alastria -> App: si, valida y no revocada",
        "4. App -> Fabric: RegisterClient(did:ala:quor:0x123..., 'Javier Garcia')",
        "5. Fabric: registra al cliente y puede operar en el canal"],
})

add_content_slide(prs, "DID/VC vs X.509/MSP en Fabric", [
    "Fabric usa nativamente certificados X.509 emitidos por una Fabric CA",
    "Los DIDs/VCs son un modelo diferente y complementario",
    "Comparativa:",
],
subbullets={
    2: ["X.509 (Fabric nativo): emitido por la CA de cada org, valido solo dentro de la red Fabric",
        "DID (Alastria/EBSI): emitido por el propio sujeto, verificable en cualquier red",
        "X.509: identifica peers, orderers, admins (infraestructura)",
        "DID/VC: identifica personas, empresas, credenciales (capa de negocio)",
        "No se reemplazan: X.509 para la infraestructura Fabric, DID/VC para los usuarios finales"],
})

add_table_slide(prs, "Comparativa: X.509 vs DID/VC",
    ["Aspecto", "X.509 (Fabric)", "DID / VC"],
    [
        ["Emisor", "Fabric CA de cada org", "Cualquier Trusted Issuer"],
        ["Alcance", "Solo dentro de la red Fabric", "Interoperable entre redes"],
        ["Revocacion", "CRL (Certificate Revocation List)", "Credential Registry on-chain"],
        ["Contenido", "Nombre, org, rol", "Cualquier atributo (KYC, titulo, empleo...)"],
        ["Control", "La CA de la org", "El propio titular (autosoberano)"],
        ["Uso tipico", "Autenticar peers y admins", "Identificar usuarios finales"],
        ["Privacidad", "El cert revela la identidad", "Zero-knowledge proofs posibles"],
    ])

# Cultura General
add_special_slide(prs, "CULTURA GENERAL", "El DNI electronico espanol: una historia de adopcion fallida", [
    "Espana fue pionera en Europa con el DNI electronico (DNIe) en 2006.",
    "Incluia un chip con certificado digital para firmar documentos y autenticarse online.",
    "La idea era revolucionaria: cada ciudadano con identidad digital en el bolsillo.",
    "",
    "¿Que paso?",
    "  - Los lectores de tarjeta eran caros y dificiles de instalar",
    "  - El software de firma era complejo y fallaba en muchos navegadores",
    "  - La renovacion del certificado requeria ir a la comisaria",
    "  - Pocos servicios publicos lo soportaban de forma fluida",
    "  - La adopcion fue minima: menos del 5% de la poblacion lo uso alguna vez",
    "",
    "Leccion: la tecnologia estaba lista, pero la UX no. Exactamente el mismo riesgo",
    "que corre hoy la identidad descentralizada si no se resuelve la experiencia de usuario.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

# ============================================================
# SECCION 5: PRACTICA Y CIERRE
# ============================================================

add_activity_slide(prs, "Disenar una arquitectura hibrida", [
    "Objetivo: disenar la arquitectura de identidad para un caso real",
    "",
    "Escenario: Un consorcio de 3 hospitales quiere compartir historiales medicos.",
    "Los pacientes deben controlar quien accede a sus datos.",
    "Los medicos necesitan credenciales verificables de su colegio profesional.",
    "",
    "Grupos de 3-4 personas. Decidir:",
    "  1. ¿Que red usariais para identidad? (Alastria, EBSI, Fabric CA, otra)",
    "  2. ¿Que red para la logica de negocio? (Fabric, Besu, otra)",
    "  3. ¿Que credenciales necesitan los pacientes? ¿Y los medicos?",
    "  4. ¿Como verificaria el Hospital B una credencial emitida por el Hospital A?",
    "  5. ¿Donde se almacenan los datos medicos? (on-chain, off-chain, IPFS...)",
    "",
    "Tiempo: 25 minutos. Presentar diagrama + justificacion.",
], badge_text="PRACTICA")

add_debate_slide(prs, "Cierre del modulo de identidad", [
    "1. ¿Alastria, EBSI o una solucion propia? ¿Que elegiriais para vuestra empresa y por que?",
    "2. ¿Tiene sentido que la identidad sea autosoberana si el Estado sigue emitiendo los documentos oficiales?",
    "3. ¿Cuando usariais X.509 de Fabric y cuando DIDs/VCs? ¿Pueden convivir?",
    "4. ¿Cual es el mayor obstaculo para la adopcion de la identidad descentralizada?",
    "5. ¿Creeis que en 5 anos tendremos todos un wallet de identidad en el movil?",
])

add_review_slide(prs, "Repaso del modulo: Identidad Digital", [
    "¿Que es EBSI y que relacion tiene con eIDAS 2?",
    "¿Que es Alastria y que redes opera?",
    "¿Que es Alastria ID y en que se basa?",
    "Describe el flujo de emision y verificacion de una VC en Alastria",
    "Da un ejemplo real de integracion de VCs en una empresa",
    "¿Que es una arquitectura hibrida y por que tiene sentido?",
    "¿Cual es la diferencia entre X.509 de Fabric y un DID?",
    "¿Cuando usarias cada uno?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 5/identidad_digital_parte2.pptx")
print("identidad_digital_parte2.pptx generado OK")
