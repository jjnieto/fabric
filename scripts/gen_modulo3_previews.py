import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

# ============================================================
# WE.TRADE
# ============================================================
prs = new_prs()

add_title_slide(prs, "We.Trade:\nTrade Finance para PYMEs",
    "Consorcio de 12 bancos europeos sobre Hyperledger Fabric",
    module="Modulo 3: Vision Empresarial")

add_section_slide(prs, "Caso 2: We.Trade", "Financiacion de comercio internacional entre PYMEs")

add_content_slide(prs, "El problema que resolvieron", [
    "Una PYME que exporta a otro pais tiene un problema de confianza",
    "¿Y si el comprador no paga? ¿Y si el vendedor no envia la mercancia?",
    "Tradicionalmente se resuelve con cartas de credito: caras y lentas",
    "Cada banco tiene sus propios sistemas, papeleo manual, semanas de proceso",
    "Las PYMEs pequenas no pueden permitirselo — comercian solo con clientes conocidos",
    "Se pierde volumen de comercio internacional por falta de confianza",
])

add_content_slide(prs, "La solucion con Hyperledger Fabric", [
    "Consorcio de 12 bancos europeos fundan We.Trade en 2018",
    "Miembros: Deutsche Bank, HSBC, Santander, KBC, Nordea, Rabobank, UBS...",
    "Ledger compartido: todos los bancos ven el estado de las operaciones en tiempo real",
    "Flujo digitalizado:",
],
subbullets={
    3: ["PYME Compradora: quiere comprar mercancia a PYME Vendedora (otro pais)",
        "Su banco garantiza el pago bajo ciertas condiciones",
        "El banco del vendedor adelanta el 90% del pago inmediatamente",
        "Cuando se confirma la entrega, se libera el resto",
        "Todo registrado en blockchain, sin papeles, en horas en vez de semanas"],
})

add_content_slide(prs, "Resultados y cierre en 2022", [
    "En produccion desde 2018",
    "Procesaron operaciones reales entre PYMEs de diferentes paises",
    "Reduccion drastica de tiempos: de semanas a horas",
    "",
    "Cerro en julio de 2022. ¿Por que?",
    "No fue un problema tecnologico",
    "Fue un problema de modelo de negocio:",
],
subbullets={
    6: ["Las 12 aseguradoras querian participar pero no financiar indefinidamente",
        "Faltaba un modelo de ingresos que sostuviera la plataforma",
        "Cuando se acabo el capital inicial, el proyecto se cerro"],
})

add_image_placeholder(prs, "Flujo de We.Trade",
    "[Diagrama: PYME compradora <-> Banco comprador <-> Banco vendedor <-> PYME vendedora, todos sobre un canal Fabric compartido]",
    "Trade finance flow diagram showing two SMEs (buyer and seller) each connected to their respective banks, all sharing a Hyperledger Fabric channel. Central shared ledger shows operation states. Clean flat design, blue and green color scheme for financial services.")

add_activity_slide(prs, "EJERCICIO: Diseña tu red de trade finance", [
    "Caso practico adaptado al aula: 3 bancos europeos gestionando operaciones comerciales.",
    "",
    "Actores:",
    "  - Banco Santander (Espana)",
    "  - Banco BBVA (Espana)",
    "  - Deutsche Bank (Alemania)",
    "  - Las PYMEs son usuarios registrados por los bancos (no orgs)",
    "",
    "Tareas:",
    "  FASE 1 (sobre el papel, 30 min):",
    "    Disenar la topologia: PYMEs como orgs o usuarios",
    "    Gestionar privacidad: canales separados o Private Data Collections",
    "    Definir maquina de estados de una operacion comercial",
    "  FASE 2 (en el ordenador, 90 min):",
    "    Montar red con 3 bancos",
    "    Crear Private Data Collections por cada par de bancos",
    "    Desplegar chaincode con politicas de endorsement",
    "    Probar flujo completo + validar privacidad",
    "",
    "Guia tecnica completa: docs/modulo-3/ejercicios/ejercicio-wetrade.md",
], badge_text="EJERCICIO")

