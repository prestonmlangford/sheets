

class CompileError(Exception):
    def __init__(self,msg):
        super().__init__(msg)

class TokenError(Exception):
    def __init__(self,msg,sheet,position):
        start = sheet[:position].rfind('|')
        end = sheet[position:].find('|')
        if (start < 0) or (end < 0):
            msg = "Missing measure bar"
        else:
            msg += " -> " +  sheet[start:position+end+1]
        super().__init__(msg)
