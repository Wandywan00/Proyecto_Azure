from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from msrest.authentication import CognitiveServicesCredentials
import os

#  Configuración de Azure Computer Vision
VISION_ENDPOINT = "https://computervisionpolicia.cognitiveservices.azure.com/"
VISION_API_KEY = "1I6Ra8XO9qT7UtD5icW7sIiQ15OBV7pOYRuJj00xF8OKgo9sGzYRJQQJ99BDACYeBjFXJ3w3AAAFACOGIfRH"

vision_client = ComputerVisionClient(VISION_ENDPOINT, CognitiveServicesCredentials(VISION_API_KEY))

#  Configuración de Azure Text Analytics
TEXT_ANALYTICS_ENDPOINT = "https://textanalyticspolicia.cognitiveservices.azure.com/"
TEXT_ANALYTICS_API_KEY = "BWhAFok9SSb6bVUAZzcuykMtnMZSxO1ZHOT9WlzpiFPrGWuJA0HcJQQJ99BDACYeBjFXJ3w3AAAaACOGbjq6"

text_analytics_client = TextAnalyticsClient(endpoint=TEXT_ANALYTICS_ENDPOINT, credential=AzureKeyCredential(TEXT_ANALYTICS_API_KEY))

#  Función para extraer texto de una imagen
def extraer_texto(imagen_path):
    with open(imagen_path, "rb") as imagen:
        respuesta = vision_client.recognize_printed_text_in_stream(imagen)
    
    texto_extraido = ""
    for region in respuesta.regions:
        for linea in region.lines:
            texto_extraido += " ".join([palabra.text for palabra in linea.words]) + "\n"
    
    return texto_extraido.strip()

#  Función para analizar palabras clave
def extraer_palabras_clave(texto):
    respuesta = text_analytics_client.extract_key_phrases([texto])
    return respuesta[0]

#  Procesar una carpeta con imágenes
def procesar_carpeta(carpeta_imagenes):
    for archivo in os.listdir(carpeta_imagenes):
        if archivo.endswith(".png") or archivo.endswith(".jpg"):
            ruta_imagen = os.path.join(carpeta_imagenes, archivo)
            
            print(f"\n Procesando imagen: {archivo}")
            
            # Extraer texto
            texto = extraer_texto(ruta_imagen)
            print(" Texto Extraído:\n", texto)
            
            # Extraer palabras clave
            palabras_clave = extraer_palabras_clave(texto)
            print(" Palabras Clave:", palabras_clave)
            print("-" * 60)

#  Define la carpeta donde están las imágenes
carpeta_imagenes = "imagen"

#  Ejecutar el procesamiento
procesar_carpeta(carpeta_imagenes)
