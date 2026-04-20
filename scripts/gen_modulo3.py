import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

# ============================================================
# DIA 1: Casos de uso reales
# ============================================================
prs = new_prs()

add_title_slide(prs, "Casos de Uso Reales:\nExitos y Fracasos",
    "Dia 1 - Que funciona, que no funciona y por que",
    module="Modulo 3: Vision Empresarial")

add_section_slide(prs, "Casos que SI funcionan", "Proyectos blockchain enterprise en produccion")

add_content_slide(prs, "Walmart Food Trust (IBM + Hyperledger Fabric)", [
    "Trazabilidad alimentaria: rastrear el origen de productos frescos",
    "Antes: rastrear un mango de la tienda a la granja tardaba 7 dias",
    "Con Fabric: el mismo rastreo tarda 2.2 segundos",
    "Mas de 150 organizaciones conectadas (proveedores, distribuidores)",
    "En produccion desde 2018 — uno de los mayores exitos de Fabric",
    "Clave del exito: Walmart exigio a sus proveedores que participaran",
],
subbullets={
    5: ["Cuando el actor mas grande del ecosistema impone la adopcion, funciona",
        "Pero genera debate: ¿es un consorcio o una imposicion?"],
})

add_content_slide(prs, "We.Trade (financiacion de comercio internacional)", [
    "Consorcio de 12 bancos europeos (Deutsche Bank, HSBC, Santander, etc.)",
    "Plataforma para financiar operaciones de comercio internacional entre PYMEs",
    "Basado en Hyperledger Fabric",
    "Flujo: PYME solicita financiacion → banco del comprador garantiza → banco del vendedor adelanta",
    "Reduce el papeleo y el riesgo de fraude en operaciones cross-border",
    "Lecciones: funciona porque todos los bancos tienen incentivo claro (reducir riesgo y coste)",
])

add_content_slide(prs, "HKMA eTradeConnect (Hong Kong)", [
    "Hong Kong Monetary Authority: plataforma de trade finance en Fabric",
    "Conecta bancos de Hong Kong para compartir informacion de operaciones comerciales",
    "Evita el fraude de doble financiacion (un exportador pide credito a dos bancos por la misma mercancia)",
    "Interoperable con We.Trade (Europa) para operaciones Asia-Europa",
    "En produccion desde 2019",
    "Clave: respaldo del regulador (HKMA) desde el inicio",
])

add_content_slide(prs, "Otros casos en produccion", [
    "ANZ + Scentre Group (Australia): tokenizacion de alquileres comerciales en Fabric",
    "Maersk + IBM TradeLens: trazabilidad maritima (cerro en 2022, pero funciono tecnicamente)",
    "Marco Polo Network: trade finance multi-banco en Corda",
    "De Beers Tracr: trazabilidad de diamantes (funciona pero adopcion limitada)",
    "Everledger: certificados de autenticidad de vinos, diamantes y arte",
    "Carrefour: trazabilidad alimentaria (pollos, tomates) en Francia",
])

add_section_slide(prs, "Casos que fracasaron", "¿Que podemos aprender?")

add_content_slide(prs, "TradeLens (Maersk + IBM) — cerro en 2022", [
    "Trazabilidad de comercio maritimo global en Hyperledger Fabric",
    "Inversion de cientos de millones de dolares",
    "¿Por que fallo?",
],
subbullets={
    2: ["Las navieras competidoras no querian unirse a una plataforma de Maersk",
        "Problema del 'fundador dominante': ¿por que dar mis datos a mi competidor?",
        "No se alcanzo masa critica: la red sin todos los actores no aportaba valor",
        "Leccion: la gobernanza importa mas que la tecnologia"],
})

add_content_slide(prs, "B3i (consorcio de aseguradoras) — cerro en 2022", [
    "Reaseguros automatizados en R3 Corda",
    "Fundadores: Allianz, Swiss Re, Zurich, Munich Re y +15 aseguradoras",
    "¿Por que fallo?",
],
subbullets={
    2: ["No encontro modelo de negocio viable: ¿quien paga la plataforma?",
        "Las aseguradoras querian participar pero no financiar indefinidamente",
        "Complejidad regulatoria: cada pais con reglas distintas",
        "Los sistemas legacy eran muy dificiles de integrar",
        "Leccion: la tecnologia funcionaba, el negocio no"],
})

