import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

# 1. Portada
add_title_slide(prs, "¿Por que blockchain\nno ha triunfado (todavia)?",
    "Casos reales, barreras de adopcion y el papel de blockchain privada",
    module="Blockchain: adopcion y barreras")

# 2. La promesa vs la realidad
add_content_slide(prs, "La promesa vs la realidad", [
    "Blockchain prometia revolucionar industrias enteras:",
    "La realidad (2024-2026):",
    "¿Que ha fallado? No es la tecnologia. Son los incentivos, la regulacion y la UX.",
],
subbullets={
    0: ["Cadenas de suministro transparentes y trazables",
        "Registros inmutables de propiedad, identidad, salud",
        "Pagos transfronterizos instantaneos y baratos",
        "Votacion electronica segura y verificable",
        "Eliminacion de intermediarios en seguros, finanzas, comercio"],
    1: ["La mayoria de pilotos no pasaron a produccion",
        "Varios consorcios de grandes empresas cerraron",
        "La adopcion masiva no ha llegado fuera de cripto/DeFi",
        "Las empresas siguen usando bases de datos tradicionales"],
})

# 3. Imagen: hype cycle
add_image_placeholder(prs, "El ciclo de hype de blockchain",
    "[Grafico: Gartner Hype Cycle con blockchain pasando del 'pico de expectativas' al 'valle de la desilusion']",
    "Gartner Hype Cycle chart showing blockchain technology moving from the Peak of Inflated Expectations down into the Trough of Disillusionment, with an arrow pointing toward the Slope of Enlightenment. Clean minimalist style, teal color scheme, labeled phases.")

# 4. Los 6 casos
add_section_slide(prs, "6 casos reales\nque no llegaron al mainstream", "¿Que podemos aprender de cada uno?")

# 5. TradeLens
add_content_slide(prs, "Caso 1: TradeLens (Maersk + IBM)", [
    "Que era: plataforma de trazabilidad de comercio maritimo global",
    "Tecnologia: Hyperledger Fabric",
    "Inversion: cientos de millones de dolares, respaldada por IBM y Maersk",
    "Participantes: llego a conectar a mas de 150 organizaciones",
    "Que paso: cerro en noviembre de 2022",
    "¿Por que fallo?",
],
subbullets={
    5: ["Las navieras competidoras (MSC, CMA CGM) no querian unirse a una plataforma controlada por Maersk",
        "Problema del 'fundador dominante': ¿por que dar mis datos a mi competidor?",
        "No se alcanzo la masa critica necesaria para que la red fuera util",
        "La propuesta de valor no compensaba el coste de integracion"],
})

# 6. B3i
add_content_slide(prs, "Caso 2: B3i (consorcio de aseguradoras)", [
    "Que era: plataforma de reaseguros automatizados con smart contracts",
    "Tecnologia: R3 Corda",
    "Fundadores: Allianz, Swiss Re, Zurich, Munich Re y otras 15+ aseguradoras",
    "Que paso: cerro en julio de 2022 tras declararse insolvente",
    "¿Por que fallo?",
],
subbullets={
    4: ["No encontro un modelo de negocio viable: ¿quien paga la plataforma?",
        "Las aseguradoras querian participar pero no financiar indefinidamente",
        "Complejidad regulatoria: cada pais con reglas distintas para reaseguros",
        "Los sistemas legacy de las aseguradoras eran muy dificiles de integrar",
        "Leccion: la tecnologia funcionaba, el negocio no"],
})

# 7. MedRec
add_content_slide(prs, "Caso 3: MedRec (MIT - historial medico)", [
    "Que era: sistema de historial medico compartido entre hospitales",
    "Tecnologia: Ethereum (red privada)",
    "Concepto: el paciente controla quien accede a sus datos medicos",
    "Que paso: nunca paso de fase de investigacion academica",
    "¿Por que fallo?",
],
subbullets={
    4: ["Regulacion sanitaria extremadamente estricta (HIPAA en EE.UU., GDPR en Europa)",
        "Los medicos no quieren aprender herramientas nuevas: la UX debe ser invisible",
        "Los hospitales tienen sistemas legacy incompatibles entre si",
        "¿Quien administra la red? ¿Quien paga los nodos? ¿Quien es responsable?",
        "Privacidad: ¿realmente queremos datos medicos en CUALQUIER tipo de blockchain?"],
})

