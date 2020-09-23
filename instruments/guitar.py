import pysound
from instruments.opcode import linen
import numpy as np
pi = np.pi
import notation 

import scipy.signal

def filter(num,den,signal):
    return scipy.signal.lfilter(num,den,signal,axis=0)

import scipy.fftpack

def dst(x):
    return np.real(scipy.fftpack.dst(x,type=1))/2


class Guitar:
    def __init__(self):
        super().__init__()
        
        A0 = notation.A0
        scale = notation.scale
        self.strings = [
            12*2 + scale["E"],
            12*2 + scale["A"],
            12*3 + scale["D"],
            12*3 + scale["G"],
            12*3 + scale["B"],
            12*4 + scale["E"]
        ]
        
        ff = list(map(lambda exp: A0*2**(exp/12),self.strings))

        self.parameters = {
                "neck length"                       : 0.650,
                "pluck position"                    : 0.25*0.650,
                "number of modes"                   : 2**6,
                "string density"                    : 1.62e-3,
                "string damping by velocity"        : 3e-3,
                "string damping by mode velocity"   : 20e-7,
                "string stiffness"                  : 1e-5,
                "string tuning"                     : ff,
                "attack"                            : 0.01,
                "decay"                             : 0.01,
        }

        self.chords = {
            "cmajor" : [None,3,2,0,1,0],
            "cminor" : [None,3,5,5,4,3],   
            "c7"     : [None,3,2,3,1,0],
            
            "dmajor" : [None,None,0,2,3,2],
            "dminor" : [None,None,0,2,3,1],
            "d7"     : [None,None,0,2,1,2],
            
            "emajor" : [0,2,2,1,0,0],
            "eminor" : [0,2,2,0,0,0],
            "e7"     : [0,2,0,1,0,0],
            
            "fmajor" : [1,3,3,2,1,1],
            "fminor" : [1,3,3,1,1,1],
            "f7"     : [1,3,1,2,1,1],
            
            "gmajor" : [3,2,0,0,0,2],
            "gminor" : [3,5,5,3,3,3],
            "g7"     : [3,2,0,0,0,1],
            
            "amajor" : [None,0,2,2,2,None],
            "aminor" : [None,0,2,2,1,0],
            "a7"     : [None,0,2,0,2,0],
            
            "bmajor" : [None,2,4,4,4,2],
            "bminor" : [None,2,4,4,3,2],
            "b7"     : [None,2,1,2,0,2],
            
        }

    def play(self,volume,duration,octave,step):
        string, fret = self.minfret(octave,step)
        return self.pluck(duration,string,fret)
    
    def minfret(self,octave,step):
        # PMLFIXME add exception for case where note is too low to be played
        result = None
        fn = 12*octave + step
        _minfret = 100000
        for string,fs in enumerate(self.strings):
            if fn >= fs:
                fret = fn - fs
                if fret < _minfret:
                    _minfret = fret
                    result = (string,fret)
                    
        return result
        
    
    def strum(self,duration,chord):
        result = 0
        frets = self.chords[chord]
        for string,fret in enumerate(frets):
            if fret is None: continue
            result += self.pluck(duration,string,fret)
        return result


    def pluck(self,duration,string,fret):
        
        Lf  = self.parameters["neck length"]
        xp  = self.parameters["pluck position"]
        m   = self.parameters["string density"]
        s0  = self.parameters["string damping by velocity"]
        s1  = self.parameters["string damping by mode velocity"]
        EI  = self.parameters["string stiffness"]
        N   = self.parameters["number of modes"]
        tun = self.parameters["string tuning"]
        att = self.parameters["attack"]
        dec = self.parameters["decay"]
        
        # fret spacing by equal temperament
        L = Lf*(2**(-fret/12))
        ff = tun[string]
        
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
        
        samples = int(duration*pysound.fs)
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
                
        
        