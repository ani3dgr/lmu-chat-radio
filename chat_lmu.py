# -*- coding: utf-8 -*-
"""
LMU CHAT RADIO - hablar y escuchar el chat de Le Mans Ultimate sin soltar el volante.

ESCRIBIR: pulsas tu boton (del volante o del teclado), hablas, y lo vuelves a
pulsar. El programa te repite en voz alta lo que ha entendido y, si en los
segundos de espera pulsas otra vez, lo manda al chat (traducido al ingles si
quieres). Si no pulsas, dice "mensaje no enviado" y no manda nada.

    "Dile al coche 33 que lo siento por el toque"
        -> en el chat:  #33 Tristan Joulia: sorry for the touch

LEER: los mensajes que escriben los demas te los dice en voz alta, traducidos
a tu idioma si quieres.

COMO HABLA CON EL JUEGO: por el servidor web que LMU levanta en tu propio
ordenador (127.0.0.1:6397), el mismo que usa su interfaz. Es la ruta
/rest/chat/: GET devuelve los mensajes y POST con texto plano los envia. No se
simulan teclas, asi que da igual que el juego este en pantalla completa.

La voz se pasa a texto EN TU ORDENADOR (Whisper, sin internet). Las
traducciones y la voz que habla si usan internet; sin internet habla con la
voz de Windows y manda el mensaje sin traducir.
"""
import asyncio
import ctypes
import json
import os
import queue
import re
import sys
import tempfile
import threading
import time
import traceback
import urllib.parse
import urllib.request
import winsound

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

CARPETA = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
CONFIG = os.path.join(CARPETA, "chat_config.json")
REGISTRO = os.path.join(CARPETA, "chat_registro.txt")
MODELO = os.path.join(CARPETA, "modelo")
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"   # sin consola, la barra de progreso no tiene donde escribir
if sys.stdout is None:   # el .exe y pythonw arrancan sin consola: que nadie se caiga por escribir en ella
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
API = "http://127.0.0.1:6397/rest/"   # 127.0.0.1 y no localhost: localhost va primero a IPv6 y el juego no escucha ahi
FRECUENCIA = 16000
MAX_GRABACION = 20   # segundos; por si se queda grabando sin querer

POR_DEFECTO = {
    "idioma": "es",
    "boton": None,              # {"tipo": "volante", "dispositivo": ..., "boton": n} o {"tipo": "teclado", "vk": n, "nombre": ...}
    "espera_confirmar": 5,
    "traducir_mios": True,      # lo que dicto yo, al ingles
    "leer_chat": True,
    "traducir_chat": True,      # lo que llega, a mi idioma
    "microfono": "",            # "" = el de Windows
    "salida_voz": "",           # "" = la de Windows
    "modo_prueba": True,        # no manda nada al chat: solo lo dice
    "quien": "ambos",           # al leer: "nombre", "numero" o "ambos"
}

IDIOMAS = [("es", "Español"), ("en", "English"), ("fr", "Français"), ("it", "Italiano"),
           ("de", "Deutsch"), ("pl", "Polski"), ("pt", "Português")]

VOCES = {"es": "es-ES-AlvaroNeural", "en": "en-GB-RyanNeural", "fr": "fr-FR-HenriNeural",
         "it": "it-IT-DiegoNeural", "de": "de-DE-ConradNeural", "pl": "pl-PL-MarekNeural",
         "pt": "pt-PT-DuarteNeural"}

# Lo que dice el programa en voz alta, en cada idioma.
FRASES = {
    "es": {"numero": "El {n} de {c}", "ambos": "{q}, el {n} de {c}",
           "listo": "Chat preparado", "para": "Para el {n}: {m}", "todos": "A todos: {m}",
           "enviado": "Enviado", "no_enviado": "Mensaje no enviado", "no_entendido": "No te he entendido",
           "dice": "{q} dice: {m}", "para_ti": "Para ti. ", "fallo": "No he podido enviarlo, el juego no contesta",
           "prueba": "Modo prueba, no se ha enviado"},
    "en": {"numero": "Car {n}, {c}", "ambos": "{q}, car {n}, {c}",
           "listo": "Chat ready", "para": "To car {n}: {m}", "todos": "To everyone: {m}",
           "enviado": "Sent", "no_enviado": "Message not sent", "no_entendido": "I didn't understand you",
           "dice": "{q} says: {m}", "para_ti": "For you. ", "fallo": "Could not send it, the game is not answering",
           "prueba": "Test mode, nothing was sent"},
    "fr": {"numero": "La {n} en {c}", "ambos": "{q}, la {n} en {c}",
           "listo": "Chat prêt", "para": "Pour la {n} : {m}", "todos": "À tous : {m}",
           "enviado": "Envoyé", "no_enviado": "Message non envoyé", "no_entendido": "Je n'ai pas compris",
           "dice": "{q} dit : {m}", "para_ti": "Pour toi. ", "fallo": "Envoi impossible, le jeu ne répond pas",
           "prueba": "Mode test, rien n'a été envoyé"},
    "it": {"numero": "La {n} in {c}", "ambos": "{q}, la {n} in {c}",
           "listo": "Chat pronta", "para": "Per la {n}: {m}", "todos": "A tutti: {m}",
           "enviado": "Inviato", "no_enviado": "Messaggio non inviato", "no_entendido": "Non ho capito",
           "dice": "{q} dice: {m}", "para_ti": "Per te. ", "fallo": "Invio non riuscito, il gioco non risponde",
           "prueba": "Modalità prova, non è stato inviato"},
    "de": {"numero": "Nummer {n}, {c}", "ambos": "{q}, Nummer {n}, {c}",
           "listo": "Chat bereit", "para": "An Nummer {n}: {m}", "todos": "An alle: {m}",
           "enviado": "Gesendet", "no_enviado": "Nachricht nicht gesendet", "no_entendido": "Ich habe dich nicht verstanden",
           "dice": "{q} sagt: {m}", "para_ti": "Für dich. ", "fallo": "Senden fehlgeschlagen, das Spiel antwortet nicht",
           "prueba": "Testmodus, nichts gesendet"},
    "pl": {"numero": "Numer {n}, {c}", "ambos": "{q}, numer {n}, {c}",
           "listo": "Czat gotowy", "para": "Do numeru {n}: {m}", "todos": "Do wszystkich: {m}",
           "enviado": "Wysłano", "no_enviado": "Wiadomość nie wysłana", "no_entendido": "Nie zrozumiałem",
           "dice": "{q} pisze: {m}", "para_ti": "Do ciebie. ", "fallo": "Nie udało się wysłać, gra nie odpowiada",
           "prueba": "Tryb testowy, nic nie wysłano"},
    "pt": {"numero": "O {n} de {c}", "ambos": "{q}, o {n} de {c}",
           "listo": "Chat pronto", "para": "Para o {n}: {m}", "todos": "Para todos: {m}",
           "enviado": "Enviado", "no_enviado": "Mensagem não enviada", "no_entendido": "Não percebi",
           "dice": "{q} diz: {m}", "para_ti": "Para ti. ", "fallo": "Não consegui enviar, o jogo não responde",
           "prueba": "Modo de teste, nada foi enviado"},
}

