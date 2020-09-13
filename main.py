from sheet import compile, CompileError
from error import CompileError, TokenError
import sys

sheet = (
    # Mary Had a Little Lamb
    
    #"treble? 4/4 120bpm 50%"
    " |:E4. D8 C4 D4|E4 E4 E2   :|:D4 D4 D2   :|E4 G4 G2|:_2 C12 C12 C12 C4` :|\n"
    " |E4. D8 C4 D4|E4 E4 E4 E4|D4 D4 E4 D4|C| "
)

try:
    score = compile(sheet)
except CompileError as err:
    print(err)
    sys.exit(-1)
except TokenError as err:
    print(err)
    sys.exit(-1)

out = open("score.sco",'w')
out.write(score)
out.close()