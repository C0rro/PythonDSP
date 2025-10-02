import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

b = [0.998445, -1.99688, 0.998445]
a = [1.0, -1.99688, 0.996891]

w, h = freqz(b, a, worN=4096, fs=48000)  # fs = frequenza di campionamento

plt.semilogx(w, 20*np.log10(abs(h)))
plt.title("Risposta in frequenza del biquad1")
plt.xlabel("Frequenza [Hz]")
plt.ylabel("Ampiezza [dB]")
plt.grid()
plt.show()
