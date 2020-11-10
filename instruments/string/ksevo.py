import math
import numpy as np
import scipy.signal as sig
from wavrw import read, write

fs = 44100

# https://ccrma.stanford.edu/~jos/Interpolation/Explicit_Formula_Lagrange_Interpolation.html
def lagdel(d,h,N=10):
    w = math.floor(d)
    f = d - w
    
    # discrete delay
    dd = np.zeros((w))
    dd[-1] = 1
    
    # fractional delay
    fd = np.zeros((N+1))+1
    for n in range(N+1):
        for k in range(N+1):
            if k == n:
                continue
            else:
                fd[n] *= (f-k)/(n-k)
    
    delay = sig.convolve(dd,fd)
    return sig.convolve(delay,h)


def nburst(n,alpha=0.1,duration=0.01):
    bl = int(duration*fs)
    noise = alpha*np.random.randn(bl)
    result = np.zeros((n))
    result[0:bl] = noise
    return result

def ks(b,a,f,t):
    x = nburst(t*fs)
    d = fs/f
    fw = b
    bk = lagdel(d,a)
    bk *= 0.95
    bk[0] = 1
    
    return sig.lfilter(fw,bk,x)

lp=sig.firwin(1000,10000,fs=fs)
hp=sig.firwin(999,10000,fs=fs,pass_zero=False)
boing=ks(hp,lp,440,4)

write("boing.wav",boing)