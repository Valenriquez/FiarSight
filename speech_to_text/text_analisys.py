#pip install -q -U google-generativeai

import google.generativeai as genai
import os
import requests
import json
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de la API
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("Google API Key obtenida correctamente.")
else:
    print("No se encontró la variable de entorno GOOGLE_API_KEY.")

genai.configure(api_key=api_key)


# Función para analizar el texto con Gemini
def analyze_text(text):
    prompt = f"""
    Analyze the following intervention in a debate and determine:
    1. Whether what was said is true. If so or if not, provide references.
    2. If any logical fallacies were used.
    3. If the question was evaded.

    Text: "{text}"
    Respond in JSON format with the keys `truthfulness`, `logical_fallacies`, and `question_evasion`.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
    
# Cargar el archivo JSON con las intervenciones
with open('time_line.json', 'r') as infile:
    interventions = json.load(infile)

# Procesar cada intervención y reemplazar el campo "text" por "analysis"
for intervention in interventions:
    text = intervention.pop("text")
    analysis = analyze_text(text)
    intervention["analysis"] = analysis

# Guardar el resultado en un archivo JSON
with open("debate_analysis.json", "w") as outfile:
    json.dump(interventions, outfile, indent=4)

print("Archivo de análisis generado con éxito.")
