import scipy.signal
import numpy as np


def audioFiltering(filtered_audio, zi_left, zi_right, sos_left, sos_right):
    
    filtered_left, zi_left = scipy.signal.sosfilt(sos_left, filtered_audio[:, 0], zi=zi_left)
    filtered_right, zi_right = scipy.signal.sosfilt(sos_right, filtered_audio[:, 1], zi=zi_right)
    return np.column_stack((filtered_left, filtered_right))