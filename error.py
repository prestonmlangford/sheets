

class CompileError(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class TokenError(Exception):
    def __init__(self,sheet):
        msg = "Unable to parse expression: " + sheet[:10].rstrip() + " . . ."
        super().__init__(msg)
