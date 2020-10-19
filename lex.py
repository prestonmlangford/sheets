import re
from error import TokenError
import notation

def copy_repeats(sheet):
    while True:
        pos = sheet.find(':')
        
        # no more repeat symbols
        if pos == -1: 
            break
        
        match = _rgx_repeat.match(sheet[pos:])
        if not match:
            raise TokenError("Unmatched repeat sign")
        
        body,_,digits,colons = match.groups()
        start, end = match.span()
        
        if sheet[pos + start - 2] != '|':
            raise TokenError("Repeat sign not at start of measure")
        
        if sheet[pos + end] != '|':
            raise TokenError("Repeat sign not at end of measure")
        
        if digits is not None:
            num = int(digits)
        elif colons is not None:
            num = len(colons)
        else:
            # this shouldn't happen if there was a match
            raise TokenError("Unknown repeat sign match error")
        
        dups = body
        for _ in range(num):
            dups += "| " + body
        
        sheet = sheet[:pos+start] + dups + sheet[pos+end:]
        
    return sheet

def preprocess(sheet):
    
    # remove single line comments
    sheet = re.sub(r"\/\/.*$","",sheet,flags=re.MULTILINE)
    
    # remove multi line comments
    sheet = re.sub(r"\/\*.*\*\/","",sheet,flags=re.DOTALL)
    
    # ignore repeated measure bars |  | -> |
    sheet = re.sub(r"\|\s*\|","|",sheet)
    
    # add whitespace around measure bars B|A -> B | A
    sheet = re.sub(r"\|"," | ",sheet)
    
    # add whitespace before signature symbols
    sheet = re.sub(r"\@"," @",sheet)
    
    # add whitespace around repeat signs
    # match any colon not followed by another colon or digit
    sheet = re.sub(r"\:(?!\:|\d+)",": ",sheet)
    # match any colon not preceded by another colon
    sheet = re.sub(r"(?<!\:)\:"," :",sheet)
    
    # make all whitespace single space B\n|\tA -> B | A
    sheet = re.sub(r"\s+"," ",sheet)
    
    # duplicate repeated measures
    sheet = copy_repeats(sheet)
    
    # trim leading/trailing whitespace
    sheet = sheet.lstrip()
    sheet = sheet.rstrip()
    
    # debug
    #print(sheet.replace(' ','+'))
    
    return enumerate(sheet.split(' '))

# these are compiled in advance for efficiency
# see https://regexr.com for help
_rgx_bar = re.compile(r"\|")
_rgx_repeat = re.compile(r"\:\s(.[^:]+)(\:(\d+)|(\:+))")
_rgx_time = re.compile(r"(\d+)\/(\d+)")
_rgx_volume = re.compile(r"(\d+)\%")
_rgx_dynamic = re.compile(r"\d+%\s<\s.*<\s\d+%")
_rgx_tempo = re.compile(r"(\d+)[Bb][Pp][Mm]")


_note = r"(A#|Ab|A|Bb|B|C#|C|D#|Db|D|Eb|E|F#|F|G#|Gb|G)"
_duration = r"(w|h|q|e|s|t|\d*)"
_durmod = r"([.`]*)"
_octave = r"(\d*)"
_octmod = r"([,']*)"
_rgx_note = re.compile(_durmod + _duration + _note + _octave + _octmod)
_rgx_chord = re.compile(_durmod + _duration + r"\((.*)\)" + _octmod)
_rgx_pitch = re.compile(_note + _octave + _octmod)
_rgx_rest = re.compile(_durmod + _duration + r"\_")

def count(s,symbol):
    result = 0
    for c in s:
        result += 1 if c == symbol else 0
    return result

# yields (type of expression,quantified expression)
# raises an exception if there is no match
def tokens(sheet):
    for i,s in preprocess(sheet):

        match = _rgx_bar.match(s)
        if match:
            yield "bar", None
            continue
        
        match = _rgx_time.match(s)
        if match:
            num, den = match.groups()
            yield "time", (int(num),int(den))
            continue

        match = _rgx_volume.match(s)
        if match:
            volume = match.group(1)
            yield "volume", int(volume)
            continue

        match = _rgx_dynamic.match(s)
        if match:
            yield "dynamic", None # PMLFIXME
            continue

        match = _rgx_tempo.match(s)
        if match:
            tempo = match.group(1)
            yield "tempo", int(tempo)
            continue

        match = _rgx_note.match(s)
        if match:
            durmod,fraction,pitch,octave,octavemod = match.groups()
            
            if fraction in notation.duration:
                fraction = notation.duration[fraction]
            elif fraction is '':
                fraction = 1
            else:
                fraction = int(fraction)
                
            yield "note",(
                count(durmod,'`'),
                count(durmod,'.')
                len(upper),
                notation.scale[note],
                1 if fraction is '' else int(fraction),
                len(dots),
                len(stacato)
            )
            continue
        
        
        match = _rgx_rest.match(s)
        if match:
            dots,fraction = match.groups()
            
            if fraction in notation.duration:
                fraction = notation.duration[fraction]
            elif fraction is '':
                fraction = 1
            else:
                fraction = int(fraction)
            
            yield "rest", (
                fraction,
                len(dots)
            )
            continue
        
        
        raise TokenError("Unknown symbol: " + s)