# Para que Whisper escriba los numeros con cifras y sepa de que va la cosa.
PISTA_WHISPER = {
    "es": "Dile al coche 33 que lo siento por el toque. Escribe buena carrera a todos.",
    "en": "Tell car 33 sorry for the contact. Write good race everyone.",
    "fr": "Dis à la voiture 33 désolé pour le contact. Écris bonne course à tous.",
    "it": "Di alla macchina 33 scusa per il contatto. Scrivi buona gara a tutti.",
    "de": "Sag Auto 33 sorry für den Kontakt. Schreib gutes Rennen an alle.",
    "pl": "Powiedz samochodowi 33 przepraszam za kontakt. Napisz dobrego wyścigu wszystkim.",
    "pt": "Diz ao carro 33 desculpa pelo toque. Escreve boa corrida a todos.",
}

# Frases que Whisper se inventa cuando solo oye ruido.
ALUCINACIONES = ("amara.org", "subtítulos", "subtitulos", "gracias por ver", "thanks for watching",
                 "suscríbete", "subscribe", "sous-titres", "untertitel")

# ---------------------------------------------------------------- textos de la ventana
sys.path.insert(0, CARPETA)
from textos import TEXTOS, INSTRUCCIONES, PAYPAL, CICLOTRACKER   # noqa: E402


def tx(cfg, clave):
    return TEXTOS.get(cfg["idioma"], {}).get(clave) or TEXTOS["en"].get(clave) or TEXTOS["es"].get(clave, clave)


def frase(cfg, clave, **kw):
    return FRASES.get(cfg["idioma"], FRASES["en"])[clave].format(**kw)


def anotar(texto):
    try:
        with open(REGISTRO, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + texto + "\n")
    except Exception:
        pass


def idioma_windows():
    """El idioma de Windows, si es uno de los nuestros; si no, ingles."""
    try:
        import locale
        codigo = locale.windows_locale.get(ctypes.windll.kernel32.GetUserDefaultUILanguage(), "en")[:2]
        return codigo if codigo in dict(IDIOMAS) else "en"
    except Exception:
        return "en"


def cargar_config():
    cfg = dict(POR_DEFECTO)
    cfg["idioma"] = idioma_windows()
    try:
        with open(CONFIG, encoding="utf-8-sig") as f:   # por si lo guarda otro programa con BOM
            cfg.update(json.load(f))
    except Exception:
        pass
    return cfg


def guardar_config(cfg):
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- el juego
def api_get(ruta, espera=3):
    with urllib.request.urlopen(API + ruta, timeout=espera) as r:
        return json.loads(r.read().decode("utf-8-sig"))   # el juego pone BOM delante


