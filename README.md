# Configuración del Entorno Virtual y Dependencias

Este archivo proporciona instrucciones para configurar un entorno virtual y gestionar las dependencias necesarias.

## Requisitos Previos

1. **Python 3.11** instalado en tu sistema.
2. **NVIDIA CUDA 12.4** instalado en tu sistema.
3. **Pip** actualizado:

   ```bash
   python -m pip install --upgrade pip
   ```

## Configuración del Entorno Virtual

1. Crear un entorno virtual:

   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual:
   - **Windows**:

     ```bash
     venv\Scripts\activate

     source venv/Scripts/activate #Si se usa Git Bash
     ```

   - **Linux/Mac**:

     ```bash
     source venv/bin/activate
     ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Instalación de PyTorch

Dado que PyTorch tiene requisitos específicos según el sistema operativo, versión de Python y soporte de hardware (CPU o GPU), es necesario instalarlo por separado. Sigue estos pasos:

1. Ve a la página oficial de instalación de PyTorch: [https://pytorch.org](https://pytorch.org).
2. Selecciona las siguientes opciones según tu sistema:
   - **PyTorch Build:** Stable
   - **Sistema Operativo:** Linux/Windows/Mac
   - **Paquete:** Pip
   - **Lenguaje:** Python
   - **Compute Platform:** 12.4 o CPU si no tienes GPU
3. Copia el comando generado en la página. Por ejemplo:
   - Para **CUDA 12.4**:

     ```bash
     pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
     ```

   - Para **CPU**:

     ```bash
     pip3 install torch torchvision torchaudio
     ```

4. Ejecuta el comando en tu terminal.

## Instalación de Whisper

Ejecuta los siguientes comandos uno detrás de otro:

   ```bash
   winget install ffmpeg # En el Símbolo del sistema o Git Bash dedicado
   ```

   ```bash
   pip install -U openai-whisper
   ```

   ```bash
   pip install git+https://github.com/openai/whisper.git 
   ```

   ```bash
   pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git 
   ```

También puedes realizar la instalación siguiendo los pasos del archivo README en: [https://github.com/openai/whisper](https://github.com/openai/whisper).
