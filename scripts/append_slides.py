"""
Añade slides al final de una presentación existente SIN regenerarla.
Preserva todos los cambios manuales que se hayan hecho en las slides ya existentes.

Uso:
    python3 append_slides.py <ruta_pptx> <tipo_slides>

Donde tipo_slides puede ser:
    dia_4_respuestas_debate
    dia_4_respuestas_repaso
    (añadir más según necesidad)
"""
import sys
sys.path.insert(0, "/mnt/d/Dev/Fabric/scripts")
from gen_helpers import *
from pptx import Presentation


def abrir_presentacion_existente(path):
    """Abre un pptx existente. TODO se preserva."""
    return Presentation(path)


# Ejemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: append_slides.py <ruta_pptx> <tipo>")
        sys.exit(1)

    path = sys.argv[1]
    tipo = sys.argv[2]

    # IMPORTANTE: abrir presentacion existente, NO crear una nueva
    prs = Presentation(path)

    # Las funciones de gen_helpers.py añaden slides al final
    # sin tocar las existentes.

    # Aqui ejemplos — se extiende segun necesidad:
    if tipo == "dia_4_respuestas_debate":
        add_content_slide(prs, "Respuestas al debate (1/2)", [
            "1. Datos falsos en el origen (garbage in, garbage out):",
            "2. Integracion con IoT (sensores de temperatura):",
            "3. Verificacion por el consumidor final sin peer:",
        ], subbullets={
            0: ["Blockchain garantiza INTEGRIDAD, NO VERACIDAD del dato inicial.",
                "Si el productor miente al registrar, la mentira queda inmutable.",
                "Mitigaciones: auditorias fisicas, peritajes, validacion cruzada.",
                "Sensores IoT reducen el problema: datos automaticos, no manuales.",
                "Responsabilidad legal: el cert identifica a quien firmo el dato."],
            1: ["Los sensores IoT NO se conectan directamente al chaincode.",
                "Patron: gateway IoT intermedio con certificado X.509.",
                "El gateway valida firmas de sensores (HMAC, TPM) y las firma al chaincode.",
                "El chaincode ve: 'gateway-X certifica que sensor-Y reporto X a las 10:30'.",
                "Responsabilidad del gateway: no manipular los datos."],
            2: ["El consumidor NO necesita cert — es solo un lector.",
                "Patron: QR -> web publica del consorcio -> API REST -> chaincode query.",
                "La web usa identidad de 'lector publico' con permisos solo consulta.",
                "Ejemplo real: Carrefour, Walmart — QR con historial completo."],
        })

    prs.save(path)
    print(f"Slides añadidas a {path}")
