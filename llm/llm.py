import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    "duracion_encharcamiento_dias": None
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

def procesa_lenguaje_natural(input_usuario):
    global historial, estado

    historial.append({"role": "user", "content": input_usuario})

    response = client.responses.create(
        model = "gpt-4o-mini",
        input = historial
    )

    faltantes = campos_faltantes(estado)
    if not faltantes:
        # Usa el modelo predictivo
        return "Todo correcto"
    else:
        return response.output[0].content[0].text