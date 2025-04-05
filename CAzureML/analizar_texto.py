



from azure.ai.textanalytics import TextAnalyticsClient 
from azure.core.credentials import AzureKeyCredential

# Configuración de Azure Text Analytics
ENDPOINT = "https://textanalyticspolicia.cognitiveservices.azure.com/"
API_KEY = "BWhAFok9SSb6bVUAZzcuykMtnMZSxO1ZHOT9WlzpiFPrGWuJA0HcJQQJ99BDACYeBjFXJ3w3AAAaACOGbjq6"

cliente_nlp = TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

# Función para extraer palabras clave
def extraer_palabras_clave(texto):
    respuesta = cliente_nlp.extract_key_phrases([texto])  
    documento = respuesta[0] 

    if not documento.is_error: 
        return documento.key_phrases  
    else:
        print("Error en la extracción de palabras clave:", documento.error)
        return []


print("=" * 50)

texto = """

Reunidn pactada
para el 25 de abril.
Coordenadas enviadas
Con Pirmar presencia,
No usar canal habitud,

"""
palabras_clave = extraer_palabras_clave(texto)

print(texto)

print("=" * 50)

print("\n Palabras Clave Detectadas:")
for palabra in palabras_clave:
    print(f"- {palabra}")
    
print("=" * 50)


