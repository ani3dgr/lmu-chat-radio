# -*- coding: utf-8 -*-
"""
Hace el .exe de LMU Chat Radio y el ZIP que se reparte.

    python compilar.py

Sale en dist/LMUChatRadio/ y dist/LMUChatRadio-<VERSION>.zip.

El modelo de voz (unos 500 MB) NO va dentro: el programa lo baja la primera
vez a su carpeta "modelo". Tampoco van la configuracion ni el registro de nadie.
Como con el mapa, lo que el usuario tiene en dist/LMUChatRadio (su modelo y su
configuracion) se aparta antes de borrar y se devuelve al terminar.
"""
import os
import shutil
import subprocess
import sys
import zipfile

VERSION = "1.1"
NOMBRE = "LMUChatRadio"
AQUI = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(AQUI, "dist")
DESTINO = os.path.join(DIST, NOMBRE)
APARTADO = os.path.join(AQUI, "_apartado")
MIO = ["modelo", "chat_config.json", "chat_registro.txt"]

LEEME = """LMU CHAT RADIO {v}
=================

EN - Talk to the Le Mans Ultimate chat with a button on your wheel, and hear
     what others write, translated into your language.
     1. Unzip this folder anywhere (not inside Program Files).
     2. Run LMUChatRadio.exe. The first time it downloads the speech
        recognition model (about 500 MB). Wait until it says "Ready".
     3. Click "Instructions" in the window. That's all.
     To update: unzip the new version on top of this folder. Your settings
     and the downloaded model are kept.

ES - Habla al chat de Le Mans Ultimate con un boton del volante y escucha lo
     que escriben los demas, traducido a tu idioma.
     1. Descomprime esta carpeta donde quieras (fuera de Archivos de programa).
     2. Abre LMUChatRadio.exe. La primera vez descarga el reconocimiento de
        voz (unos 500 MB). Espera a que diga "Listo".
     3. Pulsa "Instrucciones" en la ventana. Nada mas.
     Para actualizar: descomprime la version nueva encima de esta carpeta. Tu
     configuracion y el modelo descargado se conservan.

Free / Gratis - https://github.com/ani3dgr/lmu-chat-radio
"""


def comprobar_cerrado():
    salida = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {NOMBRE}.exe"],
                            capture_output=True, text=True).stdout
    if f"{NOMBRE}.exe" in salida:
        sys.exit(f"{NOMBRE}.exe esta abierto: cierralo antes de compilar.")


def apartar_lo_mio():
    shutil.rmtree(APARTADO, ignore_errors=True)
    os.makedirs(APARTADO)
    for n in MIO:
        origen = os.path.join(DESTINO, n)
        if os.path.exists(origen):
            shutil.move(origen, os.path.join(APARTADO, n))


def devolver_lo_mio():
    for n in MIO:
        origen = os.path.join(APARTADO, n)
        if os.path.exists(origen):
            shutil.move(origen, os.path.join(DESTINO, n))
    shutil.rmtree(APARTADO, ignore_errors=True)


def compilar():
    orden = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
             "--name", NOMBRE, "--distpath", DIST, "--workpath", os.path.join(AQUI, "build"),
             "--specpath", AQUI,
             "--collect-all", "faster_whisper", "--collect-all", "ctranslate2",
             "--collect-all", "onnxruntime", "--collect-all", "tokenizers",
             "--collect-all", "edge_tts", "--collect-data", "certifi",
             "--collect-all", "sounddevice", "--hidden-import", "_sounddevice_data",
             "--hidden-import", "win32com.client", "--hidden-import", "pygame._sdl2.audio", "--hidden-import", "pygame.sndarray",
             "--exclude-module", "torch", "--exclude-module", "matplotlib",
             "--exclude-module", "scipy", "--exclude-module", "pandas",
             # no hacen falta y pesan: "av" (video, 50 MB; ver cargar_whisper), imagenes, y el
             # acelerador de descargas de Hugging Face (sin el baja igual, por HTTP normal)
             "--exclude-module", "av", "--exclude-module", "PIL", "--exclude-module", "hf_xet",
             os.path.join(AQUI, "chat_lmu.py")]
    subprocess.run(orden, check=True)


def empaquetar():
    with open(os.path.join(DESTINO, "LEEME - README.txt"), "w", encoding="utf-8") as f:
        f.write(LEEME.format(v=VERSION))
    zip_ruta = os.path.join(DIST, f"{NOMBRE}-{VERSION}.zip")
    if os.path.exists(zip_ruta):
        os.remove(zip_ruta)
    with zipfile.ZipFile(zip_ruta, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for raiz, _, archivos in os.walk(DESTINO):
            for a in archivos:
                ruta = os.path.join(raiz, a)
                z.write(ruta, os.path.join(NOMBRE, os.path.relpath(ruta, DESTINO)))
    print(f"\nZIP: {zip_ruta}  ({os.path.getsize(zip_ruta) / 1e6:.1f} MB)")


if __name__ == "__main__":
    comprobar_cerrado()
    apartar_lo_mio()
    try:
        shutil.rmtree(DESTINO, ignore_errors=True)
        compilar()
        empaquetar()   # antes de devolver lo suyo, para que no se cuele en el ZIP
    finally:
        os.makedirs(DESTINO, exist_ok=True)
        devolver_lo_mio()
