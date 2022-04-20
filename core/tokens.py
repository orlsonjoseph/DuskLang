# ----------------------------------------------------------------------
# tokens.py
#
# Token specifications for symbols in Dusk.
# ----------------------------------------------------------------------

class Tokens:

    # Reserved words
    reserved = ['and', 'bool', 'define', 'edge', 'else', 'false', 'float', 'graph', 'if',
                'int', 'let', 'list', 'node', 'not', 'or', 'return', 'str',
                'struct', 'true', 'while']

    # Literals (identifier)
    t_ID        = r'[A-Za-z_][A-Za-z0-9_]*'
        
    t_INTEGER   = r'\d+'
    t_FLOAT     = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    t_STRING    = r'\".*?\"'
    
    # Operators
    t_PLUS      = r'\+'
    t_MINUS     = r'-'
    t_TIMES     = r'\*'
    t_DIVIDE    = r'/'
    t_MODULE    = r'%'

    # Assignment
    t_EQUALS    = r'='

    # Conditional Operators
    t_LT        = r'<'
    t_GT        = r'>'
    t_NT        = r'!'

    t_LE        = r'<='
    t_GE        = r'>='
    t_NE        = r'!='

    t_EQ        = r'=='

    # Delimiters ( ) [ ] { } , . =

    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'
    t_LBRACE    = r'\{'
    t_RBRACE    = r'\}'
    t_COMMA     = r'\,' 
    t_PERIOD    = r'\.' 
    t_SEMI      = r'\;' 
    t_COLON     = r'\:'
  
    # Comments
    comment     = r'#'

    # Whitespace
    whitespace  = r' '
    
    # Newline
    newline     = r'\n'

    # Quote
    quote       = r'\"'

    # Operators
    operators   = [t_EQUALS, t_LT, t_GT, t_NT]