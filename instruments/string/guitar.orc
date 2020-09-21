

#define M_12r2 #1.0594630943592953# ; 12th root of 2

instr 1
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Guitar
; physical model using a spectral method
; implemented by Preston M Langford / Sep 2020
;
; uses k-rate vectors for audio signals
; set ksmps = 1 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;-------------------------------------------------------------
; constants for setup
;-------------------------------------------------------------

; fundamentals for the 6 strings
iE4 = 329.63
iB3 = 246.94
iG3 = 196.00
iD3 = 146.83
iA2 = 110.00
iE2 =  82.41

idebug = p5
iff = p3 ;PMLFIXME which parameter?
ifret = p4 ;PMLFIXME which parameter?
iLf = 0.650      ; length of whole string for fundamental [m]
iXp = 0.25*iLf   ; point on string where the pluck occurs [m]
im  = 1.62e-3    ; linear density of string [kg/m]
is0 = 3e-3       ; string damping
is1 = 20e-7      ; frequency dependent string damping
iEI = 1e-5       ; stiffness of string
iN  = 64         ; number of simulated modes

iL = iLf*($M_12r2 ^ (-ifret))
ivw = 2*iLf*iff
;iX = ;pluck PMLFIXME
;iV0 fft ;PMLFIXME
iw[] genarray 1, iN
iw *= $M_PI/iL
iw2[] = iw*iw
ia[] = iw2*(is1/im)
ia += (is0/im)
ib[] = iw2*(-iEI/im)
ib += (ivw*ivw)
ib[] = iw2*ib
ip[] = (-0.5)*ia
iq[] = (ip*ip) - ib
iq maparray iq, "abs"
iq maparray iq, "sqrt"
ibeta[] = ip/iq

;-------------------------------------------------------------
; audio rate processing
;-------------------------------------------------------------

kt timeinsts
kexp_pt[] = ip
kcos_qt[] = iq
ksin_qt[] = iq
kpt[] = ip * kt
kqt[] = iq * kt
kexp_pt maparray kpt, "exp"
kcos_qt maparray kqt, "cos"
ksin_qt maparray kqt, "sin"
kv[] = ksin_qt
kv *= ksin_qt
;kv += kcos_qt
;kv *= kexp_pt


asig = 0
outs asig, asig

endin