# -*- coding: utf-8 -*-
"""
A quien va el mensaje cuando NO dices su numero.

En el juego casi nunca ves el numero de los demas: la tabla de arriba solo
ensena al primero y a los que van cerca de ti, y la de abajo la inicial y el
apellido. Asi que se puede decir:

    "dile al de delante ..."                  el que va justo delante en la pista
    "dile al de detras de GT3 ..."            el GT3 mas cercano por detras
    "dile al que me acaba de adelantar ..."   el ultimo que te ha pasado
    "dile al tercero ..."                     el 3.o de TU clase
    "dile al tercero de hypercar ..."         el 3.o de esa clase
    "dile al que esta en posicion 15 ..."     el 15.o de tu clase (o de la que digas)
    "dile al 15 ..." / "al coche 15"          el que lleva el NUMERO 15 (eso no es de aqui)

Todo se resuelve con la FOTO que se hace al pulsar el boton (lo pidio Manuel):
entre que hablas, te lo repite y confirmas pasan segundos, y el que te acaba
de pasar ya puede ir en otro sitio.
"""
import re
import threading
import time

# ---------------------------------------------------------------- clases
CLASES = [
    ("hyper", r"h[iy]per\s*car|h[iy]per"),
    ("lmp2", r"l\.?\s*m\.?\s*p\.?\s*(?:2|dos|two|deux|due|zwei|dwa|dois)\b"),
    ("lmp3", r"l\.?\s*m\.?\s*p\.?\s*(?:3|tres|three|trois|tre|drei|trzy|tr[eê]s)\b"),
    ("gt3", r"(?:l\.?\s*m\.?\s*)?g\.?\s*t\.?\s*(?:3|tres|three|trois|tre|drei|trzy|tr[eê]s)\b|g\.?\s*t\.?\s*e\b"),
]
GENERAL = r"(?:la\s+)?general|overall|g[ée]n[ée]ral|generale|gesamt\w*|geral|og[oó]ln\w*"
NOMBRE_CLASE = {"hyper": "Hypercar", "lmp2": "LMP2", "lmp3": "LMP3", "gt3": "GT3"}


def clase_de(nombre_juego):
    """'Hyper' -> 'hyper', 'LMGT3' -> 'gt3'... para comparar sin lios."""
    n = re.sub(r"[^a-z0-9]", "", (nombre_juego or "").lower())
    for clave in ("hyper", "lmp2", "lmp3"):
        if clave in n:
            return clave
    if "gt3" in n or "gte" in n:
        return "gt3"
    return n


