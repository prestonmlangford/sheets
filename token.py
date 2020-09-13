import re
from error import TokenError

# these are compiled in advance for efficiency
# see https://regexr.com for help
_rgx_bar = re.compile(r"\|\s")
_rgx_repeat = re.compile(r"\:\s(.[^:]+)(\:(\d+)|(\:+))\s")
_rgx_time = re.compile(r"(d+)\/(\d+)\s")
_rgx_volume = re.compile(r"(\d+)\%\s")
_rgx_dynamic = re.compile(r"\d+%\s<\s.*<\s\d+%\s")
_rgx_tempo = re.compile(r"(\d+)[Bb][Pp][Mm]\s")
_rgx_note = re.compile(r"(\^?)(\,*)(\'*)(A#|Ab|A|Bb|B|C#|C|D#|Db|D|Eb|E|F#|F|G#|Gb|G)(\d*)(\.*)(\`*)\s")
_rgx_rest = re.compile(r"\_(\d*)(\.*)\s")

# returns (position in string,type of expression,quantified expression) 
# raises an exception if there is no match
def next(sheet):

    match = _rgx_bar.match(sheet)
    if match:
        return match.end(),"bar", None

    match = _rgx_time.match(sheet)
    if match:
        num, den = match.groups()
        return match.end(),"time", (int(num),int(den))

    match = _rgx_volume.match(sheet)
    if match:
        volume = match.group(1)
        return match.end(),"volume", int(volume)

    match = _rgx_dynamic.match(sheet)
    if match:
        return match.end(),"dynamic", None # PMLFIXME

    match = _rgx_tempo.match(sheet)
    if match:
        tempo = match.group(1)
        return match.end(),"tempo", int(tempo)

    match = _rgx_note.match(sheet)
    if match:
        tie,lower,upper,note,fraction,dots,stacato = match.groups()
        
        return match.end(),"note",(
            tie is not '',
            len(lower),
            len(upper),
            note,
            1 if fraction is '' else int(fraction),
            len(dots),
            len(stacato)
        )

    match = _rgx_rest.match(sheet)
    if match:
        fraction,dots = match.groups()
        fraction = 1 if fraction is '' else fraction
        
        return match.end(),"rest", (
            int(fraction),
            len(dots)
        )

    raise TokenError(sheet)
        

def copy_repeats(sheet):
    while True:
        pos = sheet.find(':')
        
        # no more repeat symbols
        if pos == -1: 
            break

        match = _rgx_repeat.match(sheet[pos:])
        if not match:
            raise TokenError(sheet[pos:])
        
        body,_,digits,colons = match.groups()
        start, end = match.span()
        
        if digits is not None:
            num = int(digits)
        elif colons is not None:
            num = len(colons)
        else:
            # this shouldn't happen if there was a match
            raise TokenError(sheet[match.end()-5:])
        
        dups = body
        for _ in range(num):
            dups += "| " + body
        
        sheet = sheet[:pos+start] + dups + sheet[pos+end:]
        
        
    return sheet
    
def preprocess(sheet):
    
    # ignore repeated measure bars |  | -> |
    sheet = re.sub(r"\|\s*\|","|",sheet)
    
    # replace all bars with space around bars to ensure whitespace B|A -> B | A
    sheet = re.sub(r"\|"," | ",sheet)
    
    # make all whitespace single space B\n|\tA -> B | A
    sheet = re.sub(r"\s+"," ",sheet)
    
    # trim leading whitespace
    sheet = sheet.lstrip(' ')
    
    # duplicate repeated measures
    sheet = copy_repeats(sheet)
    
    # debug
    print(sheet.replace(' ','+'))
    
    return sheet