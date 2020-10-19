import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import scipy.io.wavfile
import scipy.signal
fs = 44100

def breakpoint():
    if input("Continue? [y/n]: ") == "n":
        exit(0)
        

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


def comb(s,f,a=-0.9):
    d = fs/f
    k1 = math.floor(d)
    k2 = k1 + 1
    r1 = k2 - d
    r2 = d - k1
    print(k1)
    print(k2)
    print(r1)
    print(r2)
    num = np.array([1])
    den = np.zeros((k2))
    den[0] = 1
    den[k1-1] = a*r1
    den[k2-1] = a*r2
    return filter(num,den,s)

x = np.concatenate((np.random.randn(100),np.zeros((int(2.8*fs)))))
pluck = comb(x,196,-0.99)

write("comb_pluck.wav",pluck)

breakpoint()

ideal = read("ideal.wav")



if len(pluck) > len(ideal):
    n = len(ideal)
    pluck = pluck[0:n]
else:
    n = len(pluck)
    ideal = ideal[0:n]

muh = 1
eps = 500
mse = 2*eps
p = 1000
h = np.zeros((p))
err = np.zeros((n))

for i in range(p,n):
    x = np.flip(pluck[i-p:i])
    mu = muh/(0.001 + np.dot(x.T,x))
    e = ideal[i] - np.dot(h.T,x)
    h = h + mu*e*x
    err[i] = np.log(e*e)

plt.plot(err)
plt.show()
plt.psd(h)
plt.show()

sig = filter(h,[1],pluck)
write("filtered.wav",sig)

f = open('body.txt','w')
for num in h:
    f.write("{}\n".format(num))
f.close()