# 8. Voatz
add_content_slide(prs, "Caso 4: Voatz (votacion electronica)", [
    "Que era: app de votacion electronica basada en blockchain",
    "Uso real: se uso en elecciones locales en West Virginia (EE.UU.) en 2018",
    "Promesa: votacion segura, verificable y accesible desde el movil",
    "Que paso: auditoria del MIT encontro vulnerabilidades criticas",
    "¿Por que fallo?",
],
subbullets={
    4: ["Investigadores del MIT demostraron que los votos podian ser alterados",
        "La app dependia de un servidor central: no era realmente descentralizada",
        "El voto electronico tiene un problema fundamental: verificabilidad vs anonimato",
        "Rechazo politico: ambos partidos desconfian del voto electronico",
        "Blockchain no resuelve el 'ultimo metro': ¿como verificas la identidad del votante?"],
})

# 9. De Beers Tracr
add_content_slide(prs, "Caso 5: De Beers - Tracr (diamantes)", [
    "Que era: trazabilidad de diamantes desde la mina al consumidor final",
    "Tecnologia: blockchain privada",
    "Objetivo: demostrar que un diamante no es 'de sangre' ni de conflicto",
    "Estado: funciona, pero adopcion limitada",
    "¿Por que no ha triunfado?",
],
subbullets={
    4: ["Los proveedores pequenos (minas artesanales) no tienen infraestructura digital",
        "Problema del 'garbage in, garbage out': si la mina miente al registrar, blockchain no lo detecta",
        "Los intermediarios que se benefician de la opacidad no quieren participar",
        "El consumidor final no sabe (ni le importa) verificar en blockchain",
        "De Beers controla la plataforma: mismo problema de 'fundador dominante' que TradeLens"],
})

# 10. Honduras
add_content_slide(prs, "Caso 6: Registro de propiedad de Honduras", [
    "Que era: registro inmobiliario en blockchain para combatir la corrupcion",
    "Contexto: en Honduras, el fraude en registros de propiedad es endemico",
    "Promesa: un registro inmutable que ningun funcionario pudiera alterar",
    "Que paso: el proyecto fue abandonado en fase inicial",
    "¿Por que fallo?",
],
subbullets={
    4: ["Resistencia institucional: los que se benefician de la corrupcion bloquearon el proyecto",
        "Marco legal: la ley hondurena no reconoce registros digitales como validos",
        "Falta de infraestructura: muchas zonas rurales sin internet fiable",
        "Problema del 'genesis': ¿quien carga los datos iniciales? ¿y si ya son fraudulentos?",
        "Blockchain no elimina la corrupcion si los corruptos controlan la entrada de datos"],
})

# 11. Tabla resumen
add_table_slide(prs, "Resumen: ¿por que no triunfaron?",
    ["Caso", "Barrera principal", "¿Fallo la tecnologia?"],
    [
        ["TradeLens", "Gobernanza: competidores no se unen a plataforma del rival", "No"],
        ["B3i", "Modelo de negocio: nadie queria pagar la plataforma", "No"],
        ["MedRec", "Regulacion + UX: demasiado complejo para medicos", "No"],
        ["Voatz", "Seguridad + confianza: vulnerabilidades y rechazo politico", "Parcialmente"],
        ["De Beers Tracr", "Adopcion: proveedores pequenos sin incentivo", "No"],
        ["Honduras", "Institucional: resistencia politica y marco legal", "No"],
    ])

# 12. Patrones comunes
add_content_slide(prs, "Patrones comunes: las 5 barreras reales", [
    "1. Gobernanza: ¿quien controla la red? El fundador dominante ahuyenta a los demas",
    "2. Incentivos: ¿por que participaria cada actor? Si no gana nada, no se une",
    "3. Regulacion: las leyes no estan preparadas para registros inmutables descentralizados",
    "4. UX y complejidad: si el usuario final necesita entender blockchain, ya has perdido",
    "5. El problema del genesis: blockchain garantiza inmutabilidad, pero no veracidad del dato inicial",
    "",
    "Ninguno de estos problemas es tecnologico. Son problemas de personas, de negocio y de regulacion.",
])

