import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# ============================================================
# PORTADA
# ============================================================
add_title_slide(prs, "Gestion de Proyectos:\nComplementos",
    "Riesgos, MVP, roles, comunicacion y particularidades de proyectos blockchain",
    module="Modulo 6: Proyecto Final")

# ============================================================
# SECCION 1: GESTION DE RIESGOS
# ============================================================
add_section_slide(prs, "Gestion de Riesgos",
    "Lo que puede salir mal, saldra mal (si no lo gestionas)")

add_content_slide(prs, "¿Que es un riesgo?", [
    "Un riesgo es un evento incierto que, si ocurre, tiene un impacto en el proyecto",
    "No es un problema: un problema ya ha ocurrido. Un riesgo PUEDE ocurrir",
    "Todo proyecto tiene riesgos. La diferencia esta en si los gestionas o te pillan por sorpresa",
    "Dos dimensiones:",
],
subbullets={
    3: ["Probabilidad: ¿que tan probable es que ocurra? (alta/media/baja)",
        "Impacto: si ocurre, ¿como de grave es? (critico/alto/medio/bajo)",
        "Riesgo = Probabilidad x Impacto"],
})

add_table_slide(prs, "Matriz de riesgos: ejemplo para un proyecto",
    ["Riesgo", "Probabilidad", "Impacto", "Mitigacion"],
    [
        ["Un miembro del equipo deja el proyecto", "Media", "Alto", "Documentar todo, pair programming"],
        ["La tecnologia elegida no soporta un requisito", "Baja", "Critico", "PoC temprana antes de comprometerse"],
        ["El cliente cambia los requisitos a mitad", "Alta", "Medio", "Contratos agiles, MVP, entregas frecuentes"],
        ["Fallo de seguridad en produccion", "Baja", "Critico", "Auditorias, tests de seguridad, pen testing"],
        ["Retraso en la integracion con sistema externo", "Media", "Alto", "Mocks, interfaces desacopladas"],
    ])

add_content_slide(prs, "Plan de respuesta a riesgos", [
    "Para cada riesgo identificado, elegir UNA estrategia:",
    "",
    "Evitar: eliminar la causa del riesgo (cambiar el enfoque, reducir alcance)",
    "Mitigar: reducir la probabilidad o el impacto (PoC, tests, documentacion)",
    "Transferir: pasar el riesgo a otro (seguros, subcontratar, SLAs)",
    "Aceptar: asumir que puede pasar y tener un plan B preparado",
    "",
    "Los riesgos se revisan periodicamente. No es un ejercicio de una sola vez.",
])

# ============================================================
# SECCION 2: MVP
# ============================================================
add_section_slide(prs, "MVP\nProducto Minimo Viable",
    "Entrega algo pequeno que funcione, valida, itera")

add_content_slide(prs, "¿Que es un MVP?", [
    "Minimum Viable Product: la version mas pequena del producto que aporta valor real",
    "No es un prototipo a medias. Es un producto funcional, solo que con alcance reducido",
    "El objetivo: validar hipotesis con usuarios reales lo antes posible",
    "Si esperas a tener el producto completo para validar, llegas tarde",
])

add_image_placeholder(prs, "MVP: lo que SI es vs lo que NO es",
    "[Diagrama: arriba 'NO es MVP' mostrando un coche construido rueda a rueda. Abajo 'SI es MVP' mostrando patinete -> bici -> moto -> coche]",
    "Split comparison diagram. Top row labeled 'NOT an MVP': shows a car being built wheel by wheel (unusable until complete). Bottom row labeled 'MVP approach': shows evolution from skateboard to bicycle to motorcycle to car (usable at every stage). Clean flat design, teal and green colors.")

add_content_slide(prs, "MVP en practica: como definirlo", [
    "1. Listar TODAS las funcionalidades deseadas",
    "2. Clasificar: Must have / Should have / Could have / Won't have (MoSCoW)",
    "3. El MVP = solo los Must have",
    "4. Entregar, poner delante del usuario, recoger feedback",
    "5. Iterar: anadir Should have segun el feedback",
    "",
    "Ejemplo FidelityChain:",
    "  Must: registrar cliente, emitir puntos, canjear, consultar saldo",
    "  Should: historial, info del token, catalogo de productos",
    "  Could: eventos en tiempo real, web UI, multiples partners",
    "  Won't (v1): caducidad de puntos, transferencia entre clientes",
])

