# ----------------------------------------------------------------------
# error.py
#
# Error
# ----------------------------------------------------------------------

# Dusk.py
class UnsupportedException(Exception):
    pass

# Lexer.py
class SyntaxError(Exception):
    pass

# Parser.py
class ParsingError(Exception):
    pass

# AST - Nodes
class NameError(Exception):
    pass

class TypeError(Exception):
    pass

class ValueError(Exception):
    pass

class IndexError(Exception):
    pass

class AttributeError(Exception):
    pass