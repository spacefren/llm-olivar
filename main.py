import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from parser.csv import leer_fila_csv
from parser.pdf import leer_todos_los_pdfs

load_dotenv()

datos = leer_fila_csv(1)

print(datos)

informacion = leer_todos_los_pdfs()
 
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
model = init_chat_model("gpt-4o-mini")

input_sistema = """
Eres un asistente experto en olivar ante lluvias extremas. Se van a subir datos sobre una parcela de olivar.

Datos de parcela y predicciones:
""" + datos + """

Contexto documental:
""" + informacion + """

Genera un informe con estas secciones basado en los datos de la parcela subida:
1. Evaluación agronómica
2. Riesgos detectados
3. Estimación de pérdida
4. Impacto económico
5. Recomendaciones técnicas
6. Nivel de incertidumbre
7. Acción automática sugerida opcional

Evita basarte en datos generales.
Intenta ajustarte a los datos dados y ser conciso en tu respuesta.

No inventes datos si no los conoces.
"""
 
response = model.invoke(input_sistema)
 
print("Respuesta:")
print(response.content)