# ============================================================
# SECCION 3: ROLES DEL EQUIPO
# ============================================================
add_section_slide(prs, "Roles del Equipo",
    "Quien decide que, quien prioriza, quien construye")

add_content_slide(prs, "Roles tipicos en un proyecto agil", [
    "Product Owner (PO): representa al negocio, prioriza el backlog, decide que se construye",
    "Scrum Master / Facilitador: elimina impedimentos, facilita ceremonias, protege al equipo",
    "Tech Lead: decisiones tecnicas, arquitectura, revision de codigo",
    "Desarrolladores: construyen el producto",
    "QA / Tester: valida que lo construido cumple los criterios de aceptacion",
    "DevOps: infraestructura, CI/CD, despliegues",
],
subbullets={
    0: ["No es el jefe del equipo: es la voz del cliente dentro del equipo"],
    1: ["No es un gestor de proyecto tradicional: no asigna tareas"],
})

add_content_slide(prs, "Antipatrones de roles", [
    "El PO que no esta disponible: el equipo toma decisiones sin el y luego hay que rehacer",
    "El Tech Lead que decide todo: el equipo no aprende ni aporta",
    "El Scrum Master que es jefe encubierto: asigna tareas y controla, no facilita",
    "No tener QA: 'ya lo probamos nosotros' = bugs en produccion",
    "Todo el mundo es 'full-stack': nadie es responsable de nada concreto",
    "",
    "La clave: roles claros con responsabilidades explicitas desde el dia 1",
])

# ============================================================
# SECCION 4: COMUNICACION Y REPORTING
# ============================================================
add_section_slide(prs, "Comunicacion y Reporting",
    "Si no se comunica, no existe")

add_content_slide(prs, "Ceremonias agiles esenciales", [
    "Daily standup (15 min): ¿que hice ayer? ¿que hare hoy? ¿tengo bloqueos?",
    "Sprint planning: ¿que vamos a hacer en las proximas 2 semanas?",
    "Sprint review / demo: mostrar al stakeholder lo que hemos construido",
    "Retrospectiva: ¿que fue bien? ¿que fue mal? ¿que mejoramos?",
    "",
    "La retrospectiva es la ceremonia mas importante y la que mas se salta.",
    "Sin retrospectiva no hay mejora continua. Es donde el equipo aprende.",
])

add_content_slide(prs, "Reporting al stakeholder", [
    "El stakeholder no quiere detalles tecnicos. Quiere saber:",
    "",
    "¿Vamos en plazo? (burndown chart, velocidad del equipo)",
    "¿Que se ha entregado? (demo funcional, no slides)",
    "¿Hay riesgos o bloqueos? (comunicar pronto, no esconder problemas)",
    "¿Necesitamos algo? (decisiones, recursos, priorizacion)",
    "",
    "Regla de oro: nunca sorprendas al stakeholder con malas noticias.",
    "Si algo va mal, comunicalo al momento. No al final del sprint.",
])

# ============================================================
# SECCION 5: DEFINITION OF DONE
# ============================================================
add_section_slide(prs, "Definition of Done",
    "¿Cuando esta 'terminado' de verdad?")

add_content_slide(prs, "Definition of Done (DoD)", [
    "Es un acuerdo del equipo sobre que significa que algo esta terminado",
    "Sin DoD, cada persona tiene un criterio diferente de 'hecho'",
    "Ejemplo de DoD para una historia de usuario:",
],
subbullets={
    2: ["Codigo escrito y revisado (code review aprobado)",
        "Tests unitarios escritos y pasando",
        "Tests de integracion pasando",
        "Documentacion actualizada (si aplica)",
        "Desplegado en entorno de test",
        "QA ha validado los criterios de aceptacion",
        "Sin bugs criticos abiertos"],
})

