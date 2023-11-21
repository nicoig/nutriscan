# Chef IA - Asistente de Cocina con Inteligencia Artificial

## Descripción
Chef IA es una innovadora aplicación de cocina asistida por inteligencia artificial que ayuda a los usuarios a identificar ingredientes a partir de una imagen y sugiere recetas que pueden ser preparadas con esos ingredientes. Utilizando tecnologías de procesamiento de imágenes y modelos de lenguaje avanzados, Chef IA ofrece una experiencia culinaria única y personalizada.

![Chef IA App Screenshot](img/app.jpg)

## Características
- **Análisis de Imágenes de Ingredientes**: Carga una imagen de tus ingredientes y deja que la IA identifique lo que tienes.
- **Sugerencias de Recetas**: Basado en los ingredientes identificados, la aplicación sugiere un plato que puedes preparar.
- **Instrucciones de Preparación**: Obtén un paso a paso detallado de cómo preparar el plato sugerido.
- **Descarga de Recetas**: La aplicación permite descargar la receta completa, incluyendo ingredientes y pasos de preparación.
- **Generación de Imágenes con DALL-E**: Visualiza un ejemplo del plato terminado generado por IA.

## Cómo usar
1. **Carga una Imagen**: Sube una foto de los ingredientes que tienes a mano.
2. **Obtén Sugerencias de Platos**: La IA analizará tu imagen y te dirá qué plato puedes cocinar.
3. **Sigue las Instrucciones**: Lee y sigue las instrucciones paso a paso para preparar tu plato.
4. **Descarga la Receta**: Guarda la receta para referencia futura.
5. **Visualiza el Plato**: Mira una imagen generada por IA de cómo podría verse tu plato.

## Tecnologías Utilizadas
- Streamlit
- OpenAI's GPT-3 y GPT-4 Vision
- Python
- DALL-E para la generación de imágenes

## Instalación
Para ejecutar Chef IA localmente, necesitarás instalar Streamlit y otras dependencias. Asegúrate también de tener las claves API necesarias para OpenAI.
pip install streamlit openai pillow requests

## Ejecución
Para iniciar la aplicación, ejecuta:
streamlit run app.py

## Nota Importante
Chef IA es una herramienta de asistencia culinaria y está diseñada para ofrecer sugerencias basadas en inteligencia artificial. Siempre se recomienda utilizar el criterio personal al cocinar.

## Autores
NicoIG

