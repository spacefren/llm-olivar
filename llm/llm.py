from dotenv import load_dotenv
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

input_procesador = """
Eres un LLM diseñado para predecir pérdidas asociadas al olivar en casos de inundación.

Tu tarea consiste en traducir lenguaje natural introducido por el usuario a una serie de datos,
para que sean usados después por un modelo predictivo.

Los datos a recoger son los siguientes:
- parcel_id: es el identificador único para cada registro.
- zona_provincia: indica la provincia andaluza donde se encuentra la
parcela.
- tipo_olivar: nos permite deducir que tipo de sistema de plantación tiene
la parcela.
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

El input del usuario es el siguiente:

"""

def process_natural_language(input_usuario):
    response = client.responses.create(
        model = "gpt-4o-mini",
        input = input_procesador + input_usuario
    )