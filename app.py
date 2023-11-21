# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/asistente-cocina-ia.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# git remote set-url origin https://github.com/nicoig/asistente-cocina-ia.git
# git remote -v
# git push -u origin main

################################################
###

import streamlit as st
import base64
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from PIL import Image
from io import BytesIO

# Cargar las variables de entorno para las claves API
load_dotenv(find_dotenv())

# Función para codificar imágenes en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Función para descargar imágenes
def download_image(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return buffered.getvalue()

# Configura el título y subtítulo de la aplicación en Streamlit
st.title("Chef IA")

# Subtítulo descriptivo del proyecto
st.markdown("""
    <style>
    .small-font {
        font-size:18px !important;
    }
    </style>
    <p class="small-font">Toma una foto a tus ingredientes, te diré que plato puedes preparar y te enseñaré el paso a paso para que aprendas a cocinarlo</p>
    """, unsafe_allow_html=True)

# Imagen
st.image('img/robot.jpg', width=350)

# Carga de imagen por el usuario
uploaded_file = st.file_uploader("Carga una imagen con ingredientes", type=["jpg", "png", "jpeg"])

# Restablecer estado si se carga una nueva imagen
if 'last_uploaded_file' not in st.session_state or (uploaded_file is not None and uploaded_file != st.session_state.get('last_uploaded_file', None)):
    st.session_state['last_uploaded_file'] = uploaded_file
    st.session_state['processed'] = False

# Botón de enviar y proceso principal
if st.button("Enviar") and uploaded_file is not None:
    st.session_state['processed'] = True
    with st.spinner('Cargando...'):
        image = encode_image(uploaded_file)
        
        
 # Configura e invoca la cadena LangChain para el reconocimiento de ingredientes
        chain = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
        msg = chain.invoke(
            [AIMessage(content="Eres un robot útil que es especialmente bueno en OCR a partir de imágenes."),
             HumanMessage(content=[{"type": "text", "text": "Identifique todos los elementos de esta imagen que estén relacionados con la comida y proporcione una lista de lo que ve."},
                                   {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}])
            ]
        )

        ingredientes = msg.content
        st.markdown("**Ingredientes:**")
        st.write(ingredientes)

        # Crear el nombre del plato
        chain = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1024)
        prompt = PromptTemplate.from_template(
            """
            Verá los siguientes alimentos en una lista de productos:
            {food}
            Crea un plato usando solo estos ingredientes y di cómo se llama. Solo devuelve el nombre del plato.
            No hay explicación adicional ni nada relacionado. solo el nombre

            Ejemplo:
            'Pizza'
            'Sushi'

            Output:
            """
        )
        runnable = prompt | chain | StrOutputParser()
        dish = runnable.invoke({"food": ingredientes})
        st.markdown("**Plato:**")
        st.write(dish)

        # Creando las instrucciones de preparación
        prompt = PromptTemplate.from_template(
            """
            Verá un plato de comida en seguida:
            {dish}

            También tienes los ingredientes: 
            {food}

            Explica cómo elaborar este plato, paso a paso, teniendo en cuenta los ingredientes, debe ser un paso a paso
            para llevar a cabo el plato.

            Output:
            """
        )
        runnable = prompt | chain | StrOutputParser()
        input_para_runnable = {"dish": dish, "food": ingredientes}
        instructions = runnable.invoke(input_para_runnable)
        st.markdown("**Preparación:**")
        st.write(instructions)

        # Crear imágen del plato con DALL-E
        #st.markdown("**Imagen del plato:**")
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Una agradable cena a la luz de las velas con {dish} para dos personas, realista",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        #st.image(image_url)

        

        # Configura e invoca la cadena LangChain para el reconocimiento de ingredientes
        # ... (el resto del código de procesamiento permanece igual)

        # Almacenar los datos generados en st.session_state
        st.session_state['ingredientes'] = ingredientes
        st.session_state['dish'] = dish
        st.session_state['instructions'] = instructions
        st.session_state['image_url'] = image_url
        
        

# Condición para mostrar la imagen y los botones de descarga solo si ya se han procesado los datos
if st.session_state.get('processed', False):
    st.markdown("**Imagen del plato:**")
    st.image(st.session_state['image_url'])
    

    # Botón para descargar la imagen generada
    image_bytes = download_image(st.session_state['image_url'])
    st.download_button(
        label="Descargar Imagen del Plato",
        data=image_bytes,
        file_name="plato.jpg",
        mime="image/jpeg"
    )

    # Creación del texto a descargar
    texto_a_descargar = f"Ingredientes:\n{st.session_state['ingredientes']}\n\nPlato:\n{st.session_state['dish']}\n\nPreparación:\n{st.session_state['instructions']}"
    st.download_button("Descargar Receta", texto_a_descargar, "receta.txt", "text/plain")
    
    
