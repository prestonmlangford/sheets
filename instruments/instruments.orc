
sr = 44100
ksmps = 32
nchnls = 2
0dbfs  = 1


instr 1
/* 
a simple sine wave with envelope
sounds a bit like a flue 
*/
ares linen  p5, 0.1*p3, p3, 0.1*p3
asig poscil ares, p4
     outs asig, asig

endin