def api_enviar_chat(texto):
    req = urllib.request.Request(API + "chat/", data=texto.encode("utf-8"), method="POST",
                                 headers={"Content-Type": "text/plain; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=3) as r:
        return r.status == 200


def coches():
    """[(numero, piloto, soy_yo, clase)] de la lista del juego."""
    try:
        return [(str(c.get("carNumber", "")), c.get("driverName", ""), bool(c.get("player")), c.get("carClass", ""))
                for c in api_get("watch/standings")]
    except Exception:
        return []


def _limpio(nombre):
    return re.sub(r"[^\w\s]", "", nombre.lower()).split()


def coche_de(quien, lista):
    """El coche de quien escribe. En el chat el juego acorta el nombre ("G To'th")
    y en la lista va entero ("Gergo To'th"): se busca igual, y si no, por inicial
    y apellido. Si hay dudas (dos que encajan), no se adivina."""
    partes = _limpio(quien)
    if not partes:
        return None
    iguales = [c for c in lista if _limpio(c[1]) == partes]
    if len(iguales) == 1:
        return iguales[0]
    apellido, inicial = partes[-1], partes[0][0]
    casi = [c for c in lista if _limpio(c[1]) and _limpio(c[1])[-1] == apellido
            and (len(partes) == 1 or _limpio(c[1])[0][0] == inicial)]
    return casi[0] if len(casi) == 1 else None


CLASES = {"Hyper": "Hypercar", "LMGT3": "GT3"}


# ---------------------------------------------------------------- reconocimiento de voz
def cargar_whisper():
    """faster_whisper importa "av" (una libreria de video de 50 MB) solo para leer
    archivos de audio. Aqui le pasamos el sonido ya en memoria, asi que el .exe no
    la lleva y se le da una vacia para que el import no se caiga."""
    try:
        import av  # noqa: F401
    except ImportError:
        import types
        sys.modules["av"] = types.ModuleType("av")
    from faster_whisper import WhisperModel
    return WhisperModel


def autoprueba():
    """LMUChatRadio.exe --autoprueba : la voz de Windows dice una frase, el
    reconocedor la escucha y se traduce. El resultado va a chat_registro.txt.
    Sirve para comprobar el .exe sin microfono."""
    import wave
    import numpy as np
    import win32com.client
    try:
        anotar(f"autoprueba: juego -> {len(coches())} coches, {len(api_get('chat/'))} mensajes en el chat")
    except Exception as e:
        anotar(f"autoprueba: juego no contesta: {e!r}")
    wav = os.path.join(tempfile.gettempdir(), "lmu_chat_radio_prueba.wav")
    flujo = win32com.client.Dispatch("SAPI.SpFileStream")
    formato = win32com.client.Dispatch("SAPI.SpAudioFormat")
    formato.Type = 18   # 16 kHz, 16 bits, mono
    flujo.Format = formato
    flujo.Open(wav, 3)
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    sapi.AudioOutputStream = flujo
    sapi.Speak("Tell car 33 sorry for the contact")
    flujo.Close()
    with wave.open(wav) as w:
        audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    t0 = time.time()
    modelo = cargar_whisper()("small", device="cpu", compute_type="int8", download_root=MODELO)
    t1 = time.time()
    segs, _ = modelo.transcribe(audio, language="en", vad_filter=True, initial_prompt=PISTA_WHISPER["en"])
    texto = " ".join(x.text.strip() for x in segs).strip()
    anotar(f"autoprueba: carga {t1 - t0:.1f}s, oido {texto!r} en {time.time() - t1:.1f}s, "
           f"entendido {entender(texto)!r}, traducido {traducir(entender(texto)[1], 'es', 'en')!r}")


# ---------------------------------------------------------------- traducir
def traducir(texto, destino, origen="auto"):
    """Devuelve (traduccion, idioma_detectado). Si falla, (None, None)."""
    try:
        url = ("https://translate.googleapis.com/translate_a/single?client=gtx&dt=t"
               f"&sl={origen}&tl={destino}&q=" + urllib.parse.quote(texto))
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as r:
            datos = json.loads(r.read().decode("utf-8"))
        return "".join(p[0] for p in datos[0] if p and p[0]).strip(), datos[2]
    except Exception as e:
        anotar(f"traducir fallo: {e}")
        return None, None


# ---------------------------------------------------------------- entender la orden
ORDEN = (r"(?:d[ií]le|d[ií]|escr[ií]bele|escribe|pon|tell|say|write|type|message|dis|[ée]cris|d[ìi]'?|"
         r"scrivi|sag|sage|schreib|schreibe|powiedz|napisz|diz|diga|escreve|escreva)")
COCHE = (r"(?:coche|auto|carro|car|voiture|macchina|vettura|wagen|fahrzeug|samoch[oó]d\w*|"
         r"n[úu]mero|number|nummer|num[ée]ro|numer)")
ENLACE = r"(?:al|a\s+la|a\s+el|a|el|to|au|[àa]\s+la|[àa]|alla|al|dem|an|der|do|ao|para|for)"
QUE = r"(?:que|that|qu'|che|dass|że|ze)"

RE_CON_COCHE = re.compile(
    rf"^\s*(?:{ORDEN}\b[\s,]*)?(?:{ENLACE}\s+)*(?P<palabra>{COCHE}\s+)?(?:{COCHE}\s+)?#?(?P<n>\d{{1,3}})\b"
    rf"[\s,.:;-]*(?:{QUE}\b)?[\s,:]*(?P<m>.+)$", re.I | re.S)
RE_SIN_COCHE = re.compile(
    rf"^\s*{ORDEN}\b[\s,:]*(?:(?:en\s+el|in\s+(?:the\s+)?|dans\s+le|nella|im|w|no)\s*chat\b)?[\s,:]*"
    rf"(?:(?:a\s+todos|para\s+todos|to\s+(?:everyone|everybody|all)|[àa]\s+tous|a\s+tutti|an\s+alle|"
    rf"do\s+wszystkich)\b)?[\s,:]*(?:{QUE}\b)?[\s,:]*(?P<m>.+)$", re.I | re.S)


def entender(texto):
    """'Dile al coche 33 que lo siento' -> ('33', 'lo siento'). Sin coche -> (None, mensaje)."""
    m = RE_CON_COCHE.match(texto)
    if m and (m.group("palabra") or re.match(rf"^\s*{ORDEN}\b", texto, re.I)):
        resto = m.group("m").strip()
        if resto:
            return m.group("n").lstrip("0") or "0", resto[0].upper() + resto[1:]
    m = RE_SIN_COCHE.match(texto)
    if m and m.group("m").strip():
        resto = m.group("m").strip()
        return None, resto[0].upper() + resto[1:]
    return None, texto.strip()


# ---------------------------------------------------------------- la voz que habla
class Voz:
    """Habla en un hilo propio. Lo del sistema (repetir tu mensaje, 'enviado') pasa
    siempre primero; los mensajes del chat esperan mientras estas grabando o confirmando."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.sistema = queue.Queue()
        self.chat = queue.Queue()
        self.pausado = threading.Event()
        self.parar = threading.Event()
        self.cambiar_salida = threading.Event()
        self.hablando = False
        threading.Thread(target=self._bucle, daemon=True).start()

    def decir(self, texto, idioma=None, sistema=True):
        hecho = threading.Event()
        (self.sistema if sistema else self.chat).put((texto, idioma or self.cfg["idioma"], hecho))
        return hecho

    def callar(self):
        self.parar.set()

    def _mixer(self, pygame):
        try:
            pygame.mixer.quit()
            pygame.mixer.init(devicename=self.cfg["salida_voz"] or None)
        except Exception:
            pygame.mixer.init()

    def _bucle(self):
        import pygame
        self._mixer(pygame)
        while True:
            try:
                item = self.sistema.get_nowait()
            except queue.Empty:
                item = None
                if not self.pausado.is_set():
                    try:
                        item = self.chat.get_nowait()
                    except queue.Empty:
                        pass
            if item is None:
                time.sleep(0.05)
                continue
            if self.cambiar_salida.is_set():
                self.cambiar_salida.clear()
                self._mixer(pygame)
            texto, idioma, hecho = item
            self.parar.clear()
            self.hablando = True
            try:
                self._hablar(pygame, texto, idioma)
            except Exception:
                anotar("voz: " + traceback.format_exc())
            self.hablando = False
            hecho.set()

    def _hablar(self, pygame, texto, idioma):
        mp3 = os.path.join(tempfile.gettempdir(), "chat_lmu_voz.mp3")
        try:
            import edge_tts
            pygame.mixer.music.unload()

            async def generar():
                await edge_tts.Communicate(texto, VOCES.get(idioma, VOCES["en"]), rate="+8%").save(mp3)
            asyncio.run(generar())
        except Exception:
            # sin internet: la voz de Windows
            import win32com.client
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            primario = {"es": 0x0A, "en": 0x09, "fr": 0x0C, "it": 0x10, "de": 0x07, "pl": 0x15, "pt": 0x16}
            for v in sapi.GetVoices():
                try:   # Language viene en hexadecimal ("C0A" = es-ES); el idioma son los 10 bits bajos
                    if int(v.GetAttribute("Language").split(";")[0], 16) & 0x3FF == primario.get(idioma):
                        sapi.Voice = v
                        break
                except Exception:
                    pass
            sapi.Speak(texto, 1)   # asincrono, para poder cortarla
            while not sapi.WaitUntilDone(100):
                if self.parar.is_set():
                    sapi.Speak("", 2)
                    return
            return
        if self.parar.is_set():
            return
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if self.parar.is_set():
                pygame.mixer.music.stop()
                break
            time.sleep(0.05)


# ---------------------------------------------------------------- botones
user32 = ctypes.windll.user32
TECLAS_RATON = {0x01, 0x02, 0x04, 0x05, 0x06}


def nombre_tecla(vk):
    sc = user32.MapVirtualKeyW(vk, 0)
    if vk in (0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2D, 0x2E, 0x6F, 0x90, 0xA3, 0xA5):
        sc |= 0x100   # teclas extendidas (flechas, Ins, Supr...)
    buf = ctypes.create_unicode_buffer(64)
    if user32.GetKeyNameTextW(sc << 16, buf, 64):
        return buf.value
    return f"VK {vk}"


def tecla_pulsada(vk):
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


class Entrada:
    """Vigila el boton elegido (volante o teclado) en su propio hilo. Tambien sirve
    para capturar uno nuevo desde la ventana."""

    def __init__(self, cfg, eventos):
        self.cfg = cfg
        self.eventos = eventos
        self.capturar = None    # funcion a la que avisar con el boton capturado
        threading.Thread(target=self._bucle, daemon=True).start()

    def _bucle(self):
        import pygame
        pygame.display.init()
        pygame.joystick.init()
        mandos, ult_busqueda, anterior = [], 0.0, False
        base_cap = None
        while True:
            try:
                if time.time() - ult_busqueda > 5:   # por si enchufan el volante despues
                    ult_busqueda = time.time()
                    if pygame.joystick.get_count() != len(mandos):
                        pygame.joystick.quit()
                        pygame.joystick.init()
                        mandos = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                        for j in mandos:
                            j.init()
                pygame.event.pump()

                if self.capturar:
                    estado = ({(j.get_name(), b) for j in mandos for b in range(j.get_numbuttons()) if j.get_button(b)},
                              {vk for vk in range(8, 255) if vk not in TECLAS_RATON and tecla_pulsada(vk)})
                    if base_cap is None:
                        base_cap = estado
                    nuevos_j = estado[0] - base_cap[0]
                    nuevas_t = estado[1] - base_cap[1] - {0x10, 0x11, 0x12}   # mejor la izquierda/derecha concreta
                    elegido = None
                    if nuevos_j:
                        nom, b = sorted(nuevos_j)[0]
                        elegido = {"tipo": "volante", "dispositivo": nom, "boton": b}
                    elif nuevas_t:
                        vk = sorted(nuevas_t)[0]
                        elegido = {"tipo": "teclado", "vk": vk, "nombre": nombre_tecla(vk)}
                    base_cap = (base_cap[0] & estado[0], base_cap[1] & estado[1])
                    if elegido:
                        aviso, self.capturar, base_cap = self.capturar, None, None
                        anterior = True   # que soltar ese mismo boton no cuente como pulsacion
                        aviso(elegido)
                    time.sleep(0.02)
                    continue

                actual = False
                b = self.cfg.get("boton")
                if b and b["tipo"] == "teclado":
                    actual = tecla_pulsada(b["vk"])
                elif b and b["tipo"] == "volante":
                    for j in mandos:
                        if j.get_name() == b["dispositivo"] and b["boton"] < j.get_numbuttons():
                            actual = bool(j.get_button(b["boton"]))
                            break
                if actual and not anterior:
                    self.eventos.put("boton")
                anterior = actual
            except Exception:
                anotar("entrada: " + traceback.format_exc())
                time.sleep(1)
            time.sleep(0.02)


# ---------------------------------------------------------------- el cerebro
class Chat:
    def __init__(self, cfg, avisar):
        self.cfg = cfg
        self.avisar = avisar          # avisar(tipo, texto) -> ventana
        self.eventos = queue.Queue()
        self.voz = Voz(cfg)
        self.entrada = Entrada(cfg, self.eventos)
        self.modelo = None
        self.mi_nombre = ""
        threading.Thread(target=self._cerebro, daemon=True).start()
        threading.Thread(target=self._lector, daemon=True).start()

    # ---------- lo que llega
    def _lector(self):
        vistos, primera, ult_nombre = set(), True, 0.0
        while True:
            try:
                if time.time() - ult_nombre > 10 or not self.mi_nombre:
                    ult_nombre = time.time()
                    self.mi_nombre = api_get("watch/sessionInfo").get("playerName", "") or self.mi_nombre
                mensajes = api_get("chat/")
                self.avisar("juego", True)
                nuevos = []
                for c in mensajes:
                    clave = (c.get("timestamp"), c.get("message"))
                    if clave not in vistos:
                        vistos.add(clave)
                        nuevos.append(c.get("message", ""))
                if primera:   # lo que ya habia al arrancar no se lee
                    primera = False
                    nuevos = []
                for m in nuevos:
                    self._llega(m)
            except Exception as e:
                if getattr(self, "_ult_fallo", None) != str(e):   # cada motivo distinto, una vez
                    self._ult_fallo = str(e)
                    anotar(f"juego no contesta: {e!r}")
                self.avisar("juego", False)
                time.sleep(2)
            time.sleep(1)

    def _llega(self, mensaje):
        if ":" not in mensaje:
            self.avisar("log", "· " + mensaje)   # avisos del servidor: se ensenan, no se leen
            return
        quien, texto = (s.strip() for s in mensaje.split(":", 1))
        if not texto or quien == self.mi_nombre:
            return
        idioma = self.cfg["idioma"]
        dicho = texto
        if self.cfg["traducir_chat"]:
            trad, detectado = traducir(texto, idioma)
            if trad and detectado != idioma:
                dicho = trad
        self.avisar("log", f"← {quien}: {texto}" + (f"  [{dicho}]" if dicho != texto else ""))
        if not self.cfg["leer_chat"]:
            return
        para_mi = ""
        mio = [c for c in coches() if c[2]]   # (se vuelve a pedir abajo; son milisegundos)
        if mio:
            num = mio[0][0]
            apellido = mio[0][1].split()[-1].lower() if mio[0][1] else ""
            if re.search(rf"(?<!\d)#?{re.escape(num)}(?!\d)", texto) or (len(apellido) >= 3 and apellido in texto.lower()):
                para_mi = frase(self.cfg, "para_ti")
        # quien habla: por nombre, por numero o las dos cosas (el nombre del chat va
        # recortado, "G To'th", y a veces se entiende mejor el numero)
        lista = coches()
        coche = coche_de(quien, lista)
        nombre = quien.replace("'", "")
        modo = self.cfg["quien"]
        if coche and modo != "nombre":
            clase = CLASES.get(coche[3], coche[3])
            nombre = frase(self.cfg, "numero" if modo == "numero" else "ambos", q=nombre, n=coche[0], c=clase)
        self.voz.decir(para_mi + frase(self.cfg, "dice", q=nombre, m=dicho), sistema=False)

    # ---------- lo que digo yo
    def _cerebro(self):
        # El modelo (unos 500 MB) no va en el ZIP: se baja la primera vez a la carpeta
        # "modelo", al lado del programa, y desde ahi se carga sin internet.
        ya_esta = any("model.bin" in f for _, _, fs in os.walk(MODELO) for f in fs)
        self.avisar("estado", "cargando" if ya_esta else "descargando")
        try:
            WhisperModel = cargar_whisper()
            self.modelo = WhisperModel("small", device="cpu", compute_type="int8", download_root=MODELO)
        except Exception:
            anotar("whisper: " + traceback.format_exc())
            self.avisar("estado", "error_whisper")
            return
        self.avisar("estado", "listo")
        self.voz.decir(frase(self.cfg, "listo"))
        while True:
            self.eventos.get()
            try:
                self._turno()
            except Exception:
                anotar("cerebro: " + traceback.format_exc())
            self.voz.pausado.clear()
            self.avisar("estado", "listo")
            while not self.eventos.empty():   # pulsaciones que llegaron mientras pensaba
                self.eventos.get_nowait()

    def _turno(self):
        import numpy as np
        import sounddevice as sd
        self.voz.pausado.set()
        self.voz.callar()
        trozos = []
        disp = None
        if self.cfg["microfono"]:
            for i, d in enumerate(sd.query_devices()):
                if d["max_input_channels"] > 0 and d["name"] == self.cfg["microfono"]:
                    disp = i
                    break
        flujo = sd.InputStream(samplerate=FRECUENCIA, channels=1, dtype="float32", device=disp,
                               callback=lambda datos, *a: trozos.append(datos.copy()))
        winsound.Beep(880, 120); winsound.Beep(1200, 150)
        flujo.start()
        self.avisar("estado", "grabando")
        try:
            self.eventos.get(timeout=MAX_GRABACION)
        except queue.Empty:
            pass
        flujo.stop(); flujo.close()
        winsound.Beep(440, 150)
        self.avisar("estado", "procesando")

        if not trozos or sum(len(t) for t in trozos) < FRECUENCIA * 0.4:
            return
        audio = np.concatenate(trozos)[:, 0]
        idioma = self.cfg["idioma"]
        segmentos, _ = self.modelo.transcribe(audio, language=idioma, beam_size=5, vad_filter=True,
                                              initial_prompt=PISTA_WHISPER.get(idioma))
        texto = " ".join(s.text.strip() for s in segmentos).strip()
        if not texto or any(a in texto.lower() for a in ALUCINACIONES):
            self.avisar("log", "✗ (" + (texto or "nada") + ")")
            self.voz.decir(frase(self.cfg, "no_entendido"))
            return

        numero, mensaje = entender(texto)
        a_enviar = mensaje
        if self.cfg["traducir_mios"] and idioma != "en":
            trad, _ = traducir(mensaje, "en", idioma)
            if not trad:   # sin internet: que lo traduzca Whisper desde el audio
                segs, _ = self.modelo.transcribe(audio, language=idioma, task="translate", vad_filter=True)
                trad = " ".join(s.text.strip() for s in segs).strip()
                trad = entender(trad)[1] if trad else ""
            a_enviar = trad or mensaje
        if numero:
            # el juego publica "04" y Whisper oye "4": se comparan sin ceros delante
            iguales = [c for c in coches() if (c[0].lstrip("0") or "0") == numero]
            if iguales:
                numero = iguales[0][0]
            # numero repetido (pasa en las salas publicas) o que no esta: sin nombre, mejor que uno equivocado
            cabeza = f"#{numero} {iguales[0][1]}" if len(iguales) == 1 else f"#{numero}"
            a_enviar = f"{cabeza}: {a_enviar}"
            repetir = frase(self.cfg, "para", n=numero, m=mensaje)
        else:
            repetir = mensaje   # sin "A todos": muchas veces es una respuesta a alguien y se sobreentiende
        self.avisar("log", f"? {texto}  →  {a_enviar}")

        # confirmar: te lo repite y tienes unos segundos para pulsar
        self.avisar("estado", "confirmando")
        while not self.eventos.empty():
            self.eventos.get_nowait()
        hecho = self.voz.decir(repetir)
        confirmado = False
        limite = None
        while True:
            if limite is None and hecho.is_set():
                limite = time.time() + float(self.cfg["espera_confirmar"])
            if limite is not None and time.time() > limite:
                break
            try:
                self.eventos.get(timeout=0.1)
                confirmado = True
                break
            except queue.Empty:
                pass
        if not confirmado:
            self.voz.decir(frase(self.cfg, "no_enviado"))
            self.avisar("log", "✗ " + frase(self.cfg, "no_enviado"))
            return
        self.voz.callar()
        if self.cfg["modo_prueba"]:
            self.voz.decir(frase(self.cfg, "prueba"))
            self.avisar("log", "· (prueba) " + a_enviar)
            return
        try:
            api_enviar_chat(a_enviar)
            winsound.Beep(1200, 80)
            self.voz.decir(frase(self.cfg, "enviado"))
            self.avisar("log", "→ " + a_enviar)
            anotar("enviado: " + a_enviar)
        except Exception as e:
            anotar(f"envio fallo: {e}")
            self.voz.decir(frase(self.cfg, "fallo"))


# ---------------------------------------------------------------- la ventana
def ventana():
    import tkinter as tk
    import webbrowser
    from tkinter import ttk
    import sounddevice as sd

    cfg = cargar_config()
    # Si se abre con el juego delante, NO hay que quitarle el foco: sin foco, Windows no
    # deja al juego mandar fuerza al volante (en el trace sale "Updating ffb failed due to
    # code 0x80040205" a cada fotograma) y el volante se queda muerto hasta volver al juego.
    # Medido el 08/10/2026: casi dos minutos sin fuerza por abrir esta ventana en pista.
    delante = user32.GetForegroundWindow()
    titulo = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(delante, titulo, 256)
    juego_delante = "le mans ultimate" in titulo.value.lower()
    raiz = tk.Tk()
    if juego_delante:
        raiz.wm_state("iconic")
        raiz.after(300, lambda: user32.SetForegroundWindow(delante))
    raiz.geometry("580x700")
    raiz.minsize(500, 600)
    cola_ui = queue.Queue()
    chat = Chat(cfg, lambda tipo, dato: cola_ui.put((tipo, dato)))

    # lo que tiene que sobrevivir a rehacer la ventana al cambiar de idioma
    w = {"estado": "cargando", "juego": False, "historial": []}

    # las listas de dispositivos se piden una vez: pedirlas cuesta y no cambian
    micros, salidas = [], []
    try:
        apis = sd.query_hostapis()
        mme = next(i for i, a in enumerate(apis) if "MME" in a["name"])
        micros = sorted({d["name"] for d in sd.query_devices() if d["max_input_channels"] > 0 and d["hostapi"] == mme
                         and "asignador" not in d["name"].lower() and "mapper" not in d["name"].lower()})
    except Exception:
        pass
    try:
        from pygame._sdl2 import audio as sdl2_audio
        salidas = list(sdl2_audio.get_audio_device_names(False))
    except Exception:
        pass

    def guardar(*_):
        guardar_config(cfg)

    def instrucciones():
        v = tk.Toplevel(raiz)
        v.title(tx(cfg, "instrucciones"))
        v.geometry("620x640")
        v.transient(raiz)
        caja = tk.Text(v, wrap="word", font=("Segoe UI", 10), padx=14, pady=12, relief="flat")
        barra = ttk.Scrollbar(v, command=caja.yview)
        caja.configure(yscrollcommand=barra.set)
        ttk.Button(v, text=tx(cfg, "cerrar"), command=v.destroy).pack(side="bottom", pady=8)
        barra.pack(side="right", fill="y")
        caja.pack(fill="both", expand=True)
        caja.tag_configure("titulo", font=("Segoe UI", 10, "bold"))
        for linea in INSTRUCCIONES.get(cfg["idioma"], INSTRUCCIONES["en"]).split("\n"):
            # los rotulos van en mayusculas: en negrita
            es_titulo = linea.strip() and linea.upper() == linea and not linea.startswith("•")
            caja.insert("end", linea + "\n", "titulo" if es_titulo else ())
        caja.configure(state="disabled")

    def construir():
        for hijo in raiz.winfo_children():
            if not isinstance(hijo, tk.Toplevel):
                hijo.destroy()
        raiz.title(tx(cfg, "titulo"))

        # ---- franja de abajo: apoyo (se coloca la primera para que nunca se quede fuera)
        pie = tk.Frame(raiz, bg="#f2f2f2", padx=12, pady=10)
        pie.pack(side="bottom", fill="x")
        tk.Label(pie, text=tx(cfg, "ciclo_texto"), bg="#f2f2f2", fg="#444", justify="center",
                 font=("Segoe UI", 9)).pack(side="top", fill="x", pady=(0, 8))
        botones = tk.Frame(pie, bg="#f2f2f2")
        botones.pack(side="top", fill="x")
        tk.Button(botones, text=tx(cfg, "cafe"), bg="#0070ba", fg="white", activebackground="#005ea6",
                  activeforeground="white", relief="flat", padx=10, pady=4, cursor="hand2",
                  font=("Segoe UI", 9, "bold"), command=lambda: webbrowser.open(PAYPAL)).pack(side="left")
        tk.Button(botones, text=tx(cfg, "ciclo_boton"), bg="#2e9e4f", fg="white", activebackground="#24803f",
                  activeforeground="white", relief="flat", padx=10, pady=4, cursor="hand2",
                  font=("Segoe UI", 9, "bold"), command=lambda: webbrowser.open(CICLOTRACKER)).pack(side="right")

        marco = ttk.Frame(raiz, padding=12)
        marco.pack(fill="both", expand=True)
        marco.columnconfigure(1, weight=1)
        fila = 0

        # ---- cabecera
        ttk.Label(marco, text=tx(cfg, "titulo"), font=("Segoe UI", 15, "bold")).grid(
            row=fila, column=0, columnspan=2, sticky="w")
        ttk.Button(marco, text="ⓘ " + tx(cfg, "instrucciones"), command=instrucciones).grid(
            row=fila, column=2, sticky="e")
        fila += 1
        ttk.Separator(marco).grid(row=fila, column=0, columnspan=3, sticky="ew", pady=(8, 6))
        fila += 1

        def etiqueta(clave):
            ttk.Label(marco, text=tx(cfg, clave)).grid(row=fila, column=0, sticky="w", pady=4, padx=(0, 10))

        # ---- idioma
        etiqueta("idioma")
        v_idioma = tk.StringVar(value=dict(IDIOMAS)[cfg["idioma"]])
        c_idioma = ttk.Combobox(marco, textvariable=v_idioma, values=[n for _, n in IDIOMAS], state="readonly")
        c_idioma.grid(row=fila, column=1, sticky="ew")

        def cambio_idioma(*_):
            cfg["idioma"] = next(c for c, n in IDIOMAS if n == v_idioma.get())
            guardar()
            raiz.after(10, construir)
        c_idioma.bind("<<ComboboxSelected>>", cambio_idioma)
        fila += 1

        # ---- boton
        etiqueta("boton")
        v_boton = tk.StringVar()

        def pintar_boton():
            b = cfg.get("boton")
            if not b:
                v_boton.set(tx(cfg, "sin_boton"))
            elif b["tipo"] == "teclado":
                v_boton.set(f"{tx(cfg, 'teclado')}: {b['nombre']}")
            else:
                v_boton.set(f"{tx(cfg, 'volante')}: {b['dispositivo']} — {b['boton'] + 1}")
        pintar_boton()
        ttk.Label(marco, textvariable=v_boton).grid(row=fila, column=1, sticky="w")

        def configurar_boton():
            v_boton.set(tx(cfg, "pulsa"))
            b_conf.state(["disabled"])

            def recibido(elegido):
                cola_ui.put(("boton", elegido))
            chat.entrada.capturar = recibido

            def caducar():
                if chat.entrada.capturar is recibido:
                    chat.entrada.capturar = None
                    cola_ui.put(("boton", None))
            raiz.after(10000, caducar)
        b_conf = ttk.Button(marco, text=tx(cfg, "configurar"), command=configurar_boton)
        b_conf.grid(row=fila, column=2, padx=(8, 0))
        w["pintar_boton"], w["b_conf"] = pintar_boton, b_conf
        fila += 1

        # ---- espera
        etiqueta("espera")
        v_espera = tk.IntVar(value=int(cfg["espera_confirmar"]))

        def cambio_espera(*_):
            try:
                cfg["espera_confirmar"] = max(1, min(30, int(v_espera.get())))
                guardar()
            except Exception:
                pass
        ttk.Spinbox(marco, from_=1, to=30, textvariable=v_espera, width=5,
                    command=cambio_espera).grid(row=fila, column=1, sticky="w")
        v_espera.trace_add("write", cambio_espera)
        fila += 1

        # ---- casillas
        for clave in ("traducir_mios", "leer", "traducir_chat", "prueba"):
            campo = {"leer": "leer_chat", "prueba": "modo_prueba"}.get(clave, clave)
            v = tk.BooleanVar(value=cfg[campo])

            def cambio(v=v, campo=campo):
                cfg[campo] = v.get()
                guardar()
            ttk.Checkbutton(marco, text=tx(cfg, clave), variable=v, command=cambio).grid(
                row=fila, column=0, columnspan=3, sticky="w", pady=2)
            fila += 1

        # ---- quien habla
        etiqueta("quien")
        opciones = [("ambos", tx(cfg, "q_ambos")), ("numero", tx(cfg, "q_numero")), ("nombre", tx(cfg, "q_nombre"))]
        v_quien = tk.StringVar(value=dict(opciones)[cfg["quien"]])
        c_quien = ttk.Combobox(marco, textvariable=v_quien, values=[n for _, n in opciones], state="readonly")
        c_quien.grid(row=fila, column=1, sticky="ew")

        def cambio_quien(*_):
            cfg["quien"] = next(c for c, n in opciones if n == v_quien.get())
            guardar()
        c_quien.bind("<<ComboboxSelected>>", cambio_quien)
        fila += 1

        # ---- micro y salida
        etiqueta("micro")
        v_micro = tk.StringVar(value=cfg["microfono"] or tx(cfg, "windows"))
        c_micro = ttk.Combobox(marco, textvariable=v_micro, values=[tx(cfg, "windows")] + micros, state="readonly")
        c_micro.grid(row=fila, column=1, columnspan=2, sticky="ew")

        def cambio_micro(*_):
            cfg["microfono"] = "" if v_micro.get() == tx(cfg, "windows") else v_micro.get()
            guardar()
        c_micro.bind("<<ComboboxSelected>>", cambio_micro)
        fila += 1

        etiqueta("salida")
        v_salida = tk.StringVar(value=cfg["salida_voz"] or tx(cfg, "windows"))
        c_salida = ttk.Combobox(marco, textvariable=v_salida, values=[tx(cfg, "windows")] + salidas, state="readonly")
        c_salida.grid(row=fila, column=1, sticky="ew")

        def cambio_salida(*_):
            cfg["salida_voz"] = "" if v_salida.get() == tx(cfg, "windows") else v_salida.get()
            chat.voz.cambiar_salida.set()
            guardar()
        c_salida.bind("<<ComboboxSelected>>", cambio_salida)
        ttk.Button(marco, text=tx(cfg, "probar"),
                   command=lambda: chat.voz.decir(frase(cfg, "listo"))).grid(row=fila, column=2, padx=(8, 0))
        fila += 1

        # ---- estado y registro
        ttk.Separator(marco).grid(row=fila, column=0, columnspan=3, sticky="ew", pady=8)
        fila += 1
        w["v_estado"] = tk.StringVar(value=tx(cfg, w["estado"]))
        w["v_juego"] = tk.StringVar(value="LMU ✓" if w["juego"] else tx(cfg, "sin_juego"))
        ttk.Label(marco, textvariable=w["v_estado"], font=("Segoe UI", 11, "bold")).grid(
            row=fila, column=0, columnspan=2, sticky="w")
        ttk.Label(marco, textvariable=w["v_juego"], foreground="gray").grid(row=fila, column=2, sticky="e")
        fila += 1
        caja = tk.Text(marco, height=8, wrap="word", font=("Segoe UI", 9))
        caja.grid(row=fila, column=0, columnspan=3, sticky="nsew", pady=(6, 0))
        marco.rowconfigure(fila, weight=1)
        caja.insert("end", "".join(w["historial"]))
        caja.see("end")
        caja.configure(state="disabled")
        w["caja"] = caja

    def escribir(linea):
        linea = time.strftime("%H:%M ") + linea + "\n"
        w["historial"] = (w["historial"] + [linea])[-200:]
        caja = w["caja"]
        caja.configure(state="normal")
        caja.insert("end", linea)
        caja.see("end")
        caja.configure(state="disabled")

    def atender():
        while True:
            try:
                tipo, dato = cola_ui.get_nowait()
            except queue.Empty:
                break
            try:
                if tipo == "estado":
                    w["estado"] = dato
                    w["v_estado"].set(tx(cfg, dato))
                elif tipo == "log":
                    escribir(dato)
                elif tipo == "juego":
                    w["juego"] = dato
                    w["v_juego"].set("LMU ✓" if dato else tx(cfg, "sin_juego"))
                elif tipo == "boton":
                    if dato:
                        cfg["boton"] = dato
                        guardar()
                    else:
                        escribir("✗ " + tx(cfg, "nada"))
                    w["pintar_boton"]()
                    w["b_conf"].state(["!disabled"])
            except tk.TclError:
                pass   # la ventana se estaba rehaciendo
        raiz.after(100, atender)

    construir()
    atender()
    raiz.mainloop()


if __name__ == "__main__":
    try:
        if "--autoprueba" in sys.argv:
            autoprueba()
            sys.exit(0)
        ventana()
    except Exception:
        anotar("arranque: " + traceback.format_exc())
        raise
