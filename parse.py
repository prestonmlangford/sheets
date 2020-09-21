import lex 
from error import CompileError, TokenError

def compile(sheet):
    sheet = lex.preprocess(sheet)
    
    # defaults
    volume = 100
    A0 = 27.5 #Hz exactly 
    tempo = 120/60 # beats per second
    beats_per_whole = 4 # beats in 4/4 time
    beats_per_measure = 4 # beats in 4/4 time
    octave = 4 # treble clef?

    
    # loop variables
    output = ""
    beat = 0
    measure_number = -1
    pos = 0
    time = 0
    
    while pos < len(sheet):
        
        # raises TokenError
        pos,kind,token = lex.token(sheet,pos)
        
        
        if kind == "tempo":
            tempo = token/60
        
        elif kind == "volume":
            volume = token
        
        elif kind == "time":
            if beat != 0:
                raise CompileError("Time change only allowed at beginning of measure")
            beats_per_measure, beats_per_whole = token
        
        elif kind == "bar":
            if (beat < beats_per_measure) and (beat != 0):
                raise CompileError(
                        "Not enough beat in measure: {} < {}"
                        .format(beat,beats_per_measure)
                    )
            elif beat > beats_per_measure:
                raise CompileError(
                        "Too many beat in measure: {} > {}"
                        .format(beat,beats_per_measure)
                    )
            else:
                measure_number += 1
                beat = 0

        elif kind == "note":
            tie,lower,upper,note,fraction,dots,stacato = token
            
            duration = beats_per_whole/fraction
            duration *= 2 - 0.5**dots
            rest = duration*(1 - 0.5**stacato)
            duration -= rest
            
            beats = duration + rest
            beat += beats
            
            # equal temperament scale
            frequency = A0*2**(octave + upper - lower + note/12)
            
            output += "i 1 {:.3f} {:.3f} {:.3f} {:.3f}\n".format(time,duration/tempo,frequency,volume/100)
            time += beats/tempo
            
        elif kind == "rest":
            fraction,dots = token
            
            rest = beats_per_whole/fraction
            rest *= 2 - 0.5**dots
            
            beat += rest
            
        else:
            raise CompileError("Unable to process token: " + kind)
        
    
    return output
    
