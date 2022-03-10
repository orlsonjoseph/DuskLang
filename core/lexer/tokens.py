# ----------------------------------------------------------------------
# tokens.py
#
# Token specifications for symbols in Dusk.
# ----------------------------------------------------------------------

class Tokens:

    # Reserved words
    reserved = ['int', 'let']

    # Literals (identifier)
    t_ID        = r'[A-Za-z_][A-Za-z0-9_]*',
        
    t_INTEGER   = r'\d+',
    t_FLOAT     = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))',
    t_STRING    = r'\".*?\"',

    
    # Operators
    t_PLUS      = r'\+',
    t_MINUS     = r'-',
    t_MULT      = r'\*',
    t_DIV       = r'/',

    # Assignment
    t_EQUALS    = r'=',

    # Delimiters ( ) [ ] { } , . =

    t_LPAREN    = r'\(',
    t_RPAREN    = r'\)',
    t_LBRACKET  = r'\[',
    t_RBRACKET  = r'\]',
    t_LBRACE    = r'\{',
    t_RBRACE    = r'\}',
    t_COMMA     = r'\,', 
    t_PERIOD    = r'\.', 
    t_SEMI      = r'\;', 
    t_COLON     = r'\:',
  
    # Comments
    comment     = r'#'

    # Whitespace
    whitespace  = r' '
    
    # Newline
    newline     = r'\n'

    # Punctuation
    punctuation = [t_PLUS, t_MINUS, t_EQUALS, t_SEMI, t_COLON]