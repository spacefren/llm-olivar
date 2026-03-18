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
Eres un asistente experto en olivar ante lluvias extremas. Se van a subir datos sobre parcelas de olivar.

Datos de parcela:
{parcela_dict}

Predicciones del modelo:
{predicciones}

Contexto documental:
{contexto_documental}

Genera un informe con estas secciones:
1. Evaluación agronómica
2. Riesgos detectados
3. Estimación de pérdida
4. Impacto económico
5. Recomendaciones técnicas
6. Nivel de incertidumbre
7. Acción automática sugerida opcional

No inventes datos si no los conoces.

Datos: """ + datos + """
Documentos: """ + informacion
 
response = model.invoke(input_sistema)
 
print("Respuesta:")
print(response.content)
