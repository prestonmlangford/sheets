import math
import numpy as np
import scipy.signal as sig
from wavrw import read, write, fs

# https://ccrma.stanford.edu/~jos/Interpolation/Explicit_Formula_Lagrange_Interpolation.html
def lagdel(d,N=10):
    w = math.floor(d)
    f = d - w
    print(w)
    print(f)
    # discrete delay
    dd = np.zeros((w))
    dd[-1] = 1

    # fractional delay (lagrange)
    fd = np.ones((N+1))
    for n in range(N+1):
        for k in range(N+1):
            if k == n:
                continue
            else:
                fd[n] *= (f-k)/(n-k)
    
    return sig.convolve(dd,fd)

def lindel(d):
    w = math.floor(d)
    f = d - w
    print(w)
    print(f)
    # discrete delay
    dd = np.zeros((w))
    dd[-1] = 1

    # fractional delay (linear)
    fd = np.zeros((2))
    fd[0] = 1 - f
    fd[1] = f

    return sig.convolve(dd,fd)



def shift(x,arr):
    arr[1:] = arr[:-1]
    arr[0] = x


def ks(h,f,t,burst_len=(0.01*fs)):
    n = t*fs
    d = lindel(fs/f-len(h)/2)
    fw = np.zeros(len(h))
    bk = np.zeros(len(d))
    y = np.zeros((n))
    for i in range(n):
        fb = np.sum(d*bk)
        if i < burst_len:
            r = np.random.randn()
            x = r + fb
        else:
            x = fb
        shift(x,fw)
        y[i] = np.sum(h*fw)
        shift(y[i],bk)
    return y

n = 30
lp = 0.999*np.ones((n))/n
ap = [0.999]
pluck = ks(lp,196,4)
write("pluck.wav",pluck)