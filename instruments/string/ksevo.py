import math
import numpy as np
import scipy.signal as sig


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


def nburst(n,alpha=0.1):
    return alpha*np.random.randn(n)

def ks(b,a,f):
    fs = 44100
    nb = int(0.01*fs)
    x = nburst(nb)
    d = f/fs
    fw = b
    bk = lagdel(d,a)
    return sig.lfilter(fw,bk,x)

