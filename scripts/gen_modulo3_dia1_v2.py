import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *

prs = new_prs()

add_title_slide(prs, "Casos de Uso Reales:\nExitos y Fracasos",
    "Dia 1 - Que funciona, que no funciona y por que",
    module="Modulo 3: Vision Empresarial")

# ============================================================
# CASO 1: WALMART — expansion del caso + ejercicio practico
# ============================================================
add_section_slide(prs, "Caso 1: Walmart Food Trust", "Trazabilidad alimentaria con Hyperledger Fabric")

add_content_slide(prs, "El problema que resolvieron", [
    "Walmart es el mayor supermercado del mundo: 10.500+ tiendas, 2.3 millones de empleados",
    "Problema 1: brotes de salmonella y E.coli requieren retirar productos inmediatamente",
    "Problema 2: antes de Fabric, rastrear un lote de mango tardaba 7 dias",
    "Problema 3: esos 7 dias = millones de productos potencialmente contaminados en circulacion",
    "Problema 4: cada proveedor tenia su propio sistema, imposible de consolidar",
    "Coste estimado: cada dia de retraso en un recall = millones de dolares en perdidas",
])

add_content_slide(prs, "La solucion con Hyperledger Fabric", [
    "Walmart + IBM lanzaron IBM Food Trust en 2018",
    "Basado en Hyperledger Fabric (permissioned)",
    "Cada actor de la cadena tiene su peer:",
    "Trazabilidad end-to-end:",
],
subbullets={
    2: ["Productor (granja)",
        "Procesador (lavado, empaquetado)",
        "Distribuidor (transporte refrigerado)",
        "Walmart (tienda)"],
    3: ["Cada movimiento del lote se registra en el ledger compartido",
        "Cualquier actor puede consultar el historial completo",
        "Con un QR en el producto, se ve todo el recorrido"],
})

add_content_slide(prs, "Resultados", [
    "Rastreo de mango de 7 dias a 2.2 segundos",
    "Mas de 150 organizaciones conectadas en 2020",
    "Productos cubiertos: hoja verde, carne, mariscos, yogur, huevos, pollo",
    "En 2019, Walmart obligo a todos sus proveedores de hoja verde a unirse al sistema",
    "Uno de los mayores exitos de Fabric en produccion",
    "Clave del exito: Walmart es el actor dominante y forzo la adopcion",
])

add_image_placeholder(prs, "Topologia simplificada de IBM Food Trust",
    "[Diagrama: granja -> procesador -> distribuidor -> supermercado, todos conectados a un canal Fabric compartido]",
    "Supply chain diagram for IBM Food Trust on Hyperledger Fabric: four organizations (Farm, Processor, Distributor, Walmart Store) each with their own peer node, connected through a shared channel. Orderer service in the middle. Food icons (mango, leafy greens) flowing through the chain. Clean flat design, teal color scheme.")

add_activity_slide(prs, "EJERCICIO: Diseña tu propia red de trazabilidad", [
    "Caso practico adaptado al aula: trazabilidad de aguacates de Malaga",
    "",
    "Actores del consorcio:",
    "  - Productor (granja)",
    "  - Distribuidor (transporte refrigerado)",
    "  - Supermercado (venta final)",
    "  - Regulador (AESAN - seguridad alimentaria)",
    "",
    "Tareas:",
    "  FASE 1 (sobre el papel, 30 min):",
    "    Disenar la topologia de red: cuantas orgs, canales, Private Data",
    "    Decidir politicas de endorsement y control de acceso",
    "  FASE 2 (en el ordenador, 90 min):",
    "    Montar la red con 4 organizaciones + orderer",
    "    Desplegar el chaincode con Private Data Collections",
    "    Probar el flujo completo de trazabilidad y un recall",
    "",
    "Guia tecnica completa: docs/modulo-3/ejercicios/ejercicio-walmart.md",
], badge_text="EJERCICIO")

add_content_slide(prs, "Preguntas clave para tu diseño", [
    "Piensa en estas preguntas antes de empezar a codificar:",
    "",
    "1. ¿Cuantas organizaciones? ¿Con peer propio cada una?",
    "2. ¿Un canal unico o multiples canales segregados?",
    "3. ¿Que datos van on-chain (publicos) y cuales en Private Data?",
    "   Pista: los precios de compra entre actores son confidenciales",
    "4. ¿Quien puede crear un lote? ¿Solo el productor?",
    "5. ¿Quien puede hacer recall? ¿Solo el regulador o cualquier actor?",
    "6. ¿Que politica de endorsement tiene sentido?",
    "   Para movimientos normales vs para recall",
    "7. ¿Como verificaria el consumidor final un QR? (no tiene peer)",
])

add_debate_slide(prs, "Debate tras el ejercicio", [
    "1. ¿Vuestra topologia se parece a la de IBM Food Trust? ¿En que difiere?",
    "2. ¿Que ventaja real aporta Fabric aqui frente a una BD compartida gestionada por Walmart?",
    "3. ¿Que pasa si el productor miente sobre el origen? ¿Blockchain lo detecta?",
    "4. Walmart fue el que impuso la adopcion. ¿Es justo? ¿Es necesario?",
    "5. ¿Como integrariais sensores IoT para automatizar el registro de temperatura?",
])

prs.save("/mnt/d/Dev/Fabric/docs/slides/Modulo 3/preview_walmart.pptx")
print("preview_walmart.pptx (preview del formato, no sobrescribe dia_1) OK")
