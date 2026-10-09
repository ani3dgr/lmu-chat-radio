# -*- coding: utf-8 -*-
"""
Los textos de la ventana y las instrucciones, en los siete idiomas del mapa.

Si a un idioma le falta una frase, sale en ingles, y si tampoco esta, en
espanol: nunca un hueco en blanco.

Lo que el programa DICE en voz alta no esta aqui: esta en FRASES, dentro de
chat_lmu.py, porque va junto a la logica que lo usa.
"""

PAYPAL = "https://paypal.me/ani3dgr"
CICLOTRACKER = "https://ciclotracker.com"

TEXTOS = {
    "es": {
        "descargando": "Descargando el reconocimiento de voz (solo la primera vez, unos 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Instrucciones", "idioma": "Idioma",
        "boton": "Botón para hablar", "configurar": "Configurar…",
        "pulsa": "Pulsa ahora el botón del volante o la tecla…", "sin_boton": "(sin configurar)",
        "volante": "Volante", "teclado": "Tecla", "nada": "No se ha pulsado nada",
        "espera": "Segundos para confirmar",
        "traducir_mios": "Traducir lo que digo al inglés", "leer": "Leer el chat en voz alta",
        "traducir_chat": "Traducir el chat a mi idioma", "prueba": "Modo prueba (no manda nada al chat)",
        "quien": "Al leer, decir", "q_ambos": "Nombre y número", "q_numero": "El número de coche",
        "q_nombre": "El nombre",
        "micro": "Micrófono", "salida": "Salida de voz", "windows": "(el de Windows)", "volumen": "Volumen de la voz", "volumen_pitido": "Volumen del pitido", "probar": "Probar voz",
        "cargando": "Cargando el reconocimiento de voz…", "error_whisper": "Error al cargar el reconocimiento de voz",
        "listo": "Listo", "sin_juego": "Esperando al juego…", "grabando": "Escuchando… (pulsa para terminar)",
        "procesando": "Pensando…", "confirmando": "Pulsa para enviar",
        "cafe": "☕ Invítame a un café",
        "ciclo_texto": "Apoya a CicloTracker y nos ayudas a seguir creando proyectos.\nGPS para la bici, en Google Play.",
        "ciclo_boton": "Conocer CicloTracker", "cerrar": "Cerrar",
    },
    "en": {
        "descargando": "Downloading speech recognition (first time only, about 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Instructions", "idioma": "Language",
        "boton": "Push-to-talk button", "configurar": "Set…",
        "pulsa": "Press the wheel button or the key now…", "sin_boton": "(not set)",
        "volante": "Wheel", "teclado": "Key", "nada": "Nothing was pressed",
        "espera": "Seconds to confirm",
        "traducir_mios": "Translate what I say into English", "leer": "Read the chat aloud",
        "traducir_chat": "Translate the chat into my language", "prueba": "Test mode (sends nothing to the chat)",
        "quien": "When reading, say", "q_ambos": "Name and number", "q_numero": "The car number",
        "q_nombre": "The name",
        "micro": "Microphone", "salida": "Voice output", "windows": "(Windows default)", "volumen": "Voice volume", "volumen_pitido": "Beep volume", "probar": "Test voice",
        "cargando": "Loading speech recognition…", "error_whisper": "Speech recognition failed to load",
        "listo": "Ready", "sin_juego": "Waiting for the game…", "grabando": "Listening… (press to finish)",
        "procesando": "Thinking…", "confirmando": "Press to send",
        "cafe": "☕ Buy me a coffee",
        "ciclo_texto": "Support CicloTracker and help us keep building projects.\nGPS for your bike, on Google Play.",
        "ciclo_boton": "Discover CicloTracker", "cerrar": "Close",
    },
    "fr": {
        "descargando": "Téléchargement de la reconnaissance vocale (la première fois seulement, environ 500 Mo)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Mode d'emploi", "idioma": "Langue",
        "boton": "Bouton pour parler", "configurar": "Choisir…",
        "pulsa": "Appuyez maintenant sur le bouton du volant ou la touche…", "sin_boton": "(non défini)",
        "volante": "Volant", "teclado": "Touche", "nada": "Aucune touche détectée",
        "espera": "Secondes pour confirmer",
        "traducir_mios": "Traduire ce que je dis en anglais", "leer": "Lire le chat à voix haute",
        "traducir_chat": "Traduire le chat dans ma langue", "prueba": "Mode test (n'envoie rien au chat)",
        "quien": "En lisant, dire", "q_ambos": "Nom et numéro", "q_numero": "Le numéro de voiture",
        "q_nombre": "Le nom",
        "micro": "Micro", "salida": "Sortie de la voix", "windows": "(celle de Windows)", "volumen": "Volume de la voix", "volumen_pitido": "Volume du bip", "probar": "Tester la voix",
        "cargando": "Chargement de la reconnaissance vocale…", "error_whisper": "Échec du chargement de la reconnaissance vocale",
        "listo": "Prêt", "sin_juego": "En attente du jeu…", "grabando": "J'écoute… (appuyez pour terminer)",
        "procesando": "Je réfléchis…", "confirmando": "Appuyez pour envoyer",
        "cafe": "☕ Offrez-moi un café",
        "ciclo_texto": "Soutenez CicloTracker et aidez-nous à créer d'autres projets.\nGPS pour le vélo, sur Google Play.",
        "ciclo_boton": "Découvrir CicloTracker", "cerrar": "Fermer",
    },
    "it": {
        "descargando": "Download del riconoscimento vocale (solo la prima volta, circa 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Istruzioni", "idioma": "Lingua",
        "boton": "Pulsante per parlare", "configurar": "Imposta…",
        "pulsa": "Premi ora il pulsante del volante o il tasto…", "sin_boton": "(non impostato)",
        "volante": "Volante", "teclado": "Tasto", "nada": "Nessun pulsante premuto",
        "espera": "Secondi per confermare",
        "traducir_mios": "Traduci in inglese quello che dico", "leer": "Leggi la chat ad alta voce",
        "traducir_chat": "Traduci la chat nella mia lingua", "prueba": "Modalità prova (non invia nulla alla chat)",
        "quien": "Leggendo, dire", "q_ambos": "Nome e numero", "q_numero": "Il numero della macchina",
        "q_nombre": "Il nome",
        "micro": "Microfono", "salida": "Uscita della voce", "windows": "(quello di Windows)", "volumen": "Volume della voce", "volumen_pitido": "Volume del bip", "probar": "Prova voce",
        "cargando": "Caricamento del riconoscimento vocale…", "error_whisper": "Errore nel caricare il riconoscimento vocale",
        "listo": "Pronto", "sin_juego": "In attesa del gioco…", "grabando": "Ascolto… (premi per finire)",
        "procesando": "Ci penso…", "confirmando": "Premi per inviare",
        "cafe": "☕ Offrimi un caffè",
        "ciclo_texto": "Sostieni CicloTracker e aiutaci a creare altri progetti.\nGPS per la bici, su Google Play.",
        "ciclo_boton": "Scopri CicloTracker", "cerrar": "Chiudi",
    },
    "de": {
        "descargando": "Spracherkennung wird heruntergeladen (nur beim ersten Mal, etwa 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Anleitung", "idioma": "Sprache",
        "boton": "Sprechtaste", "configurar": "Festlegen…",
        "pulsa": "Drücke jetzt die Lenkradtaste oder die Taste…", "sin_boton": "(nicht festgelegt)",
        "volante": "Lenkrad", "teclado": "Taste", "nada": "Nichts gedrückt",
        "espera": "Sekunden zum Bestätigen",
        "traducir_mios": "Was ich sage ins Englische übersetzen", "leer": "Chat vorlesen",
        "traducir_chat": "Chat in meine Sprache übersetzen", "prueba": "Testmodus (sendet nichts in den Chat)",
        "quien": "Beim Vorlesen sagen", "q_ambos": "Name und Nummer", "q_numero": "Die Startnummer",
        "q_nombre": "Den Namen",
        "micro": "Mikrofon", "salida": "Sprachausgabe", "windows": "(Windows-Standard)", "volumen": "Lautstärke Stimme", "volumen_pitido": "Lautstärke Piepton", "probar": "Stimme testen",
        "cargando": "Spracherkennung wird geladen…", "error_whisper": "Spracherkennung konnte nicht geladen werden",
        "listo": "Bereit", "sin_juego": "Warte auf das Spiel…", "grabando": "Ich höre zu… (drücken zum Beenden)",
        "procesando": "Moment…", "confirmando": "Drücken zum Senden",
        "cafe": "☕ Spendier mir einen Kaffee",
        "ciclo_texto": "Unterstütze CicloTracker und hilf uns, weitere Projekte zu bauen.\nGPS fürs Fahrrad, bei Google Play.",
        "ciclo_boton": "CicloTracker ansehen", "cerrar": "Schließen",
    },
    "pl": {
        "descargando": "Pobieranie rozpoznawania mowy (tylko za pierwszym razem, około 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Instrukcja", "idioma": "Język",
        "boton": "Przycisk do mówienia", "configurar": "Ustaw…",
        "pulsa": "Naciśnij teraz przycisk na kierownicy lub klawisz…", "sin_boton": "(nie ustawiono)",
        "volante": "Kierownica", "teclado": "Klawisz", "nada": "Nic nie naciśnięto",
        "espera": "Sekundy na potwierdzenie",
        "traducir_mios": "Tłumacz to, co mówię, na angielski", "leer": "Czytaj czat na głos",
        "traducir_chat": "Tłumacz czat na mój język", "prueba": "Tryb testowy (nic nie wysyła na czat)",
        "quien": "Czytając, podawaj", "q_ambos": "Nazwisko i numer", "q_numero": "Numer samochodu",
        "q_nombre": "Nazwisko",
        "micro": "Mikrofon", "salida": "Wyjście głosu", "windows": "(domyślne Windows)", "volumen": "Głośność głosu", "volumen_pitido": "Głośność sygnału", "probar": "Test głosu",
        "cargando": "Ładowanie rozpoznawania mowy…", "error_whisper": "Nie udało się załadować rozpoznawania mowy",
        "listo": "Gotowe", "sin_juego": "Czekam na grę…", "grabando": "Słucham… (naciśnij, aby zakończyć)",
        "procesando": "Myślę…", "confirmando": "Naciśnij, aby wysłać",
        "cafe": "☕ Postaw mi kawę",
        "ciclo_texto": "Wesprzyj CicloTracker i pomóż nam tworzyć kolejne projekty.\nGPS dla roweru, w Google Play.",
        "ciclo_boton": "Poznaj CicloTracker", "cerrar": "Zamknij",
    },
    "pt": {
        "descargando": "A descarregar o reconhecimento de voz (só da primeira vez, cerca de 500 MB)…",
        "titulo": "LMU Chat Radio", "instrucciones": "Instruções", "idioma": "Idioma",
        "boton": "Botão para falar", "configurar": "Definir…",
        "pulsa": "Carrega agora no botão do volante ou na tecla…", "sin_boton": "(não definido)",
        "volante": "Volante", "teclado": "Tecla", "nada": "Nada foi carregado",
        "espera": "Segundos para confirmar",
        "traducir_mios": "Traduzir o que digo para inglês", "leer": "Ler o chat em voz alta",
        "traducir_chat": "Traduzir o chat para o meu idioma", "prueba": "Modo de teste (não envia nada para o chat)",
        "quien": "Ao ler, dizer", "q_ambos": "Nome e número", "q_numero": "O número do carro",
        "q_nombre": "O nome",
        "micro": "Microfone", "salida": "Saída de voz", "windows": "(o do Windows)", "volumen": "Volume da voz", "volumen_pitido": "Volume do bip", "probar": "Testar voz",
        "cargando": "A carregar o reconhecimento de voz…", "error_whisper": "Erro ao carregar o reconhecimento de voz",
        "listo": "Pronto", "sin_juego": "À espera do jogo…", "grabando": "A ouvir… (carrega para terminar)",
        "procesando": "A pensar…", "confirmando": "Carrega para enviar",
        "cafe": "☕ Paga-me um café",
        "ciclo_texto": "Apoia o CicloTracker e ajuda-nos a criar mais projetos.\nGPS para a bicicleta, no Google Play.",
        "ciclo_boton": "Conhecer o CicloTracker", "cerrar": "Fechar",
    },
}

