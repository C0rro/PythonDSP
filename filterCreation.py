import scipy
import numpy as np

#def build_sos(filter_data_left, filter_data_right, iir_left, iir_right):
    #sos_left, sos_right = [], []

    #Per ogni filtro creo gli array a e b per calcolare i filtri
#    for i in range(0, len(filter_data_left), 5):
#        bL = [filter_data_left[i], filter_data_left[i+1], filter_data_left[i+2]]
#        aL = [1, -filter_data_left[i+3], -filter_data_left[i+4]]
 #       bR = [filter_data_right[i], filter_data_right[i+1], filter_data_right[i+2]]
 ##       aR = [1, -filter_data_right[i+3], -filter_data_right[i+4]]
        #Creo i filtri usanso tf2sos
#        iir_left.add_sos(scipy.signal.tf2sos(bL, aL))
 #       iir_right.add_sos(scipy.signal.tf2sos(bR, aR))
    #Ritorno gli array in stack per renderli compatibili con la matrice dell'audio
    #return np.vstack(sos_left), np.vstack(sos_right)

def build_sos(filter_data, iir_stereo):


    #Per ogni filtro creo gli array a e b per calcolare i filtri
    for i in range(0, len(filter_data), 5):
        b = [filter_data[i], filter_data[i+1], filter_data[i+2]]
        a = [1, -filter_data[i+3], -filter_data[i+4]]
        
        #Creo i filtri usanso tf2sos
        iir_stereo.add_sos(scipy.signal.tf2sos(b, a))
    

