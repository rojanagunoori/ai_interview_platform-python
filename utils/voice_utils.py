import speech_recognition as sr
import pyttsx3
import threading
import queue


# Global shared state
speech_queue = queue.Queue()
engine = pyttsx3.init()
stop_speaking_flag = False
voice_thread = None
stop_event = threading.Event()

def speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            if stop_event.is_set():
                stop_event.clear()
                continue
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("[ERROR] Speaking failed:", e)
        speech_queue.task_done()

# Initialize speech thread once
def init_speech_thread():
    global speech_thread_started
    if not speech_thread_started:
        threading.Thread(target=speech_worker, daemon=True).start()
        speech_thread_started = True

def speak(text):
    if text not in list(speech_queue.queue):
        speech_queue.put(text)

def stop_speaking():
    stop_event.set()
    engine.stop()

def speak1(text):
    global stop_speaking_flag, voice_thread
    def _speak():
        global stop_speaking_flag
        engine.say(text)
        engine.runAndWait()
    #threading.Thread(target=_speak).start()
    # Stop previous thread if running
    if voice_thread and voice_thread.is_alive():
        stop_speaking1()
    
    stop_speaking_flag = False
    voice_thread = threading.Thread(target=_speak)
    voice_thread.start()


def stop_speaking1():
    global stop_speaking_flag
    engine.stop()
    stop_speaking_flag = True

def listen(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return recognizer.recognize_google(audio)
