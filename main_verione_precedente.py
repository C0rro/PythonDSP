import numpy as np
import soundfile as sf
import pyaudio
import scipy 
from loadData import loadData
from audioFiltering import audioFiltering

CHUNK = 128
RATE = 48000



#input audio 
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32,  
                channels=2,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=2,    
                output_device_index=1,   
                frames_per_buffer=CHUNK)

# Carica i dati del filtro
filter_data = loadData()

try:
    if input == 'f':
        while True:
            data_bytes = stream.read(CHUNK, exception_on_overflow=False)
        
            # Converti bytes in array NumPy scrivibile
            data_array = np.frombuffer(data_bytes, dtype=np.int32).reshape(-1, 2).copy()

            # Applica i filtri
            filtered_audio = audioFiltering(data_array, filter_data, 2)
        
            # Scrivi sull'output
            stream.write(filtered_audio.astype(np.int32).tobytes())
    else: 
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            stream.write(data)
    
except KeyboardInterrupt:
    print("\nInterruzione manuale ricevuta. Chiudo stream...")

