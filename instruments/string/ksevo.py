import math
import numpy as np
import scipy.signal as sig
from wavrw import read, write
from scipy.optimize import differential_evolution
from numpy.fft import fft
import IPython


fs = 44100

# https://ccrma.stanford.edu/~jos/Interpolation/Explicit_Formula_Lagrange_Interpolation.html
def lagdel(d,h,N=10):
    w = math.floor(d)
    f = d - w
    
    # discrete delay
    dd = np.zeros((w))
    dd[-1] = 1
    
    # fractional delay
    fd = np.zeros((N+1))+1
    for n in range(N+1):
        for k in range(N+1):
            if k == n:
                continue
            else:
                fd[n] *= (f-k)/(n-k)
    
    delay = sig.convolve(dd,fd)
    return sig.convolve(delay,h)

def nburst(n,alpha=0.1,duration=0.01):
    bl = int(duration*fs)
    noise = alpha*np.random.randn(bl)
    result = np.zeros((n))
    result[0:bl] = noise
    return result

def ks(b,a,f,n):
    x = nburst(n)
    d = fs/f
    fw = b
    bk = np.concatenate(([1],lagdel(d,a)))
    return sig.lfilter(fw,bk,x)

def mse(a,b):
    d = a - b
    return np.sum(d*d)

def unitygain(h):
    H = np.abs(fft(h))
    return h / np.max(H)

def normalize(sig):
    return sig/np.max(np.abs(sig))

ideal = read("ideal.wav")

def optimize(h):
    n = int(len(h)/2)
    b = h[:n]
    a = unitygain(h[n:])
    pluck = ks(b,a,196,len(ideal))
    err = mse(normalize(pluck),normalize(ideal))
    return err

fw=sig.firwin(100,1000,fs=fs)
bk=sig.firwin(100,100,fs=fs)
# boing=ks(hp,lp,440,4)
# write("boing.wav",boing)


lm = np.concatenate((fw,bk))
init_population = []
for _ in range(100):
    init_population.append(lm + 0.001*np.random.randn(len(lm)))
init_population = np.array(init_population)

m = 100
bounds = []
for _ in range(len(lm)):
    bounds.append((-m,m))


def de(fobj, bounds, pop, mut=0.8, crossp=0.7, its=1000):
    dimensions = len(bounds)
    popsize = len(pop)
    #pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            choice = np.random.choice(idxs, 3, replace = False)
            a, b, c = pop[choice]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]

for best in de(optimize,bounds,init_population):
    print(best)