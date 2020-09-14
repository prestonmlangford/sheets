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
    
def goertzel1(v,w,axis=1):
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

L = 0.648/4       # m
T = 70      # N
mu = 0.02     # kg/m^3
s0 = 0.1
s1 = 0.005
E = 1.5e-5
N = 128
pi = np.pi
fs = 44100 # hz
period = 5  # s
samples = int(period*fs)

# [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
x = np.linspace(0,L,N+2) 
k = np.linspace(0,N-1,N).reshape(1,N)
n = k
t = np.linspace(0,period,samples).reshape(samples,1)

x0 = L/4
f = (x/x0)*(x<x0) + (L-x)/(L-x0)*(x>=x0)
#f = np.sin(pi*x/L)
u0 = f[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dst(u0)
vp0 = v0*0 # zeros, same shape as v0
w  = pi*(k + 1)/L
w2 = w*w
a  = 2*s0 + w2*s1
b  = w2*(T/mu - w2*E)
p = a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
pt = p*t
qt = q*t
v = v0*np.exp(-pt)*(np.cos(qt) + beta*np.sin(qt))
u = idst(v)
bridge = goertzel(v,w)
psd_plot(bridge,fs)
plt.plot(t,bridge)

# normalize to [-1,1]
z = np.zeros((samples,1))
u_plot  = np.concatenate((z, u/np.max(np.abs( u)),z),axis=1)
#up_plot = np.concatenate((z,up/np.max(np.abs(up)),z),axis=1)
#v_plot = v/np.max(np.abs(v))
#logv_plot = np.log(v*v)/20


wav = (bridge/np.max(np.abs(bridge))*32767).astype(np.int16)
write("pluck.wav",fs,wav)



fig, ax = plt.subplots()
line, = plt.plot([], [])

def init():
    ax.set_xlim(( 0, L))
    ax.set_ylim((-1, 1))
    return (line,)

def update(i):
    line.set_data(x, u_plot[i,:])
    #line.set_data(x, up_plot[i,:])
    #line.set_data(k, v_plot[i,:])
    #line.set_data(k, logv_plot[i,:])
    return (line,)

anim = animate(fig, update, init_func=init, frames=samples, interval=1, blit=True)

plt.show(block=False)
play("pluck.wav")
plt.show()
