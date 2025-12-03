import scipy



def build_sos(filter_data, iir_stereo):


    #Per ogni filtro creo gli array a e b per calcolare i filtri
    for i in range(0, len(filter_data), 5):
        b = [filter_data[i], filter_data[i+1], filter_data[i+2]]
        a = [1, -filter_data[i+3], -filter_data[i+4]]
        
        #Creo i filtri usanso tf2sos
        iir_stereo.add_sos(scipy.signal.tf2sos(b, a))
    

