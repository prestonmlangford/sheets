import re
from token import next_token
import notation

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

def compile(instrument,sheet,path):
    score = open(path,'w')
    
    # defaults
    A0 = 27.5 #Hz exactly 
    tempo = 120/60 # beats per second
    whole = 4 # beats in 4/4 time
    beats_in_measure = 4 # beats in 4/4 time
    scale = notation.equal_temperament # tuning of musical scale
    clef = 4 # treble clef?
    
    # loop variables
    measure = -1
    time = 0
    beats = beats_in_measure
    
    sheet = preprocess(sheet)
    while(len(sheet) > 0):
        result = next_token(sheet)
        if result is None:
            print("Error in sheet")
            print(sheet)
            return
        
        pos,kind,token = result
        print(kind)
        
        if kind == "bar":
            if beats < beats_in_measure:
                print("Not enough beats in measure")
                print(beats)
                print(sheet)
                return
            elif beats > beats_in_measure:
                print("Too many beats in measure")
                print(beats)
                print(sheet)
                return
            else:
                measure += 1
                beats = 0
    
        elif kind == "note":
            tie,lower,upper,note,fraction,dots,stacato = token
            
            duration = whole/fraction
            duration *= 2 - 0.5**dots
            rest = duration*(1 - 0.5**stacato)
            duration -= rest            
            
            schedule = (measure*beats_in_measure + beats)/tempo
            beats += duration + rest
            
            frequency = A0
            frequency *= 2**(clef + upper - lower)
            frequency *= scale[note]
            
            print("frequency: {:.3f}".format(frequency))
            print("schedule: {:.3f}".format(schedule))
            print("duration: {:.3f}".format(duration/tempo))
            score.write("i 1 {:.3f} {:.3f} {:.3f}\n".format(schedule,duration/tempo,frequency))
        
        print("+")
        sheet = sheet[pos:]
    
    score.close()


sheet = (
    # Mary Had a Little Lamb
    
    #"treble? 4/4 120bpm 50%"
    " |E4. D8 C4 D4|E4 E4 E2   |D4 D4 D2   |E4 G4 G2|\n"
    " |E4. D8 C4 D4|E4 E4 E4 E4|D4 D4 E4 D4|C| "
)

compile(None,sheet,"score.csd")