import requests

# URL del endpoint del microservicio Flask
url = "http://26.164.147.61:8000/process_audio"

# Datos que quieres enviar al microservicio
file_path = "C:/Users/gevas/Desktop/proyectoIA/Audios/AudiosIA/Dialogo24.mp3"

# Abrir el archivo en modo binario y enviarlo en la solicitud
with open(file_path, 'rb') as file:
    # Nombre del campo debe coincidir con el usado en Flask
    files = {'file': file}
    try:
        # Realiza una solicitud POST para enviar el archivo
        response = requests.post(url, files=files)

        # Verifica el código de estado de la respuesta
        if response.status_code == 200:
            print("Respuesta del servidor:", response.json())
        else:
            print(f"Error: {response.status_code}, Detalle: {response.text}")
    except requests.RequestException as e:
        print("Error al conectarse con el microservicio:", e)
