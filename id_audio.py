import pyaudio

# Funzione per la lettura e salvataggio dispositivi di input e output
def stampa_id():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    in_device = []
    out_device = []

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            name =  p.get_device_info_by_host_api_device_index(0, i).get('name')
            out_device.append((i,name))


    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            name =  p.get_device_info_by_host_api_device_index(0, i).get('name')
            in_device.append((i,name))
    p.terminate()
    return in_device, out_device

