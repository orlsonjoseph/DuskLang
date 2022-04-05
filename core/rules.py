# ----------------------------------------------------------------------
# fxs.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

# TODO linepos to every Node

from logging import root
from core.nodes import *
from core.nodes import binop

from core.resources.constants import EOF
from core.resources.exceptions import ParsingError

def p_error(p, expected):
    raise ParsingError(
        f"Expected token {expected} got {p.current_token.value}")

def p_program(p):
    # program: (statement_list EOF)
    statement_list = p_statement_list(p)

    if p.next_token == EOF:
        return Program(body = statement_list)
    return p_error(p, EOF)

def p_statement_list(p):
    # statement_list: statement statement_list EOF
    #               | statement EOF

    statement = [p_statement(p)]

    if p.next_token == EOF:
        return statement

    if p.current_token == 'RBRACE':
        p.update()

    statement.extend(p_statement_list(p))
    return statement

def p_statement(p):
    # statement : expression_statement
    #           | let_statement
    #           | ... TODO

    if p.current_token == 'LET':
        return p_let_statement(p)

    if p.current_token == 'IF':
        return p_if_statement(p)
  
    if p.current_token == 'WHILE':
        return p_while_statement(p)

    if p.current_token == 'STRUCT':
        return p_struct_statement(p)

    return p_expression(p)

def p_let_statement(p):
    # let_statement : LET expression SEMI

    p.update()

    expr = p_assignment_expression(p); p.update()
    return expr

def p_if_statement(p):
    # if_statement : IF expression block
    #              : IF expression block ELSE block

    p.update()
    
    condition = p_conditional_expression(p)

    if p.current_token == 'LBRACE':
        block = p_compound_statement(p)

        if p.current_token == 'ELSE':
            p.update()

            else_block = p_compound_statement(p)
            return If(condition, block, else_block)
        return If(condition, block)
    return p_error(p, 'LBRACE')

def p_while_statement(p):
    # while_statement : WHILE expression block
    p.update()

    condition = p_conditional_expression(p)

    if p.current_token == 'LBRACE':
        block = p_compound_statement(p)

        return While(condition, block)
    return p_error(p, 'LBRACE')

def p_struct_statement(p):
    # struct_statement : STRUCT literal LBRACE declarator_list RBRACE
    p.update()

    name = p_literal(p)
    if p.current_token == 'LBRACE':
        p.update()

        variables = p_declarator_list(p)
        return Struct(name, variables, p.current_token)
    return p_error(p, 'RBRACE')

def p_expression(p):
    # expression : arithmetic_expression
    #                      | group_expression
    #                      | ... TODO
    
    if p.current_token == 'LBRACE':
        return p_compound_statement(p)

    expression = p_conditional_expression(p)
    if p.current_token == 'SEMI': p.update();
    return expression

def p_compound_statement(p):
    # compound_statement : LBRACE expression_statement RBRACE
    p.update()

    # Empty braces
    if p.current_token == 'RBRACE':
        block = None
    else:
        block = p_statement_list(p)
        if p.current_token != 'RBRACE':
            return p_error(p, 'RBRACE')

    p.update()
    return Block(body = block)

# Helper function
def binary_operator(p, peer, child, operator):
    left = child(p)

    while p.current_token in operator:
        token = p.current_token
        p.update()

        right = peer(p)
        left = (Assign if token == 'EQUALS' else BinOp)(left, right, token)

    return left

def p_conditional_expression(p):
    return p_assignment_expression(p)

def p_assignment_expression(p):
    return binary_operator(p, p_assignment_expression, p_inclusive_or_expression, ['EQUALS'])

def p_inclusive_or_expression(p):
    return binary_operator(p, p_inclusive_or_expression, p_and_expression, ['OR'])

def p_and_expression(p):
    return binary_operator(p, p_and_expression, p_equality_expression, ['AND'])
    
def p_equality_expression(p):
    return binary_operator(p, p_equality_expression, p_relational_expression, ['EQ', 'NE'])

