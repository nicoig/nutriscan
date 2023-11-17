# DocGPT - Consulta Médica Virtual con Análisis de Imágenes

## Descripción
DocGPT es una aplicación revolucionaria que utiliza modelos avanzados de inteligencia artificial para analizar imágenes y proporcionar información general sobre posibles afecciones médicas. La aplicación combina la potencia de la IA con un análisis de imágenes para ofrecer sugerencias de tratamiento y recomendaciones sobre qué tipo de profesional médico sería adecuado para una consulta específica.

![DocGPT App Screenshot](img/app.jpg)

## Funcionalidades
- **Análisis de Imágenes Médicas**: Los usuarios pueden cargar imágenes relacionadas con sus consultas médicas, y la aplicación analizará estas imágenes utilizando el modelo de IA GPT-4 Vision.
- **Diagnóstico Preliminar**: Basado en el análisis de la imagen y la descripción proporcionada por el usuario, la aplicación proporciona un diagnóstico preliminar.
- **Sugerencias de Tratamiento**: Se generan recomendaciones generales de tratamiento utilizando el modelo GPT-3.5 Turbo.
- **Recomendaciones de Especialistas Médicos**: La aplicación sugiere qué tipo de profesional médico podría ser más adecuado para tratar la afección identificada.
- **Descarga de Resumen**: Los usuarios pueden descargar un resumen de la consulta, incluyendo el diagnóstico y las sugerencias de tratamiento.

## Cómo Usar
1. Cargar una imagen relacionada con la consulta médica.
2. Describir la consulta o los síntomas en el campo de texto proporcionado.
3. Presionar "Enviar Consulta" para que la aplicación procese la información.
4. Leer el diagnóstico preliminar y las sugerencias de tratamiento.
5. Consultar al profesional médico recomendado según sea necesario.
6. Descargar el resumen de la consulta si se desea.

## Instalación y Configuración

Para ejecutar DocGPT, es necesario tener Python y Streamlit instalados. Además, se requieren claves API para utilizar los modelos de OpenAI.
pip install streamlit
pip install openai


Antes de ejecutar la aplicación, asegúrese de configurar las claves API en su entorno.

## Ejecución
streamlit run app.py

## Nota Importante
DocGPT es una herramienta de asistencia y no debe usarse como un sustituto de un diagnóstico médico profesional. Siempre se recomienda consultar a un profesional médico calificado para cualquier problema de salud.

## Autor
NicoIG

