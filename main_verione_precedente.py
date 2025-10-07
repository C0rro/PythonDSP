import numpy as np
import pyaudio
import threading
import scipy
from loadData import loadData
from flask import Flask, render_template_string
from audioFiltering import audioFiltering
from filterCreation import build_sos
from iir import IIR


CHUNK = 1024
RATE = 48000


# Inizializza PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32,  
                channels=2,
                rate=RATE,
                input=True,
                output=True,
                input_device_index=2,    
                output_device_index=2,   
                frames_per_buffer=CHUNK)

# Carica i dati del filtro
filter_data_left = loadData("L")
filter_data_right = loadData("R")
filter_data = loadData("2_LR")

#Creo i filtri
#sos_left, sos_right = build_sos(filter_data_left, filter_data_right)

iir_left = IIR(2, RATE)
iir_right = IIR(2, RATE)

iir_stereo = IIR(2, RATE)

#aggiungo filtri sos
#build_sos(filter_data_left, filter_data_right, iir_left, iir_right)
build_sos(filter_data, iir_stereo)

#Inizzializzo i filtri
#A typical use of this function is to set the initial state so that the output of the filter starts at the same value as the first element of the signal to be filtered.
#zi_left = scipy.signal.sosfilt_zi(sos_left)
#zi_right = scipy.signal.sosfilt_zi(sos_right)


def funzione_pass_through():
    data = stream.read(CHUNK, exception_on_overflow=False)
    stream.write(data)

def funzione_filtrata():
    data_bytes = stream.read(CHUNK, exception_on_overflow=False)

    # Converti in float32
    data_array = np.frombuffer(data_bytes, dtype=np.int32).reshape(-1, 2).astype(np.float32)

    filtered_audio = iir_stereo.filter(data_array)
    # Scrivi sullo stream
    stream.write(filtered_audio.astype(np.int32).tobytes())




# Variabile per la funzione corrente, inizialmente pass-through
funzione_corrente = funzione_pass_through


app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Audio Control</title>
</head>
<body>
    <div align= center>
  <h1>Controllo Audio</h1>
  <p>Modalità corrente: <b>{{ mode }}</b></p>
  <form action="/mode/pass" method="post">
    <button type="submit">Pass-Through</button>
  </form>
  <form action="/mode/filter" method="post">
    <button type="submit">Filtrato</button>
  </form>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE, mode=("Filtrato" if funzione_corrente == funzione_filtrata else "Pass-Through"))

@app.route("/mode/pass", methods=["POST"])
def set_pass():
    global funzione_corrente
    funzione_corrente = funzione_pass_through
    return index()

@app.route("/mode/filter", methods=["POST"])
def set_filter():
    global funzione_corrente
    funzione_corrente = funzione_filtrata
    return index()


# Thread Flask
def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

# Avvia server web
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Ciclo principale audio
try:
    while True:
        funzione_corrente()
except KeyboardInterrupt:
    print("\nStop manuale.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
