# ----------------------------------------------------------------------
# parser.py
#
# Parser
# ----------------------------------------------------------------------

from core.parser.fxs import p_program

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = iter(tokens)

        self.current_token = None
        self.next_token = None

        self.update()
        self.update()

    def update(self):
        self.current_token = self.next_token
        self.next_token = next(self.tokens)

        if self.current_token is None:
            return False

        return True

    def parse(self):
        return p_program(self)