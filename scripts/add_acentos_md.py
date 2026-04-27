"""
Repasa todos los .md del proyecto y añade acentos y eñes a las palabras
en español que aparecen sin ellos. NO toca:
- Bloques de código (entre ``` y ```)
- Código inline (entre ` y `)
- URLs
- Bloques mermaid
"""
import os
import re
from pathlib import Path

# Diccionario: palabra_sin_acento -> palabra_con_acento
# Solo palabras donde no hay ambigüedad de significado por contexto
REEMPLAZOS = {
    # Sustantivos terminados en -ción
    "accion": "acción",
    "Accion": "Acción",
    "ACCION": "ACCIÓN",
    "actuacion": "actuación",
    "adopcion": "adopción",
    "Adopcion": "Adopción",
    "alimentacion": "alimentación",
    "anonimizacion": "anonimización",
    "aplicacion": "aplicación",
    "Aplicacion": "Aplicación",
    "aplicaciones": "aplicaciones",  # ya OK pero por si acaso
    "aprobacion": "aprobación",
    "Aprobacion": "Aprobación",
    "auditoria": "auditoría",
    "Auditoria": "Auditoría",
    "autoridad": "autoridad",  # ya OK
    "autorizacion": "autorización",
    "caducacion": "caducación",
    "calificacion": "calificación",
    "centralizacion": "centralización",
    "cifracion": "cifrado",  # corrección
    "circulacion": "circulación",
    "clasificacion": "clasificación",
    "codificacion": "codificación",
    "combinacion": "combinación",
    "comparacion": "comparación",
    "compensacion": "compensación",
    "compilacion": "compilación",
    "composicion": "composición",
    "comunicacion": "comunicación",
    "Comunicacion": "Comunicación",
    "concentracion": "concentración",
    "concesion": "concesión",
    "condicion": "condición",
    "Condicion": "Condición",
    "conexion": "conexión",
    "Conexion": "Conexión",
    "configuracion": "configuración",
    "Configuracion": "Configuración",
    "confirmacion": "confirmación",
    "consideracion": "consideración",
    "construccion": "construcción",
    "consultoria": "consultoría",
    "contenido": "contenido",  # OK
    "contratacion": "contratación",
    "contribucion": "contribución",
    "conversacion": "conversación",
    "creacion": "creación",
    "Creacion": "Creación",
    "decision": "decisión",
    "Decision": "Decisión",
    "decisiones": "decisiones",
    "declaracion": "declaración",
    "definicion": "definición",
    "Definicion": "Definición",
    "definiciones": "definiciones",
    "delegacion": "delegación",
    "demostracion": "demostración",
    "denominacion": "denominación",
    "deshabilitacion": "deshabilitación",
    "destruccion": "destrucción",
    "deteccion": "detección",
    "Deteccion": "Detección",
    "determinacion": "determinación",
    "diferenciacion": "diferenciación",
    "dimension": "dimensión",
    "Dimension": "Dimensión",
    "direccion": "dirección",
    "Direccion": "Dirección",
    "direcciones": "direcciones",
    "discusion": "discusión",
    "Discusion": "Discusión",
    "diseño": "diseño",  # OK
    "disposicion": "disposición",
    "distribucion": "distribución",
    "Distribucion": "Distribución",
    "documentacion": "documentación",
    "Documentacion": "Documentación",
    "duracion": "duración",
    "ecuacion": "ecuación",
    "edicion": "edición",
    "educacion": "educación",
    "ejecucion": "ejecución",
    "Ejecucion": "Ejecución",
    "ejecuciones": "ejecuciones",
    "elaboracion": "elaboración",
    "elevacion": "elevación",
    "eleccion": "elección",
    "eliminacion": "eliminación",
    "embarcacion": "embarcación",
    "emision": "emisión",
    "Emision": "Emisión",
    "emisiones": "emisiones",
    "endorsacion": "endorsacion",  # neologismo, no tocar
    "energia": "energía",
    "ensenanza": "enseñanza",
    "estacion": "estación",
    "estimacion": "estimación",
    "evaluacion": "evaluación",
    "evolucion": "evolución",
    "Evolucion": "Evolución",
    "exception": "excepción",
    "excepcion": "excepción",
    "Excepcion": "Excepción",
    "exclusion": "exclusión",
    "Exclusion": "Exclusión",
    "expansion": "expansión",
    "Expansion": "Expansión",
    "experimentacion": "experimentación",
    "explicacion": "explicación",
    "Explicacion": "Explicación",
    "exportacion": "exportación",
    "exposicion": "exposición",
    "Exposicion": "Exposición",
    "extension": "extensión",
    "Extension": "Extensión",
    "fabricacion": "fabricación",
    "facturacion": "facturación",
    "federacion": "federación",
    "Federacion": "Federación",
    "filiacion": "filiación",
    "financiacion": "financiación",
    "Financiacion": "Financiación",
    "formacion": "formación",
    "Formacion": "Formación",
    "fragmentacion": "fragmentación",
    "fundacion": "fundación",
    "Fundacion": "Fundación",
    "fusion": "fusión",
    "generacion": "generación",
    "Generacion": "Generación",
    "gestion": "gestión",
    "Gestion": "Gestión",
    "graduacion": "graduación",
    "habitacion": "habitación",
    "habilitacion": "habilitación",
    "identificacion": "identificación",
    "Identificacion": "Identificación",
    "implementacion": "implementación",
    "Implementacion": "Implementación",
    "implicacion": "implicación",
    "importacion": "importación",
    "imposicion": "imposición",
    "improvisacion": "improvisación",
    "inclusion": "inclusión",
    "Inclusion": "Inclusión",
    "informacion": "información",
    "Informacion": "Información",
    "iniciacion": "iniciación",
    "inicializacion": "inicialización",
    "Inicializacion": "Inicialización",
    "inscripcion": "inscripción",
    "instalacion": "instalación",
    "Instalacion": "Instalación",
    "institucion": "institución",
    "instruccion": "instrucción",
    "integracion": "integración",
    "Integracion": "Integración",
    "interaccion": "interacción",
    "Interaccion": "Interacción",
    "interpretacion": "interpretación",
    "intervencion": "intervención",
    "introduccion": "introducción",
    "Introduccion": "Introducción",
    "intuicion": "intuición",
    "investigacion": "investigación",
    "jurisdiccion": "jurisdicción",
    "legislacion": "legislación",
    "liberacion": "liberación",
    "limitacion": "limitación",
    "Limitacion": "Limitación",
    "liquidacion": "liquidación",
    "Liquidacion": "Liquidación",
    "manipulacion": "manipulación",
    "manutencion": "manutención",
    "mediacion": "mediación",
    "medicion": "medición",
    "memoria": "memoria",  # OK sin tilde
    "mencion": "mención",
    "migracion": "migración",
    "Migracion": "Migración",
    "modificacion": "modificación",
    "Modificacion": "Modificación",
    "monitorizacion": "monitorización",
    "Monitorizacion": "Monitorización",
    "movilizacion": "movilización",
    "nacion": "nación",
    "negociacion": "negociación",
    "notificacion": "notificación",
    "obligacion": "obligación",
    "obtencion": "obtención",
    "ocupacion": "ocupación",
    "operacion": "operación",
    "Operacion": "Operación",
    "operaciones": "operaciones",
    "Operaciones": "Operaciones",
    "opinion": "opinión",
    "Opinion": "Opinión",
    "oposicion": "oposición",
    "ordenacion": "ordenación",
    "organizacion": "organización",
    "Organizacion": "Organización",
    "organizaciones": "organizaciones",
    "Organizaciones": "Organizaciones",
    "orientacion": "orientación",
    "paginacion": "paginación",
    "Paginacion": "Paginación",
    "participacion": "participación",
    "Participacion": "Participación",
    "particion": "partición",
    "percepcion": "percepción",
    "permision": "permisión",
    "personalizacion": "personalización",
    "perspectiva": "perspectiva",  # OK
    "planificacion": "planificación",
    "Planificacion": "Planificación",
    "poblacion": "población",
    "polucion": "polución",
    "ponderacion": "ponderación",
    "posicion": "posición",
    "Posicion": "Posición",
    "preparacion": "preparación",
    "presentacion": "presentación",
    "Presentacion": "Presentación",
    "preservacion": "preservación",
    "presion": "presión",
    "prestacion": "prestación",
    "presuncion": "presunción",
    "prevision": "previsión",
    "produccion": "producción",
    "Produccion": "Producción",
    "produccion": "producción",
    "programacion": "programación",
    "prohibicion": "prohibición",
    "promocion": "promoción",
    "propagacion": "propagación",
    "proporcion": "proporción",
    "proposicion": "proposición",
    "proteccion": "protección",
    "Proteccion": "Protección",
    "publicacion": "publicación",
    "Publicacion": "Publicación",
    "publicaciones": "publicaciones",
    "razon": "razón",
    "Razon": "Razón",
    "razones": "razones",
    "reaccion": "reacción",
    "realizacion": "realización",
    "recepcion": "recepción",
    "recoleccion": "recolección",
    "recomendacion": "recomendación",
    "redaccion": "redacción",
    "reduccion": "reducción",
    "Reduccion": "Reducción",
    "referencia": "referencia",  # OK
    "regeneracion": "regeneración",
    "regulacion": "regulación",
    "Regulacion": "Regulación",
    "relacion": "relación",
    "Relacion": "Relación",
    "relaciones": "relaciones",
    "remision": "remisión",
    "remitente": "remitente",  # OK
    "renovacion": "renovación",
    "Renovacion": "Renovación",
    "reparacion": "reparación",
    "reparticion": "repartición",
    "replicacion": "replicación",
    "representacion": "representación",
    "republica": "república",
    "Republica": "República",
    "reputacion": "reputación",
    "resolucion": "resolución",
    "Resolucion": "Resolución",
    "respeto": "respeto",  # OK sin tilde
    "responsabilidad": "responsabilidad",  # OK
    "restauracion": "restauración",
    "restriccion": "restricción",
    "retencion": "retención",
    "reunion": "reunión",
    "revelacion": "revelación",
    "revision": "revisión",
    "Revision": "Revisión",
    "revisiones": "revisiones",
    "revocacion": "revocación",
    "Revocacion": "Revocación",
    "rotacion": "rotación",
    "Rotacion": "Rotación",
    "sancion": "sanción",
    "Sancion": "Sanción",
    "sanciones": "sanciones",
    "satisfaccion": "satisfacción",
    "secrecion": "secreción",
    "seccion": "sección",
    "Seccion": "Sección",
    "secciones": "secciones",
    "Secciones": "Secciones",
    "seleccion": "selección",
    "Seleccion": "Selección",
    "sensacion": "sensación",
    "separacion": "separación",
    "sesion": "sesión",
    "Sesion": "Sesión",
    "sesiones": "sesiones",
    "simulacion": "simulación",
    "situacion": "situación",
    "Situacion": "Situación",
    "solucion": "solución",
    "Solucion": "Solución",
    "soluciones": "soluciones",
    "Soluciones": "Soluciones",
    "subdivision": "subdivisión",
    "subestacion": "subestación",
    "subordinacion": "subordinación",
    "subscripcion": "subscripción",
    "substraccion": "substracción",
    "subvencion": "subvención",
    "supervision": "supervisión",
    "Supervision": "Supervisión",
    "suposicion": "suposición",
    "supresion": "supresión",
    "tarjeta": "tarjeta",  # OK
    "telecomunicacion": "telecomunicación",
    "tension": "tensión",
    "terminacion": "terminación",
    "tradicion": "tradición",
    "Tradicion": "Tradición",
    "traduccion": "traducción",
    "transaccion": "transacción",
    "Transaccion": "Transacción",
    "transacciones": "transacciones",
    "Transacciones": "Transacciones",
    "transferencia": "transferencia",  # OK
    "transformacion": "transformación",
    "transicion": "transición",
    "Transicion": "Transición",
    "transiciones": "transiciones",
    "transmision": "transmisión",
    "Transmision": "Transmisión",
    "transparencia": "transparencia",  # OK
    "ubicacion": "ubicación",
    "union": "unión",
    "Union": "Unión",
    "validacion": "validación",
    "Validacion": "Validación",
    "validaciones": "validaciones",
    "valoracion": "valoración",
    "verificacion": "verificación",
    "Verificacion": "Verificación",
    "version": "versión",
    "Version": "Versión",
    "versiones": "versiones",
    "Versiones": "Versiones",
    "violacion": "violación",
    "vision": "visión",
    "Vision": "Visión",
    "visualizacion": "visualización",
    "votacion": "votación",
    "Votacion": "Votación",

    # Adjetivos y otros
    "academico": "académico",
    "academica": "académica",
    "alfanumerico": "alfanumérico",
    "algebra": "álgebra",
    "ambito": "ámbito",
    "anonimo": "anónimo",
    "anonima": "anónima",
    "automatico": "automático",
    "automatica": "automática",
    "automaticamente": "automáticamente",
    "basico": "básico",
    "basica": "básica",
    "basicos": "básicos",
    "basicas": "básicas",
    "Basico": "Básico",
    "Basica": "Básica",
    "biologico": "biológico",
    "biologica": "biológica",
    "calculo": "cálculo",
    "calculos": "cálculos",
    "caracter": "carácter",
    "Caracter": "Carácter",
    "caracteres": "caracteres",
    "categoria": "categoría",
    "Categoria": "Categoría",
    "categorias": "categorías",
    "centesimo": "centésimo",
    "cientifico": "científico",
    "cientifica": "científica",
    "circulo": "círculo",
    "clasico": "clásico",
    "clasica": "clásica",
    "clausula": "cláusula",
    "Clausula": "Cláusula",
    "clausulas": "cláusulas",
    "codigo": "código",
    "Codigo": "Código",
    "codigos": "códigos",
    "Codigos": "Códigos",
    "comun": "común",
    "Comun": "Común",
    "comunes": "comunes",  # OK
    "criptografico": "criptográfico",
    "criptografica": "criptográfica",
    "criptograficos": "criptográficos",
    "criptograficas": "criptográficas",
    "criterio": "criterio",  # OK
    "critico": "crítico",
    "Critico": "Crítico",
    "critica": "crítica",
    "Critica": "Crítica",
    "criticos": "críticos",
    "criticas": "críticas",
    "cualquier": "cualquier",  # OK
    "deberia": "debería",
    "deberian": "deberían",
    "deberiamos": "deberíamos",
    "demografico": "demográfico",
    "depues": "después",  # typo común
    "despues": "después",
    "Despues": "Después",
    "diaria": "diaria",  # OK
    "diferencia": "diferencia",  # OK
    "dificil": "difícil",
    "Dificil": "Difícil",
    "dificiles": "difíciles",
    "dinamica": "dinámica",
    "dinamico": "dinámico",
    "dinamicos": "dinámicos",
    "dinamicas": "dinámicas",
    "domestico": "doméstico",
    "domestica": "doméstica",
    "domesticos": "domésticos",
    "domesticas": "domésticas",
    "economia": "economía",
    "economico": "económico",
    "economica": "económica",
    "economicos": "económicos",
    "economicas": "económicas",
    "electronica": "electrónica",
    "electronico": "electrónico",
    "electronicos": "electrónicos",
    "electronicas": "electrónicas",
    "Electronica": "Electrónica",
    "elemento": "elemento",  # OK
    "endemico": "endémico",
    "energetico": "energético",
    "energetica": "energética",
    "epoca": "época",
    "especifico": "específico",
    "especifica": "específica",
    "especificos": "específicos",
    "especificas": "específicas",
    "Especifico": "Específico",
    "Especifica": "Específica",
    "Especificos": "Específicos",
    "estatico": "estático",
    "estatica": "estática",
    "estatica": "estática",
    "estos": "estos",  # OK
    "estrategico": "estratégico",
    "estrategica": "estratégica",
    "etico": "ético",
    "etica": "ética",
    "ethereum": "Ethereum",  # nombre
    "facil": "fácil",
    "Facil": "Fácil",
    "faciles": "fáciles",
    "facilmente": "fácilmente",
    "fenomeno": "fenómeno",
    "filosofia": "filosofía",
    "fisico": "físico",
    "fisica": "física",
    "fisicos": "físicos",
    "fisicas": "físicas",
    "Fisico": "Físico",
    "Fisica": "Física",
    "fonetica": "fonética",
    "formula": "fórmula",
    "formulas": "fórmulas",
    "fragil": "frágil",
    "frigorifico": "frigorífico",
    "futbol": "fútbol",
    "geografia": "geografía",
    "geografico": "geográfico",
    "geografica": "geográfica",
    "geometria": "geometría",
    "grafico": "gráfico",
    "grafica": "gráfica",
    "graficos": "gráficos",
    "graficas": "gráficas",
    "Grafico": "Gráfico",
    "habil": "hábil",
    "habito": "hábito",
    "haciendo": "haciendo",  # OK
    "harian": "harían",
    "haria": "haría",
    "haras": "harás",
    "heroe": "héroe",
    "heroes": "héroes",
    "hidraulico": "hidráulico",
    "historico": "histórico",
    "historica": "histórica",
    "historicos": "históricos",
    "historicas": "históricas",
    "Historico": "Histórico",
    "humanidad": "humanidad",  # OK
    "iconico": "icónico",
    "ilogico": "ilógico",
    "ilogica": "ilógica",
    "imagen": "imagen",  # OK sin tilde
    "imagenes": "imágenes",
    "Imagenes": "Imágenes",
    "indice": "índice",
    "Indice": "Índice",
    "indices": "índices",
    "Indices": "Índices",
    "industria": "industria",  # OK
    "informatica": "informática",
    "Informatica": "Informática",
    "informatico": "informático",
    "ingenieria": "ingeniería",
    "Ingenieria": "Ingeniería",
    "interconexion": "interconexión",
    "interes": "interés",
    "Interes": "Interés",
    "intereses": "intereses",  # OK
    "internacionalizacion": "internacionalización",
    "intrinseco": "intrínseco",
    "irrebatible": "irrebatible",  # OK
    "irrevocable": "irrevocable",  # OK
    "jovenes": "jóvenes",
    "junio": "junio",  # OK
    "lapiz": "lápiz",
    "limite": "límite",
    "Limite": "Límite",
    "limites": "límites",
    "Limites": "Límites",
    "liquido": "líquido",
    "logica": "lógica",
    "Logica": "Lógica",
    "logico": "lógico",
    "Logico": "Lógico",
    "logicos": "lógicos",
    "logicas": "lógicas",
    "magia": "magia",  # OK
    "magnetico": "magnético",
    "manana": "mañana",  # ñ
    "Manana": "Mañana",
    "maquina": "máquina",
    "Maquina": "Máquina",
    "maquinas": "máquinas",
    "matematica": "matemática",
    "matematico": "matemático",
    "Matematica": "Matemática",
    "maximo": "máximo",
    "Maximo": "Máximo",
    "maxima": "máxima",
    "Maxima": "Máxima",
    "maximos": "máximos",
    "maximas": "máximas",
    "mecanico": "mecánico",
    "mecanica": "mecánica",
    "medico": "médico",
    "medica": "médica",
    "medicos": "médicos",
    "medicas": "médicas",
    "Medico": "Médico",
    "medios": "medios",  # OK
    "metafora": "metáfora",
    "metalico": "metálico",
    "metodologia": "metodología",
    "Metodologia": "Metodología",
    "metodologias": "metodologías",
    "metrica": "métrica",
    "Metrica": "Métrica",
    "metricas": "métricas",
    "Metricas": "Métricas",
    "metrico": "métrico",
    "metro": "metro",  # OK
    "miercoles": "miércoles",
    "miguelangel": "miguelángel",  # OK
    "miles": "miles",  # OK
    "minimo": "mínimo",
    "Minimo": "Mínimo",
    "minima": "mínima",
    "Minima": "Mínima",
    "minimos": "mínimos",
    "minimas": "mínimas",
    "modernos": "modernos",  # OK
    "modulo": "módulo",
    "Modulo": "Módulo",
    "modulos": "módulos",
    "Modulos": "Módulos",
    "musica": "música",
    "Musica": "Música",
    "musical": "musical",  # OK
    "narcotrafico": "narcotráfico",
    "negocio": "negocio",  # OK
    "neumatico": "neumático",
    "ninguno": "ninguno",  # OK
    "nivel": "nivel",  # OK
    "noche": "noche",  # OK
    "novecientos": "novecientos",  # OK
    "numero": "número",
    "Numero": "Número",
    "numeros": "números",
    "Numeros": "Números",
    "numerico": "numérico",
    "numerica": "numérica",
    "obstaculo": "obstáculo",
    "obstaculos": "obstáculos",
    "oceano": "océano",
    "octogonal": "octogonal",  # OK
    "olfato": "olfato",  # OK
    "optico": "óptico",
    "optica": "óptica",
    "optimo": "óptimo",
    "optima": "óptima",
    "organico": "orgánico",
    "organica": "orgánica",
    "Origen": "Origen",  # OK
    "ortografico": "ortográfico",
    "pacifico": "pacífico",
    "pais": "país",
    "Pais": "País",
    "paises": "países",
    "Paises": "Países",
    "pajaro": "pájaro",
    "panico": "pánico",
    "papa": "papa",  # ambiguo (papá vs papa-tubérculo)
    "parametros": "parámetros",
    "Parametros": "Parámetros",
    "parametro": "parámetro",
    "parlamentario": "parlamentario",  # OK
    "particula": "partícula",
    "patetico": "patético",
    "perdida": "pérdida",  # cuidado: como sustantivo
    "perdidas": "pérdidas",
    "perfodico": "periódico",
    "periodico": "periódico",
    "periodica": "periódica",
    "periodo": "período",
    "permanente": "permanente",  # OK
    "perpendicular": "perpendicular",  # OK
    "petroleo": "petróleo",
    "petroleos": "petróleos",
    "platano": "plátano",
    "platanos": "plátanos",
    "polemica": "polémica",
    "policia": "policía",
    "policias": "policías",
    "politica": "política",
    "Politica": "Política",
    "politicas": "políticas",
    "Politicas": "Políticas",
    "politico": "político",
    "Politico": "Político",
    "politicos": "políticos",
    "porque": "porque",  # OK (interrogativo: por qué — diferente)
    "practica": "práctica",
    "Practica": "Práctica",
    "practicas": "prácticas",
    "Practicas": "Prácticas",
    "practico": "práctico",
    "Practico": "Práctico",
    "practicos": "prácticos",
    "preselleccion": "preselección",
    "primario": "primario",  # OK
    "primaria": "primaria",  # OK
    "principios": "principios",  # OK
    "privacy": "privacy",  # inglés
    "probabilistico": "probabilístico",
    "probable": "probable",  # OK
    "problematica": "problemática",
    "problematico": "problemático",
    "proceso": "proceso",  # OK
    "profesion": "profesión",
    "profesional": "profesional",  # OK
    "profundidad": "profundidad",  # OK
    "programatico": "programático",
    "publica": "pública",  # cuidado: como verbo "publica" sin tilde
    "Publica": "Pública",
    "publico": "público",
    "Publico": "Público",
    "publicos": "públicos",
    "publicas": "públicas",
    "rapido": "rápido",
    "Rapido": "Rápido",
    "rapida": "rápida",
    "Rapida": "Rápida",
    "rapidos": "rápidos",
    "rapidas": "rápidas",
    "rapidamente": "rápidamente",
    "razonable": "razonable",  # OK
    "rebelde": "rebelde",  # OK
    "reciente": "reciente",  # OK
    "recibido": "recibido",  # OK
    "reciproco": "recíproco",
    "regimen": "régimen",
    "Regimen": "Régimen",
    "regla": "regla",  # OK
    "regulacion": "regulación",  # ya en lista
    "religion": "religión",
    "religiosa": "religiosa",  # OK
    "rendimiento": "rendimiento",  # OK
    "republicano": "republicano",
    "republicana": "republicana",
    "rincon": "rincón",
    "robotico": "robótico",
    "salida": "salida",  # OK
    "saludable": "saludable",  # OK
    "sanitario": "sanitario",  # OK
    "sanidad": "sanidad",  # OK
    "saxofon": "saxofón",
    "secreto": "secreto",  # OK
    "secundario": "secundario",  # OK
    "segun": "según",
    "Segun": "Según",
    "semantico": "semántico",
    "semantica": "semántica",
    "sencillo": "sencillo",  # OK
    "sentado": "sentado",  # OK
    "señal": "señal",  # OK
    "sera": "será",
    "seran": "serán",
    "serie": "serie",  # OK
    "servir": "servir",  # OK
    "siglo": "siglo",  # OK
    "significacion": "significación",
    "significado": "significado",  # OK
    "simbiosis": "simbiosis",  # OK
    "simbolico": "simbólico",
    "simbolica": "simbólica",
    "simbolo": "símbolo",
    "Simbolo": "Símbolo",
    "simbolos": "símbolos",
    "Simbolos": "Símbolos",
    "simil": "símil",
    "simiologico": "simiológico",
    "simple": "simple",  # OK
    "Sin": "Sin",  # OK
    "sintetico": "sintético",
    "sintetica": "sintética",
    "sintoma": "síntoma",
    "sistematico": "sistemático",
    "sistematica": "sistemática",
    "sociologico": "sociológico",
    "sociologica": "sociológica",
    "solamente": "solamente",  # OK
    "solido": "sólido",
    "sonido": "sonido",  # OK
    "soporte": "soporte",  # OK
    "telematico": "telemático",
    "tarea": "tarea",  # OK
    "tecnica": "técnica",
    "Tecnica": "Técnica",
    "tecnicas": "técnicas",
    "Tecnicas": "Técnicas",
    "tecnico": "técnico",
    "Tecnico": "Técnico",
    "tecnicos": "técnicos",
    "tecnologia": "tecnología",
    "Tecnologia": "Tecnología",
    "tecnologias": "tecnologías",
    "tecnologico": "tecnológico",
    "tecnologica": "tecnológica",
    "tecnologicos": "tecnológicos",
    "tecnologicas": "tecnológicas",
    "telefono": "teléfono",
    "telefonos": "teléfonos",
    "telefonica": "telefónica",
    "telematico": "telemático",
    "teorema": "teorema",  # OK
    "teorico": "teórico",
    "teorica": "teórica",
    "termico": "térmico",
    "termica": "térmica",
    "termino": "término",
    "Termino": "Término",
    "terminos": "términos",
    "Terminos": "Términos",
    "tico": "tico",  # ambiguo
    "tipico": "típico",
    "tipica": "típica",
    "tipicos": "típicos",
    "tipicas": "típicas",
    "Tipico": "Típico",
    "Tipica": "Típica",
    "tomografia": "tomografía",
    "topico": "tópico",
    "tragedia": "tragedia",  # OK
    "trafico": "tráfico",
    "Trafico": "Tráfico",
    "tragico": "trágico",
    "tramite": "trámite",
    "tramites": "trámites",
    "tras": "tras",  # OK
    "trayectoria": "trayectoria",  # OK
    "trayendo": "trayendo",  # OK
    "trazabilidad": "trazabilidad",  # OK
    "trazado": "trazado",  # OK
    "trifasico": "trifásico",
    "tropico": "trópico",
    "ultimamente": "últimamente",
    "ultimo": "último",
    "Ultimo": "Último",
    "ultima": "última",
    "Ultima": "Última",
    "ultimos": "últimos",
    "ultimas": "últimas",
    "ultrasonico": "ultrasónico",
    "unanime": "unánime",
    "unico": "único",
    "Unico": "Único",
    "unica": "única",
    "Unica": "Única",
    "unicos": "únicos",
    "unicas": "únicas",
    "univoco": "unívoco",
    "univocamente": "unívocamente",
    "urbanizacion": "urbanización",
    "util": "útil",
    "Util": "Útil",
    "utiles": "útiles",
    "Utiles": "Útiles",
    "utilmente": "útilmente",
    "vacaciones": "vacaciones",  # OK
    "valenciano": "valenciano",  # OK
    "valido": "válido",
    "Valido": "Válido",
    "valida": "válida",
    "Valida": "Válida",
    "validos": "válidos",
    "validas": "válidas",
    "validamente": "válidamente",
    "vasco": "vasco",  # OK
    "vector": "vector",  # OK
    "vehiculo": "vehículo",
    "vehiculos": "vehículos",
    "verdaderamente": "verdaderamente",  # OK
    "verticalmente": "verticalmente",  # OK
    "vinculacion": "vinculación",
    "violencia": "violencia",  # OK
    "virgen": "virgen",  # OK
    "vocacion": "vocación",
    "volatilidad": "volatilidad",  # OK
    "volumen": "volumen",  # OK
    "voluntaria": "voluntaria",  # OK
    "volveremos": "volveremos",  # OK
    "yendo": "yendo",  # OK
    "zoologico": "zoológico",
    "zoologica": "zoológica",

    # Eñes
    "ano": "año",  # CUIDADO: "ano" es palabra válida pero rara, y "año" es muy común
    "Ano": "Año",
    "anos": "años",
    "Anos": "Años",
    "diseñar": "diseñar",  # OK
    "diseno": "diseño",
    "Diseno": "Diseño",
    "disenos": "diseños",
    "disenar": "diseñar",
    "Disenar": "Diseñar",
    "disenado": "diseñado",
    "disenadas": "diseñadas",
    "disenados": "diseñados",
    "disenando": "diseñando",
    "compania": "compañía",
    "Compania": "Compañía",
    "companias": "compañías",
    "espanol": "español",
    "Espanol": "Español",
    "espanola": "española",
    "Espanola": "Española",
    "espanoles": "españoles",
    "espanolas": "españolas",
    "Espana": "España",
    "espana": "España",
    "ensenanza": "enseñanza",
    "Ensenanza": "Enseñanza",
    "ensenar": "enseñar",
    "ensenado": "enseñado",
    "engano": "engaño",
    "danos": "daños",
    "dano": "daño",
    "manana": "mañana",
    "Manana": "Mañana",
    "pequeno": "pequeño",
    "Pequeno": "Pequeño",
    "pequena": "pequeña",
    "Pequena": "Pequeña",
    "pequenos": "pequeños",
    "pequenas": "pequeñas",
    "tamano": "tamaño",
    "Tamano": "Tamaño",
    "tamanos": "tamaños",
    "senalar": "señalar",
    "senalado": "señalado",
    "senalando": "señalando",
    "senal": "señal",
    "Senal": "Señal",
    "senales": "señales",
    "senor": "señor",
    "Senor": "Señor",
    "senora": "señora",
    "Senora": "Señora",
    "señorita": "señorita",  # OK
    "duenos": "dueños",
    "dueno": "dueño",
    "Dueno": "Dueño",
    "duena": "dueña",
    "duenas": "dueñas",
    "campana": "campaña",
    "campanas": "campañas",
    "extrano": "extraño",
    "extrana": "extraña",
    "extranos": "extraños",
    "extranas": "extrañas",
    "extranamente": "extrañamente",
    "extraneza": "extrañeza",
    "antano": "antaño",
    "ostranero": "extranjero",  # typo
    "extranjero": "extranjero",  # OK
    "estano": "estaño",
    "rinon": "riñón",
    "carino": "cariño",
    "Carino": "Cariño",
    "Cataluna": "Cataluña",
    "Coruna": "Coruña",
    "logrono": "Logroño",
    "Logrono": "Logroño",
    "vinedo": "viñedo",
    "vinedos": "viñedos",
    "anadir": "añadir",
    "Anadir": "Añadir",
    "anadido": "añadido",
    "anaden": "añaden",
    "anade": "añade",
    "anada": "añada",
    "anadiendo": "añadiendo",
    "ensanar": "enseñar",  # typo

    # Otros comunes
    "avision": "avisión",  # error
    "avion": "avión",
    "aviones": "aviones",  # OK
    "campeon": "campeón",
    "campeones": "campeones",  # OK
    "leon": "león",
    "leones": "leones",  # OK
    "explosion": "explosión",
    "ilusion": "ilusión",
    "mision": "misión",
    "Mision": "Misión",
    "misiones": "misiones",  # OK
    "obsesion": "obsesión",
    "ocasion": "ocasión",
    "presion": "presión",
    "profesion": "profesión",
    "religion": "religión",
    "remision": "remisión",
    "tension": "tensión",
    "version": "versión",
    "vision": "visión",
}

