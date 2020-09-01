from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import numpy as np
from scipy.io.wavfile import write
from audio import play
import scipy.fftpack

def dft(x):
    return np.fft.fft(x)

def idft(x): # default applies transform to last axis of x
    return np.fft.ifft(x)

from scipy.integrate import odeint as ode

def goertzel(v,axis=1):
    return np.real(np.sum(v,axis=axis)/v.shape[axis])

from scipy import signal

def psd_plot(data,fs):
    f, Pxx_den = signal.welch(data, fs)
    print(f[np.argmax(Pxx_den)])
    plt.semilogy(f, Pxx_den)
    plt.xlim([0,1000])
    plt.ylim([0.5e-3, 1])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')
    plt.show()

"""
U'' = -d/m*delta(x)*U' - h/m*delta(x)*U + T/mu*Uxx - 2*s0*U' + s1*U'xx + E*Uxxxx
F{U} = V
F{U'} = V'
F{delta(x)*U} = U[0]
F{delta(x - (N - 1))*U} = U[N - 1]*exp(2j*pi*k/N)
let dw = 2*pi*i*(N - 1)/L
let w = dw*(k + 1)/(N + 1)
F{Uxx} = (w^2)*V
F{Uxxxx} = (w^4)*V
V'' = T/mu*(w^2)*V - 2*s0*V' + s1*(w^2)*V' + E*(w^4)*V - (d0*U'[0] + d1*U'[N - 1] - h0*U[0] + h1*U[N - 1])/m
V'' = -(2*s0 - s1*(w^2))V' - (-T/mu*(w^2) - E*(w^4))*V
let a = 2*s0 - s1*(w^2)
let b = -T/mu*(w^2) - E*(w^4)
V'' = -a*V' - b*V - d/m*U'0 - h/m*U0
U0 = sum(V)
U'0 = sum(V')
"""

# characteristic equation
# U'' = T/mu*Uxx - 2*s0*U' + s1*U'xx + E*Uxxxx

L = 0.648/4       # m
T = 70      # N
mu = 0.02     # kg/m^3
m = 1 # mass of bridge resonator
s0 = 0.1
s1 = 0.005
E = 1.0e-1#1.5e-5
N = 128
pi = np.pi
fs = 44100 # hz
period = 0.1  # s
samples = int(period*fs)

x = np.linspace(0,L,N) 
k = np.linspace(0,N-1,N).reshape(1,N)
h = k*0 # same dimensions as k
h[0,0] = 1000 # hookes constant for restoring force on bridge.  N/m
h[0,N - 1] = 100000

d = h
d[0,0] = 10 # damping of the bridge
d[0,N - 1] = 100000
n = k
t = np.linspace(0,period,samples).reshape(samples,1)

print(k)
print(h)
print(d)

x0 = L/4
f = (x/x0)*(x<x0) + (L-x)/(L-x0)*(x>=x0)
#f = np.sin(pi*x/L)
u0 = f # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dft(u0)
vp0 = v0*0 # zeros, same shape as v0
dw = 2j*pi*(N - 1)/L
w  = dw*k/N
w2 = w*w
a  = d/m + 2*s0 - w2*s1
b  = h/m - w2*(T/mu + w2*E)
p = a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
pt = p*t
qt = q*t
v = v0*np.exp(-pt)*(np.cos(qt) + beta*np.sin(qt))
u = idft(v)
bridge = goertzel(v)
#psd_plot(bridge,fs)
plt.plot(t,bridge)

# normalize to [-1,1]
u_plot  = u/np.max(np.abs(u))
#up_plot = np.concatenate((z,up/np.max(np.abs(up)),z),axis=1)
v_plot = v/np.max(np.abs(v))
#logv_plot = np.log(v*v)/20

wav = (bridge/np.max(np.abs(bridge))*32767).astype(np.int16)
write("pluck.wav",fs,wav)

fig, ax = plt.subplots()
line, = plt.plot([], [])

def init():
    ax.set_xlim(( 0, N - 1))
    ax.set_ylim((-1, 1))
    return (line,)

def update(i):
    #line.set_data(x, u_plot[i,:])
    #line.set_data(x, up_plot[i,:])
    line.set_data(k, v_plot[i,:])
    #line.set_data(k, logv_plot[i,:])
    return (line,)

anim = animate(fig, update, init_func=init, frames=samples, interval=1, blit=True)

plt.show(block=False)
#play("pluck.wav")
plt.show()
