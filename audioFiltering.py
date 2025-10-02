import scipy.signal

def audioFiltering(filtered_audio, filter_data_left, filter_data_right):
    
    if len(filter_data_right)!=len(filter_data_left):
        IndexError
    #Applica i filtri in cascata
    for i in range(0,len(filter_data_left),5):
        #Crea il filtro peak
        bL = [filter_data_left[i], filter_data_left[i+1], filter_data_left[i+2]]
        #inverto i segni dei coefficienti a per compensare la differenza tra le notazioni REW e scipy.signal.lfilter
        aL = [1, -filter_data_left[i+3], -filter_data_left[i+4]]

        #stessa cosa per il canale destro
        bR = [filter_data_right[i], filter_data_right[i+1], filter_data_right[i+2]]
        aR = [1, -filter_data_right[i+3], -filter_data_right[i+4]]


        #applico il filtro, [i, 0] canale sinistro [i, 1] canale destro
        filtered_audio[:, 0] = scipy.signal.lfilter(bL, aL, filtered_audio[:, 0])
        filtered_audio[:, 1] = scipy.signal.lfilter(bR, aR, filtered_audio[:, 1])
            

    return filtered_audio