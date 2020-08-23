
# Mary Had a Little Lamb
sheet = (
    "treble? 4/4 120bpm 50%"
    "| E4. D8 C4 D4 | E4 E4 E2 | D4 D4 D2 | E4 G4 G2 | E4. D8 C4 D4 | E4 E4 E4 E4 | D4 D4 E4 D4 | C |"
)

import re
from lex import token
import notation



def compile(instrument,sheet):
    sheet = preprocess(sheet)
    
    # default 120 BPM
    tempo = 120
    
    # default 4/4 time
    beat = 4
    length = 4
    
    while(len(sheet) > 0):
        id,pos,token = tokenize(sheet)
        schedule_instrument(token)
        sheet = sheet[pos:]

            
compile(None,sheet)