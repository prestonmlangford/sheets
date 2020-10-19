import pysound
import numpy as np
import instruments.guitar
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import scipy.io.wavfile

def read(file):
    rate, data = scipy.io.wavfile.read(file)
    print(
        "scipy.io.wavfile.read(" + file + ") -> " 
        + str(rate) + " Hz, " + 
        str(data.shape)
    )
    return data[:,0] + data[:,1]

guitar = instruments.guitar.Guitar()
pluck = guitar.pluck(2.8,3,0)
ideal = read("ideal.wav")

if len(pluck) > len(ideal):
    n = len(ideal)
    pluck = pluck[0:n]
else:
    n = len(pluck)
    ideal = ideal[0:n]

muh = 0.1
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

h = np.flip(h)
plt.plot(err)
plt.show()
plt.psd(h)
plt.show()

f = open('body.txt','w')
for num in h:
    f.write("{}\n".format(num))
f.close()