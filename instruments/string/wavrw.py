import numpy as np
import scipy.io.wavfile

def read(file):
    rate, data = scipy.io.wavfile.read(file)
    print(
        "scipy.io.wavfile.read(" + file + ") -> " 
        + str(rate) + " Hz, " + 
        str(data.shape)
    )
    return data[:,0] + data[:,1]

def write(file,data,fs=44100):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = fs,
        data = scaled_data.astype(np.int16)
    )
