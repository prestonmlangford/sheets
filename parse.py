import lex 
from error import CompileError, TokenError
import notation


def compile(sheet):
    sheet = lex.preprocess(sheet)
    
    # defaults
    volume = 100
    A0 = 27.5 #Hz exactly 
    tempo = 120/60 # beats per second
    whole = 4 # beats in 4/4 time
    beats_in_measure = 4 # beats in 4/4 time
    scale = notation.equal_temperament # tuning of musical scale
    clef = 4 # treble clef?

    
    # loop variables
    output = ""
    beats = beats_in_measure
    measure_number = -1
    pos = 0
    
    while pos < len(sheet):
        
        # raises TokenError
        pos,kind,token = lex.token(sheet,pos)
        
        
        if kind == "tempo":
            tempo = token
        
        elif kind == "volume":
            volume = token
        
        elif kind == "time":
            if beats != 0:
                raise CompileError("Time change only allowed at beginning of measure")
            beats_in_measure, whole = token
        
        elif kind == "bar":
            if beats < beats_in_measure:
                raise CompileError(
                        "Not enough beats in measure: {} < {}"
                        .format(beats,beats_in_measure)
                    )
            elif beats > beats_in_measure:
                raise CompileError(
                        "Too many beats in measure: {} > {}"
                        .format(beats,beats_in_measure)
                    )
            else:
                pos_start_of_measure = pos
                measure_number += 1
                beats = 0

        elif kind == "note":
            tie,lower,upper,note,fraction,dots,stacato = token
            
            duration = whole/fraction
            duration *= 2 - 0.5**dots
            rest = duration*(1 - 0.5**stacato)
            duration -= rest
            
            # PMLFIXME a change in tempo is going to break this
            schedule = measure_number*beats_in_measure + beats
            
            frequency = A0
            frequency *= 2**(clef + upper - lower)
            frequency *= scale[note]
            
            output += "i 1 {:.3f} {:.3f} {:.3f}\n".format(schedule/tempo,duration/tempo,frequency)
            beats += duration + rest
            
        elif kind == "rest":
            fraction,dots = token
            
            rest = whole/fraction
            rest *= 2 - 0.5**dots
            
            beats += rest
            
        else:
            raise CompileError("Unable to process token: " + kind)
        
    
    return output
    
