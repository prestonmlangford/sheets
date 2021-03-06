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
E2 = 82.41

Lf = 0.650/4    # length of whole string for fundamental [m]
xp = 0.25*Lf    # point on string where the pluck occurs [m]
fret = 4        # the selected fret
ff = 182.6      # fundamental vibration frequency [hz]
m  = 1.62e-3    # linear density of string [kg/m]
s0 = 5.83e-3    # string damping
s1 = 1.62e-7    # frequency dependent string damping
EI = 1e-6       # stiffness of string
N  = 32         # number of simulated modes
d  = 0.1        # bridge damping ratio
fb = 3000       # bridge resonant frequency
fs = 44100      # sampling frequency for audio (hz)
period = 3      # sampling period for audio


# fret positions
# https://www.stewmac.com/FretCalculator.html
scale = {
    0 : 0.0,
    1 : 0.056126153846153846,
    2 : 0.10910153846153846,
    3 : 0.15910307692307693,
    4 : 0.2063,
    5 : 0.2508461538461539,
    6 : 0.29289384615384617,
    7 : 0.33258,
    8 : 0.37004000000000004,
    9 : 0.40539692307692304,
    10 : 0.43876923076923074,
    11 : 0.4702676923076923,
    12 : 0.5,
    13 : 0.5280630769230769,
    14 : 0.5545507692307693,
    15 : 0.5795523076923077,
    16 : 0.6031492307692308,
    17 : 0.6254230769230769,
    18 : 0.6464461538461539,
    19 : 0.6662907692307692,
    20 : 0.68502,
    21 : 0.7026984615384616,
}


samples = int(period*fs)


L = Lf*(1 - scale[fret])
# [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
x = np.linspace(0,L,N+2) 
k = np.linspace(0,N-1,N).reshape(1,N)
t = np.linspace(0,period,samples)


pluck = (x/xp)*(x<xp) + (L-x)/(L-xp)*(x>=xp)
u0 = pluck[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dst(u0)
vw = 2*Lf*ff
w  = pi*(k + 1)/L
a  = (s0/m) + (s1/m)*w*w
b  = w*w*(vw*vw - w*w*EI/m)
p = -a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
v0Lwcosw = (v0*(w/L)*np.cos(w)).reshape(N,1)

ar = 2*d*fb
br = fb*fb

def f(y,ts):
    v = np.exp(p*ts)*(np.cos(q*ts) + beta*np.sin(q*ts))
    ux = np.dot(v,v0Lwcosw)
    
    r = y[0]
    rp = y[1]
    rpp = -ar*rp - br*r + ux
    
    return [rp,rpp,ux]

y0 = [0,0,0]
y = ode(f,y0,t)
bridge = y[:,1]

write("pluck.wav",bridge,fs)