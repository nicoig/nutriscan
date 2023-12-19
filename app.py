# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/LabelGPT.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# git remote set-url origin https://github.com/nicoig/LabelGPT.git
# git remote -v
# git push -u origin main


################################################


import streamlit as st
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Función para codificar imágenes en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Función Texto a Voz
def tts(text):
    if api_key == '':
        st.error('Por favor, configura tu clave API de OpenAI en el archivo .env')
        return None
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.audio.speech.create(
                model="tts-1",  # Modelo por defecto
                voice="echo",   # Voz por defecto
                input=text,
            )
            return response.content
        except Exception as error:
            st.error(f"Se produjo un error al generar el habla: {error}")
            return None

# Función para convertir audio a base64 y crear elemento HTML para audio
def get_audio_file_content(audio_content):
    base64_audio = base64.b64encode(audio_content).decode('utf-8')
    audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{base64_audio}" type="audio/mpeg"></audio>'
    return audio_html

# Diseño de la Aplicación Streamlit para LabelGPT
st.title("LabelGPT")

# Configura el subtítulo de la aplicación con un tamaño de fuente más pequeño
st.markdown("""
    <style>
    .subheader-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="subheader-font">LabelGPT: tu asistente IA para entender etiquetas nutricionales y seleccionar alimentos para dietas especiales.</p>', unsafe_allow_html=True)

# Imagen
st.image('img/app.png', width=250)


# Carga de imagen por el usuario
uploaded_file = st.file_uploader("Sube una imagen de la etiqueta del producto", type=["jpg", "png", "jpeg"])

# Input para condiciones dietéticas específicas
user_condition = st.text_input("Ingresa cualquier condición de salud o restricción dietética (opcional):")

if st.button("Analizar Etiqueta") and uploaded_file is not None:
    with st.spinner('Transcribiendo y analizando la etiqueta...'):
        image = encode_image(uploaded_file)
        chain = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
        
        # Transcribir la etiqueta
        transcripcion_msg = chain.invoke(
            [AIMessage(content="Por favor, identifique la información nutricional y los ingredientes que se muestran en la siguiente imagen. Incluya todos los detalles como calorías, grasas, carbohidratos, proteínas, vitaminas, minerales, y la lista completa de ingredientes."),
            HumanMessage(content=[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}])
            ]
        )
        st.session_state['transcripcion_etiqueta'] = transcripcion_msg.content
        st.markdown("**Transcripción de la Etiqueta:**")
        st.write(st.session_state['transcripcion_etiqueta'])

        # Analizar ingredientes en relación a la condición del usuario
        prompt_analisis_ingredientes = PromptTemplate.from_template(
            """
            Dada la siguiente transcripción de una etiqueta nutricional:
            {transcription}
            y considerando la condición dietética específica: {condition}
            ¿Hay algún ingrediente que podría ser perjudicial para la salud del usuario según su condición?

            Output:
            """
        )
        runnable = prompt_analisis_ingredientes | chain | StrOutputParser()
        st.session_state['analisis_ingredientes'] = runnable.invoke({"transcription": st.session_state['transcripcion_etiqueta'], "condition": user_condition})
        st.markdown("**Análisis de Ingredientes Según la Condición Ingresada:**")
        st.write(st.session_state['analisis_ingredientes'])

        # Generar y reproducir audio automáticamente
        texto_para_audio = st.session_state['analisis_ingredientes']
        if texto_para_audio:
            audio_content = tts(texto_para_audio)
            if audio_content is not None:
                audio_html = get_audio_file_content(audio_content)
                st.markdown(audio_html, unsafe_allow_html=True)
