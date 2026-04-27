"""
Genera una nueva PPT en Modulo 5 sobre PKI, certificados, CAs y MSP en Fabric.
Crea un archivo nuevo (no regenera nada existente).
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# ============================================================
# PORTADA
# ============================================================
add_title_slide(prs, "Identidades en Fabric:\nPKI, Certificados, CAs y MSP",
    "De la criptografía asimetrica al control de acceso en consorcios",
    module="Modulo 5: Identidad Digital — Profundizacion técnica")

add_review_slide(prs, "Lo que vas a aprender", [
    "¿Qué es un certificado y para qué sirve?",
    "¿Quién es la autoridad certificadora (CA) y por qué confiamos en ella?",
    "¿Qué es un certificado raíz y qué significa la cadena de confianza?",
    "¿Por qué Fabric usa DOS CAs distintas (identidad y TLS)?",
    "¿Qué es el MSP y cómo se materializa físicamente?",
    "¿Cómo se valida una transaccion paso a paso?",
])

# ============================================================
# SECCION 1: CERTIFICADOS
# ============================================================
add_section_slide(prs, "1. ¿Qué es un certificado?",
    "Criptografía asimetrica + identidad firmada")

add_content_slide(prs, "Repaso: criptografía asimetrica", [
    "Cada usuario tiene un par de claves criptograficamente ligadas:",
    "Propiedades:",
    "Ejemplo cotidiano:",
], subbullets={
    0: ["Clave privada — secreta, nunca se comparte",
        "Clave pública — derivada de la privada, se comparte libremente"],
    1: ["Lo cifrado con la pública solo se descifra con la privada",
        "Lo firmado con la privada se verifica con la pública",
        "De la pública NO se puede deducir la privada (en tiempo razonable)"],
    2: ["DNI electrónico, certificado de firma de la FNMT",
        "TLS de las webs (https://) usa exactamente este mismo principio"],
})

add_content_slide(prs, "Problema: ¿como sabemos a quién pertenece una clave pública?", [
    "Cualquiera puede generar un par de claves y reclamar ser quien quiera",
    "Si Alice genera claves y dice 'soy el Banco Santander', ¿quién la cree?",
    "Necesitamos un mecanismo para asociar una clave pública con una identidad real",
    "",
    "La solución: una entidad de confianza firma esa asociación",
    "Esa firma se materializa en un documento llamado 'certificado'",
])

add_content_slide(prs, "El certificado X.509: definicion", [
    "Un certificado es un documento digital firmado que ASOCIA:",
    "Y todo eso firmado por una autoridad de confianza (la CA)",
    "X.509 es el estandar internacional (RFC 5280) que define el formato",
    "Es lo que usa toda Internet: TLS/HTTPS, DNI electronico, Fabric, Bitcoin (parcialmente)...",
], subbullets={
    0: ["Una identidad (nombre, email, organizacion, atributos)",
        "Una clave pública (la del titular)",
        "Un periodo de validez (fecha de inicio y caducidad)",
        "Un identificador unico (serial number)"],
})

add_content_slide(prs, "Estructura de un certificado X.509", [
    "Subject: a quien identifica (CN=peer0.org1, O=Org1)",
    "Issuer: quién lo emite (la CA)",
    "Validity: desde cuando hasta cuando es valido",
    "Subject Public Key: la clave pública del titular",
    "Extensions: atributos custom, SANs (alt names), Key Usage...",
    "Signature: firma de la CA sobre todo lo anterior",
    "",
    "La firma de la CA es lo que da validez al certificado.",
    "Sin firma valida, el certificado no vale nada.",
])

add_image_placeholder(prs, "Anatomía de un certificado X.509",
    "[Diagrama: cuadro con campos del cert (Subject, Issuer, Public Key, Validity, Extensions) y al final la firma de la CA aplicada sobre el hash del resto]",
    "Detailed visual diagram of an X.509 certificate structure showing: Subject, Issuer, Validity dates, Subject Public Key, Extensions, and at the bottom the CA Signature applied over a hash of all the previous fields. Arrow from CA private key to the signature. Clean technical illustration, blue and gray colors.")

# ============================================================
# SECCION 2: AUTORIDAD CERTIFICADORA
# ============================================================
add_section_slide(prs, "2. La Autoridad Certificadora (CA)",
    "Quién emite los certificados y por qué confiamos en ella")

add_content_slide(prs, "¿Qué es una CA?", [
    "Certificate Authority — autoridad que emite certificados",
    "Es la entidad que firma los certificados de los usuarios finales",
    "Su firma es lo que convierte un par de claves en una identidad reconocida",
    "",
    "Analogía: el registro civil emite los DNIs. Su sello hace que un DNI sea valido.",
    "Sin esa autoridad, cualquiera podria fabricar su propio 'DNI' y nadie lo creeria.",
])

add_content_slide(prs, "Tipos de CA según ámbito", [
    "CAs publicas (mundo abierto):",
    "CAs privadas (organizaciones internas):",
    "CAs de consorcio (entre orgs que se conocen):",
], subbullets={
    0: ["Let's Encrypt, DigiCert, GlobalSign, Sectigo...",
        "Su raíz esta preinstalada en navegadores y sistemas operativos",
        "Cualquiera puede pedir un cert (con verificación)",
        "Caso: HTTPS de tu web"],
    1: ["Una empresa monta su propia CA para certificados internos",
        "VPN, intranet, sistemas internos",
        "Solo sus empleados confian en esa CA"],
    2: ["Cada miembro del consorcio opera SU propia CA",
        "Las orgs intercambian sus certs raíz publicos para confiar mutuamente",
        "Caso: Hyperledger Fabric (Fabric CA)"],
})

add_content_slide(prs, "¿Por qué confiamos en una CA?", [
    "Por una de tres razones:",
    "Tecnológicamente: la firma criptografica es matematicamente verificable",
    "Pero la decision de confiar en CA es una decision HUMANA, no técnica",
])

add_content_slide(prs, "Problema clave: si la CA es comprometida...", [
    "El atacante puede emitir certificados falsos firmados por la CA",
    "Esos certificados son técnicamente validos — pasan la verificación",
    "Pueden suplantar identidades, firmar transacciones fraudulentas",
    "Caso real: en 2011 hackearon DigiNotar (una CA de Holanda)",
    "  — emitieron certs falsos de google.com",
    "  — se usaron para espiar a usuarios iranies",
    "  — DigiNotar quebro y fue eliminada de los navegadores",
    "",
    "Por eso la clave privada de la CA es el activo MAS critico.",
    "En produccion seria, suele estar offline (HSM, bovedas) y se usa lo minimo posible.",
], subbullets={
})

# ============================================================
# SECCION 3: CERT RAIZ Y CADENA DE CONFIANZA
# ============================================================
add_section_slide(prs, "3. Certificado raíz y cadena de confianza",
    "El árbol de la confianza")

add_content_slide(prs, "¿Qué es un certificado raíz?", [
    "Es el certificado original de la CA — la 'raíz' del árbol de confianza",
    "Característica única: es AUTO-FIRMADO",
    "  — el Subject y el Issuer son la misma entidad (la CA)",
    "  — es el unico cert que no necesita otro cert por encima",
    "Otros nombres: root cert, trust anchor (ancla de confianza), CA cert",
    "",
    "Es el punto de partida de toda la cadena. Si confias en el raíz,",
    "puedes confiar en todo lo que de el deriva.",
])

add_image_placeholder(prs, "El árbol de certificados",
    "[Diagrama jerarquico de árbol: Cert Raíz arriba, certs intermedios en el medio, certs de usuarios al final, con flechas mostrando 'firma a' de arriba abajo]",
    "Hierarchical tree diagram of a certificate trust chain. At the top: Root CA cert (red). Middle layer: 2 Intermediate CA certs. Bottom layer: 4-5 end-user certs (peers, users). Arrows from top to bottom labeled 'signs'. Clean technical diagram.")

add_content_slide(prs, "Cadena de confianza (chain of trust)", [
    "Es la secuencia de certificados que conecta a un titular con la raíz",
    "Cada cert es firmado por el cert que esta encima",
    "Para validar, recorres la cadena hasta llegar al raíz",
    "",
    "Ejemplo de validación de un cert de Alice:",
])

add_content_slide(prs, "Validación paso a paso", [
    "Tienes el cert de Alice y quieres validarlo:",
    "1. ¿La firma del cert de Alice es valida usando la clave pública del Intermedio 1?",
    "2. ¿La firma del cert del Intermedio 1 es valida usando la clave pública del Raíz?",
    "3. ¿Conoces el cert Raíz? ¿Esta en tu lista de certs de confianza?",
    "",
    "Si todas las respuestas son SI -> el cert de Alice es valido",
    "Si alguna falla -> el cert se rechaza",
    "",
    "Importante: el verificador SOLO necesita tener el cert RAIZ",
    "  — no necesita tener todos los certs de Alice, Bob, Carlos, etc.",
])

add_content_slide(prs, "¿Por qué hay certs intermedios?", [
    "Para PROTEGER el cert raíz",
    "El raíz es el activo mas crítico — comprometerlo seria catastrofico",
    "Solucion: el raíz emite un cert intermedio y se guarda offline",
    "El intermedio es el que esta online y emite los certs de usuarios",
    "",
    "Si comprometen el intermedio:",
    "  — Se revoca y se emite uno nuevo desde el raíz",
    "  — Solo afecta a los certs emitidos por ese intermedio",
    "Si comprometieran el raíz:",
    "  — Hay que regenerar TODA la cadena, todos los miembros vuelven a empezar",
    "",
    "Por eso en producción seria es habitual ver cadenas de 2-3 niveles.",
])

add_content_slide(prs, "En Fabric con cryptogen vs producción", [
    "Cryptogen (desarrollo y aula):",
    "Producción seria:",
], subbullets={
    0: ["Una sola CA raíz por org",
        "Esa raíz firma directamente todos los certs (peers, admins, users)",
        "Sin intermedios — cadena de 1 nivel",
        "Simple pero menos seguro"],
    1: ["CA raíz offline en HSM o bóveda",
        "CA intermedia online, firma certs de usuarios",
        "Cadena tipica de 2-3 niveles",
        "Si comprometen el intermedio, se revoca sin afectar a la raíz"],
})

# Treasure Hunt
add_special_slide(prs, "TREASURE HUNT", "El día que se rompio la confianza", [
    "En 2011, una CA holandesa fue hackeada y emitio cientos de certificados falsos.",
    "Entre ellos un cert de google.com que se uso para espiar a 300.000 usuarios iranies.",
    "El daño fue tal que la CA quebro y fue eliminada de la lista de CAs de confianza.",
    "",
    "Misión: investigar y responder:",
    "  1. ¿Como se llamaba esa CA holandesa?",
    "  2. ¿Cuantos certificados falsos emitieron exactamente?",
    "  3. ¿Que medidas tomaron Mozilla, Microsoft y Google despues del hack?",
    "  4. ¿Que es 'Certificate Transparency' y como surgio como respuesta a este caso?",
    "",
    "Tiempo: 15 minutos. Es un caso fascinante de seguridad informatica.",
])

# Respuestas treasure hunt
add_content_slide(prs, "Treasure Hunt: respuestas", [
    "1. La CA se llamaba DigiNotar — una empresa holandesa que tambien emitia certs",
    "   para el gobierno de Paises Bajos (PKIoverheid).",
    "",
    "2. Emitieron al menos 531 certificados fraudulentos. Entre ellos:",
    "   *.google.com, *.facebook.com, *.skype.com, *.cia.gov, *.mozilla.org",
    "",
    "3. Mozilla, Microsoft y Google retiraron a DigiNotar de sus stores de confianza.",
    "   El gobierno holandes intervino la empresa, que quebro en septiembre 2011.",
    "",
    "4. Certificate Transparency (CT) es un sistema publico donde TODAS las CAs",
    "   deben registrar los certificados que emiten en logs publicos auditables.",
    "   Si una CA emite un cert sospechoso, cualquiera lo detecta. Surgio en 2013",
    "   directamente como respuesta al caso DigiNotar y otros similares.",
])

# ============================================================
# SECCION 4: DOS CAs DISTINTAS
# ============================================================
add_section_slide(prs, "4. Las dos CAs de Fabric:\nidentidad y TLS",
    "Por qué se separan y qué consecuencias tiene")

add_content_slide(prs, "Dos problemas, dos soluciones", [
    "En Fabric (y en muchos sistemas) hay dos preguntas a resolver:",
    "Problema 1 — Identidad: ¿quién firmo esta transacción?",
    "Problema 2 — Comunicacion: ¿esta conexion es segura y entre quién?",
    "",
    "Cada problema requiere su propia infraestructura criptografica:",
    "  — Identidad → CA de identidad y certificados de identidad",
    "  — Comunicación → TLS CA y certificados TLS",
])

add_table_slide(prs, "Comparativa: CA de identidad vs TLS CA",
    ["Aspecto", "CA de identidad", "TLS CA"],
    [
        ["¿Qué autoriza?", "Quién firma transacciones", "Quién abre conexiones de red"],
        ["¿Donde actua?", "Capa de aplicacion (chaincode, lifecycle)", "Capa de transporte (gRPC + TLS)"],
        ["¿Quién la usa?", "Peers, admins, usuarios firmando datos", "Peers y orderers cifrando comunicacion"],
        ["¿En que carpeta del MSP?", "cacerts/", "tlscacerts/"],
        ["¿Qué pasa si la comprometen?", "CATASTROFE — emiten transacciones falsas", "Grave — pueden interceptar conexiones"],
        ["Frecuencia de uso", "Cada transaccion", "Cada conexion gRPC"],
    ])

add_content_slide(prs, "Analogía: la carta firmada en sobre certificado", [
    "Imaginate enviar una carta importante:",
    "",
    "CA de identidad → tu firma manuscrita validada por notario",
    "  — Garantiza que TU has escrito esa carta",
    "  — Sin firma, cualquiera podria haberla escrito",
    "",
    "TLS CA → el sobre cerrado y certificado por correos",
    "  — Garantiza que la carta llega cerrada al destinatario correcto",
    "  — Sin sobre, cualquiera la lee por el camino",
    "",
    "Las dos cosas son necesarias y resuelven problemas distintos.",
    "Una carta firmada en sobre abierto -> cualquiera la lee",
    "Una carta sin firmar en sobre cerrado -> ¿quién la escribio?",
])

add_content_slide(prs, "¿Por qué separar las dos CAs?", [
    "Aislamiento de daños — si comprometen una, la otra sigue protegiendo",
    "Diferentes ciclos de vida — los TLS rotan mas a menudo que los de identidad",
    "Diferentes politicas de gestion:",
    "Diferentes responsables:",
], subbullets={
    2: ["CA de identidad: offline, en boveda, uso minimo",
        "TLS CA: online, accesible para emitir/renovar TLS"],
    3: ["CA de identidad: equipo de seguridad / compliance",
        "TLS CA: equipo de operaciones / DevOps"],
})

add_content_slide(prs, "Flujo de una transaccion: dónde actúa cada CA", [
    "Cuando un peer del Hotel envia una transaccion al peer de la Cafeteria:",
    "",
    "1. Conexion TCP segura (TLS):",
    "   El peer Hotel se conecta al peer Cafeteria por gRPC",
    "   Se establece TLS — los certificados TLS se validan con TLS CA",
    "   Si el cert TLS no esta firmado por una TLS CA conocida -> conexion rechazada",
    "",
    "2. Envio de transaccion firmada (identidad):",
    "   El peer Hotel firma la transaccion con su clave privada de identidad",
    "   El peer Cafeteria valida la firma con la CA de identidad del Hotel",
    "   Si la firma no es valida -> transaccion rechazada",
    "",
    "Sin las dos CAs, la transaccion no llega o no se valida.",
])

add_image_placeholder(prs, "Las dos capas de seguridad",
    "[Diagrama: dos capas apiladas. Capa inferior 'TLS / transporte' con sus certs TLS. Capa superior 'identidad / firma' con sus certs de identidad. Mensaje pasando por ambas capas]",
    "Layered security diagram showing two stacked security layers: bottom layer 'TLS Transport' with TLS certificates handling encryption, top layer 'Identity Signing' with identity certificates handling authentication. A message flows through both layers. Clean technical illustration.")

# ============================================================
# SECCION 5: MSP EN FABRIC
# ============================================================
add_section_slide(prs, "5. El MSP en Fabric",
    "Membership Service Provider — la pieza que conecta todo")

add_content_slide(prs, "¿Qué es el MSP?", [
    "MSP = Membership Service Provider",
    "Es el componente de Fabric que responde a:",
    "Físicamente: una CARPETA con varios archivos de certificados",
    "Lógicamente: la 'guia' que dice quién puede hacer qué en la red",
], subbullets={
    1: ["¿Esta identidad pertenece a esta organización?",
        "¿Que tipo de identidad es (peer, admin, client, orderer)?",
        "¿Tiene los atributos necesarios para esta operacion?"],
})

add_content_slide(prs, "Estructura del MSP", [
    "msp/",
    "  cacerts/             — Cert raíz de la CA de identidad de la org",
    "  tlscacerts/          — Cert raíz de la TLS CA",
    "  keystore/            — Clave privada de ESTA identidad (privado)",
    "  signcerts/           — Cert público de ESTA identidad",
    "  intermediatecerts/   — Certs intermedios de la CA (opcional)",
    "  crls/                — Listas de revocacion (opcional)",
    "  config.yaml          — Configuracion de NodeOUs (roles)",
])

add_content_slide(prs, "Dos tipos de MSP", [
    "MSP de identidad (Local MSP):",
    "MSP de organización (Channel MSP):",
], subbullets={
    0: ["Representa a UN nodo o usuario concreto",
        "Tiene clave privada en keystore/ (la del propio nodo)",
        "Ubicacion: peers/peer0.../msp/, users/Admin@.../msp/, etc.",
        "Lo usa el peer/admin/user para firmar"],
    1: ["Representa a la ORGANIZACION en su conjunto",
        "NO tiene clave privada — solo certs raíz publicos",
        "Ubicacion: org1.example.com/msp/",
        "Es lo que se referencia en configtx.yaml (campo MSPDir)",
        "Lo usan los demas peers para validar a miembros de esta org"],
})

add_content_slide(prs, "config.yaml: NodeOUs", [
    "Define cómo se identifican los TIPOS de identidad dentro de una org",
    "Hay 4 tipos estándar: client, peer, admin, orderer",
    "Cada tipo se identifica por una OU (Organizational Unit) en el cert X.509",
    "",
    "Sin NodeOUs, todos los miembros de la org son iguales — no hay distincion",
    "  entre admins y usuarios normales",
    "Con NodeOUs, el chaincode puede saber si quien le habla es un cliente, un peer,",
    "  un admin o un orderer, y aplicar permisos diferentes",
    "",
    "Por eso en cryptogen ponemos: EnableNodeOUs: true",
])

add_image_placeholder(prs, "Estructura completa del MSP en Fabric",
    "[Diagrama: a la izquierda el árbol de carpetas del MSP. A la derecha qué hace cada subcarpeta. Conexiones entre los certs y la CA raíz]",
    "Detailed file tree diagram showing the complete MSP folder structure on the left side: cacerts, tlscacerts, keystore, signcerts, intermediatecerts, crls, config.yaml. On the right side, brief descriptions of what each folder contains and its purpose. Connecting arrows showing how certs relate to the CA root.")

# ============================================================
# SECCION 6: VALIDACION DE TRANSACCION
# ============================================================
add_section_slide(prs, "6. Cómo se valida una transacción",
    "El flujo completo paso a paso")

add_content_slide(prs, "Setup previo (lo que ya esta en su sitio)", [
    "Antes de cualquier transaccion, en el canal hay configurado:",
    "MSP de Org1 con su cert raíz de identidad y de TLS",
    "MSP de Org2 con sus certs raíz",
    "MSP del Orderer con sus certs raíz",
    "Cada peer tiene SUS claves privadas y SU MSP local",
    "Las orgs YA se han intercambiado los certs raíz publicos",
])

add_content_slide(prs, "Flujo: Alice (Hotel) emite puntos a un cliente", [
    "1. Alice crea la propuesta de transaccion en su app cliente",
    "2. La app firma la propuesta con la clave privada de Alice (identidad)",
    "3. La app abre conexion TLS al peer del Hotel",
    "4. El peer Hotel recibe la propuesta:",
    "5. El peer Hotel ejecuta el chaincode (simulacion)",
    "6. El peer Hotel firma la respuesta con SU clave privada",
    "7. La app envia la propuesta endorsada al orderer:",
    "8. El orderer ordena en bloques y los distribuye a todos los peers",
    "9. Cada peer valida el bloque:",
], subbullets={
    3: ["TLS valida la conexion TCP usando TLS CA",
        "Verifica firma de Alice usando MSP del Hotel (CA de identidad)",
        "Comprueba que Alice tiene rol 'admin' (NodeOU + atributos)"],
    7: ["Conexion TLS con orderer (validada con TLS CA del Orderer)",
        "Orderer verifica las firmas de los endorsers"],
    8: ["Conexion TLS"],
})

add_content_slide(prs, "Cuántas verificaciones hay en una transacción?", [
    "Por cada propuesta de transaccion que llega a un peer:",
    "Sumando: 4-6 verificaciones criptograficas por transaccion",
    "Cada una usa una CA distinta (TLS o identidad) y tarda microsegundos",
    "Por eso el rendimiento de Fabric depende mucho de la CPU y de la rapidez",
    "  con la que valida firmas",
], subbullets={
    0: ["Validacion del TLS de la conexion → TLS CA",
        "Validacion del cert de identidad de quien envia → CA de identidad",
        "Verificacion de la firma de la transaccion → clave publica del firmante",
        "Verificacion de cada firma de endorsement (por org) → CA de cada org",
        "Verificacion del cert del orderer cuando llega el bloque → TLS CA del orderer"],
})

# ============================================================
# CULTURA GENERAL
# ============================================================
add_special_slide(prs, "CULTURA GENERAL", "Whitfield Diffie y Martin Hellman: los padres de la cripto moderna", [
    "En 1976, Diffie y Hellman publicaron 'New Directions in Cryptography'",
    "Inventaron el concepto de criptografía de clave PUBLICA",
    "Hasta ese momento, toda la cripto era simetrica — necesitabas compartir la clave",
    "Su idea revoluciono todo: comunicación segura entre desconocidos",
    "",
    "Sin Diffie-Hellman no existiria:",
    "  — HTTPS (cada vez que entras en una web)",
    "  — Cualquier cert X.509 (incluido los de Fabric)",
    "  — Bitcoin, Ethereum, Hyperledger, blockchain en general",
    "  — Las firmas digitales tal como las conocemos",
    "",
    "Recibieron el Premio Turing en 2015 (el Nobel de informatica) por este trabajo.",
    "Curiosidad: el algoritmo RSA llego un año despues (1977) basandose en sus ideas.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

# ============================================================
# DEBATE
# ============================================================
add_debate_slide(prs, "Debate: PKI y consorcios", [
    "1. En un consorcio Fabric, ¿quién deberia operar las CAs? ¿Cada org la suya, una neutra, ambas?",
    "2. Si comprometen la CA del Hotel, ¿que pueden hacer los atacantes en la red? ¿Y si comprometen la TLS CA?",
    "3. ¿Es razonable que la clave privada de la CA raíz se almacene en una boveda fisica con HSM? ¿O es excesivo?",
    "4. Si una org abandona el consorcio, ¿que pasa con los certs que emitio? ¿Como se invalidan?",
    "5. ¿Tiene sentido que Fabric soporte certificados intermedios cuando la mayoria de proyectos no los usa?",
])

# Respuestas debate
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. Quién deberia operar las CAs:",
    "2. Si comprometen la CA del Hotel:",
    "3. CA raíz en boveda con HSM:",
], subbullets={
    0: ["Cada org SU propia CA — es la solucion estandar y mas autonoma",
        "Una CA central neutral seria mas simple pero crea un punto de fallo",
        "Lo habitual: cada org opera la suya y se intercambian certs raíz",
        "El orderer puede tener su propia CA dedicada (para mayor aislamiento)"],
    1: ["Atacantes pueden emitir certs falsos firmados por la CA del Hotel",
        "Pueden firmar transacciones como si fueran cualquier miembro del Hotel",
        "Pueden suplantar al admin del Hotel y aprobar chaincodes",
        "Si comprometen la TLS CA: pueden interceptar conexiones (MITM)",
        "  — pero NO pueden firmar transacciones validas",
        "  — el daño es mucho menor pero hay que rotar igualmente"],
    2: ["Es absolutamente razonable, no excesivo, en proyectos serios",
        "Los HSM evitan que la clave salga del hardware (ni siquiera el admin la ve)",
        "Coste: ~10-30k EUR por HSM, pero protege un activo de millones",
        "En aula no usamos HSM — pero hay que saberlo para el dia que se haga real"],
})

add_content_slide(prs, "Respuestas al debate (2/2)", [
    "4. Org que abandona el consorcio — que hacer con sus certs:",
    "5. ¿Tiene sentido los certs intermedios en Fabric?",
], subbullets={
    0: ["Tecnicamente: no se pueden borrar los datos del ledger (inmutabilidad)",
        "Lo que se hace: revocar todos los certs emitidos por su CA",
        "Generar nueva CRL (Certificate Revocation List) y distribuirla a los MSPs",
        "Eliminar la org del MSP del canal (config update)",
        "Sus transacciones historicas siguen siendo verificables (eran validas en su momento)",
        "Pero NO puede emitir nuevas transacciones — su MSP ya no esta en el canal"],
    1: ["Si, tiene mucho sentido en producción seria",
        "Permite mantener la raíz offline y proteger el activo mas critico",
        "Si comprometen el intermedio, lo revocas y emites otro sin tocar la raíz",
        "En cryptogen no se usa por simplicidad (cadena de 1 nivel)",
        "Fabric CA si lo soporta nativamente — config 'intermediate CA mode'",
        "En proyectos enterprise serios es la norma, no la excepcion"],
})

# ============================================================
# ACTIVIDAD
# ============================================================
add_activity_slide(prs, "Inspeccionar un certificado X.509 real", [
    "Ejercicio practico para fijar conceptos.",
    "",
    "1. Usa la red FidelityChain levantada (o cualquier red Fabric)",
    "2. Localiza un cert de un peer:",
    "   $HOME/proyecto-fidelitychain/network/crypto-config/",
    "   peerOrganizations/hotel.fidelitychain.com/",
    "   peers/peer0.../msp/signcerts/cert.pem",
    "",
    "3. Inspecciona el cert con openssl:",
    "   openssl x509 -in cert.pem -text -noout",
    "",
    "4. Identifica:",
    "   - Subject: ¿quién es el titular?",
    "   - Issuer: ¿quién lo emitio? ¿Coincide con la CA raíz de la org?",
    "   - Validity: ¿cuando caduca?",
    "   - Subject Alternative Names: ¿estan los hostnames y SANs correctos?",
    "   - Public Key: ¿que algoritmo usa? (ECDSA, P-256...)",
    "",
    "5. Compara con el cert raíz (cacerts/ca-cert.pem). ¿En que se parecen y diferencian?",
    "",
    "Tiempo: 30 minutos. Trabajar en parejas.",
])

# ============================================================
# REPASO FINAL
# ============================================================
add_review_slide(prs, "Repaso final", [
    "¿Que es un certificado X.509 y que campos tiene?",
    "¿Que es una CA y por que confiamos en ella?",
    "¿Que es un cert raíz y por que se llama raíz?",
    "¿Que es la cadena de confianza y para que sirve?",
    "¿Por que Fabric usa dos CAs distintas? Nombra cada una y su funcion.",
    "¿Que es un MSP? Tipos y estructura de carpetas.",
    "¿Que son los NodeOUs y para que sirven?",
    "¿Cuantas verificaciones criptograficas hay en una transaccion?",
])

add_content_slide(prs, "Respuestas al repaso (1/2)", [
    "1. Certificado X.509:",
    "2. CA y por qué confiamos:",
    "3. Cert raíz:",
    "4. Cadena de confianza:",
], subbullets={
    0: ["Documento digital firmado que asocia identidad + clave publica",
        "Campos: Subject, Issuer, Public Key, Validity, Extensions, Signature",
        "Estandar internacional definido en RFC 5280"],
    1: ["Certificate Authority — autoridad que emite certs firmandolos",
        "Confiamos por: presencia en stores oficiales (publicas), acuerdos comerciales",
        "  o decision interna del consorcio (privadas/Fabric)"],
    2: ["Cert auto-firmado al inicio del arbol de confianza",
        "Subject e Issuer son la misma entidad",
        "No tiene cert por encima — es el ancla de confianza"],
    3: ["Secuencia de certs desde un cert hasta la raiz",
        "Cada cert firmado por el de arriba",
        "Para validar: recorrer la cadena hasta llegar a un raíz conocido"],
})

add_content_slide(prs, "Respuestas al repaso (2/2)", [
    "5. Las dos CAs de Fabric:",
    "6. MSP — Membership Service Provider:",
    "7. NodeOUs:",
    "8. Verificaciones criptograficas en una transaccion:",
], subbullets={
    0: ["CA de identidad — quien firma transacciones (capa aplicacion)",
        "TLS CA — quien establece conexiones (capa transporte)",
        "Estan separadas por seguridad y aislamiento de daños"],
    1: ["Carpeta con certs que define quién pertenece a una org",
        "Tipos: Local MSP (un nodo/usuario, con clave privada) y",
        "       Channel MSP (la org en si, sin clave privada)",
        "Estructura: cacerts/, tlscacerts/, keystore/, signcerts/, etc."],
    2: ["Organizational Units que distinguen tipos de identidad: client, peer, admin, orderer",
        "Permiten al chaincode aplicar permisos diferentes a cada tipo",
        "Se activan con EnableNodeOUs: true"],
    3: ["TLS de la conexion (TLS CA)",
        "Cert de identidad del firmante (CA de identidad)",
        "Firma de la transaccion (clave publica del firmante)",
        "Firma de cada endorsement (CA de cada org)",
        "Cert TLS del orderer (TLS CA del orderer)",
        "Total: 4-6 verificaciones por transaccion"],
})

# ============================================================
# CIERRE
# ============================================================
add_section_slide(prs, "Lo que ya sabes",
    "Has entendido la base de identidad en Fabric")

add_content_slide(prs, "Resumen ejecutivo", [
    "PKI: la criptografia asimetrica + certificados firmados por una CA",
    "CA: la autoridad cuya firma da validez a los certificados",
    "Cert raíz: el ancla de confianza, auto-firmada, en la cima del arbol",
    "Cadena de confianza: la secuencia firma-firma desde un cert hasta el raíz",
    "Fabric usa DOS CAs separadas: identidad (firmar transacciones) y TLS (cifrar comunicacion)",
    "MSP: la carpeta de certs que define una identidad o una organizacion en Fabric",
    "NodeOUs: distinguen tipos de identidad (client, peer, admin, orderer)",
    "Cada transaccion implica 4-6 verificaciones criptograficas — Fabric esta optimizado para ello",
    "",
    "Ya tienes la base para entender Fabric CA, MSPs, lifecycle y operaciones avanzadas.",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 5/pki_certificados_msp.pptx")
print("pki_certificados_msp.pptx generado OK")
print(f"Total slides: {len(prs.slides)}")
