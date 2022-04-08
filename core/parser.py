# ----------------------------------------------------------------------
# parser.py
#
# Parser
# ----------------------------------------------------------------------

from core.rules import p_program

S = p_program

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = iter(tokens)

        self.current_token = None
        self.next_token = None

        self.update()
        self.update()

    def update(self):
        self.current_token = self.next_token
        
        try:
            self.next_token = next(self.tokens)
        except StopIteration:
            return False

        return True

    def parse(self):
        return S(self)