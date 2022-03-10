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

# AST - Eval
class DuskNameError(NameError):
    pass

class DuskTypeError(TypeError):
    pass