# LMU Chat Radio

Talk to the **Le Mans Ultimate** chat with a button on your wheel, and **hear** what the others write — translated into your language.

Free, and it always will be.

> ### ⚠️ The first time you run it, it downloads ~500 MB
> LMU Chat Radio understands your voice **on your own PC**, without sending your audio anywhere. For that it needs a speech recognition model that is too big to fit in the ZIP, so **the first launch downloads it** (about 500 MB, once).
> While it downloads, the window says *"Downloading speech recognition (first time only, about 500 MB)…"*. Depending on your connection it can take from a few seconds to several minutes. **It is not frozen — wait until it says "Ready".** From then on it starts in a few seconds, even without internet.

## What it does

**Write in the chat without letting go of the wheel.** Press your button, speak, press again. The program reads back what it understood, and if you press once more within a few seconds, it sends it. If you don't, it says *"Message not sent"* and nothing goes out — so a misheard sentence never reaches the server.

- *"Tell car 33 I'm sorry"* → `#33 Driver Name: I'm sorry`
- *"Good luck everyone"* → `Good luck everyone`

When you name a car number, it looks up who is driving it and adds their name. If that number is duplicated in the server (it happens in public lobbies) or isn't there, it writes only the number — it never names the wrong driver.

**Don't know their number? Say where they are.** In the game you rarely see other drivers' numbers, so you can also say:

- *"Tell the car in front…"* / *"Tell the car behind…"* — the car right ahead of or behind you on track. *"…in LMP2"* to pick a class.
- *"Tell who just overtook me…"* — the last car that passed you.
- *"Tell the third…"* — third in **your** class; *"the third in Hypercar"*, *"…overall"*.
- *"Tell the car in position 15…"* — easier to say than "fifteenth".

Careful: *"Tell 15…"* is the car with **number** 15; *"Tell the car in position 15…"* is the one running **fifteenth**.
Everything is captured **the moment you press the button**, so it doesn't matter if they pass you while you speak and confirm. The read-back tells you who it found (*"To car 33, GT3: …"*) — if it's not them, just don't confirm.

**Questions stay questions.** Speech recognition hears the words but not the intonation; the program adds the question mark when the sentence is a question (*"Are you OK?"*), and *"ask car 33 if…"* works too.

**Hear the chat.** Messages from other drivers are read aloud through your headset. You choose whether it says the driver's name, the car number and class, or both — useful because the game shortens names in the chat. If a message mentions your number or your surname, it starts with *"For you"*.

**Translation, both ways, optional.** You speak in your language and it writes in English. What others write is translated into your language. Each direction can be switched off.

**Works in fullscreen.** It draws nothing on top of the game and doesn't simulate key presses: it talks to the game through the game's own local web interface. Fullscreen, windowed or borderless — it makes no difference.

**Your button or your key.** Any button of any wheel, button box or controller, or any keyboard key.

**Seven languages:** English, Español, Français, Italiano, Deutsch, Polski, Português. Window, instructions and voice.

**Volume controls** for the voice and for the beeps, separately, right in the window.

**Test mode** (on by default): everything works but nothing is sent, so you can practise without bothering anyone. Untick it when you're ready.

## Install

1. Download the ZIP from [Releases](https://github.com/ani3dgr/lmu-chat-radio/releases).
2. Unzip it anywhere (not inside *Program Files*).
3. Run `LMUChatRadio.exe` and **wait for the first download** (see above).
4. Click **Set…** and press the button you want to use. Pick your microphone and voice output. Click **Instructions** for the rest.

**Update:** unzip the new version on top of the old folder. Your settings and the downloaded model are kept.

## Good to know

- **Speech recognition is local** ([Whisper](https://github.com/SYSTRAN/faster-whisper), *small* model, on the CPU). Your voice never leaves your PC.
- **Translation and the voice use the internet** (Google Translate and Microsoft Edge voices). Without internet it speaks with the Windows voice and the English translation is done by the speech model, which is simpler.
- If the game window loses focus, Windows stops the force feedback until you click back into the game. LMU Chat Radio starts minimised when the game is in front, so it doesn't steal it.

## From the source

Python 3.12 on Windows: `pip install faster-whisper sounddevice pygame edge-tts pywin32 numpy`, then `python chat_lmu.py`. `python compilar.py` builds the `.exe` and the ZIP (PyInstaller).

## Support

If it's useful to you and you feel like chipping in: [☕ Buy me a coffee (PayPal)](https://paypal.me/ani3dgr).
And if you also ride a real bike, have a look at **[CicloTracker](https://ciclotracker.com)** — GPS for your bike on Google Play. Supporting it helps us keep building projects like this one.

Also by the same author: [Track Map for Le Mans Ultimate](https://github.com/ani3dgr/mapa-lmu).

## License

GPL-3.0
