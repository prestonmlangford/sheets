import numpy as np
fs = 44100


def add(track,time,clip):
    if time < 0:
        raise ValueError("time must be greater than zero")
    
    t = int(time*fs)
    cs = clip.shape[0]
    ts = track.shape[0]
    
    if t + cs > ts:
        ds = t + cs - ts
        z = np.zeros((ds,))
        track = np.concatenate((track,z))
        
    track[t:t + cs] += clip