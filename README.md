# NutriScan

NutriScan es tu asistente inteligente para entender las etiquetas nutricionales de tus alimentos favoritos. Con NutriScan, puedes identificar ingredientes y valores nutricionales al instante para elegir alimentos que cuiden de tu salud.

## Descripción

¡Hola! Soy NutriScan, tu asistente IA para entender las etiquetas nutricionales. Descubre la forma más fácil y rápida de identificar ingredientes y valores al instante, ayudándote a elegir alimentos que cuiden de tu salud. Solo sube una foto de la etiqueta y deja que te guíe hacia decisiones más saludables. ¡Empieza ahora y transforma tu alimentación con confianza!

## Características

- Análisis rápido y preciso de etiquetas nutricionales.
- Identificación de ingredientes y valores nutricionales.
- Evaluación de la adecuación de los alimentos según condiciones de salud específicas.
- Generación de descripciones de audio para las etiquetas analizadas.

## Requisitos

- Python 3.7 o superior
- Flask
- python-dotenv
- langchain
- openai
- PIL (Pillow)
- pytesseract

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/nicoig/nutriscan.git
   cd nutriscan
Crea un entorno virtual e instale las dependencias:

python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
pip install -r requirements.txt
Crea un archivo .env en el directorio raíz del proyecto con tu clave API de OpenAI:

OPENAI_API_KEY=tu_clave_api_aqui
Coloca la imagen app.png en la carpeta static.

Ejecuta la aplicación:
python app.py
Abre tu navegador y visita http://127.0.0.1:5000/ para acceder a NutriScan.

Uso
Sube una imagen de la etiqueta del producto que deseas analizar.
Ingresa cualquier condición de salud o restricción dietética (opcional).
Haz clic en "Analizar Etiqueta".
NutriScan te proporcionará una transcripción de la etiqueta y un análisis de los ingredientes según tu condición de salud ingresada. También puedes escuchar una descripción de audio del análisis.
Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor, sigue estos pasos:

