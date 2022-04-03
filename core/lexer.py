# ----------------------------------------------------------------------
# lexer.py
#
# Lexer
# ----------------------------------------------------------------------

import re

from core.tokens import Tokens as library

from core.resources.exceptions import SyntaxError
from core.resources.constants import EMPTY_STRING, EOF
    
class Token:
    def __init__(self, type, value, pos) -> None:
        self.type = type.split('_')[-1]
        self.value = value

        self.linepos, self.charpos = pos

    def __str__(self) -> str:
        return f"({self.type}, {self.value})"

    def __repr__(self) -> str:
        return self.__str__()
    
    # Overloading comparison
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self.type == __o

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

class Lexer:
    def __init__(self) -> None:
        self.tokens = []

        # Retrieve rules and labels from tokens
        self.rules = [(k, v) 
            for k, v in vars(library).items() if k.startswith('t_')]

    def _process(self, lexeme, stream):
        if lexeme:
            # Priority
            # 1. Reserved words
            if lexeme in library.reserved:
                return Token(
                    lexeme.upper(), lexeme, stream.get_position()), EMPTY_STRING

            # 2. Everything in order of definition
            for label, expression in self.rules:
                string = str.join(EMPTY_STRING, lexeme)

                if re.fullmatch(expression, string):
                    return Token(label, string, stream.get_position()), EMPTY_STRING

            # Error if we get here
            line, _ = stream.get_position()
            raise SyntaxError(f"Invalid token <{lexeme}> on line {line}")

        return None, EMPTY_STRING

    def tokenize(self, stream):
        lexeme, predicate = EMPTY_STRING, None
        in_quote = False

        # Add newline to input to process last characters
        stream.input += " "

        # Ideally read until eof
        while not stream.eof():
            character = stream.next()

            # Skip until predicate is met
            if predicate:
                flag = re.fullmatch(predicate, character)
                if flag: predicate = None
                continue
            
            # Skip comments
            if re.fullmatch(library.comment, character):
                predicate = library.newline
                continue
            
            if re.fullmatch(library.quote, character):
                in_quote = not in_quote

            # Is this character a punctuation / delimiter
            punctuation = any(
                    re.fullmatch(pattern, character or EMPTY_STRING)
                        for pattern in library.punctuation)

            # If punctuation; handles composed operators
            if punctuation:
                split = any(
                    re.fullmatch(pattern, character) for pattern in library.composed_operators)
                
                # 2nd half of composed operators is equals
                if split and re.fullmatch(library.t_EQUALS[0], stream.peek()):
                    character += stream.next()
                    
            # If whitespace
            if (re.fullmatch(library.whitespace, character) or punctuation) and not in_quote:
                token, lexeme = self._process(lexeme, stream)
                if token: self.tokens.append(token)
                
                if punctuation and character:
                    token, _ = self._process(character, stream)
                    self.tokens.append(token)

                continue

            if not re.fullmatch(library.newline, character):
                lexeme += character
                
        return self.tokens

    def add_EOF_token(self):
        token = Token(EOF, None, (0, 0))

        self.tokens.append(token)
        return self.tokens