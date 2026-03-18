import os
from PyPDF2 import PdfReader

def leer_todos_los_pdfs():
    carpeta = "documentos"
    texto_total = ""

    if not os.path.exists(carpeta):
        print(f"La carpeta '{carpeta}' no existe.")
        return ""

    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(carpeta, archivo)
            try:
                with open(ruta, "rb") as f:
                    reader = PdfReader(f)
                    for pagina in reader.pages:
                        texto_total += (pagina.extract_text() or "") + "\n"
            except Exception as e:
                print(f"Error al leer '{archivo}': {e}")

    return texto_total

'''
def read_pdfs_from_folder(folder_path: str) -> dict:
    """
    Lee todos los archivos PDF de una carpeta especificada y extrae su contenido de texto.

    Args:
        folder_path (str): La ruta a la carpeta que contiene los archivos PDF.

    Returns:
        dict: Un diccionario donde las claves son los nombres de los archivos PDF
              (sin la extensión .pdf) y los valores son el texto extraído de cada archivo.
    """
    documents_text = {}
    if not os.path.exists(folder_path):
        print(f"La carpeta '{folder_path}' no existe.")
        return documents_text

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            filepath = os.path.join(folder_path, filename)
            text = ""
            try:
                with open(filepath, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                documents_text[os.path.splitext(filename)[0]] = text
                print(f"Texto extraído de '{filename}'.")
            except Exception as e:
                print(f"Error al leer '{filename}': {e}")

    return documents_text

# Ejemplo de uso de la función:
# Asegúrate de que tienes una carpeta llamada 'documentos' y algunos PDFs dentro
# Si no tienes PDFs, puedes crear algunos dummy para probar

# Crea una carpeta 'documentos' si no existe
if not os.path.exists('documentos'):
    os.makedirs('documentos')
    print("Carpeta 'documentos' creada.")

# Crea un PDF dummy para la demostración si no hay archivos en la carpeta
if not any(f.endswith('.pdf') for f in os.listdir('documentos')):
    dummy_pdf_content_1 = b"""
%PDF-1.4
1 0 obj
<</Type/Catalog/Pages 2 0 R>>
endobj
2 0 obj
<</Type/Pages/Count 1/Kids[3 0 R]>>
endobj
3 0 obj
<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>
endobj
4 0 obj
<</Length 80>>stream
BT /F1 24 Tf 100 700 Td (Este es el documento uno con informacion util.) Tj ET
BT /F1 12 Tf 100 650 Td (Contiene detalles sobre el proyecto alfa.) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000074 00000 n
0000000155 00000 n
0000000305 00000 n
trailer
<</Size 5/Root 1 0 R>>
startxref
450
%%EOF
"""
    with open('documentos/documento_uno.pdf', 'wb') as f:
        f.write(dummy_pdf_content_1)
    print("PDF dummy 'documento_uno.pdf' creado en 'documentos'.")

    dummy_pdf_content_2 = b"""
%PDF-1.4
1 0 obj
<</Type/Catalog/Pages 2 0 R>>
endobj
2 0 obj
<</Type/Pages/Count 1/Kids[3 0 R]>>
endobj
3 0 obj
<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>
endobj
4 0 obj
<</Length 80>>stream
BT /F1 24 Tf 100 700 Td (Documento dos enfocado en resultados.) Tj ET
BT /F1 12 Tf 100 650 Td (Muestra estadisticas del mes de enero.) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000074 00000 n
0000000155 00000 n
0000000305 00000 n
trailer
<</Size 5/Root 1 0 R>>
startxref
450
%%EOF
"""
    with open('documentos/documento_dos.pdf', 'wb') as f:
        f.write(dummy_pdf_content_2)
    print("PDF dummy 'documento_dos.pdf' creado en 'documentos'.")


pdfs_as_text = read_pdfs_from_folder('documentos')

# Imprimir el contenido extraído (primeros 200 caracteres de cada documento)
for doc_name, doc_content in pdfs_as_text.items():
    display.display(display.Markdown(f"**Contenido de '{doc_name}' (primeras 200 caracteres):**\n```\n{doc_content[:200]}...\n```"))
'''