# ---------------------------------------------------------------- numeros dichos
CARDINALES = {
    # para "posicion diez" y "el que va quince"
    "uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8,
    "nueve": 9, "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15,
    "dieciseis": 16, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20,
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
    "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
}
ORDINALES = {
    "primero": 1, "primer": 1, "segundo": 2, "tercero": 3, "tercer": 3, "cuarto": 4, "quinto": 5,
    "sexto": 6, "séptimo": 7, "septimo": 7, "octavo": 8, "noveno": 9, "décimo": 10, "decimo": 10,
    "undécimo": 11, "undecimo": 11, "duodécimo": 12, "duodecimo": 12, "decimoprimero": 11,
    "decimosegundo": 12, "decimotercero": 13, "decimocuarto": 14, "decimoquinto": 15, "decimosexto": 16,
    "decimoséptimo": 17, "decimoseptimo": 17, "decimoctavo": 18, "decimonoveno": 19, "vigésimo": 20,
    "vigesimo": 20,
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
    "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
    "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19, "twentieth": 20,
    "premier": 1, "première": 1, "deuxième": 2, "troisième": 3, "quatrième": 4, "cinquième": 5,
    "sixième": 6, "septième": 7, "huitième": 8, "neuvième": 9, "dixième": 10,
    "primo": 1, "terzo": 3, "sesto": 6, "settimo": 7, "ottavo": 8, "nono": 9,
    "erste": 1, "ersten": 1, "erster": 1, "zweite": 2, "zweiten": 2, "dritte": 3, "dritten": 3,
    "vierte": 4, "vierten": 4, "fünfte": 5, "fünften": 5, "sechste": 6, "siebte": 7, "achte": 8,
    "neunte": 9, "zehnte": 10,
    "primeiro": 1, "terceiro": 3, "sétimo": 7, "oitavo": 8,
    # en polaco se dice "powiedz trzeciemu": el ordinal va en dativo
    "pierwszemu": 1, "drugiemu": 2, "trzeciemu": 3, "czwartemu": 4, "piątemu": 5, "szóstemu": 6,
    "siódmemu": 7, "ósmemu": 8, "dziewiątemu": 9, "dziesiątemu": 10,
}
# decimo quinto (separado) -> 15
_DECENA = r"(?:d[ée]cimo|decimo)\s+(primero|segundo|tercero|cuarto|quinto|sexto|s[ée]ptimo|octavo|noveno)"
# la terminacion pegada al numero: "al 3 o al 4" no es "al 3º"
ORDINAL_DIGITOS = r"(\d{1,2})(?:º|°|ª|o|er|ro|do|to|vo|no|st|nd|rd|th|e|ème|eme)(?![\w])"
NUMEROS = {**CARDINALES, **ORDINALES}
_alternativas = lambda d: "|".join(sorted((re.escape(k) for k in d), key=len, reverse=True))
PALABRA_NUMERO = _alternativas(NUMEROS)
# "al tercero" si, pero "al uno" o "the one behind" no: ahi solo valen ordinales
PALABRA_ORDINAL = _alternativas(ORDINALES)


def numero_de(texto):
    """'15', 'quince', 'decimoquinto', 'décimo quinto', '15º', '15th' -> 15."""
    t = texto.strip().lower()
    if t.isdigit():
        return int(t)
    m = re.fullmatch(ORDINAL_DIGITOS, t)
    if m:
        return int(m.group(1))
    m = re.fullmatch(_DECENA, t)
    if m:
        return 10 + NUMEROS[m.group(1)]
    return NUMEROS.get(t)


# ---------------------------------------------------------------- frases
# "celui", "quello", "dem", "temu", "aquele": el "el" de "al de delante" en otros idiomas
PRONOMBRE = r"(?:celui|celle|quello|quella|dem|temu|aquele|aquela)"
_QUIEN = (rf"(?:(?:coche|car|el|one|que\s+(?:va|tengo|est[aá]))\s+|the\s+(?:car\s+|one\s+)?|"
          rf"{PRONOMBRE}\s*,?\s+)?")
DELANTE = (_QUIEN + r"(?:de\s+)?"
           r"(?:a?delante(?:\s+de\s+m[ií])?|in\s+front(?:\s+of\s+me)?|ahead(?:\s+of\s+me)?|"
           r"devant(?:\s+moi)?|davanti(?:\s+a\s+me)?|vor\s+mir|(?:da\s+)?frente|przede\s+mn[aą])")
DETRAS = (_QUIEN + r"(?:de\s+)?"
          r"(?:detr[aá]s(?:\s+de\s+m[ií])?|atr[aá]s|behind(?:\s+me)?|derri[eè]re(?:\s+moi)?|"
          r"dietro(?:\s+di\s+me)?|hinter\s+mir|tr[aá]s(?:\s+de\s+mim)?|za\s+mn[aą])")
ADELANTO = (r"(?:que\s+|who\s+|qui\s+|che\s+|der\s+|kt[oó]ry\s+)?"
            r"(?:me\s+(?:acaba\s+de\s+|ha\s+|acabou\s+de\s+)?(?:adelantar|adelantado|adelant[oó]|pasar|pasado|"
            r"pas[oó]|ultrapassar|ultrapassou)|(?:just\s+)?(?:overtook|passed)\s+me|m'a\s+(?:d[ée]pass[ée]|doubl[ée])|"
            r"mi\s+ha\s+(?:sorpassato|superato)|mich\s+(?:gerade\s+)?[üu]berholt(?:\s+hat)?|"
            r"mnie\s+(?:w[lł]a[sś]nie\s+)?wyprzedzi[lł])")
