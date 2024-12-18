from flask import Flask, request, jsonify
import whisper
import torch
import os
import hashlib
from datetime import datetime

# Crear una instancia de Flask para iniciar la aplicación web.
app = Flask(__name__)

# Verificar si una GPU está disponible utilizando PyTorch.
# Si está disponible, se usará "cuda" (GPU); de lo contrario, se usará "cpu".
device = "cuda" if torch.cuda.is_available() else "cpu"
# Informar al usuario sobre el dispositivo seleccionado.
print(f"Dispositivo utilizado para la ejecución: {device}")

# Cargar el modelo Whisper en el dispositivo especificado.
# Whisper es un modelo de transcripción de voz a texto desarrollado por OpenAI.
model = whisper.load_model("turbo", device=device)

# Crear un directorio temporal para almacenar archivos de audio subidos por los usuarios.
# Si el directorio no existe, lo creará automáticamente.
temp_dir = "uploaded_audios"
os.makedirs(temp_dir, exist_ok=True)

# Definir una ruta para el endpoint raíz ('/') que muestra un mensaje simple.


@app.route('/')
def home():
    # Responde con un mensaje indicando que el servicio está funcionando.
    return "transcribe_service is mounted"

# Definir el endpoint para transcribir archivos de audio.
# Este endpoint acepta solicitudes POST en la ruta "/transcribe".


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """
    Endpoint para transcribir un archivo de audio enviado por el usuario.
    """
    # Verificar si la solicitud contiene un archivo con la clave "file".
    if "file" not in request.files:
        # Responder con un error 400 si no se proporciona un archivo.
        return jsonify({"error": "No se encontró un archivo en la solicitud"}), 400

    # Obtener el archivo subido.
    file = request.files["file"]

    # Verificar que el archivo subido sea un archivo MP3 o M4A.
    if not (file.filename.endswith(".mp3") or file.filename.endswith(".m4a")):
        # Responder con un error 400 si el archivo no es del formato esperado.
        return jsonify({"error": "Solo se aceptan archivos .mp3 o .m4a"}), 400

    try:
        # Generar un nombre de archivo único concatenando la fecha, hora y un hash.
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_hash = hashlib.md5(
            (file.filename + timestamp).encode()).hexdigest()
        unique_filename = f"{os.path.splitext(file.filename)[0]}_{timestamp}_{unique_hash}{os.path.splitext(file.filename)[1]}"

        # Guardar el archivo en el directorio temporal con el nombre único generado.
        file_path = os.path.join(temp_dir, unique_filename)
        file.save(file_path)

        # Utilizar el modelo Whisper para transcribir el archivo de audio.
        # El método transcribe devuelve un diccionario con el texto y otros datos.
        result = model.transcribe(file_path)
        # Extraer solo el texto de la transcripción.
        transcription_text = result["text"]

        # Guardar la transcripción en un archivo de texto con el nombre único generado.
        output_filename = file_path.replace(
            os.path.splitext(file.filename)[1], "_transcription.txt")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(transcription_text)

        # Eliminar el archivo de audio original después de procesarlo para liberar espacio.
        os.remove(file_path)

        # Responder al usuario con la transcripción en formato JSON.
        return jsonify({"transcription": transcription_text})

    except Exception as e:
        # Capturar cualquier error durante el procesamiento y devolver un error 500.
        return jsonify({"error": f"Error al procesar el archivo: {str(e)}"}), 500


# Ejecutar la aplicación Flask si este archivo se ejecuta como un script principal.
if __name__ == "__main__":
    # La aplicación escuchará en la dirección IP y puerto especificados.
    app.run(host="26.164.147.61", port=5000, debug=True)
