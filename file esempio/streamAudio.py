import pyaudio

CHUNK = 128
RATE = 48000

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32,  
                channels=2,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=0,    # tuo device di input
                output_device_index=2,   # tuo device di output
                frames_per_buffer=CHUNK)

print("Streaming audio... premi Ctrl+C per interrompere.")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        stream.write(data)
except KeyboardInterrupt:
    print("\nInterruzione manuale ricevuta. Chiudo stream...")

stream.stop_stream()
stream.close()
p.terminate()

