import scipy.signal

def audioFiltering(filtered_audio, filter_data, channels):
    #Applica i filtri in cascata
    for i in range(0,len(filter_data),5):
        #Crea il filtro peak
        b = [filter_data[i], filter_data[i+1], filter_data[i+2]]
        #inverto i segni dei coefficienti a per compensare la differenza tra le notazioni REW e scipy.signal.lfilter
        a = [1, -filter_data[i+3], -filter_data[i+4]]
        #applico il filtro
        for ch in range(channels):
            filtered_audio[:, ch] = scipy.signal.lfilter(b, a, filtered_audio[:, ch])
            #print(f"Filtro {i//5 + 1} applicato")

    return filtered_audio