# 13. Actividad
add_activity_slide(prs, "Debate: ¿Por que blockchain no ha triunfado?", [
    "Dividirse en 3 grupos. Cada grupo recibe 2 casos.",
    "",
    "Para cada caso, debatir y preparar (15 minutos):",
    "  1. ¿El problema era real? ¿Blockchain era la solucion correcta?",
    "  2. ¿Cual fue la barrera principal? (gobernanza, incentivos, regulacion, UX, genesis)",
    "  3. ¿Podria funcionar HOY con una blockchain privada/permissioned tipo Fabric?",
    "  4. ¿Que condiciones deberian darse para que funcionase?",
    "",
    "Puesta en comun (5 minutos por grupo):",
    "  - Presentar los 2 casos y las conclusiones",
    "  - ¿Hay patrones comunes entre los fracasos?",
    "",
    "Grupo A: TradeLens + B3i",
    "Grupo B: MedRec + Voatz",
    "Grupo C: De Beers Tracr + Honduras",
], badge_text="ACTIVIDAD")

# 14. Debate dirigido
add_debate_slide(prs, "Preguntas para el debate conjunto", [
    "1. De los 6 casos, ¿cual creeis que tiene mas posibilidades de funcionar en el futuro? ¿Por que?",
    "2. ¿Blockchain privada (Fabric) resuelve alguna de las 5 barreras? ¿Cuales si y cuales no?",
    "3. ¿Conoceis algun caso en vuestro sector que podria caer en las mismas trampas?",
    "4. Si tuvierais que convencer a vuestro jefe de usar blockchain, ¿que argumentos usariais sabiendo estos fracasos?",
    "5. ¿Hay casos donde simplemente NO se necesita blockchain y una base de datos basta?",
])

# 15. El puente hacia blockchain privada
add_content_slide(prs, "¿Y si el problema no es blockchain, sino QUE blockchain?", [
    "Muchos de estos proyectos usaron blockchain publica o redes mal gobernadas",
    "Blockchain privada/permissioned (Fabric) resuelve varias barreras:",
    "Pero NO resuelve:",
    "La clave: blockchain privada funciona cuando hay un consorcio con incentivos alineados",
],
subbullets={
    1: ["Escalabilidad: miles de TPS sin gas fees",
        "Privacidad: canales y Private Data (clave para salud, finanzas)",
        "Identidades conocidas: cumplimiento regulatorio (KYC, AML)",
        "UX: el usuario final no necesita saber que hay blockchain detras",
        "Gobernanza: reglas claras desde el inicio (politicas de endorsement)"],
    2: ["El problema del genesis: si el dato inicial es falso, blockchain lo hace inmutable, no verdadero",
        "Incentivos: si los participantes no ganan nada, no se unen",
        "Resistencia institucional: si los que mandan no quieren transparencia, la bloquearan"],
})

# 16. Casos que SI funcionan
add_content_slide(prs, "Casos que SI estan funcionando (con blockchain privada)", [
    "Walmart + IBM Food Trust: trazabilidad alimentaria en produccion desde 2018",
    "We.Trade: financiacion de comercio internacional entre bancos europeos",
    "Marco Polo Network: trade finance con multiples bancos en Corda",
    "HKMA (Hong Kong): plataforma de trade finance eTradeConnect en Fabric",
    "ANZ + Scentre Group: tokenizacion de alquileres comerciales en Fabric",
    "",
    "¿Que tienen en comun los que SI funcionan?",
],
subbullets={
    6: ["Consorcio con incentivos claros y alineados",
        "Un problema real que no se resolvia sin blockchain",
        "Gobernanza equilibrada (ningun actor domina)",
        "UX transparente: el usuario no ve blockchain",
        "Regulacion compatible o apoyo del regulador"],
})

prs.save(f"{OUT_DIR}/adopcion.pptx")
print("adopcion.pptx generado OK")