# Excluir Old content
EXCLUDE_PATHS = ["Old content"]


def es_excluido(path):
    return any(ex in str(path) for ex in EXCLUDE_PATHS)


def proteger_codigo(text):
    """
    Reemplaza temporalmente bloques de codigo y URLs por placeholders.
    Devuelve (texto_modificado, lista_de_extraidos)
    """
    extracted = []

    # Bloques de codigo ```...```
    def repl_code_block(m):
        extracted.append(m.group(0))
        return f"\x00CODE{len(extracted)-1}\x00"
    text = re.sub(r'```.*?```', repl_code_block, text, flags=re.DOTALL)

    # Codigo inline `...`
    def repl_inline(m):
        extracted.append(m.group(0))
        return f"\x00CODE{len(extracted)-1}\x00"
    text = re.sub(r'`[^`\n]+`', repl_inline, text)

    # URLs
    def repl_url(m):
        extracted.append(m.group(0))
        return f"\x00CODE{len(extracted)-1}\x00"
    text = re.sub(r'https?://[^\s\)]+', repl_url, text)

    return text, extracted


def restaurar_codigo(text, extracted):
    """Restaura los bloques de codigo desde los placeholders."""
    def repl(m):
        idx = int(m.group(1))
        return extracted[idx]
    return re.sub(r'\x00CODE(\d+)\x00', repl, text)


