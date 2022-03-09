# ----------------------------------------------------------------------
# fxs.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

from core.ast.ast import Literal, Program

def p_program(p):
    # if p.next_token.type == TODO handle function declaration
    return Program(body = p_expression(p))

def p_expression(p):
    # if p.current_token.type == 
    return 

def p_factor(p):
    if p.current_token.type == "ID":
        return 