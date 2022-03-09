#!/usr/bin/env python3

# Author: Orlson Joseph

import sys

from argparse import ArgumentParser, ArgumentError

from core.exceptions import UnsupportedException
from core.config import EXTENSION

from core.lexer.lexer import Lexer
from core.lexer.stream import Stream
from core.parser.parser import Parser

# Limit Python builtin traceback system for clearer exceptions
sys.tracebacklimit = 0

# TODO Logging

class Dusk:
    def __init__(self, file) -> None:
        self.file = file
        self.source = None

        if not self.file.lower().endswith(EXTENSION):
            raise UnsupportedException(
                f"{self.file} has unsupported extensions. " + 
                f"The only supported extension is ({EXTENSION})")

    def _read(self):
        with open(self.file, "r") as fh:
            source = fh.read()

            fh.close()
            
        return source

    def execute(self):
        # Read source file contents
        self.source = self._read()

        # 
        self.lexer = Lexer()
        self.stream = Stream(self.source)

        # Split input into token list
        self.lexer.tokenize(self.stream)
        self.tokens = self.lexer.add_EOF_token()

        print(self.tokens)
        
        # Parser
        self.parser = Parser(self.tokens)
        self.ast = self.parser.parse()

if __name__ == "__main__":
    
    # Create ArgumentParser
    parser = ArgumentParser(
        description = "Dusk Interpreter",
        allow_abbrev = True)

    # Add arguments to parser
    parser.add_argument("file", help = "the target file")
    
    # TODO Interactive mode
    
    try:
        arguments = parser.parse_args()

    except ArgumentError as ex:
        sys.stdout(sys.argv[0] + ":", ex, file = sys.stderr)
        sys.exit(2)

    app = Dusk(file = arguments.file)
    app.execute()