POSICION = (rf"(?:the\s+|{PRONOMBRE}\s+)?(?:car\s+|one\s+)?(?:que\s+(?:est[aá]|va)\s+|who\s+is\s+|qui\s+est\s+|che\s+[eè]\s+|der\s+|que\s+est[aá]\s+)?"
            rf"(?:en\s+|in\s+|na\s+|auf\s+)?(?:la\s+|el\s+)?"
            rf"(?:posici[oó]n|puesto|position|posizione|posi[cç][aã]o|platz|pozycj\w*|p)\s*"
            rf"(?P<npos>\d{{1,2}}|{PALABRA_NUMERO})\b")
VA_N = rf"que\s+(?:est[aá]|va)\s+(?:el\s+)?(?P<nva>\d{{1,2}}|{PALABRA_NUMERO})(?:\s*(?:º|°|o))?\b"
ORDINAL = rf"(?:el\s+|the\s+|le\s+|la\s+|il\s+|den\s+|o\s+)?(?P<nord>{_DECENA}|{ORDINAL_DIGITOS}|(?:{PALABRA_ORDINAL})\b)"
CLASE = (r"(?:\s*,?\s+(?:de\s+la|del|de|en|in|of|du|des|di|della|der|im|da|z|w)\s+(?:la\s+|the\s+)?"
         r"(?:clase\s+|class\s+|categor[ií]a\s+|cat[ée]gorie\s+|classe\s+|klasse\s+|klasy\s+)?"
         rf"(?P<clase>{'|'.join(p for _, p in CLASES)}|{GENERAL}))?")


def _compilar(orden, enlace, que):
    cabeza = rf"^\s*(?:{orden}\b[\s,]*)(?:{enlace}\s+)*"
    cola = rf"{CLASE}[\s,.:;-]*(?:{que}\b)?[\s,:]*(?P<m>.+)$"
    return [
        ("adelanto", re.compile(cabeza + rf"(?:el\s+|the\s+one\s+|the\s+car\s+|{PRONOMBRE}\s*,?\s+)?{ADELANTO}" + cola, re.I | re.S)),
        ("delante", re.compile(cabeza + DELANTE + cola, re.I | re.S)),
        ("detras", re.compile(cabeza + DETRAS + cola, re.I | re.S)),
        ("posicion", re.compile(cabeza + POSICION + cola, re.I | re.S)),
        ("posicion", re.compile(cabeza + VA_N + cola, re.I | re.S)),
        # el ordinal solo si es palabra de orden o lleva su terminacion: "al 3" sin mas es el NUMERO 3
        ("posicion", re.compile(cabeza + ORDINAL + cola, re.I | re.S)),
    ]


_patrones = None


def analizar(texto, orden, enlace, que):
    """('delante'|'detras'|'adelanto'|'posicion', n, clase) y el resto del mensaje,
    o (None, None) si el texto no se refiere a un coche asi."""
    global _patrones
    if _patrones is None:
        _patrones = _compilar(orden, enlace, que)
    for tipo, rx in _patrones:
        m = rx.match(texto)
        if not m or not m.group("m").strip():
            continue
        n = None
        if tipo == "posicion":
            crudo = next((m.group(g) for g in ("npos", "nva", "nord") if g in rx.groupindex and m.group(g)), None)
            n = numero_de(crudo) if crudo else None
            if not n:
                continue
            if crudo.strip().isdigit() and "nord" in rx.groupindex and m.group("nord"):
                continue   # "dile al 3" sin terminacion: es el numero de coche, no la posicion
        clase = m.group("clase")
        if clase:
            clase = "general" if re.fullmatch(GENERAL, clase, re.I) else next(
                k for k, p in CLASES if re.fullmatch(p, clase, re.I))
        return {"tipo": tipo, "n": n, "clase": clase}, m.group("m").strip()
    return None, None


