<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform
-odac    ;;;realtime audio out
;-iadc    ;;;uncomment -iadc if realtime audio input is needed too
; For Non-realtime ouput leave only the line below:
; -o oscils.wav -W ;;; for file output any platform
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs  = 1

instr 1

ares linen  0.7, 0.1*p3, p3, 0.1*p3
asig poscil ares, p4
     outs asig, asig

endin



</CsInstruments>
<CsScore>
i 1 0.000 0.375 239.729
i 1 0.375 0.125 213.574
i 1 0.500 0.250 190.273
i 1 0.750 0.250 213.574
i 1 1.000 0.250 239.729
i 1 1.250 0.250 239.729
i 1 1.500 0.500 239.729
i 1 2.000 0.250 213.574
i 1 2.250 0.250 213.574
i 1 2.500 0.500 213.574
i 1 3.000 0.250 239.729
i 1 3.250 0.250 285.088
i 1 3.500 0.500 285.088
i 1 4.000 0.375 239.729
i 1 4.375 0.125 213.574
i 1 4.500 0.250 190.273
i 1 4.750 0.250 213.574
i 1 5.000 0.250 239.729
i 1 5.250 0.250 239.729
i 1 5.500 0.250 239.729
i 1 5.750 0.250 239.729
i 1 6.000 0.250 213.574
i 1 6.250 0.250 213.574
i 1 6.500 0.250 239.729
i 1 6.750 0.250 213.574
i 1 7.000 1.000 190.273

e
</CsScore>
</CsoundSynthesizer>