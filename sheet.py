import re
from token import next_token
import notation

def geometric(n):
    r = 0
    for i in range(n + 1):
        r += 0.5**i
    return r

def preprocess(sheet):
    # ignore repeated measure bars |  | -> |
    sheet = re.sub(r"\|\s*\|","|",sheet)
    
    # replace all bars with space around bars to ensure whitespace B|A -> B | A
    sheet = re.sub(r"\|"," | ",sheet)
    
    # make all whitespace single space B\n|\tA -> B | A
    sheet = re.sub(r"\s+"," ",sheet)
    
    # trim leading whitespace
    sheet = sheet.lstrip(' ')
    
    print(sheet.replace(' ','+'))
    
    return sheet

def compile(instrument,sheet):
    sheet = preprocess(sheet)
    
    # default 120 BPM
    tempo = 120
    
    # default 4/4 time
    relative_duration = 4
    beats_per_measure = 4
    beats = beats_per_measure
    
    while(len(sheet) > 0):
        result = next_token(sheet)
        if result is None:
            print("Error in sheet")
            print(sheet)
            return
        
        pos,kind,token = result
        
        if kind == "bar":
            if beats < beats_per_measure:
                print("Not enough beats in measure")
                print(beats)
                print(sheet)
                return
            elif beats > beats_per_measure:
                print("Too many beats in measure")
                print(beats)
                print(sheet)
                return
            else:
                beats = 0
                
        if kind == "note":
            tie,lower,upper,note,duration,dots,stacato = token
            beats += (relative_duration/duration)*geometric(dots)
            print(beats)
            
        
        print(kind)
        print(token)
        print()
        sheet = sheet[pos:]



compile(None,
    
    # Mary Had a Little Lamb
    
    #"treble? 4/4 120bpm 50%"
    " |E4. D8 C4 D4|E4 E4 E2   |D4 D4 D2   |E4 G4 G2|\n"
    " |E4. D8 C4 D4|E4 E4 E4 E4|D4 D4 E4 D4|C| "
)