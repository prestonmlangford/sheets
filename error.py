

class CompileError(Exception):
    def __init__(self,msg):
        super().__init__(msg)

class TokenError(Exception):
    def __init__(self,msg):
        super().__init__(msg)
