import re
_regex_table = [
    ("bar", re.compile(r"\s\|\s")),
    ("repeat", re.compile(r"\s\:(\d+)\s|\s(\:+)\s")),
    ("time", re.compile(r"\s\(d+)\/(\d+)\s")),
    ("volume", re.compile(r"\s(\d+)\%\s")),
    ("dynamic", re.compile(r"\s\d+%\s<\s.*<\s\d+%\s")),
    ("tempo", re.compile(r"\s(\d+)[Bb][Pp][Mm]\s") ),
    ("note", re.compile(r"(\^?)(\,*)(\'*)(A#|Ab|A|Bb|B|C#|C|D#|Db|D|Eb|E|F#|F|G#|Gb|G)(\d*)(\.*)(\`*)")),
]


def preprocess(sheet):
    # ignore repeated measure bars
    sheet = re.sub(r"\|\s*\|","|",sheet)
    
    # replace all bars with space around bars to ensure whitespace
    sheet = re.sub(r"\|"," | ",sheet)
    
    # make all whitespace single space
    sheet = re.sub(r"\s+"," ",sheet)
    
    return sheet

def lex()

# returns ("id",position in string,quantified expression)
def token(sheet):
    for token, regex in _regex_table:
        match = regex.match(sheet)
        if match:
            return token, match
    
    
    match = _rgx_bar.match(s)
    if match:
        return "bar", None

    match = _rgx_repeat.match(s)
    if match:
        digits, colons = match.groups()
        if digits is not None:
            return "repeat", int(digits)
        elif colons is not None:
            return "repeat", len(colons)
        else:
            return None

    match = _rgx_time.match(s)
    if match:
        num, den = match.groups()
        return "time", (int(num),int(den))

    match = _rgx_volume.match(s)
    if match:
        volume = match.group(1)
        return "volume", int(volume)

    match = _rgx_dynamic.match(s)
    if match:
        return "dynamic", None # PMLFIXME

    match = _rgx_tempo.match(s)
    if match:
        tempo = match.group(1)
        return "tempo", int(tempo)

    match = _rgx_note.match(s)
    if match:
        tie,lower,upper,note,length,dots,stacato = match.groups()

        return "note",(
            tie is not None,
            0 if lower is None else len(lower),
            0 if upper is None else len(upper),
            note,
            1 if length is None else int(length),
            0 if dots is None else len(dots),
            stacato is None
        )

    return None
        
        
    