add_content_slide(prs, "Mas fracasos y sus lecciones", [
    "MedRec (MIT): historial medico en Ethereum — nunca paso de piloto",
    "  Regulacion sanitaria + UX para medicos = barrera insalvable",
    "",
    "Voatz: votacion electronica — auditores encontraron vulnerabilidades",
    "  Seguridad + desconfianza politica = rechazo total",
    "",
    "Registro de propiedad Honduras: abandonado por resistencia institucional",
    "  Los beneficiarios de la corrupcion bloquearon el proyecto",
])

add_table_slide(prs, "Resumen: exitos vs fracasos",
    ["Factor", "Los que funcionan", "Los que fracasan"],
    [
        ["Gobernanza", "Equilibrada o respaldada por regulador", "Fundador dominante o sin gobierno claro"],
        ["Incentivos", "Todos ganan algo concreto", "Solo unos pocos se benefician"],
        ["Masa critica", "Actor principal impone o regulador exige", "Voluntario y sin urgencia"],
        ["Regulacion", "Compatible o con apoyo del regulador", "Choca con leyes existentes"],
        ["UX", "Invisible para el usuario final", "Requiere que el usuario entienda blockchain"],
        ["MVP", "Empiezan pequeno y escalan", "Intentan todo desde el dia 1"],
    ])

add_content_slide(prs, "¿Blockchain o base de datos? Arbol de decision", [
    "Hazte estas preguntas en orden:",
    "",
    "1. ¿Hay multiples partes que no confian entre si? → Si no, usa una BD",
    "2. ¿Necesitan compartir datos y validar transacciones? → Si no, usa APIs",
    "3. ¿La inmutabilidad del registro es critica? → Si no, usa una BD compartida",
    "4. ¿Las reglas de negocio deben ser verificables por todos? → Si no, usa una BD con permisos",
    "5. ¿Ningun actor puede ser 'el dueño' de la base de datos? → Si no, que ese actor la gestione",
    "",
    "Si has respondido SI a todas: blockchain tiene sentido.",
    "Si has respondido NO a alguna: probablemente no necesitas blockchain.",
])

add_image_placeholder(prs, "Arbol de decision: ¿necesito blockchain?",
    "[Diagrama de arbol de decision con preguntas si/no que llevan a 'Usa blockchain' o 'Usa base de datos']",
    "Decision tree flowchart: starting question 'Multiple parties that don't trust each other?' branching YES/NO through questions about shared data, immutability, verifiable rules, and neutral ownership. YES path leads to 'Consider blockchain', NO paths lead to 'Use a database'. Clean flat design, teal for YES paths, red for NO paths.")

add_debate_slide(prs, "¿Blockchain o base de datos?", [
    "Para cada caso, decidir en grupo si blockchain tiene sentido o no. Justificar:",
    "",
    "1. Un hospital quiere registrar historiales medicos de sus pacientes",
    "2. Tres hospitales quieren compartir historiales de pacientes compartidos",
    "3. Un banco quiere un registro inmutable de sus transacciones internas",
    "4. Diez bancos quieren un sistema de liquidacion interbancaria sin intermediario",
    "5. Una empresa quiere rastrear sus envios internos entre almacenes",
    "6. Un consorcio de 50 productores quiere certificar el origen de sus productos",
])

add_special_slide(prs, "TREASURE HUNT", "El primer proyecto blockchain enterprise", [
    "Antes de Fabric, antes de Corda, antes de los consorcios...",
    "hubo un proyecto que demostro que blockchain podia usarse en empresas.",
    "",
    "Mision: Investigar:",
    "  1. ¿Que proyecto se considera el primero en usar blockchain en enterprise?",
    "     Pista: fue en el sector financiero, en 2015, y no usaba Ethereum.",
    "  2. ¿Que empresa lo impulso?",
    "  3. ¿En que se convirtio ese proyecto despues?",
    "",
    "Tiempo: 10 minutos.",
])

