import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno (incluida OPENAI_API_KEY) desde .env
load_dotenv()

# Si no hay API key, esto fallará de forma explícita
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY no está definida. Ponla en .env o en el entorno.")

client = OpenAI(api_key=api_key)

input_procesador = """
Eres un sistema que extrae datos estructurados sobre parcelas de olivar.

Devuelve SIEMPRE un JSON válido.
- Solo incluye los campos que el usuario mencione.
- No inventes datos.
- No expliques nada.

Los datos a recoger son los siguientes:
- parcel_id: es el identificador único para cada registro.
- zona_provincia: indica la provincia andaluza donde se encuentra la parcela.
- tipo_olivar: nos permite deducir que tipo de sistema de plantación tiene la parcela.
- riego: indica si la parcela es de Riego o Secano.
- superficie_ha: Extensión de la parcela en hectáreas.
- variedad: diferentes variedades como Picual, Arbequina, Cornicabra...
- estado_fenolológico: fase del ciclo biológico del olivo (Brotación, Floración, Cuajado, Engorde, Reposo).
- tipo_suelo: tipo de textura del suelo de la parcela.
- drenaje: facilidad que tiene el suelo para drenar el agua de lluvia.
- profundidad_suelo_cm: profundidad del suelo que tiene cada parcela en centímetros.
- materia_orgaranica_%: porcentaje de materia orgánica en el suelo.
- pendiente_%: es el porcentaje de pendiente que tiene dicha parcela.
- distancia_rio_m: proximidad a cauces de agua en metros.
- altitud_m: altura sobre el nivel del mar.
- rain_72h_mm: precipitaciones acumuladas en las últimas 72h.
- rain_7d_mm: precipitación acumulada en los últimos 7 días.
- temp_media_7d: temperatura media en los últimos 7días.
- humedad_suelo_%: nivel de humedad en el suelo en porcentaje.
- rendimiento_esperado_kg_ha: producción esperada de kg/ha por parcela de aceitunas.
- precio_mercado_eur_kg: precio del kg de aceituna.
- coste_variabe_ha: gastos operativos y tiempos de ejecución de tareas.
- duracion_encharcamiento_dias: tiempo que la parcela se encuentra encharcada en días.
"""

estado = {
    "parcel_id": None,
    "zona_provincia": None,
    "tipo_olivar": None,
    "riego": None,
    "superficie_ha": None,
    "variedad": None,
    "estado_fenologico": None,
    "tipo_suelo": None,
    "drenaje": None,
    "profundidad_suelo_cm": None,
    "materia_organica_%": None,
    "pendiente_%": None,
    "distancia_rio_m": None,
    "altitud_m": None,
    "rain_72h_mm": None,
    "rain_7d_mm": None,
    "temp_media_7d": None,
    "humedad_suelo_%": None,
    "rendimiento_esperado_kg_ha": None,
    "precio_mercado_eur_kg": None,
    "coste_variable_ha": None,
    "duracion_encharcamiento_dias": None,
}

historial = [
    {
        "role": "system",
        "content": input_procesador
    }
]

def actualizar_estado(respuesta_modelo, estado):
    try:
        nuevos_datos = json.loads(respuesta_modelo)

        for clave, valor in nuevos_datos.items():
            if valor is not None:
                estado[clave] = valor

    except:
        print("Error parseando JSON")

    return estado

def campos_faltantes(estado):
    return [k for k, v in estado.items() if v is None]

def procesa_lenguaje_natural(input_usuario: str) -> str:
    """
    Usa el modelo para extraer/actualizar datos estructurados de la parcela
    y devuelve un mensaje amigable indicando qué se ha rellenado y qué falta.
    """
    global historial, estado

    if not input_usuario or not input_usuario.strip():
        return "Escribe algún dato sobre tu parcela para poder ayudarte."

    historial.append({"role": "user", "content": input_usuario})

    response = client.responses.create(
        model="gpt-4o-mini",
        input=historial,
    )

    # El modelo devuelve SOLO un JSON con los campos mencionados.
    try:
        texto_modelo = response.output[0].content[0].text
    except Exception:
        return "He tenido un problema leyendo la respuesta del modelo."

    # Actualizamos el estado global con los nuevos datos extraídos.
    estado_actualizado = actualizar_estado(texto_modelo, estado)

    faltantes = campos_faltantes(estado_actualizado)

    # Construimos una respuesta de texto para el chat.
    partes = []
    partes.append("He actualizado los datos de tu parcela con lo que has indicado.")

    # Campos que ya tienen valor
    campos_rellenos = {k: v for k, v in estado_actualizado.items() if v is not None}
    if campos_rellenos:
        resumen = "\n".join(f"- {k}: {v}" for k, v in campos_rellenos.items())
        partes.append("\nActualmente tengo estos datos:\n" + resumen)

    if not faltantes:
        partes.append(
            "\nYa tengo todos los campos necesarios. "
            "Puedes preguntar por el riesgo de pérdidas o el impacto económico."
        )
    else:
        lista = "\n".join(f"- {nombre}" for nombre in faltantes)
        partes.append(
            "\nTodavía me faltan algunos datos. "
            "Cuéntame, aunque sea de forma natural, esta información:\n" + lista
        )

    return "\n".join(partes)