import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import scipy.io.wavfile
import scipy.signal
from scipy import signal
fs = 44100

def normalize(x):
    return x/(0.00001+np.linalg.norm(x))

class Delay:
    def __init__(self,d):
        self.d = d
        self.k = math.floor(d) + 1
        self.buf = np.zeros((self.k))
        self.i = 0
        self.r = self.d - self.k
    
    def next(self):
        return (
            self.buf[self.i]*(1 - self.r) + 
            self.buf[self.i]*self.r
        )

    def store(self,x):
        self.buf[self.i] = x
        self.i = (self.i + 1) % self.k
        
    def reset(self):
        self.buf = np.zeros((self.k))
        self.i = 0

class FIR:
    def __init__(self,order):
        self.p = order
        self.buf = np.zeros((self.p))
        self.h = np.random.randn(self.p)*0.01#signal.firwin(self.p,10000,fs=fs)#
        
    def filter(self,x):
        self.buf[1:] = self.buf[:-1]
        self.buf[0] = x
        return np.dot(self.h.T,self.buf)
    
    def reset(self):
        self.buf = np.zeros((self.p))
    
    def xnorm(self):
        return normalize(self.buf)
  

def breakpoint():
    if input("Continue? [y/n]: ") == "n":
        exit(0)
        
def freqz(b):
    w, h = signal.freqz(b)
    fig, ax1 = plt.subplots()
    ax1.set_title('Digital filter frequency response')
    ax1.plot(w, 20 * np.log10(abs(h)), 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('Frequency [rad/sample]')
    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(h))
    ax2.plot(w, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()
    ax2.axis('tight')
    plt.show()
    return w,h

def filter(num,den,signal):
    return scipy.signal.lfilter(num,den,signal,axis=0)


def read(file):
    rate, data = scipy.io.wavfile.read(file)
    print(
        "scipy.io.wavfile.read(" + file + ") -> " 
        + str(rate) + " Hz, " + 
        str(data.shape)
    )
    s = data[:,0] + data[:,1]
    n = len(s)
    energy = np.dot(s.T,s)
    return normalize(s)

def write(file,data):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = fs,
        data = scaled_data.astype(np.int16)
    )

ideal = read("ideal.wav")
print(ideal)
samples = ideal.shape[0]
burst = np.zeros((samples))
#burstlen = int(0.01*fs)
#burst[0:burstlen] = np.random.randn(burstlen)
burst[0] = 1
y = np.zeros((samples))
pa = 100
pb = 100
fa = FIR(pa)
fb = FIR(pb)
ff = 196
d = Delay(fs/ff)
err = 1
mua = 1
mub = 1


plt.ion()

while err > 0.00001:
    err = 0
    fa.reset()
    fb.reset()
    d.reset()
    ea = np.zeros((pa))
    eb = np.zeros((pb))
    for i in range(samples):
        yd = d.next()
        y[i] = fa.filter(burst[i]) + fb.filter(yd)
        d.store(y[i])
        e = ideal[i] - y[i]
        ea += e*fa.buf
        eb += e*fb.buf
        err += e*e
    
    fa.h += 2*mua*ea/samples
    fb.h += 2*mub*eb/samples
    print(err)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.plot(fa.h)
    ax2.plot(fb.h)
    ax3.plot(y)
    plt.draw()
    plt.pause(0.1)
    plt.clf()
    
    
