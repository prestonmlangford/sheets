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
            raise TokenError("Unmatched repeat sign in measure",sheet,pos)
        
        body,_,digits,colons = match.groups()
        start, end = match.span()
        
        if sheet[pos + start - 2] != '|':
            raise TokenError("Repeat sign not at start of measure",sheet,pos)
        
        if sheet[pos + end] != '|':
            raise TokenError("Repeat sign not at end of measure",sheet,pos)
        
        if digits is not None:
            num = int(digits)
        elif colons is not None:
            num = len(colons)
        else:
            # this shouldn't happen if there was a match
            raise TokenError("Unknown repeat sign match error",sheet,pos)
        
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
    
    # trim leading whitespace
    sheet = sheet.lstrip(' ')
    
    # duplicate repeated measures
    sheet = copy_repeats(sheet)
    
    # debug
    print(sheet.replace(' ','+'))
    
    return sheet

# these are compiled in advance for efficiency
# see https://regexr.com for help
_rgx_bar = re.compile(r"\|\s")
_rgx_repeat = re.compile(r"\:\s(.[^:]+)(\:(\d+)|(\:+))\s")
_rgx_time = re.compile(r"(\d+)\/(\d+)\s")
_rgx_volume = re.compile(r"(\d+)\%\s")
_rgx_dynamic = re.compile(r"\d+%\s<\s.*<\s\d+%\s")
_rgx_tempo = re.compile(r"(\d+)[Bb][Pp][Mm]\s")
_rgx_note = re.compile(r"(\^?)(\,*)(\'*)(A#|Ab|A|Bb|B|C#|C|D#|Db|D|Eb|E|F#|F|G#|Gb|G)(\d*)(\.*)(\`*)\s")
_rgx_rest = re.compile(r"\_(\d*)(\.*)\s")


# returns (position in string,type of expression,quantified expression) 
# raises an exception if there is no match
def token(sheet,position):    
    match = _rgx_bar.match(sheet[position:])
    if match:
        return match.end()+position,"bar", None

    match = _rgx_time.match(sheet[position:])
    if match:
        num, den = match.groups()
        return match.end()+position,"time", (int(num),int(den))

    match = _rgx_volume.match(sheet[position:])
    if match:
        volume = match.group(1)
        return match.end()+position,"volume", int(volume)

    match = _rgx_dynamic.match(sheet[position:])
    if match:
        return match.end()+position,"dynamic", None # PMLFIXME

    match = _rgx_tempo.match(sheet[position:])
    if match:
        tempo = match.group(1)
        return match.end()+position,"tempo", int(tempo)

    match = _rgx_note.match(sheet[position:])
    if match:
        tie,lower,upper,note,fraction,dots,stacato = match.groups()
        
        return match.end()+position,"note",(
            tie is not '',
            len(lower),
            len(upper),
            notation.scale[note],
            1 if fraction is '' else int(fraction),
            len(dots),
            len(stacato)
        )

    match = _rgx_rest.match(sheet[position:])
    if match:
        fraction,dots = match.groups()
        fraction = 1 if fraction is '' else fraction
        
        return match.end()+position,"rest", (
            int(fraction),
            len(dots)
        )

    raise TokenError("Unknown symbol in measure",sheet,position)
