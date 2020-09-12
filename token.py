import re

# these can be compiled in advance for efficiency
_rgx_bar = re.compile(r"\|\s")
_rgx_repeat = re.compile(r"\:(\d+)\s|\s(\:+)\s")
_rgx_time = re.compile(r"(d+)\/(\d+)\s")
_rgx_volume = re.compile(r"(\d+)\%\s")
_rgx_dynamic = re.compile(r"\d+%\s<\s.*<\s\d+%\s")
_rgx_tempo = re.compile(r"(\d+)[Bb][Pp][Mm]\s") 
_rgx_note = re.compile(r"(\^?)(\,*)(\'*)(A#|Ab|A|Bb|B|C#|C|D#|Db|D|Eb|E|F#|F|G#|Gb|G)(\d*)(\.*)(\`*)\s")

# returns (position in string,type of expression,quantified expression) 
# or None if there is not a match
def next_token(sheet):

    match = _rgx_bar.match(sheet)
    if match:
        return match.end(),"bar", None
    
    match = _rgx_repeat.match(sheet)
    if match:
        digits, colons = match.groups()
        if digits is not None:
            return match.end(),"repeat", int(digits)
        elif colons is not None:
            return match.end(),"repeat", len(colons)
        else:
            return None

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
        tie,lower,upper,note,length,dots,stacato = match.groups()

        return match.end(),"note",(
            tie is not '',
            len(lower),
            len(upper),
            note,
            1 if length is '' else int(length),
            len(dots),
            stacato is not ''
        )

    return None
        
        
    