# ---------------------------------------------------------------- la foto
def foto(lista, largo, ultimo_adelanto=None):
    """Lo que hace falta del momento de pulsar el boton."""
    coches = [{"num": str(c.get("carNumber", "")), "nombre": c.get("driverName", ""),
               "clase": clase_de(c.get("carClass")), "clase_juego": c.get("carClass", ""),
               "pos": c.get("position") or 999, "dist": c.get("lapDistance") or 0.0,
               "yo": bool(c.get("player")), "garaje": bool(c.get("inGarageStall")),
               "slot": c.get("slotID")} for c in lista]
    return {"coches": coches, "largo": largo or 0.0, "adelanto": ultimo_adelanto, "hora": time.time()}


def resolver(objetivo, f):
    """El coche (dict de la foto) al que se refiere, o None si no se encuentra."""
    if not f or not f["coches"]:
        return None
    yo = next((c for c in f["coches"] if c["yo"]), None)
    otros = [c for c in f["coches"] if not c["yo"]]
    clase = objetivo.get("clase")
    tipo = objetivo["tipo"]

    if tipo == "adelanto":
        a = f.get("adelanto")
        if not a or f["hora"] - a["hora"] > ADELANTO_VALE:
            return None
        return next((c for c in otros if c["slot"] == a["slot"]), None)

    if tipo in ("delante", "detras"):
        if yo is None or not f["largo"]:
            return None
        en_pista = [c for c in otros if not c["garaje"] and (clase in (None, "general") or c["clase"] == clase)]
        if not en_pista:
            return None
        if tipo == "delante":
            hueco = lambda c: (c["dist"] - yo["dist"]) % f["largo"]
        else:
            hueco = lambda c: (yo["dist"] - c["dist"]) % f["largo"]
        return min(en_pista, key=hueco)

    # posicion: de la clase que digas, de la general, o de la TUYA si no dices nada
    if clase == "general":
        grupo = f["coches"]
    else:
        clase = clase or (yo["clase"] if yo else None)
        grupo = [c for c in f["coches"] if clase is None or c["clase"] == clase]
    grupo = sorted(grupo, key=lambda c: c["pos"])
    n = objetivo["n"]
    if 1 <= n <= len(grupo):
        return grupo[n - 1]
    return None


# ---------------------------------------------------------------- quien me ha adelantado
ADELANTO_VALE = 60      # s: pasado esto, "el que me acaba de adelantar" ya no vale
ADELANTO_CERCA = 150    # m: solo cuenta si pasa cerca (no un doblado al otro lado)


class Vigia:
    """Mira la pista cada medio segundo y apunta al ultimo que te ha pasado."""

    def __init__(self, pedir_lista, pedir_largo):
        self.pedir_lista = pedir_lista
        self.pedir_largo = pedir_largo
        self.ultimo = None          # {"slot", "hora"}
        self.largo = 0.0
        self._antes = {}
        threading.Thread(target=self._bucle, daemon=True).start()

    def _bucle(self):
        ult_largo = 0.0
        while True:
            try:
                if time.time() - ult_largo > 10:
                    ult_largo = time.time()
                    self.largo = self.pedir_largo() or self.largo
                self.mirar(self.pedir_lista())
            except Exception:
                self._antes = {}
                time.sleep(2)
            time.sleep(0.5)

    def mirar(self, lista):
        yo = next((c for c in lista if c.get("player")), None)
        if yo is None or not self.largo or yo.get("inGarageStall") or yo.get("pitting"):
            self._antes = {}
            return
        mitad = self.largo / 2
        ahora = {}
        for c in lista:
            if c.get("player") or c.get("inGarageStall") or c.get("pitting"):
                continue
            # separacion con signo: + delante, - detras, por el camino mas corto
            d = ((c.get("lapDistance", 0) - yo.get("lapDistance", 0) + mitad) % self.largo) - mitad
            ahora[c.get("slotID")] = d
            antes = self._antes.get(c.get("slotID"))
            if antes is not None and antes < 0 <= d and abs(antes) < ADELANTO_CERCA and d < ADELANTO_CERCA:
                self.ultimo = {"slot": c.get("slotID"), "hora": time.time()}
        self._antes = ahora