add_review_slide(prs, "Repaso del dia", [
    "Nombra 3 proyectos blockchain enterprise que funcionan en produccion",
    "Nombra 2 que fracasaron y la razon principal de cada uno",
    "¿Cuales son las 5 preguntas del arbol de decision para saber si necesitas blockchain?",
    "¿Que significa el 'problema del fundador dominante'?",
    "¿Por que el respaldo del regulador es un factor clave de exito?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/dia_1.pptx")
print("Modulo 3 dia_1.pptx OK")

# ============================================================
# DIA 2: Identificar oportunidades de negocio
# ============================================================
prs = new_prs()

add_title_slide(prs, "Identificar Oportunidades\nde Negocio",
    "Dia 2 - Cuando tiene sentido blockchain y como venderlo",
    module="Modulo 3: Vision Empresarial")

add_content_slide(prs, "¿Cuando tiene sentido blockchain enterprise?", [
    "Multiples organizaciones que necesitan compartir datos",
    "Desconfianza mutua: ninguna quiere que otra controle la base de datos",
    "Necesidad de trazabilidad inmutable (regulacion, auditoria, compliance)",
    "Reglas de negocio que deben ser verificables por todos los participantes",
    "Transacciones entre partes que hoy requieren intermediarios costosos",
    "",
    "Si se cumplen TODAS estas condiciones, blockchain aporta valor.",
    "Si falta alguna, probablemente hay una solucion mas sencilla.",
])

add_content_slide(prs, "¿Cuando NO tiene sentido?", [
    "Un solo actor gestiona todos los datos (usa una base de datos)",
    "Los datos no se comparten entre organizaciones (usa APIs)",
    "El rendimiento es critico y necesitas miles de TPS con baja latencia",
    "Los datos necesitan ser editables o borrables (GDPR, derecho al olvido)",
    "No hay problema de confianza entre las partes (usa un SaaS compartido)",
    "El coste de montar y mantener la red no compensa el beneficio",
    "",
    "Blockchain NO es la solucion a todo. Saber cuando NO usarlo",
    "es tan importante como saber cuando si.",
])

add_content_slide(prs, "Oportunidades por sector", [
    "Finanzas: liquidacion, trade finance, tokenizacion de activos, KYC compartido",
    "Supply chain: trazabilidad, certificacion de origen, cold chain",
    "Salud: historiales compartidos, trazabilidad de farmacos, ensayos clinicos",
    "Administracion publica: registro de propiedad, licitaciones, subvenciones",
    "Energia: certificados de origen renovable, mercados P2P de energia",
    "Seguros: reaseguros automatizados, gestion de siniestros multi-aseguradora",
    "Educacion: titulos verificables, credenciales profesionales",
])

add_content_slide(prs, "Como presentar un proyecto blockchain al comite de direccion", [
    "NO empieces por la tecnologia. Empieza por el problema de negocio:",
    "",
    "1. ¿Cual es el problema? (coste, tiempo, fraude, desconfianza)",
    "2. ¿Cuanto nos cuesta hoy? (euros, dias, riesgo)",
    "3. ¿Por que las soluciones actuales no funcionan? (intermediarios, silos)",
    "4. ¿Que propones? (consorcio + ledger compartido — sin decir 'blockchain' aun)",
    "5. ¿Con quien lo hariamos? (socios del consorcio)",
    "6. ¿Cuanto cuesta y cuanto ahorra? (ROI, payback)",
    "7. ¿Que riesgos tiene? (y como los mitigamos)",
    "",
    "Consejo: la palabra 'blockchain' genera ruido. Usa 'registro distribuido compartido'.",
])

add_content_slide(prs, "ROI y metricas: ¿como mides el exito?", [
    "Metricas de eficiencia:",
    "Metricas de confianza:",
    "Metricas de coste:",
],
subbullets={
    0: ["Tiempo de proceso: ¿cuanto se redujo? (ej: KYC de 2 semanas a 2 minutos)",
        "Errores: ¿cuantos errores manuales se eliminaron?",
        "Intermediarios: ¿cuantos pasos/actores se eliminaron?"],
    1: ["Disputas: ¿cuantas disputas comerciales se evitaron?",
        "Auditoria: ¿cuanto tarda una auditoria ahora vs antes?",
        "Fraude: ¿cuantos casos de fraude se detectaron/evitaron?"],
    2: ["Coste de infraestructura: ¿cuanto cuesta mantener la red?",
        "Coste de intermediarios eliminados: ¿cuanto ahorramos?",
        "Payback: ¿en cuanto tiempo se recupera la inversion?"],
})

add_activity_slide(prs, "Elevator pitch: tu proyecto blockchain", [
    "Cada alumno (o pareja) prepara un elevator pitch de 2 minutos:",
    "",
    "1. Elegir un problema real de su empresa o sector",
    "2. Verificar con el arbol de decision que blockchain tiene sentido",
    "3. Preparar el pitch con esta estructura:",
    "   - El problema (30 seg)",
    "   - Por que las soluciones actuales no sirven (30 seg)",
    "   - La propuesta con blockchain (30 seg)",
    "   - Los socios del consorcio y el beneficio esperado (30 seg)",
    "",
    "Presentar al resto de la clase. Feedback constructivo.",
    "Tiempo de preparacion: 20 minutos.",
], badge_text="ACTIVIDAD")

add_special_slide(prs, "CULTURA GENERAL", "Gartner y el Hype Cycle", [
    "Gartner publica cada ano su Hype Cycle for Blockchain and Web3.",
    "En 2017, blockchain estaba en el 'Pico de Expectativas Infladas'.",
    "En 2023, blockchain enterprise habia caido al 'Valle de la Desilusion'.",
    "En 2025, empieza a subir la 'Pendiente de la Iluminacion'.",
    "",
    "Esto es normal: TODAS las tecnologias pasan por este ciclo.",
    "Internet en 2001, cloud en 2010, IA en 2024... y blockchain ahora.",
    "",
    "La pregunta no es '¿blockchain esta muerto?'",
    "La pregunta es '¿para que casos concretos es util?'",
    "Eso es exactamente lo que estamos aprendiendo en este modulo.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

add_review_slide(prs, "Repaso del dia", [
    "¿Cuando tiene sentido blockchain enterprise? Da 3 condiciones",
    "¿Cuando NO tiene sentido? Da 3 razones",
    "¿Como presentarias un proyecto blockchain a un comite de direccion?",
    "¿Que metricas usarias para medir el exito?",
    "¿Por que es mejor no empezar con la palabra 'blockchain'?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/dia_2.pptx")
print("Modulo 3 dia_2.pptx OK")

# ============================================================
# DIA 3: Gobernanza
# ============================================================
prs = new_prs()

add_title_slide(prs, "Gobernanza y Toma\nde Decisiones",
    "Dia 3 - Quien manda en un consorcio blockchain",
    module="Modulo 3: Vision Empresarial")

add_content_slide(prs, "¿Que es la gobernanza de un consorcio?", [
    "El conjunto de reglas que definen como se toman las decisiones en la red",
    "No es un tema tecnico: es un tema politico, legal y de negocio",
    "Si la gobernanza no esta clara desde el dia 1, el proyecto fracasara",
    "Preguntas que debe responder:",
],
subbullets={
    3: ["¿Quien puede unirse a la red? ¿Y quien puede ser expulsado?",
        "¿Quien aprueba cambios en los chaincodes?",
        "¿Quien paga la infraestructura (orderers, CAs)?",
        "¿Como se resuelven los conflictos?",
        "¿Que pasa con los datos si una org abandona?"],
})

add_content_slide(prs, "Modelos de gobernanza", [
    "Fundador dominante: una empresa crea la red y pone las reglas",
    "  Ejemplo: Walmart Food Trust. Walmart decide, los proveedores acatan",
    "  Pro: rapido de arrancar. Contra: los demas desconfian",
    "",
    "Democratico: todas las orgs tienen el mismo voto",
    "  Ejemplo: Alastria. Cada miembro un voto en la asamblea",
    "  Pro: equitativo. Contra: lento, dificil llegar a acuerdos",
    "",
    "Federado: un comite tecnico/ejecutivo toma las decisiones operativas",
    "  Ejemplo: EBSI. La EBP decide la estrategia, los estados operan",
    "  Pro: agil. Contra: el comite puede desconectarse de los miembros",
])

add_content_slide(prs, "Gobernanza en Fabric: las politicas como herramienta", [
    "Fabric codifica la gobernanza directamente en la configuracion del canal:",
    "",
    "Politicas de canal: quien puede leer, escribir, administrar",
    "  MAJORITY Admins: la mayoria de orgs deben aprobar cambios",
    "  ALL Admins: unanimidad requerida",
    "",
    "Politicas de endorsement: quien valida cada transaccion",
    "  AND(Org1, Org2): ambas deben aprobar",
    "  OR(Org1, Org2): basta con una",
    "",
    "Lifecycle: aprobar chaincodes requiere mayoria de orgs",
    "",
    "Las politicas de Fabric son gobernanza ejecutable: no son un documento, son codigo.",
])

add_content_slide(prs, "¿Quien paga que?", [
    "Cada organizacion paga SU infraestructura:",
    "  Sus peers, su Fabric CA, su almacenamiento",
    "",
    "La infraestructura compartida es el debate:",
    "  Orderer: ¿quien lo opera? ¿se reparte el coste?",
    "  Desarrollo de chaincodes: ¿quien lo paga? ¿quien lo mantiene?",
    "  Soporte y operaciones: ¿hay un equipo central o cada org se apana?",
    "",
    "Modelos comunes:",
    "  Cuota fija: todos pagan lo mismo (simple, pero ¿justo?)",
    "  Por uso: paga mas quien mas transacciones hace",
    "  Por tamano: las orgs grandes pagan mas que las pequenas",
    "  Sponsor: una org grande subvenciona al resto (al principio)",
])

add_content_slide(prs, "Onboarding y offboarding de organizaciones", [
    "Incorporar una nueva org (onboarding):",
    "Expulsar o que se vaya una org (offboarding):",
],
subbullets={
    0: ["Evaluacion: ¿cumple los requisitos del consorcio?",
        "Aprobacion: las orgs existentes votan (MAJORITY o ALL)",
        "Tecnico: generar identidades, anadir al canal (doc 06)",
        "Legal: firmar el acuerdo de consorcio",
        "Operativo: instalar chaincodes, sincronizar ledger"],
    1: ["¿Que pasa con sus datos en el ledger? (son inmutables, no se pueden borrar)",
        "¿Que pasa con sus certificados? (revocar via CRL)",
        "¿Puede llevarse una copia de los datos? (depende del acuerdo)",
        "¿Como se redistribuyen sus responsabilidades?",
        "Esto DEBE estar definido ANTES de que pase"],
})

add_content_slide(prs, "Caso Alastria: gobernanza de un consorcio real", [
    "Alastria es una asociacion sin animo de lucro con +500 miembros",
    "Estructura de gobierno:",
    "Decisiones tecnicas: Comite Tecnico (rotativo entre miembros activos)",
    "Cuotas anuales segun tamano de la empresa",
    "Leccion: el modelo funciona pero es lento. 500 miembros = 500 opiniones.",
],
subbullets={
    1: ["Asamblea General: todos los miembros votan (1 miembro = 1 voto)",
        "Junta Directiva: 15 miembros elegidos, toma decisiones ejecutivas",
        "Grupos de trabajo: identidad, tokenizacion, regulacion, etc."],
})

add_debate_slide(prs, "Disenar la gobernanza de un consorcio", [
    "Escenario: 5 bancos quieren crear una plataforma de KYC compartido en Fabric.",
    "",
    "Decidir en grupo:",
    "1. ¿Que modelo de gobernanza elegis? (fundador, democratico, federado)",
    "2. ¿Que politica de endorsement usariais? (AND, OR, MAJORITY)",
    "3. ¿Quien opera los orderers?",
    "4. ¿Como se incorpora un nuevo banco?",
    "5. ¿Que pasa si un banco quiere salir? ¿Y con los datos KYC de sus clientes?",
])

add_review_slide(prs, "Repaso del dia", [
    "¿Que es la gobernanza de un consorcio y por que es critica?",
    "Nombra los 3 modelos de gobernanza y un ejemplo de cada uno",
    "¿Como codifica Fabric la gobernanza? (politicas)",
    "¿Quien deberia pagar los orderers?",
    "¿Que hay que definir ANTES de que una org abandone el consorcio?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/dia_3.pptx")
print("Modulo 3 dia_3.pptx OK")

# ============================================================
# DIA 4: Marco legal y regulatorio
# ============================================================
prs = new_prs()

add_title_slide(prs, "Marco Legal y\nRegulatorio",
    "Dia 4 - GDPR, MiCA, smart contracts y responsabilidad legal",
    module="Modulo 3: Vision Empresarial")

add_content_slide(prs, "Blockchain y GDPR: la tension fundamental", [
    "GDPR (Reglamento General de Proteccion de Datos) establece:",
    "  Derecho al olvido: el ciudadano puede pedir que borren sus datos",
    "  Minimizacion: solo guardar los datos estrictamente necesarios",
    "  Limitacion de almacenamiento: no conservar datos mas de lo necesario",
    "",
    "Blockchain establece: los datos son inmutables y permanentes",
    "",
    "¿Es incompatible? No del todo, pero hay que disenar con cuidado:",
],
subbullets={
    7: ["NUNCA guardar datos personales directamente en el ledger",
        "Guardar un hash o referencia: los datos reales off-chain (BD normal)",
        "Private Data Collections: los datos se pueden purgar (blockToLive)",
        "Si se borra el dato off-chain, el hash on-chain es inutil (pseudonimizacion)"],
})

add_content_slide(prs, "Smart contracts: ¿son contratos legales?", [
    "Respuesta corta: NO, al menos no automaticamente",
    "Un smart contract es codigo, no un contrato juridico",
    "Para que tenga valor legal necesita:",
    "",
    "Jurisprudencia actual: muy limitada, varia por pais",
    "Enfoque practico: el smart contract EJECUTA las clausulas de un contrato legal separado",
    "El contrato legal dice QUE se hace. El smart contract COMO se ejecuta.",
],
subbullets={
    2: ["Consentimiento de las partes (firma digital)",
        "Objeto licito (lo que hace el contrato es legal)",
        "Identificacion de las partes (no anonimas)",
        "Jurisdiccion y ley aplicable definidas",
        "Mecanismo de resolucion de disputas"],
})

add_content_slide(prs, "MiCA: regulacion europea de criptoactivos", [
    "Markets in Crypto-Assets Regulation (MiCA) — en vigor desde diciembre 2024",
    "Aplica a: tokens de utilidad, stablecoins, criptoactivos en general",
    "NO aplica directamente a: blockchain enterprise/permissioned sin tokens publicos",
    "Pero es relevante si tu proyecto Fabric incluye tokens que salen al mercado",
    "",
    "Puntos clave de MiCA:",
],
subbullets={
    5: ["Emisores de stablecoins: necesitan autorizacion y reservas auditadas",
        "Exchanges y custodios: necesitan licencia",
        "Whitepaper obligatorio: describir el token, riesgos, derechos",
        "Proteccion al inversor: informacion clara, derecho de retirada",
        "Supervisores: ESMA y autoridades nacionales (CNMV en Espana)"],
})

add_content_slide(prs, "Tokenizacion de activos: regulacion actual", [
    "Si tokenizas un activo real (bono, accion, inmueble) en Fabric:",
    "  El token puede ser un 'valor negociable' segun MiFID II",
    "  Necesitas autorizacion de la CNMV (Espana) o equivalente europeo",
    "  Aplican las mismas reglas que a los valores tradicionales",
    "",
    "Security Token Offerings (STOs): tokenizar + vender al publico",
    "  Mas regulado que una ICO, pero legal y con marco claro",
    "  Ejemplo: Bit2Me STX (autorizado por CNMV bajo regimen sandbox)",
    "",
    "Tokenizacion interna (entre orgs de un consorcio): menos regulacion",
    "  Si los tokens no salen de la red permissioned, MiCA no aplica directamente",
])

add_content_slide(prs, "Responsabilidad legal: si el chaincode tiene un bug", [
    "¿Quien responde si un chaincode transfiere fondos incorrectamente?",
    "",
    "Escenarios:",
    "  1. Bug del desarrollador: ¿responsabilidad del desarrollador o de la org que lo aprobo?",
    "  2. Todas las orgs aprobaron el chaincode (lifecycle): ¿responsabilidad compartida?",
    "  3. Una org detecto el bug pero no lo reporto: ¿negligencia?",
    "",
    "En la practica: el acuerdo del consorcio debe definir",
    "  ¿Quien audita los chaincodes antes de aprobarlos?",
    "  ¿Hay seguro de responsabilidad?",
    "  ¿Que mecanismo de compensacion existe?",
    "  ¿Que jurisdiccion y ley aplican?",
])

add_debate_slide(prs, "Marco legal y blockchain", [
    "1. ¿Donde guardarias los datos personales de clientes en un proyecto Fabric? ¿On-chain o off-chain?",
    "2. Si un smart contract ejecuta una clausula incorrectamente, ¿quien es responsable?",
    "3. ¿Deberia el regulador tener acceso de solo lectura a todos los canales de Fabric?",
    "4. Un consorcio de bancos tokeniza bonos en Fabric. ¿Que regulacion aplica?",
    "5. ¿Es MiCA un freno o un acelerador para blockchain enterprise en Europa?",
])

add_special_slide(prs, "CULTURA GENERAL", "El caso DAO y la ley", [
    "En 2016, el hack de The DAO robo 60 millones de dolares en ETH.",
    "La comunidad Ethereum hizo un hard fork para revertir el robo.",
    "",
    "Preguntas legales sin respuesta clara (aun hoy):",
    "  ¿Fue un robo si el atacante 'solo' ejecuto el codigo tal como estaba escrito?",
    "  ¿El hard fork fue una confiscacion de activos?",
    "  ¿Quien tenia jurisdiccion? ¿Suiza (donde estaba The DAO)? ¿Internet?",
    "",
    "En 2023, la SEC demando a los creadores de The DAO por vender valores no registrados.",
    "7 anos despues, la ley sigue poniendose al dia con la tecnologia.",
], badge_color=RGBColor(0x7C, 0x3A, 0xED))

add_review_slide(prs, "Repaso del dia", [
    "¿Como se reconcilia GDPR con la inmutabilidad de blockchain?",
    "¿Un smart contract es un contrato legal? ¿Que le falta?",
    "¿Que es MiCA y a quien aplica?",
    "¿Que regulacion aplica si tokenizas un bono en Fabric?",
    "Si un chaincode tiene un bug, ¿quien responde?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/dia_4.pptx")
print("Modulo 3 dia_4.pptx OK")

# ============================================================
# DIA 5: Diseno de proyectos empresariales
# ============================================================
prs = new_prs()

add_title_slide(prs, "Diseño de Proyectos\nEmpresariales con Fabric",
    "Dia 5 - De la idea al proyecto: metodologia practica",
    module="Modulo 3: Vision Empresarial")

add_content_slide(prs, "Metodologia: de la idea al proyecto", [
    "1. Identificar el problema (dia 2): ¿que duele? ¿a quien? ¿cuanto cuesta?",
    "2. Validar que blockchain aporta (dia 1): arbol de decision",
    "3. Definir el consorcio: quienes participan, que rol tiene cada uno",
    "4. Disenar la gobernanza (dia 3): politicas, costes, onboarding",
    "5. Disenar la red Fabric: organizaciones, canales, datos",
    "6. Definir el MVP: empezar pequeno, demostrar valor",
    "7. Planificar: roadmap, equipo, presupuesto, riesgos",
])

add_content_slide(prs, "Disenar la red: preguntas clave", [
    "¿Cuantas organizaciones? ¿Cada una tiene su propio peer?",
    "¿Cuantos canales? ¿Todas las orgs comparten todo o hay datos segregados?",
    "¿Que datos van on-chain y cuales off-chain?",
    "¿Private Data Collections o canales separados para datos confidenciales?",
    "¿CouchDB (rich queries) o LevelDB (rendimiento)?",
    "¿Cuantos orderers? ¿Quien los opera?",
    "¿cryptogen (piloto) o Fabric CA (produccion)?",
    "¿On-premise o cloud (AWS, Azure, IBM)?",
])

add_image_placeholder(prs, "Template: topologia de red Fabric",
    "[Diagrama en blanco con cajas para rellenar: Org1, Org2, Org3, Orderer, Canal A, Canal B, Private Data]",
    "Blank network topology template for Hyperledger Fabric: empty boxes labeled Org1, Org2, Org3, Orderer Service. Dashed lines showing potential channels (Channel A, Channel B). Separate box for Private Data Collections. Clean wireframe style, ready to be filled in by students.")

add_content_slide(prs, "Estimar costes de un proyecto Fabric", [
    "Infraestructura:",
    "Desarrollo:",
    "Operaciones:",
],
subbullets={
    0: ["Servidores/cloud para peers, orderers, CAs, CouchDB",
        "Estimacion: 500-2000 EUR/mes por organizacion (cloud)",
        "Mas barato on-premise pero requiere equipo de sistemas"],
    1: ["Chaincodes: 2-6 meses de desarrollo segun complejidad",
        "Aplicacion cliente: 1-3 meses adicionales",
        "Integracion con sistemas legacy: el coste mas impredecible"],
    2: ["Administracion de la red: 0.5-1 persona por org",
        "Soporte y mantenimiento: 20-30% del coste de desarrollo anual",
        "Gobernanza: reuniones, comites, decision-making (tiempo de directivos)"],
})

add_content_slide(prs, "Roadmap tipico de un proyecto Fabric", [
    "Mes 1-2: Descubrimiento",
    "  Definir el problema, validar blockchain, identificar socios",
    "",
    "Mes 3-4: PoC (Proof of Concept)",
    "  Red minima (2 orgs), chaincode basico, demostrar que funciona",
    "",
    "Mes 5-8: MVP (Minimum Viable Product)",
    "  Red con Fabric CA, chaincode completo, app cliente, tests",
    "",
    "Mes 9-12: Piloto",
    "  Datos reales, mas organizaciones, integracion con sistemas",
    "",
    "Mes 12+: Produccion",
    "  SLAs, monitorizacion, soporte 24/7, gobernanza formal",
])

add_activity_slide(prs, "Disena tu proyecto Fabric", [
    "Cada grupo disena un proyecto completo para un caso de uso de su sector.",
    "",
    "Entregables (en papel o pizarra):",
    "  1. Problema y propuesta de valor (2 frases)",
    "  2. Organizaciones del consorcio (quienes, que rol)",
    "  3. Diagrama de la red: orgs, canales, datos on/off-chain",
    "  4. Modelo de gobernanza: politicas, costes, onboarding",
    "  5. MVP: que incluye la primera version",
    "  6. Roadmap: 4 fases con duraciones estimadas",
    "  7. 3 riesgos principales y como mitigarlos",
    "",
    "Tiempo: 40 minutos. Presentar en 10 minutos por grupo.",
    "El resto de la clase hace de 'comite de inversion' y da feedback.",
], badge_text="PROYECTO")

add_debate_slide(prs, "Cierre del Modulo 3", [
    "1. ¿Que ha sido lo mas sorprendente de este modulo?",
    "2. ¿Habeis cambiado de opinion sobre blockchain enterprise respecto al inicio del curso?",
    "3. ¿Veis una oportunidad real en vuestro sector? ¿Cual?",
    "4. ¿Que es mas dificil: la tecnologia, la gobernanza o la regulacion?",
    "5. Si tuvierais presupuesto ilimitado, ¿que proyecto blockchain montariais?",
])

add_review_slide(prs, "Repaso del Modulo 3", [
    "Casos de exito y fracaso: patrones comunes",
    "Arbol de decision: ¿blockchain o base de datos?",
    "Como presentar un proyecto blockchain a direccion",
    "Modelos de gobernanza: fundador, democratico, federado",
    "GDPR vs inmutabilidad: como resolverlo",
    "MiCA y regulacion de tokens",
    "Metodologia: de la idea al roadmap",
    "Costes tipicos de un proyecto Fabric",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/dia_5.pptx")
print("Modulo 3 dia_5.pptx OK")
