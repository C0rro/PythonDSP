import soundfile as sf
import pyaudio
import scipy 

file_name = "pinknoise_stereo.wav"
filter_name = "IIR_Eq1.1-48k.wav"

# Carica il file come array NumPy di float32
data, samplerate = sf.read(file_name, dtype="float32")
channels = data.shape[1] if data.ndim > 1 else 1  # gestisce mono/stereo

# Carica il filtro come array NumPy di float32
filter_data, filter_samplerate = sf.read(filter_name, dtype="float32")

#effettuo convoluzione
filtered_audio = scipy.signal.convolve(data, filter_data, mode='same', method='fft')

# Inizializza PyAudio
p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paFloat32,   # perché i dati sono float32
    channels=channels,
    rate=samplerate,
    output=True
)

print("Riproduzione audio NON filtrato...")
print(channels)
print(data.shape)
stream.write(data.tobytes())  # converte l'array in bytes per PyAudio
print("Finito.")

print("Riproduzione audio filtrato...")
print(channels)
print(data.shape)
stream.write(filtered_audio.tobytes())  # converte l'array in bytes per PyAudio
print("Finito.")

stream.stop_stream()
stream.close()
p.terminate()
