# ----------------------------------------------------------------------
# lexer.py
#
# Lexer
# ----------------------------------------------------------------------

import re

from core.tokens import Tokens as library

from core.resources.token import Token
from core.resources.exceptions import SyntaxError
from core.resources.constants import EMPTY_STRING, EOF, UNDERSCORE

class Lexer:
    def __init__(self) -> None:
        self.tokens = []

        # Retrieve rules and labels from tokens
        self.rules = [(k, v) 
            for k, v in vars(library).items() if k.startswith('t_')]

    def _recognize(self, lexeme, stream):
        token, lexeme = self._process(lexeme, stream)
        if token: self.tokens.append(token)

        return lexeme

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

        # Add whitespace to input to process last characters
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
                if not in_quote: # but were
                    lexeme += character
                    character = stream.next()

            # Is this character a punctuation / delimiter
            punctuation = not character.isalnum() and not character.isspace() and character != UNDERSCORE

            # If punctuation was a period, makes sure that
            # next character is not a digit
            if punctuation and re.fullmatch(library.t_PERIOD, character):
                if not stream.peek().isalpha(): punctuation = False
                
            # If punctuation; handle two parts binary operators
            if punctuation:
                isoperator = any(
                    re.fullmatch(pattern, character) for pattern in library.operators)
                
                if isoperator and re.fullmatch(library.t_EQUALS[0], stream.peek()):
                    character += stream.next()

            # If whitespace
            if (character.isspace() or punctuation) and not in_quote:
                lexeme = self._recognize(lexeme, stream)
                
                if punctuation and character:
                    self._recognize(character, stream)

                continue

            if not re.fullmatch(library.newline, character):
                lexeme += character
                
        return self.tokens

    def eof_token(self):
        token = Token(EOF, None, (0, 0))

        self.tokens.append(token)
        return self.tokens