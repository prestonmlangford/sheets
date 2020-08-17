import re


_regex_table = {
    "time" : re.compile("\s\d+\/\d+\s"), #  4/4 7/16
    "volume" : re.compile("\s\d+\%\s"), # 100% 50% 0%
    "tempo" : re.compile("\s\d+(B|b)(P|p)(M|m)\s"), # 120BPM 100bpm 50Bpm
    
}

def token(kind,s):
    if not kind in _regex_table:
        return None
    
    regex = _regex_table[kind]
    
    return search(s).group(0)[]
        
        
    