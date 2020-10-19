import scipy.io.wavfile
import instruments.guitar
import pysound
import numpy as np

def write(file,data):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = pysound.fs,
        data = scaled_data.astype(np.int16)
    )


guitar = instruments.guitar.Guitar()
pluck = guitar.pluck(3.5,3,0)

write("out.wav",pluck)