INSTRUCCIONES = {
    "es": """LMU CHAT RADIO — CÓMO SE USA

ANTES DE EMPEZAR
1. Elige tu idioma.
2. Pulsa «Configurar…» y después el botón del volante o la tecla que quieras usar. Mejor uno que no uses para nada en el juego.
3. Elige tu micrófono y por dónde quieres oír la voz, y pulsa «Probar voz».
4. Abre Le Mans Ultimate. Cuando el programa lo encuentre verás «LMU ✓». Funciona igual con el juego en pantalla completa, en ventana o sin bordes: no pone nada encima del juego.

ESCRIBIR EN EL CHAT
1. Pulsa tu botón: oirás un pitido. Habla.
2. Pulsa otra vez para terminar.
3. El programa te repite en voz alta lo que ha entendido.
4. Si está bien, pulsa el botón antes de que pasen los segundos de espera y se envía. Si no pulsas, oirás «Mensaje no enviado» y no se manda nada.

Ejemplos:
• «Dile al coche 33 que lo siento» → #33 Nombre del piloto: I'm sorry
• «Suerte a todos» → Good luck everyone

Si dices un número de coche, el programa busca quién lo lleva y pone su nombre. Si el número está repetido en la sala o no aparece, escribe solo el número, para no equivocarse de piloto.

A QUIÉN VA EL MENSAJE
Muchas veces no sabes el número de los demás. No pasa nada: di dónde está.
• «Dile al de delante…» / «Dile al de detrás…» → el coche que tienes justo delante o detrás en la pista.
• «Dile al de delante de LMP2…» → el LMP2 más cercano por delante (valen Hypercar, LMP2, LMP3 y GT3).
• «Dile al que me acaba de adelantar…» → el último que te ha pasado (vale durante un minuto).
• «Dile al tercero…» → el tercero de TU clase. «Dile al tercero de Hypercar…» → el tercero de esa clase. «…de la general» → de toda la carrera.
• «Dile al que está en posición 15…» → lo mismo que «al decimoquinto», pero más fácil de decir.

¡OJO, NO ES LO MISMO!
• «Dile al 15…» → el coche que lleva el NÚMERO 15.
• «Dile al que está en posición 15…» o «al que va 15…» → el que va el DECIMOQUINTO.

Todo se calcula en el momento en que pulsas el botón: aunque luego te adelante o cambie de puesto, el mensaje va a quien era. Al repetírtelo te dice su número y su clase («Para el 33 de GT3: …»); si no es él, no confirmes. Si no lo encuentra, te lo dice y no se envía nada.

LEER EL CHAT
Los mensajes de los demás se dicen en voz alta, traducidos a tu idioma si tienes la casilla marcada. Puedes elegir si dice el nombre, el número de coche o las dos cosas (en el chat el juego acorta los nombres, así que el número suele ayudar).
Si un mensaje lleva tu número o tu apellido, empieza con «Para ti».
Mientras hablas o confirmas, los mensajes que llegan esperan su turno.

MODO PRUEBA
Con esa casilla marcada todo funciona igual, pero no se manda nada al chat. Sirve para practicar sin molestar a nadie.

BUENO SABER
• El reconocimiento de voz funciona en tu ordenador, sin internet.
• Las traducciones y la voz usan internet. Sin internet habla con la voz de Windows y la traducción al inglés es más sencilla.
• Si no oyes nada, revisa la «Salida de voz». Si no te entiende, revisa el «Micrófono».""",

    "en": """LMU CHAT RADIO — HOW TO USE IT

BEFORE YOU START
1. Pick your language.
2. Click "Set…" and then press the wheel button or the key you want to use. Better one you don't use for anything in the game.
3. Pick your microphone and where you want to hear the voice, and click "Test voice".
4. Start Le Mans Ultimate. When the program finds it you will see "LMU ✓". It works the same with the game in fullscreen, windowed or borderless: it draws nothing on top of the game.

WRITING IN THE CHAT
1. Press your button: you'll hear a beep. Speak.
2. Press it again to finish.
3. The program reads back what it understood.
4. If it's right, press the button before the waiting time runs out and it is sent. If you don't press, you'll hear "Message not sent" and nothing is sent.

Examples:
• "Tell car 33 I'm sorry" → #33 Driver name: I'm sorry
• "Good luck everyone" → Good luck everyone

If you say a car number, the program looks up who drives it and adds their name. If that number appears twice in the server, or isn't there, it writes only the number, so it never names the wrong driver.

WHO THE MESSAGE IS FOR
You often don't know the other drivers' numbers. No problem: say where they are.
• "Tell the car in front…" / "Tell the car behind…" → the car right in front of or behind you on track.
• "Tell the car in front in LMP2…" → the nearest LMP2 ahead (Hypercar, LMP2, LMP3 and GT3 work).
• "Tell who just overtook me…" → the last car that passed you (valid for one minute).
• "Tell the third…" → third in YOUR class. "Tell the third in Hypercar…" → third in that class. "…overall" → in the whole race.
• "Tell the car in position 15…" → the same as "the fifteenth", but easier to say.

CAREFUL, THEY ARE NOT THE SAME!
• "Tell car 15…" / "Tell 15…" → the car with the NUMBER 15.
• "Tell the car in position 15…" → the car running FIFTEENTH.

Everything is worked out the moment you press the button: even if they overtake you or change places afterwards, the message goes to that car. When it reads it back it says their number and class ("To car 33, GT3: …"); if it's not them, don't confirm. If it can't find the car, it says so and nothing is sent.

READING THE CHAT
Messages from other drivers are read aloud, translated into your language if that box is ticked. You can choose whether it says the name, the car number or both (the game shortens names in the chat, so the number usually helps).
If a message contains your number or your surname, it starts with "For you".
While you are speaking or confirming, incoming messages wait their turn.

TEST MODE
With that box ticked everything works the same, but nothing is sent to the chat. Good for practising without bothering anyone.

GOOD TO KNOW
• Speech recognition runs on your computer, without internet.
• Translations and the voice use the internet. Without internet it speaks with the Windows voice and the English translation is simpler.
• If you hear nothing, check "Voice output". If it doesn't understand you, check "Microphone".""",

    "fr": """LMU CHAT RADIO — MODE D'EMPLOI

AVANT DE COMMENCER
1. Choisissez votre langue.
2. Cliquez sur « Choisir… » puis appuyez sur le bouton du volant ou la touche que vous voulez utiliser. De préférence une que vous n'utilisez pas dans le jeu.
3. Choisissez votre micro et où vous voulez entendre la voix, puis cliquez sur « Tester la voix ».
4. Lancez Le Mans Ultimate. Quand le programme le trouve, vous verrez « LMU ✓ ». Il fonctionne pareil en plein écran, en fenêtre ou sans bordure : il n'affiche rien par-dessus le jeu.

ÉCRIRE DANS LE CHAT
1. Appuyez sur votre bouton : vous entendrez un bip. Parlez.
2. Appuyez à nouveau pour terminer.
3. Le programme vous répète à voix haute ce qu'il a compris.
4. Si c'est bon, appuyez sur le bouton avant la fin du délai et le message part. Sinon, vous entendrez « Message non envoyé » et rien n'est envoyé.

Exemples :
• « Dis à la voiture 33 désolé » → #33 Nom du pilote : Sorry
• « Bonne chance à tous » → Good luck everyone

Si vous dites un numéro de voiture, le programme cherche qui la pilote et ajoute son nom. Si le numéro est en double sur le serveur, ou absent, il n'écrit que le numéro, pour ne jamais se tromper de pilote.

À QUI VA LE MESSAGE
Souvent vous ne connaissez pas le numéro des autres. Pas grave : dites où ils sont.
• « Dis à celui devant… » / « Dis à celui derrière… » → la voiture juste devant ou derrière vous en piste.
• « Dis à celui devant en LMP2… » → la LMP2 la plus proche devant (Hypercar, LMP2, LMP3 et GT3).
• « Dis à celui qui m'a dépassé… » → le dernier qui vous a doublé (valable une minute).
• « Dis au troisième… » → le troisième de VOTRE catégorie. « Dis au troisième en Hypercar… » → le troisième de cette catégorie. « …au général » → de toute la course.
• « Dis à celui en position 15… » → comme « au quinzième », plus facile à dire.

ATTENTION, CE N'EST PAS PAREIL !
• « Dis à la 15… » → la voiture qui porte le NUMÉRO 15.
• « Dis à celui en position 15… » → celui qui est QUINZIÈME.

Tout est calculé au moment où vous appuyez sur le bouton : même s'il vous double ensuite, le message va à cette voiture. En le répétant, le programme dit son numéro et sa catégorie (« Pour la 33 en GT3 : … ») ; si ce n'est pas lui, ne confirmez pas. S'il ne la trouve pas, il le dit et rien n'est envoyé.

LIRE LE CHAT
Les messages des autres sont lus à voix haute, traduits dans votre langue si la case est cochée. Vous pouvez choisir s'il dit le nom, le numéro de voiture ou les deux (le jeu raccourcit les noms dans le chat, le numéro aide souvent).
Si un message contient votre numéro ou votre nom de famille, il commence par « Pour toi ».
Pendant que vous parlez ou confirmez, les messages qui arrivent attendent leur tour.

MODE TEST
Avec cette case cochée tout fonctionne pareil, mais rien n'est envoyé au chat. Pratique pour s'entraîner sans déranger personne.

BON À SAVOIR
• La reconnaissance vocale tourne sur votre ordinateur, sans internet.
• Les traductions et la voix utilisent internet. Sans internet, il parle avec la voix de Windows et la traduction en anglais est plus simple.
• Si vous n'entendez rien, vérifiez « Sortie de la voix ». S'il ne vous comprend pas, vérifiez « Micro ».""",

    "it": """LMU CHAT RADIO — COME SI USA

PRIMA DI INIZIARE
1. Scegli la tua lingua.
2. Clicca «Imposta…» e poi premi il pulsante del volante o il tasto che vuoi usare. Meglio uno che non usi nel gioco.
3. Scegli il microfono e dove vuoi sentire la voce, poi clicca «Prova voce».
4. Avvia Le Mans Ultimate. Quando il programma lo trova vedrai «LMU ✓». Funziona allo stesso modo a schermo intero, in finestra o senza bordi: non disegna niente sopra il gioco.

SCRIVERE IN CHAT
1. Premi il tuo pulsante: sentirai un bip. Parla.
2. Premi di nuovo per finire.
3. Il programma ti ripete ad alta voce quello che ha capito.
4. Se va bene, premi il pulsante prima che scada il tempo di attesa e viene inviato. Se non premi, sentirai «Messaggio non inviato» e non parte niente.

Esempi:
• «Di alla macchina 33 scusa» → #33 Nome del pilota: Sorry
• «Buona fortuna a tutti» → Good luck everyone

Se dici un numero di macchina, il programma cerca chi la guida e aggiunge il suo nome. Se il numero è ripetuto nel server, o non c'è, scrive solo il numero, per non sbagliare pilota.

A CHI VA IL MESSAGGIO
Spesso non sai il numero degli altri. Nessun problema: di' dove sono.
• «Di a quello davanti…» / «Di a quello dietro…» → la macchina subito davanti o dietro di te in pista.
• «Di a quello davanti in LMP2…» → la LMP2 più vicina davanti (Hypercar, LMP2, LMP3 e GT3).
• «Di a quello che mi ha sorpassato…» → l'ultimo che ti ha passato (vale per un minuto).
• «Di al terzo…» → il terzo della TUA classe. «Di al terzo di Hypercar…» → il terzo di quella classe. «…della generale» → di tutta la gara.
• «Di a quello in posizione 15…» → come «al quindicesimo», ma più facile da dire.

ATTENZIONE, NON È LA STESSA COSA!
• «Di alla 15…» → la macchina con il NUMERO 15.
• «Di a quello in posizione 15…» → quello che è QUINDICESIMO.

Tutto si calcola nel momento in cui premi il pulsante: anche se poi ti sorpassa o cambia posizione, il messaggio va a quella macchina. Quando lo ripete ti dice numero e classe («Per la 33 in GT3: …»); se non è lui, non confermare. Se non la trova te lo dice e non invia niente.

LEGGERE LA CHAT
I messaggi degli altri vengono letti ad alta voce, tradotti nella tua lingua se la casella è spuntata. Puoi scegliere se dire il nome, il numero della macchina o entrambi (in chat il gioco accorcia i nomi, quindi il numero di solito aiuta).
Se un messaggio contiene il tuo numero o il tuo cognome, inizia con «Per te».
Mentre parli o confermi, i messaggi in arrivo aspettano il loro turno.

MODALITÀ PROVA
Con questa casella spuntata tutto funziona uguale, ma non si invia niente in chat. Utile per esercitarsi senza disturbare nessuno.

BUONO A SAPERSI
• Il riconoscimento vocale funziona sul tuo computer, senza internet.
• Le traduzioni e la voce usano internet. Senza internet parla con la voce di Windows e la traduzione in inglese è più semplice.
• Se non senti niente, controlla «Uscita della voce». Se non ti capisce, controlla «Microfono».""",

    "de": """LMU CHAT RADIO — SO FUNKTIONIERT ES

VOR DEM START
1. Wähle deine Sprache.
2. Klicke auf „Festlegen…“ und drücke dann die Lenkradtaste oder die Taste, die du benutzen willst. Am besten eine, die du im Spiel nicht brauchst.
3. Wähle dein Mikrofon und wo du die Stimme hören willst, und klicke auf „Stimme testen“.
4. Starte Le Mans Ultimate. Wenn das Programm es findet, siehst du „LMU ✓“. Es funktioniert gleich im Vollbild, im Fenster oder randlos: Es zeichnet nichts über das Spiel.

IM CHAT SCHREIBEN
1. Drück deine Taste: Du hörst einen Piepton. Sprich.
2. Drück sie noch einmal, um fertig zu werden.
3. Das Programm wiederholt laut, was es verstanden hat.
4. Wenn es stimmt, drück die Taste, bevor die Wartezeit abläuft, und es wird gesendet. Wenn nicht, hörst du „Nachricht nicht gesendet“ und nichts geht raus.

Beispiele:
• „Sag Auto 33 sorry“ → #33 Fahrername: Sorry
• „Viel Glück an alle“ → Good luck everyone

Wenn du eine Startnummer sagst, sucht das Programm, wer das Auto fährt, und fügt den Namen hinzu. Gibt es die Nummer auf dem Server doppelt oder gar nicht, schreibt es nur die Nummer, damit nie der falsche Fahrer genannt wird.

AN WEN GEHT DIE NACHRICHT
Oft kennst du die Nummer der anderen nicht. Kein Problem: sag, wo er ist.
• „Sag dem vor mir…“ / „Sag dem hinter mir…“ → das Auto direkt vor oder hinter dir auf der Strecke.
• „Sag dem vor mir in LMP2…“ → das nächste LMP2 vor dir (Hypercar, LMP2, LMP3 und GT3).
• „Sag dem, der mich gerade überholt hat…“ → der Letzte, der dich überholt hat (gilt eine Minute).
• „Sag dem Dritten…“ → der Dritte DEINER Klasse. „Sag dem Dritten in Hypercar…“ → der Dritte dieser Klasse. „…gesamt“ → im ganzen Rennen.
• „Sag dem auf Platz 15…“ → wie „dem Fünfzehnten“, nur leichter zu sagen.

ACHTUNG, DAS IST NICHT DASSELBE!
• „Sag der 15…“ → das Auto mit der STARTNUMMER 15.
• „Sag dem auf Platz 15…“ → der FÜNFZEHNTE.

Alles wird in dem Moment berechnet, in dem du die Taste drückst: auch wenn er dich danach überholt, geht die Nachricht an dieses Auto. Beim Wiederholen sagt das Programm Nummer und Klasse („An Nummer 33, GT3: …“); ist er es nicht, bestätige nicht. Findet es das Auto nicht, sagt es das und sendet nichts.

CHAT VORLESEN
Nachrichten der anderen werden vorgelesen, in deine Sprache übersetzt, wenn das Kästchen angehakt ist. Du kannst wählen, ob der Name, die Startnummer oder beides gesagt wird (das Spiel kürzt die Namen im Chat, die Nummer hilft meistens).
Enthält eine Nachricht deine Nummer oder deinen Nachnamen, beginnt sie mit „Für dich“.
Während du sprichst oder bestätigst, warten neue Nachrichten, bis sie dran sind.

TESTMODUS
Mit diesem Kästchen funktioniert alles gleich, aber nichts wird in den Chat gesendet. Gut zum Üben, ohne jemanden zu stören.

GUT ZU WISSEN
• Die Spracherkennung läuft auf deinem Computer, ohne Internet.
• Übersetzungen und Stimme brauchen Internet. Ohne Internet spricht die Windows-Stimme und die englische Übersetzung ist einfacher.
• Hörst du nichts, prüfe „Sprachausgabe“. Versteht es dich nicht, prüfe „Mikrofon“.""",

    "pl": """LMU CHAT RADIO — JAK UŻYWAĆ

ZANIM ZACZNIESZ
1. Wybierz swój język.
2. Kliknij „Ustaw…”, a potem naciśnij przycisk na kierownicy lub klawisz, którego chcesz używać. Najlepiej taki, którego nie używasz w grze.
3. Wybierz mikrofon i gdzie chcesz słyszeć głos, i kliknij „Test głosu”.
4. Uruchom Le Mans Ultimate. Gdy program je znajdzie, zobaczysz „LMU ✓”. Działa tak samo na pełnym ekranie, w oknie i bez ramki: nie rysuje nic na grze.

PISANIE NA CZACIE
1. Naciśnij swój przycisk: usłyszysz sygnał. Mów.
2. Naciśnij ponownie, aby zakończyć.
3. Program powtórzy na głos to, co zrozumiał.
4. Jeśli się zgadza, naciśnij przycisk, zanim minie czas oczekiwania, i wiadomość zostanie wysłana. Jeśli nie naciśniesz, usłyszysz „Wiadomość nie wysłana” i nic nie pójdzie.

Przykłady:
• „Powiedz samochodowi 33 przepraszam” → #33 Nazwisko kierowcy: Sorry
• „Powodzenia wszystkim” → Good luck everyone

Jeśli podasz numer samochodu, program sprawdzi, kto nim jedzie, i doda jego nazwisko. Jeśli numer powtarza się na serwerze albo go nie ma, napisze sam numer, żeby nigdy nie pomylić kierowcy.

DO KOGO IDZIE WIADOMOŚĆ
Często nie znasz numerów innych. Nic nie szkodzi: powiedz, gdzie jest.
• „Powiedz temu przede mną…” / „Powiedz temu za mną…” → samochód tuż przed tobą lub za tobą na torze.
• „Powiedz temu przede mną z LMP2…” → najbliższe LMP2 z przodu (Hypercar, LMP2, LMP3 i GT3).
• „Powiedz temu, który mnie wyprzedził…” → ostatni, który cię wyprzedził (ważne przez minutę).
• „Powiedz trzeciemu…” → trzeci w TWOJEJ klasie. „…z Hypercar” → w tej klasie. „…w klasyfikacji ogólnej” → w całym wyścigu.
• „Powiedz temu na pozycji 15…” → to samo co „piętnastemu”, ale łatwiej powiedzieć.

UWAGA, TO NIE TO SAMO!
• „Powiedz 15…” → samochód z NUMEREM 15.
• „Powiedz temu na pozycji 15…” → ten, który jest PIĘTNASTY.

Wszystko liczy się w chwili naciśnięcia przycisku: nawet jeśli potem cię wyprzedzi, wiadomość idzie do tego samochodu. Powtarzając, program podaje numer i klasę („Do numeru 33, GT3: …”); jeśli to nie on, nie potwierdzaj. Jeśli go nie znajdzie, powie to i nic nie wyśle.

CZYTANIE CZATU
Wiadomości innych są czytane na głos, przetłumaczone na twój język, jeśli pole jest zaznaczone. Możesz wybrać, czy podaje nazwisko, numer samochodu, czy oba (gra skraca nazwiska na czacie, więc numer zwykle pomaga).
Jeśli wiadomość zawiera twój numer lub nazwisko, zaczyna się od „Do ciebie”.
Gdy mówisz lub potwierdzasz, nowe wiadomości czekają na swoją kolej.

TRYB TESTOWY
Z tym polem wszystko działa tak samo, ale nic nie jest wysyłane na czat. Dobre do ćwiczeń bez przeszkadzania innym.

WARTO WIEDZIEĆ
• Rozpoznawanie mowy działa na twoim komputerze, bez internetu.
• Tłumaczenia i głos korzystają z internetu. Bez internetu mówi głos Windows, a tłumaczenie na angielski jest prostsze.
• Jeśli nic nie słyszysz, sprawdź „Wyjście głosu”. Jeśli cię nie rozumie, sprawdź „Mikrofon”.""",

    "pt": """LMU CHAT RADIO — COMO SE USA

ANTES DE COMEÇAR
1. Escolhe o teu idioma.
2. Clica em «Definir…» e depois carrega no botão do volante ou na tecla que queres usar. De preferência um que não uses no jogo.
3. Escolhe o microfone e onde queres ouvir a voz, e clica em «Testar voz».
4. Abre o Le Mans Ultimate. Quando o programa o encontrar vais ver «LMU ✓». Funciona igual com o jogo em ecrã inteiro, em janela ou sem bordas: não desenha nada por cima do jogo.

ESCREVER NO CHAT
1. Carrega no teu botão: vais ouvir um bip. Fala.
2. Carrega outra vez para terminar.
3. O programa repete em voz alta o que percebeu.
4. Se estiver bem, carrega no botão antes de acabar o tempo de espera e é enviado. Se não carregares, vais ouvir «Mensagem não enviada» e nada é enviado.

Exemplos:
• «Diz ao carro 33 desculpa» → #33 Nome do piloto: Sorry
• «Boa sorte a todos» → Good luck everyone

Se disseres um número de carro, o programa procura quem o conduz e junta o nome. Se o número estiver repetido no servidor, ou não aparecer, escreve só o número, para nunca trocar de piloto.

PARA QUEM VAI A MENSAGEM
Muitas vezes não sabes o número dos outros. Não faz mal: diz onde está.
• «Diz ao da frente…» / «Diz ao de trás…» → o carro logo à tua frente ou atrás de ti em pista.
• «Diz ao da frente de LMP2…» → o LMP2 mais próximo à frente (Hypercar, LMP2, LMP3 e GT3).
• «Diz ao que me acabou de ultrapassar…» → o último que te passou (vale durante um minuto).
• «Diz ao terceiro…» → o terceiro da TUA classe. «Diz ao terceiro de Hypercar…» → o terceiro dessa classe. «…da geral» → de toda a corrida.
• «Diz ao que está na posição 15…» → o mesmo que «ao décimo quinto», mas mais fácil de dizer.

ATENÇÃO, NÃO É A MESMA COISA!
• «Diz ao 15…» → o carro com o NÚMERO 15.
• «Diz ao que está na posição 15…» → o que vai em DÉCIMO QUINTO.

Tudo é calculado no momento em que carregas no botão: mesmo que depois te ultrapasse, a mensagem vai para esse carro. Ao repetir, o programa diz o número e a classe («Para o 33 de GT3: …»); se não for ele, não confirmes. Se não o encontrar, diz-to e nada é enviado.

LER O CHAT
As mensagens dos outros são lidas em voz alta, traduzidas para o teu idioma se a caixa estiver marcada. Podes escolher se diz o nome, o número do carro ou as duas coisas (no chat o jogo encurta os nomes, por isso o número costuma ajudar).
Se uma mensagem tiver o teu número ou o teu apelido, começa com «Para ti».
Enquanto falas ou confirmas, as mensagens que chegam esperam a sua vez.

MODO DE TESTE
Com essa caixa marcada tudo funciona igual, mas nada é enviado para o chat. Serve para praticar sem incomodar ninguém.

BOM SABER
• O reconhecimento de voz funciona no teu computador, sem internet.
• As traduções e a voz usam internet. Sem internet fala com a voz do Windows e a tradução para inglês é mais simples.
• Se não ouvires nada, verifica a «Saída de voz». Se não te perceber, verifica o «Microfone».""",
}