add_content_slide(prs, "Criterios de aceptacion vs Definition of Done", [
    "Son cosas diferentes y complementarias:",
    "",
    "Criterios de aceptacion: especificos de cada historia",
    "  'Como usuario, puedo canjear puntos y mi saldo se reduce correctamente'",
    "",
    "Definition of Done: comun a TODAS las historias",
    "  'El codigo tiene tests, esta revisado y desplegado en test'",
    "",
    "Una historia esta terminada cuando cumple SUS criterios de aceptacion",
    "Y ADEMAS cumple la Definition of Done del equipo",
])

# ============================================================
# SECCION 6: ESTIMACION
# ============================================================
add_section_slide(prs, "Estimacion de Esfuerzo",
    "No cuanto tiempo tardara, sino cuanto esfuerzo requiere")

add_content_slide(prs, "Tecnicas de estimacion", [
    "Story Points: unidad relativa de esfuerzo (no horas ni dias)",
    "  Se usa la serie Fibonacci: 1, 2, 3, 5, 8, 13, 21",
    "  Un 5 no es el doble de dificil que un 2, es 'bastante mas complejo'",
    "",
    "T-shirt sizing: S, M, L, XL para estimaciones rapidas y gruesas",
    "  Util al inicio del proyecto para dimensionar el backlog",
    "",
    "Planning Poker: cada miembro del equipo estima de forma independiente",
    "  Se revelan las cartas a la vez para evitar sesgos",
    "  Si hay mucha discrepancia, se debate y se vuelve a estimar",
])

add_content_slide(prs, "Errores comunes al estimar", [
    "Estimar en horas: genera compromisos rigidos que no se pueden cumplir",
    "Estimar solo el desarrollo: olvidar testing, documentacion, despliegue, bugs",
    "El optimismo del desarrollador: 'esto lo hago en una tarde' (nunca es una tarde)",
    "No re-estimar: la estimacion inicial era con informacion parcial, hay que ajustar",
    "Presion del stakeholder: 'necesito que esto sean 3 puntos, no 8' — NO",
    "",
    "La estimacion es del equipo, no del jefe. Si el equipo dice 13, es 13.",
])

# ============================================================
# SECCION 7: PARTICULARIDADES BLOCKCHAIN
# ============================================================
add_section_slide(prs, "Particularidades de\nProyectos Blockchain",
    "Lo que cambia cuando tu proyecto es un consorcio descentralizado")

add_content_slide(prs, "¿Que tiene de especial un proyecto blockchain?", [
    "En un proyecto tradicional hay UN cliente y UN equipo",
    "En un proyecto blockchain enterprise hay un CONSORCIO:",
    "",
    "Multiples organizaciones que son a la vez clientes Y participantes",
    "Cada org tiene sus propios intereses, plazos y prioridades",
    "Las decisiones tecnicas afectan a todas las orgs (politicas de endorsement, datos compartidos)",
    "El despliegue requiere coordinacion entre orgs (lifecycle: approve de cada una)",
    "",
    "Gestionar un proyecto blockchain es gestionar un proyecto POLITICO ademas de tecnico",
])

add_image_placeholder(prs, "Proyecto tradicional vs proyecto blockchain",
    "[Diagrama: izquierda un proyecto con 1 cliente y 1 equipo. Derecha un consorcio con multiples orgs, cada una con su equipo, conectadas por un canal compartido]",
    "Split comparison diagram. Left side: traditional project with single client pointing to single development team (simple hierarchy). Right side: blockchain consortium with 3-4 organizations each with their own team, connected by a shared channel in the center. Arrows showing governance decisions flowing between orgs. Clean corporate style, teal color scheme.")

add_content_slide(prs, "La gobernanza como workstream", [
    "En un proyecto Fabric, la gobernanza del consorcio NO es un detalle tecnico",
    "Es un workstream completo que hay que planificar desde el dia 1:",
    "",
    "¿Quien puede proponer cambios en el chaincode?",
    "¿Como se aprueba un nuevo chaincode o una actualizacion? (lifecycle)",
    "¿Quien paga la infraestructura? (orderers, CAs)",
    "¿Como se incorpora una nueva organizacion al consorcio?",
    "¿Que pasa si una organizacion quiere salir?",
    "¿Quien tiene acceso a que datos? (canales, Private Data)",
    "",
    "Si no resuelves esto antes de escribir codigo, el proyecto fracasara.",
    "TradeLens y B3i fracasaron por gobernanza, no por tecnologia.",
])

