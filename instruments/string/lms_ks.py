import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import scipy.io.wavfile
import scipy.signal
from scipy import signal
fs = 44100

class Delay:
    def __init__(self,d):
        self.d = d
        self.k = math.floor(d) + 1
        self.buf = np.zeros((self.k))
        self.i = 0
        self.r = self.d - self.k
    
    def next(self):
        return self.buf[self.i]*(1 - self.r) + self.buf[self.i]*self.r

    def store(self,x):
        self.buf[self.i] = x
        self.i = (self.i + 1) % self.k

class FIR:
    def __init__(self,order):
        self.p = order
        self.buf = np.zeros((p))
        self.h = np.random.randn(p)
        
    def filter(self,x):
        self.buf[1:] = self.buf[:-1]
        self.buf[0] = x
        return np.dot(self.h.T,self.buf)
    
    

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
    return data[:,0] + data[:,1]

def write(file,data):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = fs,
        data = scaled_data.astype(np.int16)
    )



ideal = read("ideal.wav")

n = len(ideal)
muh = 1
eps = 500
mse = 2*eps
p = 1000
err = np.zeros((n))
y = np.zeros((n))
burst = np.random.randn(1000)
delay = Delay(fs/196)
fir = FIR(p)

for _ in range(10):
    for i in range(len(burst)):
        d = delay.next()
        fb = fir.filter(d)
        y[i] = burst[i] + fb
        delay.store(y[i])
        
    for i in range(len(burst),len(ideal)):
        d = delay.next()
        y[i] = fir.filter(d)
        delay.store(y[i])
        
        x = fir.buf
        mu = muh/(0.001 + np.dot(x.T,x))
        e = ideal[i] - y[i]
        fir.h = fir.h + mu*e*x
        fir.h /= np.sqrt(np.dot(fir.h.T,fir.h))
        err[i] = np.log(e*e)

write("lms.wav",y)

plt.plot(y)
plt.show()
plt.plot(err)
plt.show()
w,h=freqz(fir.h)
plt.show()

scale = np.max(np.abs(h))
fir.h /= scale
freqz(fir.h)

delay = Delay(fs/196)
h = fir.h
fir = FIR(p)
fir.h = h
print(np.dot(h.T,h))
for i in range(len(burst)):
    d = delay.next()
    fb = fir.filter(d)
    y[i] = burst[i] + fb
    delay.store(y[i])
    
for i in range(len(burst),len(ideal)):
    d = delay.next()
    y[i] = fir.filter(d)
    delay.store(y[i])

write("filtered.wav",y)

f = open('body.txt','w')
for num in fir.h:
    f.write("{}\n".format(num))
f.close()