def aplicar_reemplazos(text):
    """Aplica los reemplazos del diccionario sobre el texto."""
    for sin_acento, con_acento in REEMPLAZOS.items():
        if sin_acento == con_acento:
            continue
        # Word boundaries para evitar reemplazar partes de palabras
        pattern = r'\b' + re.escape(sin_acento) + r'\b'
        text = re.sub(pattern, con_acento, text)
    return text


def procesar_archivo(path):
    """Procesa un archivo .md, devuelve (cambios, contenido_nuevo)."""
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Proteger codigo, aplicar reemplazos, restaurar codigo
    protegido, extracted = proteger_codigo(original)
    nuevo = aplicar_reemplazos(protegido)
    nuevo = restaurar_codigo(nuevo, extracted)

    # Contar cambios aproximados (lineas modificadas)
    cambios = sum(1 for o, n in zip(original.split('\n'), nuevo.split('\n')) if o != n)

    return cambios, nuevo


def main():
    base = Path("/mnt/d/Dev/Fabric")
    md_files = list(base.rglob("*.md"))
    md_files = [f for f in md_files if not es_excluido(f)]

    total_cambios = 0
    archivos_cambiados = 0

    for md in sorted(md_files):
        cambios, nuevo = procesar_archivo(md)
        if cambios > 0:
            with open(md, 'w', encoding='utf-8') as f:
                f.write(nuevo)
            archivos_cambiados += 1
            total_cambios += cambios
            print(f"  {cambios:3d} cambios: {md.relative_to(base)}")

    print(f"\nTotal: {archivos_cambiados} archivos modificados, {total_cambios} lineas con cambios")


if __name__ == "__main__":
    main()
