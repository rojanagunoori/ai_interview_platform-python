from gtts import gTTS
import pygame
import tempfile
import time
import os
import threading
import speech_recognition as sr

# Initialize pygame mixer
if os.environ.get("RENDER") is None:
    pygame.mixer.init()
#pygame.mixer.init()
stop_playback = False

def speak(text):
    global stop_playback
    stop_playback = False

    def play():
        try:
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                tts.save(fp.name)
                pygame.mixer.music.load(fp.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    if stop_playback:
                        pygame.mixer.music.stop()
                        break
                    time.sleep(0.1)
        except Exception as e:
            print(f"[ERROR] TTS failed: {e}")

    threading.Thread(target=play, daemon=True).start()

def stop_speaking():
    global stop_playback
    stop_playback = True
    pygame.mixer.music.stop()


def listen(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return recognizer.recognize_google(audio)