def p_relational_expression(p):
    return binary_operator(p, p_relational_expression, p_additive_expression, ['LT', 'LE', 'GT', 'GE'])

def p_additive_expression(p):
    return binary_operator(p, p_additive_expression, p_multiplicative_expression, ['PLUS', 'MINUS'])

def p_multiplicative_expression(p):
    return binary_operator(p, p_multiplicative_expression, p_unary_expression, ['TIMES', 'DIVIDE', 'MODULE'])

def p_unary_expression(p):
    if p.current_token in ['PLUS', 'MINUS', 'NOT']:
        operator = p.current_token
        p.update()

        return UnaryOp(operator, p_unary_expression(p))

    return p_postfix_expression(p)

def p_postfix_expression(p):
    # Argument Expression List
    if p.current_token == 'LBRACKET':
        p.update()

        expr = p_argument_expr_list(p); p.update()
        return List(expr, p.current_token)

    # Indexing
    if p.next_token == 'LBRACKET':
        label = p_primary_expression(p)
        return Indexing(label, p_group_expression(p, 'RBRACKET'), p.next_token)

    if p.next_token == 'LPAREN':
        pass # argument_expr_list for function call

    # Composed name (person.name)
    # TODO composed name followed by indexing
    if p.next_token == 'PERIOD':
        prefix = p_literal(p)

        while p.current_token == 'PERIOD':
            p.update()

            root = p_postfix_expression(p)
            prefix = Prefix(prefix, root, p.current_token)

        return prefix

    return p_primary_expression(p)

def p_primary_expression(p):
    if p.next_token == 'COLON':
        return p_declarator(p)
    
    if p.current_token == 'ID':
        return p_literal(p) 

    if p.current_token == 'LPAREN':
        return p_group_expression(p, 'RPAREN')

    return p_constant(p)

def p_group_expression(p, endmarker):
    # group_expression : LPAREN expression RPAREN
    p.update()

    group = p_expression(p)
    if p.current_token == endmarker:
        p.update(); return group
    
    return p_error(p, endmarker)
    
def p_declarator(p):
    # declarator : ID COLON type_specifier
    name = p_literal(p)
    p.update()

    type = p_type_identifier(p)
    return Let(name, type, p.current_token)

def p_declarator_list(p):
    # declarator_list : declarator
    #                 : declarator_list COMMA declarator
    
    expr = [p_declarator(p)]

    while p.current_token in ['COMMA']:
        p.update()

        next = p_declarator(p)
        expr = expr + [next]

    return expr

def p_type_identifier(p):
    # type_identifier : FLOAT
    #                 : INT
    #                 : LIST
    #                 : STR
    
    if p.current_token in ['FLOAT', 'INT', 'LIST', 'STR', 'BOOL']:
        type = p.current_token.type
        p.update()

        return TypeId(type)

    if p.current_token == 'ID':
        type = p.current_token.value
        p.update()
        return TypeId(type)

    return p_error(p, 'type identifer')

def p_argument_expr_list(p):
    # argument_expr_list : assignment_expression
    #                    | argument_expr_list COMMA assignment_expression

    expr = [p_assignment_expression(p)]

    while p.current_token in ['COMMA']:
        p.update()

        next = p_assignment_expression(p)
        expr = expr + [next]

    return expr

def p_constant(p):
    token = p.current_token
    
    if token == 'INTEGER':
        p.update()
        return Number(token.value)

    if token == 'FLOAT':
        p.update()
        return Float(token.value)

    if token == 'STRING':
        p.update()
        return String(token.value)

    if token in ['TRUE', 'FALSE']:
        p.update()
        return Boolean(True if token == 'TRUE' else False)

    return p_empty(p)

def p_literal(p):
    token = p.current_token

    if token == 'ID':
        p.update()
        return Literal(token.value, token)

    return p_error(p, 'ID')

def p_empty(p):
    return Undefined()