add_content_slide(prs, "Preguntas clave para tu diseño", [
    "1. ¿Las PYMEs son organizaciones o usuarios de los bancos?",
    "2. ¿Un canal unico o canales por pareja de bancos?",
    "3. ¿Donde guardas los importes y datos sensibles? (Private Data)",
    "4. Estados de una operacion: proposed, approved, in_transit, delivered, paid",
    "5. ¿Que politica de endorsement para crear una operacion? ¿Y para liberar el pago?",
    "6. ¿Un regulador (BCE) deberia estar en el canal?",
    "7. Con N bancos se necesitan N*(N-1)/2 Private Data Collections. ¿Escala?",
])

add_debate_slide(prs, "Debate tras el ejercicio", [
    "1. ¿Por que We.Trade cerro a pesar de tener tecnologia y 12 grandes bancos?",
    "2. ¿Que modelo de ingresos propondriais para que sea sostenible?",
    "3. ¿Tiene sentido que las PYMEs sean usuarios y no orgs? ¿Que cambia?",
    "4. Si una PYME cambia de banco, ¿que pasa con su historial crediticio en la red?",
    "5. ¿Deberia haber un regulador (BCE) en el canal como en el caso HKMA?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/preview_wetrade.pptx")
print("preview_wetrade.pptx OK")

# ============================================================
# HKMA
# ============================================================
prs = new_prs()

add_title_slide(prs, "HKMA eTradeConnect:\nRegulador en el consorcio",
    "El banco central de Hong Kong como miembro de la red",
    module="Modulo 3: Vision Empresarial")

add_section_slide(prs, "Caso 3: HKMA eTradeConnect", "Plataforma interbancaria con el regulador dentro")

add_content_slide(prs, "El problema que resolvieron", [
    "Hong Kong es un hub de comercio internacional",
    "Fraude de doble financiacion: un exportador pide credito a 2 bancos por la misma mercancia",
    "Sin red compartida, cada banco solo ve sus operaciones — imposible detectar solapamientos",
    "Cada ano se pierden millones por este tipo de fraude",
    "La HKMA (banco central) necesitaba una forma de supervisar sin crear overhead burocratico",
])

add_content_slide(prs, "La solucion con Hyperledger Fabric", [
    "Lanzado en 2018 por la Hong Kong Monetary Authority (HKMA)",
    "Miembros iniciales: 12 bancos principales de Hong Kong",
    "HSBC, Standard Chartered, BOC HK, DBS, ICBC, ANZ, Hang Seng, BNP Paribas...",
    "Diferencia clave con We.Trade:",
],
subbullets={
    3: ["El regulador (HKMA) esta en el consorcio como una org mas",
        "Tiene visibilidad completa de todas las operaciones",
        "Puede marcar operaciones sospechosas para revision",
        "Pero NO puede modificar operaciones entre bancos",
        "Este diseno da equilibrio entre supervision y autonomia bancaria"],
})

add_content_slide(prs, "Deteccion automatica de doble financiacion", [
    "Identificador unico: el hash SHA-256 de la factura original",
    "Antes de financiar, el chaincode verifica que ese hash no este ya registrado",
    "Si existe: se rechaza la transaccion Y se emite evento al regulador",
    "",
    "Resultado: el fraude se detecta en el momento de la solicitud, no meses despues",
    "",
    "En produccion: millones de operaciones procesadas, cientos de fraudes detectados automaticamente",
    "Interoperable con We.Trade para operaciones Asia-Europa",
])

add_image_placeholder(prs, "Topologia HKMA eTradeConnect",
    "[Diagrama: 3-4 bancos conectados a un canal compartido, con la HKMA tambien conectada como org con permisos especiales]",
    "Network topology for HKMA eTradeConnect: three commercial banks (HSBC, Standard Chartered, BOC) each with their peer, plus a regulator node (HKMA) with special privileges. All connected to a shared channel. The regulator has reading access to everything plus flagging rights. Clean flat design with red accent for regulator.")

add_activity_slide(prs, "EJERCICIO: Diseña tu red con regulador", [
    "Caso practico adaptado al aula: 3 bancos + regulador.",
    "",
    "Actores:",
    "  - HSBC Hong Kong",
    "  - Standard Chartered",
    "  - BOC Hong Kong",
    "  - HKMA (banco central como org auditora)",
    "",
    "Tareas:",
    "  FASE 1 (sobre el papel, 30 min):",
    "    Definir permisos del regulador (leer, marcar, bloquear?)",
    "    Mecanismo de deteccion de doble financiacion",
    "    Conciliar privacidad bancaria con auditoria del regulador",
    "  FASE 2 (en el ordenador, 90 min):",
    "    Montar red con 4 orgs (3 bancos + regulador)",
    "    Desplegar chaincode con control de acceso por MSPID",
    "    Probar flujo happy path + intento de doble financiacion",
    "    Validar que el regulador audita pero no modifica",
    "",
    "Guia completa: docs/modulo-3/ejercicios/ejercicio-hkma.md",
], badge_text="EJERCICIO")

add_content_slide(prs, "Preguntas clave para tu diseño", [
    "1. ¿El regulador endorsea cada transaccion o solo audita?",
    "2. ¿Como identificas univocamente una factura para detectar duplicados?",
    "3. ¿Que datos personales PUEDES guardar on-chain? (cuidado con GDPR)",
    "4. ¿El regulador deberia poder CONGELAR operaciones sospechosas?",
    "5. ¿Que pasa si el certificado del regulador es comprometido?",
    "6. ¿Un rich query por invoiceHash es rapido con LevelDB? ¿Necesitas CouchDB?",
])

add_debate_slide(prs, "Debate: regulador como miembro del consorcio", [
    "1. ¿Tiene sentido que el regulador este en el consorcio o es mejor acceso via API?",
    "2. Hong Kong tiene a la HKMA. En Europa, ¿seria la BCE? ¿Cada pais su banco central?",
    "3. ¿Un regulador con acceso total a todas las operaciones es privacy-friendly?",
    "4. Si el regulador es comprometido, ¿que impacto tendria?",
    "5. ¿Puede un banco oponerse a una marca del regulador sin saltarse las reglas?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/preview_hkma.pptx")
print("preview_hkma.pptx OK")

# ============================================================
# TRADELENS
# ============================================================
prs = new_prs()

add_title_slide(prs, "TradeLens:\nCuando la gobernanza falla",
    "Un caso de fracaso a pesar de la tecnologia",
    module="Modulo 3: Vision Empresarial")

add_section_slide(prs, "Caso 4: TradeLens", "El problema del fundador dominante")

add_content_slide(prs, "El proyecto ambicioso", [
    "Lanzado en 2018 por Maersk (la mayor naviera del mundo) e IBM",
    "Objetivo: digitalizar y hacer trazable el comercio maritimo global",
    "Basado en Hyperledger Fabric",
    "Llego a conectar a mas de 150 organizaciones",
    "Procesaba millones de eventos al dia: loading, transbordos, aduanas, entregas",
    "Trazabilidad end-to-end de contenedores desde origen hasta destino",
])

add_content_slide(prs, "¿Por que cerro en 2022?", [
    "No fue un problema tecnico — la plataforma funcionaba bien",
    "No fue falta de inversion — IBM y Maersk pusieron cientos de millones",
    "No fue falta de adopcion general — 150+ organizaciones participaron",
    "",
    "El problema: las navieras competidoras no quisieron unirse",
    "MSC, CMA CGM, Hapag-Lloyd (40% del trafico mundial) se negaron",
    "¿Por que? No querian dar sus datos operacionales a su mayor rival (Maersk)",
    "",
    "Sin los 3 grandes competidores, la plataforma no tenia cobertura real",
    "Leccion: el problema del fundador dominante",
])

add_image_placeholder(prs, "TradeLens: fundador dominante",
    "[Diagrama: Maersk en el centro controlando la plataforma, con algunos puertos y aduanas conectados pero MSC, CMA CGM y Hapag-Lloyd FUERA de la red]",
    "Conceptual diagram showing the dominant founder problem of TradeLens: Maersk at the center controlling the platform with ports and customs connected, while competing shipping companies MSC, CMA CGM and Hapag-Lloyd are shown outside the network, refusing to join. Red crosses on the excluded companies. Warning-themed color palette.")

add_activity_slide(prs, "EJERCICIO: Rediseña TradeLens", [
    "Caso practico: crear una alternativa a TradeLens que SI funcione.",
    "",
    "Tu mision: disenar una red de trazabilidad maritima que evite el problema del fundador dominante.",
    "",
    "Actores (en la red de aula):",
    "  - Maersk, MSC, CMA CGM (3 navieras competidoras)",
    "  - Puerto Valencia, Puerto Rotterdam (2 infraestructuras)",
    "  - Aduanas UE (regulador)",
    "",
    "Tareas:",
    "  FASE 1 (sobre el papel, 30 min):",
    "    Elegir modelo de gobernanza: fundacion, democratico, federado?",
    "    Distribuir los orderers (nadie controla el ordering)",
    "    Modelo de financiacion sostenible",
    "  FASE 2 (en el ordenador, 90 min):",
    "    Montar red con 6 orgs + orderer Raft distribuido",
    "    Probar flujo completo incluyendo TRANSBORDOS entre navieras",
    "    State-based endorsement: transbordo requiere firma de AMBAS navieras",
    "",
    "Guia completa: docs/modulo-3/ejercicios/ejercicio-tradelens.md",
], badge_text="EJERCICIO")

add_content_slide(prs, "Preguntas clave para tu rediseño", [
    "1. ¿Quien es el fundador ideal? ¿Fundacion neutral? ¿Organismo internacional?",
    "2. ¿Como distribuyes los orderers para que nadie controle el ordering?",
    "3. ¿Modelo de financiacion: cuota fija, pay-per-use, fondos publicos?",
    "4. ¿Que incentivo tienen MSC, CMA CGM para unirse esta vez?",
    "5. ¿Los puertos y aduanas son orgs de pleno derecho o acceso limitado?",
    "6. Un transbordo cambia el contenedor de naviera A a naviera B. ¿Quien endorsa?",
])

add_debate_slide(prs, "Gobernanza: TradeLens vs. tu solucion", [
    "1. ¿Por que el modelo de fundacion es mas robusto que 'Maersk lanza la plataforma'?",
    "2. Si todos los miembros tienen voto igual, ¿Maersk aceptaria participar?",
    "3. ¿Es realista esperar que competidores directos colaboren en una red comun?",
    "4. ¿Que rol tendria la IMO (Organizacion Maritima Internacional) en tu solucion?",
    "5. Despues del fracaso de TradeLens, ¿quien deberia relanzar este tipo de proyecto?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/preview_tradelens.pptx")
print("preview_tradelens.pptx OK")

# ============================================================
# B3i
# ============================================================
prs = new_prs()

add_title_slide(prs, "B3i:\nCuando el modelo de negocio falla",
    "Reaseguros automatizados que no encontraron como sostenerse",
    module="Modulo 3: Vision Empresarial")

add_section_slide(prs, "Caso 5: B3i", "El fracaso por falta de modelo de ingresos")

add_content_slide(prs, "El proyecto", [
    "Lanzado en 2016 como Blockchain Insurance Industry Initiative",
    "Consorcio de 15+ aseguradoras y reaseguradoras europeas top",
    "Allianz, Swiss Re, Zurich, Munich Re, AIG, Generali, Hannover Re...",
    "Objetivo: digitalizar y automatizar contratos de reaseguro",
    "Tecnologia: R3 Corda (similar a Fabric, otra blockchain permissioned)",
    "",
    "Prometia: contratos inteligentes que se activan automaticamente ante siniestros",
    "Distribuyendo reclamaciones entre aseguradoras segun porcentajes pactados",
])

add_content_slide(prs, "¿Por que cerro en 2022?", [
    "No fue un problema tecnico — los pilotos funcionaban correctamente",
    "No fue falta de miembros — tenian a los mayores jugadores del sector",
    "No fue problema de gobernanza — consorcio equilibrado sin dominancia",
    "",
    "El problema: modelo de negocio",
    "Las aseguradoras querian participar pero NO querian financiar indefinidamente",
    "Sin un flujo de ingresos claro, el capital inicial se agoto",
    "Los miembros votaron en 2022: no invertimos mas, cerramos",
    "",
    "Contraste con TradeLens: aqui la tecnologia y la gobernanza estaban bien",
    "Lo que fallo fue la sostenibilidad economica",
])

add_content_slide(prs, "¿Que es un contrato de reaseguro?", [
    "Un cliente contrata un seguro de 10M€ con Allianz (fabrica, terremoto...)",
    "Allianz NO quiere asumir 10M€ de riesgo ella sola",
    "Cede parte a Munich Re (60%) y a Swiss Re (20%), retiene 20%",
    "Si ocurre siniestro de 3M€:",
],
subbullets={
    3: ["Allianz paga al cliente 3M€",
        "Luego Allianz reclama 1.8M€ a Munich Re (60%)",
        "Y 0.6M€ a Swiss Re (20%)",
        "Proceso actual: meses de papeleo y disputas",
        "Con blockchain: automatico en minutos"],
})

add_image_placeholder(prs, "Flujo de reaseguros",
    "[Diagrama: cliente paga prima a aseguradora primaria, que cede partes a reaseguradoras 1 y 2. Cuando hay siniestro, la aseguradora primaria reclama proporcionalmente a cada reaseguradora]",
    "Reinsurance flow diagram: primary insurer (Allianz) at center, receiving premium from client. Allianz cedes portions of risk to two reinsurers (Munich Re 60%, Swiss Re 20%). Arrows show payment flows in both directions. Clean financial diagram, teal and gold colors.")

add_activity_slide(prs, "EJERCICIO: Diseña un B3i sostenible", [
    "Caso practico: crear una plataforma de reaseguros que SI sea sostenible.",
    "",
    "Aprender de los errores de B3i: disena con modelo de negocio desde el dia 1.",
    "",
    "Actores:",
    "  - 4 aseguradoras: Allianz, Munich Re, Swiss Re, Zurich",
    "  - 1 regulador: EIOPA (European Insurance Authority)",
    "",
    "Tareas:",
    "  FASE 1 (sobre el papel, 30 min):",
    "    Disenar modelo de ingresos (fees por transaccion?)",
    "    Como se distribuyen automaticamente los pagos",
    "    Politicas de endorsement: contratos multi-parte",
    "  FASE 2 (en el ordenador, 90 min):",
    "    Montar red con 4 aseguradoras + regulador",
    "    Chaincode con contratos de reaseguro y siniestros",
    "    State-based endorsement: contrato requiere firma de TODAS las partes",
    "    Probar: crear contrato, reportar siniestro, validacion y liquidacion automatica",
    "",
    "Guia completa: docs/modulo-3/ejercicios/ejercicio-b3i.md",
], badge_text="EJERCICIO")

add_content_slide(prs, "Preguntas clave para tu diseño", [
    "1. ¿Fee por transaccion? ¿Cuota anual? ¿Escalado por volumen?",
    "2. ¿Los contratos multi-parte requieren endorsement de TODAS o MAJORITY?",
    "3. ¿Como se valida que un siniestro es real? (oraculos, peritaje, validacion cruzada)",
    "4. EIOPA: ¿voto en governance o solo acceso de lectura?",
    "5. ¿Que datos del cliente final pueden ir on-chain? (GDPR!)",
    "6. ¿Como gestionarias contratos viejos pre-blockchain al lanzar?",
])

add_debate_slide(prs, "Comparativa: TradeLens vs B3i", [
    "Ambos fracasaron. Ambos tenian buena tecnologia. ¿Pero por que?",
    "",
    "1. TradeLens fracaso por gobernanza (fundador dominante)",
    "2. B3i fracaso por modelo de negocio (sin ingresos)",
    "",
    "Preguntas:",
    "- ¿Cual es peor de los dos problemas?",
    "- ¿Cual es mas facil de arreglar a posteriori?",
    "- ¿Cual evitarias primero en tu proyecto?",
    "- ¿Es posible evitar ambos al mismo tiempo?",
    "- Si tuvieras que relanzar B3i, ¿que harias distinto?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/preview_b3i.pptx")
print("preview_b3i.pptx OK")
