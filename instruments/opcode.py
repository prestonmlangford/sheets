import pysound
import numpy as np

def linen(signal,rise,decay):
    fs = pysound.fs
    ss = signal.shape[0]
    rs = int(rise*fs)
    ds = int(decay*fs)
    
    if rs > ss:
        raise ValueError("Rise time exceeds signal duration")
    
    if ds > ss:
        raise ValueError("Decay time exceeds signal duration")
    
    signal[0:rs] *= np.linspace(0,1,rs)
    signal[ss-ds:] *= np.linspace(1,0,ds)
