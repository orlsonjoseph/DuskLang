#!/usr/bin/env python3

# ----------------------------------------------------------------------
# dusk.py
#
# Entry point for Dusk source code interpreter
# ----------------------------------------------------------------------

import sys

from argparse import ArgumentParser, ArgumentError

from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter

from core.resources.exceptions import UnsupportedException
from core.resources.constants import EXTENSION
from core.resources.stream import Stream

# Limit Python builtin traceback system for clearer exceptions
# sys.tracebacklimit = 0

# TODO Logging

class Dusk:
    def __init__(self, file) -> None:
        self.file = file
        self.source = None

        if not self.file.lower().endswith(EXTENSION):
            raise UnsupportedException(
                f"{self.file} has unsupported extensions. " + 
                f"The only supported extension is ({EXTENSION})")

        # Interpreter variables
        self.environment = {}

    def _read(self):
        with open(self.file, "r") as fh:
            source = fh.read()

            fh.close()
            
        return source

    def execute(self, debug = False):
        # Read source file contents
        self.source = self._read()

        # 
        self.stream = Stream(self.source)

        # Split input into token list
        self.lexer = Lexer()
        self.lexer.tokenize(self.stream)
        self.tokens = self.lexer.eof_token()

        # if debug: print(self.tokens)

        # Parser
        self.parser = Parser(self.tokens)
        self.ast = self.parser.parse()

        if debug: print(self.ast)
        
        # Evaluator / Interpreter
        self.interpreter = Interpreter(
                self.ast, self.environment, debug=True)
        self.interpreter.evaluate()

        # if debug: print(self.environment)

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
    app.execute(debug = True)