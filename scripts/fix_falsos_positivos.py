"""
Corrige falsos positivos del paso anterior: "válida" como verbo,
"pública" como verbo, etc. donde no deben llevar tilde.
"""
import re
from pathlib import Path

# Patrones a revertir (forma corregida -> forma original)
# Solo en contextos donde claramente es verbo
REVERSIONES_VERBALES = [
    # "válida" como verbo (3a persona singular)
    (r'\bválida las transacciones\b', 'valida las transacciones'),
    (r'\bválida la firma\b', 'valida la firma'),
    (r'\bválida los endorsements\b', 'valida los endorsements'),
    (r'\bválida el certificado\b', 'valida el certificado'),
    (r'\bválida que\b', 'valida que'),
    (r'\bválida si\b', 'valida si'),
    (r'\bválida los datos\b', 'valida los datos'),
    (r'\bválida el saldo\b', 'valida el saldo'),
    (r'\bválida el cold chain\b', 'valida el cold chain'),
    (r'\bvalida saldo\b', 'valida saldo'),  # ya estaba bien, por si acaso
    (r'\bválidan\b', 'validan'),  # plural verbal
    # "El chaincode válida" -> verbo
    (r'(?i)el chaincode válida\b', 'el chaincode valida'),
    (r'(?i)el peer válida\b', 'el peer valida'),
    (r'(?i)el cliente válida\b', 'el cliente valida'),
    (r'(?i)el sistema válida\b', 'el sistema valida'),
    (r'(?i)el regulador válida\b', 'el regulador valida'),
    (r'(?i)cada peer válida\b', 'cada peer valida'),
    (r'(?i)se válida\b', 'se valida'),
    (r'(?i)se válidan\b', 'se validan'),

    # "pública" como verbo (3a persona singular)
    (r'\bpública el evento\b', 'publica el evento'),
    (r'\bpública la transacción\b', 'publica la transacción'),

    # "andiria" -> "anadiría" -> "añadiría" (typo del original)
    (r'\bse andiria\b', 'se añadiría'),
    (r'\bse anadiria\b', 'se añadiría'),

    # "ano" como año en contextos donde es claro (lo común)
    # Pero "1-2 año" debería ser "1-2 años"
    (r'\b1-2 año\b', '1-2 años'),

    # "tecnologia" en contextos donde aparezca sin que el dict lo capture
    # (no aplica, ya está)

    # Errores de typo introducidos
    (r'\bbásica las\b', 'básica'),  # si quedó algo raro
    (r'\bsalí\b', 'salió'),  # typo en "que sali mal" -> "que salió mal"
    (r'\b\.que sali mal\b', 'que salió mal'),
    (r'\bque salí mal\b', 'que salió mal'),
]


def main():
    base = Path("/mnt/d/Dev/Fabric")
    md_files = list(base.rglob("*.md"))
    md_files = [f for f in md_files if "Old content" not in str(f)]

    total_cambios = 0
    for md in sorted(md_files):
        with open(md, 'r', encoding='utf-8') as f:
            original = f.read()
        nuevo = original
        for pattern, replacement in REVERSIONES_VERBALES:
            nuevo = re.sub(pattern, replacement, nuevo)
        if nuevo != original:
            with open(md, 'w', encoding='utf-8') as f:
                f.write(nuevo)
            cambios = sum(1 for o, n in zip(original.split('\n'), nuevo.split('\n')) if o != n)
            print(f"  {cambios:3d} correcciones: {md.relative_to(base)}")
            total_cambios += cambios

    print(f"\nTotal correcciones: {total_cambios}")


if __name__ == "__main__":
    main()
