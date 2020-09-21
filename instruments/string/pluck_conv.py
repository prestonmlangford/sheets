import sys
import numpy as np
pi = np.pi
from audio import play
import scipy.io.wavfile

def write(file,data,fs):
    max_data = np.max(np.abs(data))
    scaled_data = 8000*data/max_data
    scipy.io.wavfile.write(
        filename = file,
        rate = fs,
        data = scaled_data.astype(np.int16)
    )

def read(file):
    rate, data = scipy.io.wavfile.read(file)
    print(
        "scipy.io.wavfile.read(" + file + ") -> " 
        + str(rate) + " Hz, " + 
        str(data.shape)
    )
    return data

import scipy.signal

def filter(num,den,signal):
    return scipy.signal.lfilter(num,den,signal,axis=0)

import scipy.fftpack

def dst(x):
    return np.real(scipy.fftpack.dst(x,type=1))/2

from scipy.integrate import odeint as ode



"""
U  := vertical displacement of string [m]
Lf := length of the string [m]
M  := mass of the string [kg]
m  := linear density of string M/L [kg/m]
T  := tension on string [kg*m/s^2]
ff := fundamental vibration frequency of string [hz]
vw := wave velocity sqrt(T/M)

ff = sqrt(T/m)/(2*Lf) = sqrt(T/(M*Lf))
T/m = (ff*2*Lf)^2 = (vw^2)
vw = 2*Lf*ff

m*U'' := [kg/m]*[m/s^2] = [kg/s^2]
Uxx := (d/dx)^2*U = [1/m^2]*[m] = [1/m]
T*Uxx := [kg*m/s^2]*[1/m] = [kg/s^2]
U' := [m/s]
s0*U' := [X]*[m/s] = [kg/s^2] s0 := [(kg/m)/s]
s1*U'' := [s1]*[(1/m)/s^2] = [kg/s^2] s1 := [kg*m]
E := [(kg/m)/s^2]
I := [m^4]
E*I*Uxxxx = [(kg/m)/s^2]*[m^4]*[1/m^3] = [kg/s^2]
U'' := [m/s^2]

T/m := [kg*m/s^2]*[m/kg] = [(m/s)^2]
T/m := [kg*m/s^2]*[m/kg] = [(m/s)^2]
s0/m := 

m*U'' + s0*U' = T*Uxx + s1*U'xx + E*I*Uxxxx
U'' + s0/m*U' - s1/m*U'xx - E*I/m*Uxxxx - (vw^2)*Uxx = 0
DST{U} = V
DST{U'} = V'
let w = pi*(k + 1)/L
DST{Uxx} = -(w^2)*V
DST{Uxxxx} = (w^4)*V
V'' + s0/m*V' + s1/m*(w^2)*V' - E*I/m*(w^4)*V + (vw^2)*(w^2)*V = 0
V'' + (s0/m + s1/m*(w^2))*V' + (-E*I/m*(w^4) + (vw^2)*(w^2))*V = 0
let a = s0/m + s1/m*(w^2)
let b = (vw^2)*(w^2) - (E*I/m)*(w^4)
V'' + a*V' + b*V = 0
(r^2) + a*r + b = 0
let p = -a/2
let q = sqrt((p^2) - b)
r = p +- q
"""
E4 = 329.63
B3 = 246.94
G3 = 196.00
D3 = 146.83
A2 = 110.00
E2 =  82.41

Lf = 0.650      # length of whole string for fundamental [m]
xp = 0.25*Lf    # point on string where the pluck occurs [m]
m  = 1.62e-3    # linear density of string [kg/m]
s0 = 3e-3       # string damping
s1 = 20e-7      # frequency dependent string damping
EI = 1e-5       # stiffness of string
N  = 2**4       # number of simulated modes
d  = 0.9        # bridge damping ratio
fs = 44100      # sampling frequency for audio (hz)
period = 3      # sampling period for audio

# fret positions
# https://www.stewmac.com/FretCalculator.html
scale = {
    0 : 0.0000,
    1 : 0.0561,
    2 : 0.1091,
    3 : 0.1591,
    4 : 0.2063,
    5 : 0.2508,
    6 : 0.2928,
    7 : 0.3325,
    8 : 0.3700,
    9 : 0.4053,
    10 : 0.4387,
    11 : 0.4702,
    12 : 0.5000,
    13 : 0.5280,
    14 : 0.5545,
    15 : 0.5795,
    16 : 0.6031,
    17 : 0.6254,
    18 : 0.6464,
    19 : 0.6662,
    20 : 0.6850,
    21 : 0.7026,
}

samples = int(period*fs)

def pluck(ff,fret):
    
    L = Lf*(1 - scale[fret])
    # [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
    x = np.linspace(0,L,N+2) 
    k = np.linspace(0,N-1,N).reshape(1,N)
    t = np.linspace(0,period,samples).reshape(samples,1)


    plk = (x/xp)*(x<xp) + (L-x)/(L-xp)*(x>=xp)
    u0 = plk[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
    v0 = dst(u0)
    vw = 2*Lf*ff
    w  = pi*(k + 1)/L
    a  = (s0/m) + (s1/m)*w*w
    b  = w*w*(vw*vw - w*w*EI/m)
    p = -a/2
    q = np.sqrt(np.abs(p*p - b))
    beta = p/q
    v0Lwcosw = (v0*(w/L)*np.cos(w)).reshape(N,1)

    pt = p*t
    qt = q*t
    v = np.exp(pt)*(np.cos(qt) + beta*np.sin(qt))
    ux = np.dot(v,v0Lwcosw)[:,0]

    # a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M] - a[1]*y[n-1] - ... - a[N]*y[n-N]
    
    # den = 0
    
    # for fb in [E2,A2,D3,G3,B3,E4]:
    #     wn = 2*pi*fb/fs
    #     wn *= 200
    #     den += np.array([
    #         1 + wn*wn + d*wn,
    #         -2,
    #         1 - d*wn
    #     ])

    # num = np.array([1/(fs*fs)])
    #bridge = filter(num,den,ux)
    #return bridge 
    
    return ux


cmajor = [None,3,2,0,1,0]
cminor = [None,3,5,5,4,3]
e2 =     [0]
e4 =     [None,None,None,None,None,0]

a2_1 =   [None,0]
a2_2 =   [5,None]

strings = [E2,A2,D3,G3,B3,E4]
chord = cminor
sound = 0
for i,fret in enumerate(chord):
    if fret is None: continue
    string = strings[i]
    sound += pluck(string,fret)

out = sys.argv[1]
write(out,sound,fs)
play(out)