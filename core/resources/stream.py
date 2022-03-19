# ----------------------------------------------------------------------
# stream.py
#
# Stream
# ----------------------------------------------------------------------

import re

from core.tokens import Tokens as library

class Stream:
    def __init__(self, input) -> None:
        self.position = 0

        self.line, self.column = 1, 0
        self.input = input

    def eof(self, increment = 0):
        return self.position + increment >= len(self.input)

    def next(self):
        if not self.eof():
            character = self.input[self.position]

            if re.fullmatch(library.newline, character):
                self.line, self.column = self.line + 1, 0
            else: self.column += 1

            self.position += 1
            return character
        
        return None

    def peek(self, increment = 0):
        if not self.eof(increment):
            return self.input[self.position + increment]

        return None

    def get_position(self):
        return (self.line, self.column)