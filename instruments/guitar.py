import pysound
from opcode import linen
import numpy as np
pi = np.pi

import scipy.signal

def filter(num,den,signal):
    return scipy.signal.lfilter(num,den,signal,axis=0)

import scipy.fftpack

def dst(x):
    return np.real(scipy.fftpack.dst(x,type=1))/2

# PMLFIXME redefine these with equal temperament to get an exact tuning
E4 = 329.63
B3 = 246.94
G3 = 196.00
D3 = 146.83
A2 = 110.00
E2 =  82.41

DEFAULT_PARAMETERS = {
        "neck length"                       : 0.650,
        "pluck position"                    : 0.25*0.650,
        "number of modes"                   : 2**6,
        "string density"                    : 1.62e-3,
        "string damping by velocity"        : 3e-3,
        "string damping by mode velocity"   : 20e-7,
        "string stiffness"                  : 1e-5,
        "string tuning"                     : [E2,A2,D3,G3,B3,E4],
        "attack"                            : 0.01,
        "decay"                             : 0.01,
}

def guitar(duration,string,fret,parameters=DEFAULT_PARAMETERS):
    
    Lf  = parameters["neck length"]
    xp  = parameters["pluck position"]
    m   = parameters["string density"]
    s0  = parameters["string damping by velocity"]
    s1  = parameters["string damping by mode velocity"]
    EI  = parameters["string stiffness"]
    N   = parameters["number of modes"]
    s   = parameters["string tuning"]
    att = parameters["attack"]
    dec = parameters["decay"]
    
    # fret spacing by equal temperament
    L = Lf*(2**(-fret/12))
    ff = s[string]
    # leave off the endpoints.  They are always zero and not included in the DST.
    x = np.linspace(0,L,N + 2)[1:-1]
    u0 = (x/xp)*(x<xp) + (L-x)/(L-xp)*(x>=xp)
    v0 = dst(u0)
    vw = 2*Lf*ff
    w  = (pi/L)*np.linspace(1,N,N).reshape(1,N)
    a  = (s0/m) + (s1/m)*w*w
    b  = w*w*(vw*vw - w*w*EI/m)
    p = -a/2
    q = np.sqrt(np.abs(p*p - b))
    beta = p/q
    v0Lwcosw = (v0*(w/L)*np.cos(w)).reshape(N,1)
    
    samples = int(duration,pysound.fs)
    t = np.linspace(0,duration,samples).reshape(samples,1)
    
    pt = p*t
    qt = q*t
    v = np.exp(pt)*(np.cos(qt) + beta*np.sin(qt))
    ux = np.dot(v,v0Lwcosw)[:,0]
    return linen(ux,att,dec)
    
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
        
        
        