add_content_slide(prs, "Coordinacion de despliegues", [
    "En un proyecto normal: despliegas en TU servidor y ya esta",
    "En Fabric: el despliegue requiere acciones de CADA organizacion",
    "",
    "Para desplegar un chaincode:",
    "  1. Alguien empaqueta el codigo y lo distribuye a las orgs",
    "  2. Cada org lo revisa, lo instala en SU peer y lo aprueba",
    "  3. Solo cuando la mayoria ha aprobado se puede hacer commit",
    "",
    "Esto significa: coordinacion de agendas, ventanas de despliegue,",
    "planes de rollback consensuados y comunicacion constante",
    "",
    "Consejo: automatizar al maximo con scripts y CI/CD",
])

add_content_slide(prs, "Riesgos especificos de proyectos blockchain", [
    "Adopcion: que las orgs del consorcio no se comprometan o abandonen a mitad",
    "Fundador dominante: una org controla demasiado y las demas desconfian",
    "Complejidad de integracion: conectar Fabric con los sistemas legacy de cada org",
    "Regulacion cambiante: leyes de proteccion de datos, smart contracts como contratos legales",
    "Rendimiento: expectativas irreales de TPS o latencia",
    "Seguridad: un certificado comprometido de una org afecta a toda la red",
    "",
    "Mitigacion clave: empezar con un MVP muy pequeno entre 2-3 orgs",
    "y ampliar solo cuando se demuestre valor.",
])

add_content_slide(prs, "El MVP en blockchain: empieza muy pequeno", [
    "Error tipico: intentar montar un consorcio de 20 orgs desde el dia 1",
    "Enfoque correcto: 2-3 orgs, 1 canal, 1 chaincode sencillo",
    "",
    "Fase 1 (MVP): 2 orgs, caso de uso basico, red minima",
    "  Ejemplo: Hotel + Cafeteria con puntos de fidelizacion",
    "  Objetivo: demostrar que funciona y que aporta valor",
    "",
    "Fase 2: anadir 1-2 orgs mas, ampliar funcionalidades",
    "  Ejemplo: anadir un restaurante y una tienda al programa de puntos",
    "",
    "Fase 3: escalar a produccion, governance formal, SLAs",
    "  Solo si la Fase 1 y 2 demostraron valor real",
])

# Debate
add_debate_slide(prs, "Gestion de proyectos blockchain", [
    "1. ¿Que es mas dificil: la tecnologia o la gobernanza del consorcio? ¿Por que?",
    "2. Si tuvierais que convencer a 3 empresas de vuestro sector para formar un consorcio, ¿que argumentos usariais?",
    "3. ¿Como gestionariais el riesgo de que una org abandone el consorcio a mitad del proyecto?",
    "4. ¿MVP de 2 orgs o lanzamiento con todo el consorcio? ¿Que preferis y por que?",
    "5. ¿Que ceremonias agiles adaptariais para un proyecto multi-organizacion?",
])

# Actividad
add_activity_slide(prs, "Planifica tu proyecto FidelityChain", [
    "Aplicar lo aprendido al proyecto que vais a desarrollar.",
    "",
    "En grupos de 3-4 personas:",
    "  1. Identificar 5 riesgos del proyecto y clasificarlos (probabilidad x impacto)",
    "  2. Definir el MVP: ¿cuales son los Must have?",
    "  3. Asignar roles: ¿quien es PO, Tech Lead, etc.?",
    "  4. Escribir la Definition of Done del equipo",
    "  5. Estimar las historias principales (S/M/L/XL)",
    "  6. Identificar 2 decisiones de gobernanza que hay que tomar",
    "     (ej: ¿quien puede emitir puntos? ¿quien aprueba nuevos partners?)",
    "",
    "Tiempo: 30 minutos. Presentar en 5 minutos por grupo.",
], badge_text="PRACTICA")

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 6/gestion_proyectos_complemento.pptx")
print("gestion_proyectos_complemento.pptx generado OK")
