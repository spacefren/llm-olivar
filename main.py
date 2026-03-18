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
Dada la siguiente información sobre el olivar y los datos recogidos, genera
un informe con información detallada sobre cada parcela, incluyendo los datos y
recomendaciones para cada caso.

La salida esperada de la herramienta desarrollada deberá contener como
mínimo:
• Evaluación agronómica (descripción breve a nivel general y/o a nivel de
parcela).
• Riesgos detectados (descripción breve a nivel general y/o a nivel de
parcela).
• Estimación de pérdida de rendimiento de las parcelas de evaluación.
• Impacto económico estimado (€/ha) por parcela y de media en las
parcelas de evaluación.
• Recomendaciones técnicas.
Datos: """ + datos + """
Documentos: """ + informacion
 
response = model.invoke(input_sistema)
 
print("Respuesta:")
print(response.content)