import speech_recognition as sr
import pyttsx3
import webbrowser
from ytmusicapi import YTMusic
from pynput.keyboard import Controller, Key
import os
import time

# Inicializa YTMusic
ytmusic = YTMusic()

# Inicializa el reconocedor de voz
r = sr.Recognizer()

engine = pyttsx3.init()
velocidad_de_voz = 160
engine.setProperty('rate', velocidad_de_voz)

# Inicializa el controlador del teclado
keyboard = Controller()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Escuchando...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-MX').lower()
            print(f"Reconocido: {text}")
        except sr.UnknownValueError:
            text = None
        except sr.RequestError as e:
            speak("Error de servicio; por favor intenta de nuevo.")
            text = None
        return text
    
def play_song(song_name):
    global indice_cancion_actual
    # Cierra la pestaña actual (Edge o Chrome)
    os.system("taskkill /im msedge.exe /f")  # Para Edge y os.system("taskkill /im chrome.exe /f") # Para Chrome.
    time.sleep(2)  # Espera un poco para asegurarte de que la pestaña se ha cerrado
    # Busca la canción en YouTube Music
    results = ytmusic.search(query=song_name, filter='songs')
    if results:
        song_id = results[0]['videoId']
        webbrowser.open(f'https://music.youtube.com/watch?v={song_id}')
        speak(f"Reproduciendo {song_name}, en YouTube Music")
        indice_cancion_actual = canciones.index(song_name)
    else:
        speak(f"No se encontró la canción {song_name}")
        
def pause_playback():
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    speak("Reproducción pausada")

def play_playback():
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    speak("Reproducción reanudada")

canciones = []
indice_cancion_actual = 0

def play_next_song():
    global indice_cancion_actual
    if indice_cancion_actual + 1 < len(canciones):
        indice_cancion_actual += 1
        play_song(canciones[indice_cancion_actual])
    else:
        speak("No hay más canciones en la lista")

numeros = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10
}

while True:
    command = listen()
    if command:
        if command == 'alexa genera una lista':
            speak("¿Cuántas canciones te gustaría agregar?")
            num_canciones = listen()
            try:
                num_canciones = numeros[num_canciones]
                for i in range(num_canciones):
                    speak(f"¿Cuál es la canción número {i+1} que te gustaría agregar?")
                    song_command = listen()
                    if song_command:
                        canciones.append(song_command)
                play_song(canciones[0])
            except KeyError:
                speak("Lo siento, no entendí el número de canciones. Intenta de nuevo.")
        elif command == 'alexa quiero escuchar':
            speak("¿Qué canción te gustaría escuchar?")
            song_command = listen()
            if song_command:
                canciones.append(song_command)
                play_song(song_command)
        elif command == 'alexa pausa':
            pause_playback()
        elif command == 'alexa play':
            play_playback()
        elif command == 'alexa siguiente':
            play_next_song()