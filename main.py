import numpy as np
import pyaudio
import threading
from loadData import loadData, get_files_name
from flask import Flask, render_template_string, request, redirect, url_for

from filterCreation import build_sos
from iir import IIR
from idAudio import stampa_id

def inizializzo_filtri(file_name):

    global rate

    # Carica i dati del filtro
    filter_data = loadData(file_name)

    #Creo oggetto IIR
    iir_stereo = IIR(2, rate)

    #aggiungo filtri sos a IIR
    build_sos(filter_data, iir_stereo)
    return iir_stereo

def apertura_stream_audio(id_in, id_out, chunk, rate):
    # Inizializza PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt32,  
                channels=2,
                rate=rate,
                input=True,
                output=True,
                input_device_index=id_in,    
                output_device_index=id_out,   
                frames_per_buffer=chunk)
    return p, stream 
    

def funzione_pass_through(stream, chunk):
    data = stream.read(chunk, exception_on_overflow=False)
    stream.write(data)

def funzione_filtrata(stream, chunk, iir_stereo):
    data_bytes = stream.read(chunk, exception_on_overflow=False)

    # Converti in float32
    data_array = np.frombuffer(data_bytes, dtype=np.int32).reshape(-1, 2).astype(np.float32)

    filtered_audio = iir_stereo.filter(data_array)
    # Scrivi sullo stream
    stream.write(filtered_audio.astype(np.int32).tobytes())



# Variabili globali
funzione_corrente = funzione_pass_through
stream = None
p = None
chunk = 0
rate = 0
iir_stereo = None
audio_running = False



app = Flask(__name__)

start_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Audio Setup</title>
</head>
<body>
  <div align="center">
    <h1>Configurazione Audio</h1>
    <form action="/start" method="post">
      <label>Dispositivo Input:</label><br>
      <select name="input_id" required>
        {% for id, name in input_devices %}
          <option value="{{ id }}">{{ id }} - {{ name }}</option>
        {% endfor %}
      </select><br><br>

      <label>Dispositivo Output:</label><br>
      <select name="output_id" required>
        {% for id, name in output_devices %}
          <option value="{{ id }}">{{ id }} - {{ name }}</option>
        {% endfor %}
      </select><br><br>

      <label for="file_name">File filtro:</label><br>
        <select name="file_name" id="file_name" required>
        {% for name in files %}
        <option value="{{ name }}">{{ name }}</option>
        {% endfor %}
       </select><br><br>

      <label>Buffer Size (chunk):</label><br>
      <input type="number" name="chunk" value="1024" min="128" required><br><br>

      <label>Sample Rate (Hz):</label><br>
      <input type="number" name="rate" value="48000" min="8000" required><br><br>


      <button type="submit">Avvia</button>
    </form>
  </div>
</body>
</html>
"""

on_off_page = """
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
  <form action="/stop" method="post">
    <button type="submit" style="margin-top:20px;">Stop stream</button>
</form>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    input_devices, output_devices = stampa_id()
    files = get_files_name()
    
    return render_template_string(start_page, input_devices=input_devices, output_devices=output_devices, files=files)


@app.route("/start", methods=["POST"])
def start():
    global p, stream, chunk, rate, iir_stereo, audio_running

    id_in = int(request.form["input_id"])
    id_out = int(request.form["output_id"])
    chunk = int(request.form["chunk"])
    rate = int(request.form["rate"])
    file_name = request.form["file_name"]
    audio_running = True

    iir_stereo = inizializzo_filtri(file_name)
    p, stream = apertura_stream_audio(id_in, id_out, chunk, rate)

    # Avvia thread audio
    threading.Thread(target=loop_audio, daemon=True).start()

    return redirect(url_for("control"))


@app.route("/control")
def control():
    return render_template_string(on_off_page, mode=("Filtrato" if funzione_corrente == funzione_filtrata else "Pass-Through"))

@app.route("/mode/pass", methods=["POST"])
def set_pass():
    global funzione_corrente
    funzione_corrente = funzione_pass_through
    return redirect(url_for("control"))

@app.route("/mode/filter", methods=["POST"])
def set_filter():
    global funzione_corrente
    funzione_corrente = funzione_filtrata
    return redirect(url_for("control"))

@app.route("/stop", methods=["POST"])
def stop_audio():
    global audio_running, stream, p
    audio_running = False  

    # Chiudi stream in sicurezza
    try:
        if stream:
            stream.stop_stream()
            stream.close()
            stream = None
        if p:
            p.terminate()
            p = None
    except Exception as e:
        print("Errore chiusura:", e)

    return redirect(url_for("index"))



#main loop applicazione
def loop_audio():
    global funzione_corrente, stream, chunk, iir_stereo
    try:
        while audio_running:
            if funzione_corrente == funzione_pass_through:
                funzione_pass_through(stream, chunk)
            else:
                funzione_filtrata(stream, chunk, iir_stereo)
    except Exception as e:
        print("Audio loop interrotto:", e)
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        if p:
            p.terminate()

# Thread Flask
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


