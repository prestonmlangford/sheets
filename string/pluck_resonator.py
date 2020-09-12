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

"""
U  := vertical displacement of string [m]
L  := length of the string [m]
M  := mass of the string
m  := linear density of string M/L [kg/m]
T  := tension on string [kg*m/s^2]
ff := fundamental vibration frequency of string [hz]
wv := wave velocity sqrt(T/M)

ff = sqrt(T/m)/(2*L) = sqrt(T/(M*L))
T/m = (ff*2*L)^2 = (wv^2)
wv = 4*pi*ff*L

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

m*U'' + s0*U' + s1*U'xx + E*I*Uxxxx = T*Uxx
U'' + s0/m*U' + s1/m*U'xx + E*I/m*Uxxxx = T/m*Uxx
let e = E*I/m
U'' + s0/m*U' + s1/m*U'xx + E*I/m*Uxxxx - (wv^2)*Uxx = 0
DST{U} = V
DST{U'} = V'
let w = pi*(k + 1)/L
DST{Uxx} = -(w^2)*V
DST{Uxxxx} = (w^4)*V
V'' + s0/m*V' - s1/m*(w^2)*V' + e*(w^4)*V + (wv^2)*(w^2)*V = 0
V'' + (s0/m - s1/m*(w^2))*V' + (e*(w^4) + (wv^2)*(w^2))*V = 0
let a = s0/m - s1/m*(w^2)
let b = e*(w^4) + (wv^2)*(w^2)
V'' + a*V' + b*V = 0
(r^2) + a*r + b = 0
let p = -a/2
let q = sqrt((p^2) - b)
r = p +- q
"""

L = 0.6        # length of string [m]
ff = 261.625565 # fundamental vibration frequency [hz]
T = 70          # tension of string [N]
m  = 1          # linear density of string kg/m
s0 = 2.5        # string damping
s1 = 1.5e-3     # frequency dependent string damping
e  = 0#1e-3       # stiffness of string
N  = 32         # number of simulated modes
d  = 0.5        # bridge damping ratio
fb = 600        # bridge resonant frequency
fs = 44100      # sampling frequency for audio (hz)
period = 3      # sampling period for audio

samples = int(period*fs)

# [0,1,2,3,0,-3,-2,-1,0,1,2, . . .] n includes 1,2,3 but not the symmetry points
x = np.linspace(0,L,N+2) 
k = np.linspace(0,N-1,N).reshape(1,N)
t = np.linspace(0,period,samples)

x0 = L/4
pluck = (x/x0)*(x<x0) + (L-x)/(L-x0)*(x>=x0)
#pluck = x*(x-2*x0)/(-x0*x0)*(x<x0) + (x+2*x0)*(x-L)/(3*x0*(x0-L))*(x>=x0)
"""
y1 = m1*x
y2 = -(x-Lp)^2 + 1
y3 = m3*(L-x)

y1(x1) = y2(x1)
y1'(x1) = y2'(x1)

m1 = -2*x1 + 2*Lp + 1

-2*x1^2 + 2*x1*Lp + x1 = -x1^2 + 2*Lp*x1 - Lp^2 + 1
0 = x1^2 + x1 + (1 - Lp^2)
x1 = -0.5 + sqrt(Lp^2 - 0.75)
Lp^2 - 0.75 - sqrt(Lp^2 - 0.75) + 0.25 - 0.5 + sqrt(Lp^2 - 0.75) + 1 - Lp^2 = 0


y3(x2) = y2(x2)
y3'(x2) = y2'(x2)


m3 = 2*x2 - 2*Lp - 1
(2*x2 - 2*Lp - 1)*(L - x2) = -(x2 - Lp)^2 + 1
2*L*x2 - 2*Lp*L - L - 2*x2^2 + 2*x2*Lp + x2 = -x2^2 + 2*Lp*x2 - Lp^2 + 1
2*L*x2 - 2*Lp*L - L + x2 = x2^2 - Lp^2 + 1
0 = x2^2 - (2*L + 1)*x2 + 2*Lp*L + L - Lp^2 + 1
x2 = L + 0.5 - sqrt((L + 0.5)^2 - (2*Lp*L + L - Lp^2 + 1))

"""


# Lp = L/4
# x1 = -0.5 + np.sqrt(Lp*Lp - 0.75)
# m1 = -2*x1 + 2*Lp + 1
# print(x1)
# print(m1)
# x2 = L + 0.5 - np.sqrt((L + 0.5)*(L + 0.5) - (2*Lp*L + L - Lp*Lp + 1))
# m3 = 2*x2 - 2*Lp - 1
# xc = x - Lp
# print(x2)
# print(m3)
# pluck = (
#     (m1*x)*(x<=x1) + 
#     (-xc*xc + 1)*(x>x1)*(x<x2) + 
#     (m3*(L - x))*(x>=x2)
# )
# print(pluck)
# plt.plot(x,pluck)
# plt.show()
u0 = pluck[1:-1] # leave off the endpoints.  They are always zero and not included in the DST.
v0 = dst(u0)
wv = 2*ff*L
w  = pi*(k + 1)/L
a  = (s0/m) + (s1/m)*w*w
b  = w*w*(wv*wv + w*w*e)
p = a/2
q = np.sqrt(np.abs(p*p - b))
beta = p/q
wcosw = (v0*w*np.cos(w)/L).reshape(N,1)

ar = 2*d*fb
br = fb*fb

def f(y,ts):
    v = np.exp(-p*ts)*(np.cos(q*ts) + beta*np.sin(q*ts))
    ux = np.dot(v,wcosw)
    
    r = y[0]
    rp = y[1]
    rpp = -ar*rp - br*r + ux
    
    return [rp,rpp,ux]

y0 = [0,0,0]
y = ode(f,y0,t)
bridge = y[:,1]

write("pluck.wav",bridge,fs)