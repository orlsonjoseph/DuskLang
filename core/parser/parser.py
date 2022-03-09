# ----------------------------------------------------------------------
# parser.py
#
# Parser
# ----------------------------------------------------------------------

from core.config import EOF
from core.lexer.tokens import Tokens

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

    def parse(self):
        pass