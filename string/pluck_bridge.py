from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import numpy as np
from scipy.io.wavfile import write
from audio import play
import scipy.fftpack

def dst(x):
    return np.real(scipy.fftpack.dst(x,type=1))/2

def idst(x,axis=1): # default applies transform to last axis of x
    return np.real(scipy.fftpack.dst(x,type=1))*2/(x.shape[axis] + 1)

from scipy.integrate import odeint as ode

def goertzel(v,w,axis=1):
    return np.sum(v*np.sin(w),axis=axis)
    
def goertzel1(v,w,axis=0):
    return np.sum(w*v*np.cos(w),axis=axis)
    


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
U'' = T/mu*Uxx - 2*s0*U' + s1*U'xx + E*Uxxxx
S{U} = V
S{U'} = V'
let w = pi*(k + 1)/(N + 1)
S{Uxx} = -(w^2)*V
S{Uxx} = (w^4)*V
V'' = -T/mu*(w^2)*V - 2*s0*V' - s1*(w^2)*V' + E*(w^4)*V
V'' = -(2*s0 + s1*(w^2))V' - (T/mu*(w^2) - E*(w^4))*V
let a = -(2*s0 + s1*(w^2))
let b = -(T/mu*(w^2) - E*(w^4))
V'' = a*V' + b*V
"""

# characteristic equation
# U'' = T/mu*Uxx - 2*s0*U' + s1*U'xx + E*Uxxxx

L = 0.648/4
T = 70      # N
mu = 0.02     # kg/m^3
s0 = 1
s1 = 0#1e-6
E = 1.5e-5
N = 32
d = 1e-2
h = 100
pi = np.pi
fs = 44100 # hz
period = 5  # s
samples = int(period*fs)

# [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
x = np.linspace(0,L,N+2) 
k = np.linspace(0,N-1,N).reshape(1,N)
n = k
t = np.linspace(0,period,samples)

x0 = L/4
pluck = (x/x0)*(x<x0) + (L-x)/(L-x0)*(x>=x0)
#f = np.sin(pi*x/L)
u0 = pluck[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dst(u0)
vp0 = v0*0 # zeros, same shape as v0
w  = pi*(k + 1)/L
w2 = w*w
a  = 2*s0 + w2*s1
b  = w2*(T/mu - w2*E)
p = a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
sinw = np.sin(w).reshape(N,1)

def f(y,ts):
    r = y[0]
    rp = y[1]
    v = v0*np.exp(-p*ts)*(np.cos(q*ts) + beta*np.sin(q*ts))
    ux = np.dot(v,sinw)/L
    rpp = -d*rp - h*r + ux
    return [rp,rpp,ux]

y0 = [0,0,0]
y = ode(f,y0,t)
# vp = y[:,N:2*N]
# up = idst(vp)
bridge = y[:,1]
string = y[:,2]
plt.plot(t,bridge)
plt.show()
plt.plot(t,string)
plt.show()

#bridge = string
wav = (bridge/np.max(np.abs(bridge))*32767).astype(np.int16)
write("pluck.wav",fs,wav)
play("pluck.wav")