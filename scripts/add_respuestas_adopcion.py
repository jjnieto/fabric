"""
Anade slides de respuestas a adopcion.pptx del Modulo 3.
Abre el pptx existente y anade slides al final SIN tocar las existentes.

Responde:
- Slide 13 (ACTIVIDAD): analisis de 6 casos en grupos
- Slide 14 (DEBATE): 5 preguntas de debate conjunto
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import add_content_slide
from pptx import Presentation

PPTX_PATH = "/mnt/d/Dev/Fabric/docs/slides/Modulo 3/adopcion.pptx"

prs = Presentation(PPTX_PATH)

# Respuestas a la actividad en grupos (parte 1: TradeLens, B3i, MedRec)
add_content_slide(prs, "Respuestas a la actividad (1/2)", [
    "TradeLens (Maersk + IBM):",
    "B3i (consorcio reaseguros):",
    "MedRec (MIT - historiales medicos):",
], subbullets={
    0: ["¿Problema real? Si — coordinacion entre navieras, puertos, aduanas.",
        "Barrera: GOBERNANZA (fundador dominante).",
        "¿Funcionaria en Fabric privada? Si, si lo funda un consorcio neutro o la IMO.",
        "Condiciones: nadie controla los orderers, reglas de entrada/salida claras,",
        "  modelo de costes proporcional (cuotas por tamano)."],
    1: ["¿Problema real? Si — duplicacion documental y liquidaciones lentas.",
        "Barrera: INCENTIVOS (modelo de negocio insostenible).",
        "¿Funcionaria hoy en Fabric privada? Si, con fees por transaccion.",
        "Condiciones: cada reaseguro paga una pequena comision al consorcio,",
        "  MVP con 1 linea de negocio (catastroficos), apoyo de EIOPA."],
    2: ["¿Problema real? Si — pacientes sin control sobre sus datos medicos.",
        "Barrera: REGULACION + UX + GENESIS.",
        "¿Funcionaria en Fabric? Parcialmente — si, con datos off-chain y hashes on-chain.",
        "Condiciones: adopcion obligatoria por el sistema nacional de salud,",
        "  UX transparente para medicos, cumplimiento GDPR estricto."],
})

# Respuestas a la actividad en grupos (parte 2: Voatz, De Beers, Honduras)
add_content_slide(prs, "Respuestas a la actividad (2/2)", [
    "Voatz (votacion electronica):",
    "De Beers Tracr (diamantes):",
    "Registro de propiedad Honduras:",
], subbullets={
    0: ["¿Problema real? Si — accesibilidad del voto, especialmente remoto/discapacidad.",
        "Barrera: REGULACION + UX + GENESIS (verificacion de identidad del votante).",
        "¿Funcionaria en Fabric? NO resuelve el problema fundamental — la identidad.",
        "Condiciones: voto verificable criptograficamente + supervision oficial.",
        "Blockchain aqui es la parte FACIL; el problema es politico, legal y social."],
    1: ["¿Problema real? Si — trazabilidad de diamantes no de conflicto.",
        "Barrera: GOBERNANZA (fundador dominante) + GENESIS (datos de mina).",
        "¿Funcionaria en Fabric? Si, si lo funda una organizacion neutra (GIA, WFDB).",
        "Condiciones: incluir mineros artesanales, usar sensores IoT para autenticar origen,",
        "  consumidor final puede verificar por QR sin entender blockchain."],
    2: ["¿Problema real? Si — corrupcion masiva en registros.",
        "Barrera: INSTITUCIONAL (los que pierden con transparencia bloquean).",
        "¿Funcionaria en Fabric? La tecnologia si. El problema no es tecnico.",
        "Condiciones: voluntad politica real, reforma del marco legal,",
        "  infraestructura digital minima, adopcion desde lo municipal (bottom-up)."],
})

# Respuestas al debate conjunto (parte 1)
add_content_slide(prs, "Respuestas al debate (1/2)", [
    "1. ¿Cual de los 6 tiene mas posibilidades de funcionar en el futuro?",
    "2. ¿Blockchain privada (Fabric) resuelve las 5 barreras?",
], subbullets={
    0: ["De Beers Tracr y MedRec son los mas prometedores — el problema es real y persistente.",
        "TradeLens podria relanzarse si es una fundacion neutral.",
        "Voatz: muy improbable — el problema central (identidad) no lo resuelve blockchain.",
        "Honduras: depende del clima politico, no de la tecnologia.",
        "B3i: posible con nuevo modelo de negocio y MVP pequeno."],
    1: ["GOBERNANZA: parcialmente — Fabric da herramientas (politicas) pero no define quien las usa.",
        "INCENTIVOS: NO — es problema de negocio, no tecnologico.",
        "REGULACION: parcialmente — Fabric es compatible con GDPR (hash on-chain, dato off-chain).",
        "UX: SI — se puede ocultar completamente detras de una app tradicional.",
        "GENESIS: NO — si entras datos falsos, blockchain los hace inmutables (no verdaderos)."],
})

# Respuestas al debate conjunto (parte 2)
add_content_slide(prs, "Respuestas al debate (2/2)", [
    "3. Casos en vuestro sector que podrian caer en las mismas trampas:",
    "4. Argumentos para convencer al jefe sabiendo estos fracasos:",
    "5. ¿Casos donde NO hace falta blockchain?",
], subbullets={
    0: ["Cualquier proyecto donde un competidor sea el fundador (problema TradeLens).",
        "Consorcios sin modelo de ingresos claro desde el dia 1 (problema B3i).",
        "Proyectos que requieren cambiar procesos profundos de usuarios (MedRec).",
        "Proyectos en sectores con regulacion muy estricta no adaptada (salud, finanzas)."],
    1: ["'Empezamos con un MVP muy pequeno, 2-3 orgs, 6 meses' — reduce el riesgo.",
        "'No somos el fundador dominante, somos uno mas' — evita problema TradeLens.",
        "'Tenemos modelo de ingresos antes de desarrollar' — evita problema B3i.",
        "'La IA esta lista, el regulador esta lista, nosotros debemos estarlo' — contexto favorable.",
        "NUNCA: 'porque es blockchain' — ese es el camino al fracaso."],
    2: ["Un solo actor gestiona todos los datos -> base de datos tradicional.",
        "Los datos no necesitan ser compartidos entre orgs -> APIs entre sistemas.",
        "No hay desconfianza entre partes -> SaaS compartido con permisos.",
        "Rendimiento es critico (>10k TPS) -> BD distribuida tradicional.",
        "Regla: si una BD + APIs resuelve el problema, no necesitas blockchain."],
})

prs.save(PPTX_PATH)
print(f"Anadidas 4 slides al final de {PPTX_PATH}")
print(f"Total slides ahora: {len(prs.slides)}")
