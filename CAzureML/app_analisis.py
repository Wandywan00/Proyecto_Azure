import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageTk

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

#  Función para abrir un archivo de imagen
def seleccionar_imagen():
    archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    if archivo:
        procesar_imagen(archivo)

#  Procesar la imagen seleccionada
def procesar_imagen(imagen_path):
    # Extraer texto
    texto = extraer_texto(imagen_path)
    
    # Extraer palabras clave
    palabras_clave = extraer_palabras_clave(texto)

    # Mostrar imagen
    imagen = Image.open(imagen_path)
    imagen = imagen.resize((250, 250))
    img = ImageTk.PhotoImage(imagen)
    label_imagen.config(image=img)
    label_imagen.image = img

    # Mostrar resultados en la interfaz
    text_resultado.delete(1.0, tk.END)
    text_resultado.insert(tk.END, f" Texto Extraído:\n{texto}\n\n")
    text_resultado.insert(tk.END, f" Palabras Clave: {', '.join(palabras_clave)}")

#  Crear la interfaz gráfica
root = tk.Tk()
root.title("Análisis de Imágenes con IA ")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_seleccionar = tk.Button(frame, text=" Seleccionar Imagen", command=seleccionar_imagen, font=("Arial", 12))
btn_seleccionar.pack()

label_imagen = tk.Label(root)
label_imagen.pack(pady=10)

text_resultado = scrolledtext.ScrolledText(root, width=70, height=10, font=("Arial", 10))
text_resultado.pack(pady=10)

# Ejecutar la interfaz gráfica
root.mainloop()