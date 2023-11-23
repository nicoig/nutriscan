# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/ecoGPT.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

# git remote set-url origin https://github.com/nicoig/ecoGPT.git
# git remote -v
# git push -u origin main


################################################
##


import streamlit as st
import base64
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from io import BytesIO

# Cargar las variables de entorno para las claves API
load_dotenv(find_dotenv())

# Función para codificar imágenes en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Configura el título y subtítulo de la aplicación en Streamlit
st.title("EcoGPT")
st.subheader("Asistencia inteligente para el reciclaje de productos")
# Imagen
st.image('img/robot.png', width=350)

# Carga de imagen por el usuario
uploaded_file = st.file_uploader("Carga una imagen del producto que deseas reciclar", type=["jpg", "png", "jpeg"])

# Botón de enviar y proceso principal
if st.button("Analizar Producto") and uploaded_file is not None:
    with st.spinner('Identificando el producto y material...'):
        image = encode_image(uploaded_file)

        # Identificar el producto y el material con la IA
        chain = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
        msg = chain.invoke(
            [AIMessage(content="Basándose en la imagen, identifique el producto y el tipo de material."),
             HumanMessage(content=[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}])
            ]
        )

        identificacion = msg.content
        st.markdown("**Identificación del producto y material:**")
        st.write(identificacion)

        # Generar recomendaciones de reciclaje
        prompt_reciclaje = PromptTemplate.from_template(
            """
            Dado el siguiente producto y material identificado:
            {identification}
            ¿Qué consejos de reciclaje se pueden dar para este producto?

            Output:
            """
        )
        runnable = prompt_reciclaje | chain | StrOutputParser()
        consejos_reciclaje = runnable.invoke({"identification": identificacion})
        st.markdown("**Consejos para reciclar este producto:**")
        st.write(consejos_reciclaje)

# Nota: Asegúrate de tener configuradas tus claves API y cualquier otro ajuste específico necesario para tu entorno y APIs.
