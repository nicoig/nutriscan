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

# git remote set-url origin https://github.com/nicoig/nutriscan.git
# git remote -v
# git push -u origin main

from flask import Flask, request, render_template_string, jsonify, send_from_directory
import base64
from langchain.chat_models import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
application = app

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Función para codificar imágenes en base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Función Texto a Voz
def tts(text):
    if api_key == '':
        return None, 'Por favor, configura tu clave API de OpenAI en el archivo .env'
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.audio.speech.create(
                model="tts-1",  # Modelo por defecto
                voice="echo",   # Voz por defecto
                input=text,
            )
            return response.content, None
        except Exception as error:
            return None, f"Se produjo un error al generar el habla: {error}"

# Función para convertir audio a base64 y crear elemento HTML para audio
def get_audio_file_content(audio_content):
    base64_audio = base64.b64encode(audio_content).decode('utf-8')
    return f'data:audio/mp3;base64,{base64_audio}'

# Ruta para servir imágenes estáticas
@app.route('/img/<path:filename>')
def serve_image(filename):
    return send_from_directory('img', filename)

# Plantilla HTML para la aplicación
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
        <style>
        body {
            background-color: #222;
            color: #ddd;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .subheader-font {
            font-size:16px !important;
        }
        .file-input {
            margin: 10px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .audio-output {
            margin: 20px 0;
        }
        form {
            display: inline-block;
            text-align: left;
            margin-top: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .file-input input[type="file"] {
            background-color: #007bff;
            color: white;
            padding: 8px 16px;
            border: none;
            cursor: pointer;
            font-size: 14px;
        }
        .file-input input[type="file"]:hover {
            background-color: #0056b3;
        }
        .response {
            white-space: pre-wrap;
            text-align: left;
            margin-top: 20px;
            padding: 20px;
            background-color: #333;
            border-radius: 10px;
            max-width: 80%;
            margin: 20px auto;
        }
        .loader {
            border: 6px solid #f3f3f3;
            border-radius: 50%;
            border-top: 6px solid #3498db;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 10px auto 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .hidden {
            display: none;
        }
        #preview {
            margin-top: 10px;
            max-width: 300px;
            max-height: 300px;
            border: 1px solid #ddd;
            display: none;
        }
    </style>
</head>
<body>
    <img src="/img/nutriscan.jpg" width="220" alt="Etiqueta del Producto" style="display: block; margin: 0 auto;">
    <p class="subheader-font">¡Hola! Soy NutriScan, tu asistente IA. Carga una foto de la etiqueta de ingredientes de tu alimento e indícame si tienes alguna condición alimenticia. Yo identificaré si ese alimento es perjudicial para tu salud.</p>
    <form id="analysis-form" method="post" enctype="multipart/form-data">
        <div class="file-input">
            <label for="image" class="file-label">Sube una imagen de la etiqueta del producto:</label><br>
            <input type="file" id="image" name="image" onchange="showPreview(event)"><br><br>
            <img id="preview" alt="Vista previa de la imagen">
        </div>
        <label for="condition">Ingresa cualquier condición de salud o restricción dietética (opcional):</label><br>
        <input type="text" id="condition" name="condition"><br><br>
        <input type="submit" value="Analizar Etiqueta">
    </form>
    <div id="loader" class="loader hidden"></div>
    <p id="loading-text" class="hidden">Cargando Respuesta...</p>
    <div id="result" class="response hidden">
        <h2>Análisis de Ingredientes Según la Condición Ingresada:</h2>
        <p id="analisis_ingredientes"></p>
        <div class="audio-output hidden" id="audio-output">
            <h2>Audio del Producto:</h2>
            <audio controls id="audio" autoplay></audio>
        </div>
    </div>
    <script>
        function showLoader() {
            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('loading-text').classList.remove('hidden');
        }

        function hideLoader() {
            document.getElementById('loader').classList.add('hidden');
            document.getElementById('loading-text').classList.add('hidden');
        }

        function showResult() {
            document.getElementById('result').classList.remove('hidden');
        }

        function setAudioSource(source) {
            const audioElement = document.getElementById('audio');
            audioElement.src = source;
            document.getElementById('audio-output').classList.remove('hidden');
        }

        function showPreview(event) {
            const [file] = event.target.files;
            if (file) {
                const preview = document.getElementById('preview');
                preview.src = URL.createObjectURL(file);
                preview.style.display = 'block';
            }
        }

        document.getElementById('analysis-form').addEventListener('submit', function(event) {
            event.preventDefault();
            showLoader();

            const formData = new FormData(event.target);

            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                hideLoader();
                displayText(data.analisis_ingredientes, 6); // Aumenta la velocidad a 25ms por letra
                showResult();

                // Solicitar el audio después de mostrar el análisis
                fetch('/generate_audio', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ texto_para_audio: data.analisis_ingredientes })
                })
                .then(response => response.json())
                .then(audioData => {
                    if (audioData.audio_url) {
                        setAudioSource(audioData.audio_url);
                    }
                });
            });
        });

        function displayText(text, speed) {
            const element = document.getElementById('analisis_ingredientes');
            let index = 0;
            element.innerHTML = '';
            function type() {
                if (index < text.length) {
                    element.innerHTML += text[index];
                    index++;
                    setTimeout(type, speed);
                }
            }
            type();
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template)

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_file = request.files.get("image")
    user_condition = request.form.get("condition")

    if uploaded_file:
        # Codificar la imagen
        image_data = encode_image(uploaded_file)
        image_url = f"data:image/jpeg;base64,{image_data}"

        # Crear el cliente de OpenAI
        client = OpenAI(api_key=api_key)

        # Enviar la solicitud al modelo
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Por favor, identifica si hay algún ingrediente en la imagen de la etiqueta que sea perjudicial para una persona con la siguiente condición: {user_condition}. Muestra solo el análisis relevante y no transcribas todos los ingredientes."},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ],
                }
            ],
            max_tokens=1500,
        )

        # Extraer el análisis de ingredientes
        analisis_ingredientes = response.choices[0].message.content

        return jsonify({"analisis_ingredientes": analisis_ingredientes})

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.get_json()
    texto_para_audio = data.get('texto_para_audio')

    if texto_para_audio:
        audio_content, error = tts(texto_para_audio)
        if audio_content:
            audio_url = get_audio_file_content(audio_content)
            return jsonify({"audio_url": audio_url})
    return jsonify({"audio_url": None})

if __name__ == '__main__':
    app.run(debug=True)
