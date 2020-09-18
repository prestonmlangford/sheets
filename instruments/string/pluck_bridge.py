from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as animate
import numpy as np
pi = np.pi

import scipy.io.wavfile

def write(file,data,fs):
    max_data = np.max(np.abs(data))
    scaled_data = 32767*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = fs,
        data = scaled_data.astype(np.int16)
    )

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

"""
U'' = T/mu*Uxx - 2*s0*U' + s1*U'xx + E*Uxxxx
S{U} = V
S{U'} = V'
let w = pi*(k + 1)/L
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

L = 0.648/4     # length of string
T = 70          # tension of string N
mu = 0.02       # density of string kg/m^3
s0 = 1.8        # string damping
s1 = 1e-4       # frequency dependent string damping
E  = 1e-3       # stiffness of string
N  = 32          # number of simulated modes
d  = 0.1        # bridge dampig ratio
fb = 600   # bridge resonant frequency
fs = 44100      # sampling frequency for audio (hz)
period = 3      # sampling period for audio

samples = int(period*fs)

# [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
x = np.linspace(0,L,N+2) 
k = np.linspace(0,N-1,N).reshape(1,N)
t = np.linspace(0,period,samples)

x0 = L/4
pluck = (x/x0)*(x<x0) + (L-x)/(L-x0)*(x>=x0)
u0 = pluck[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dst(u0)
w  = pi*(k + 1)/L
a  = 2*s0 + w*w*s1
b  = w*w*(T/mu - w*w*E)
p = a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
wcosw = (v0*w*np.cos(w)/L).reshape(N,1)

wb = 2*pi*fb
ar = -2*d*wb
br = -wb*wb

def f(y,ts):
    r = y[0]
    rp = y[1]
    v = np.exp(-p*ts)*(np.cos(q*ts) + beta*np.sin(q*ts))
    ux = np.dot(v,wcosw)
    rpp = ar*rp + br*r + ux
    return [rp,rpp,ux]

y0 = [0,0,0]
y = ode(f,y0,t)
bridge = y[:,1]

write("pluck.wav",bridge,fs)