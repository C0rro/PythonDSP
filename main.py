import numpy as np
import pyaudio
import threading
from loadData import loadData
from audioFiltering import audioFiltering

CHUNK = 128
RATE = 48000

# Inizializza PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32,  
                channels=2,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=0,    
                output_device_index=2,   
                frames_per_buffer=CHUNK)

# Carica i dati del filtro
filter_data_left = loadData("L")
filter_data_rigth = loadData("R")

def funzione_pass_through():
    data = stream.read(CHUNK, exception_on_overflow=False)
    stream.write(data)

def funzione_filtrata():
    data_bytes = stream.read(CHUNK, exception_on_overflow=False)
    
    # Converti bytes in array NumPy scrivibile
    data_array = np.frombuffer(data_bytes, dtype=np.int32).reshape(-1, 2).copy()

    # Applica i filtri
    filtered_audio = audioFiltering(data_array, filter_data_left, filter_data_rigth)

    # Scrivi sull'output
    stream.write(filtered_audio.astype(np.int32).tobytes())

# Variabile per la funzione corrente, inizialmente pass-through
funzione_corrente = funzione_pass_through

# Thread per input utente 
def input_thread():
    global funzione_corrente
    while True:
        user_input = input("Premi 'f' per filtrare, 'p' per pass-through: ").strip()
        if user_input == 'f':
            funzione_corrente = funzione_filtrata
            print("Modalità FILTRATA attivata")
        elif user_input == 'p':
            funzione_corrente = funzione_pass_through
            print("Modalità PASS-THROUGH attivata")

# Avvio thread per input
thread = threading.Thread(target=input_thread, daemon=True)
thread.start()

# Loop principale
try:
    while True:
        funzione_corrente()
except KeyboardInterrupt:
    print("\nInterruzione manuale ricevuta. Chiudo stream...")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

