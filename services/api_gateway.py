from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Crear la aplicación Flask para el API Gateway
app = Flask(__name__)
CORS(app)

# Configuración de los microservicios
TRANSCRIPTION_SERVICE_URL = "http://26.164.147.61:5000/transcribe"
FORM_SERVICE_URL = "http://26.164.147.61:5001/process_text"


@app.route('/')
def home():
    return "API Gateway is running"


@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Endpoint principal del API Gateway para procesar un archivo de audio y generar un formulario.
    """
    # Verificar si se incluye un archivo en la solicitud
    if "file" not in request.files:
        return jsonify({"error": "No se encontró un archivo en la solicitud"}), 400

    file = request.files["file"]

    # Verificar formato del archivo
    # if not (file.filename.endswith(".mp3") or file.filename.endswith(".m4a")):
    #     return jsonify({"error": "Solo se aceptan archivos .mp3 o .m4a"}), 400

    try:
        # Paso 1: Enviar el archivo al servicio de transcripción
        files = {"file": (file.filename, file.stream, file.content_type)}
        transcription_response = requests.post(
            TRANSCRIPTION_SERVICE_URL, files=files)

        if transcription_response.status_code != 200:
            return jsonify({"error": "Error en el servicio de transcripción",
                            "details": transcription_response.json()}), 500

        transcription_data = transcription_response.json()
        transcription_text = transcription_data.get("transcription")

        if not transcription_text:
            return jsonify({"error": "El servicio de transcripción no devolvió datos válidos"}), 500

        # Paso 2: Enviar la transcripción al servicio de generación de formularios
        form_response = requests.post(FORM_SERVICE_URL, json={
                                      "transcription": transcription_text})

        if form_response.status_code != 200:
            return jsonify({"error": "Error en el servicio de formularios",
                            "details": form_response.json()}), 500

        form_data = form_response.json()

        # Devolver ambos resultados al cliente
        return jsonify({
            "transcription": transcription_text,
            "form_data": form_data
        })

    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {str(e)}"}), 500


if __name__ == "__main__":
    # Configurar host y puerto para el API Gateway
    app.run(host="26.164.147.61", port=8000, debug=True)
