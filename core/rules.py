# ----------------------------------------------------------------------
# rules.py
#
# Parsing Rules
# ----------------------------------------------------------------------

from core.nodes import *

from core.resources.constants import BUILTIN_TYPES, EOF
from core.resources.exceptions import ParsingError

def p_error(p, expected):
    raise ParsingError(
        f"Expected token {expected}; got {p.current_token.value}")

def p_program(p):
    statement_list = p_statement_list(p)

    if p.next_token == EOF:
        return Program(body = statement_list)

    return p_error(p, EOF)

def p_statement_list(p, endmarker=None):
    statement = [p_statement(p)]

    if p.next_token == EOF or p.current_token == endmarker:
        return statement

    statement.extend(p_statement_list(p))   
    return statement

def p_statement(p):
    if p.current_token == 'DEFINE':
        return p_define_stmt(p)

    if p.current_token == 'EDGE':
        return p_edge_stmt(p)

    if p.current_token == 'IF':
        return p_if_stmt(p)
    
    if p.current_token == 'LET':
        return p_let_stmt(p)

    if p.current_token == 'RETURN':
        return p_return_stmt(p)

    if p.current_token == 'WHILE':
        return p_while_stmt(p)

    if p.current_token == 'STRUCT':
        return p_struct_decl(p)

    return p_expr(p)

def p_define_stmt(p):
    p.update()

    token, name = p.current_token, p_literal(p)
    parameters = None

    if p.current_token == 'LPAREN':
        p.update();
        
        parameters = p_declaration_list(p)

        if p.current_token != 'RPAREN': return p_error(p, 'RPAREN')
        p.update()

    return Function(name, parameters, p_compound_stmt(p), token)

def p_edge_stmt(p):
    p.update()

    token, graph = p.current_token, p_literal(p)
    start, end = p_constant(p), p_constant(p)
    return Edge(graph, start, end, token)

def p_if_stmt(p):
    p.update()
    
    condition = p_conditional_expr(p)

    if p.current_token == 'LBRACE':
        block, alternate = p_compound_stmt(p), None

        if p.current_token == 'ELSE':
            alternate = else_stmt(p)

        return If(condition, block, alternate)
    return p_error(p, 'LBRACE')

def else_stmt(p):
    p.update()

    return p_compound_stmt(p)

def p_let_stmt(p):
    p.update()
    
    expr = p_assignment_expr(p); p.update()
    return expr 

def p_return_stmt(p):
    p.update()

    token, expr = p.current_token, p_expr(p); p.update()
    return Return(expr, token)

def p_while_stmt(p):
    p.update()

    condition = p_conditional_expr(p)

    if p.current_token == 'LBRACE':
        block = p_compound_stmt(p)

        return While(condition, block)
    return p_error(p, 'LBRACE')

def p_struct_decl(p):
    p.update()

    token = p.current_token
    name = p_literal(p)
    variables =  p_declaration_list(p)
    p.update(); return Struct(name, variables, token)

def p_compound_stmt(p):
    if not p.current_token == 'LBRACE':
        return p_error(p, 'LBRACE')

    p.update()

    # Empty braces
    if p.current_token == 'RBRACE':
        p.update()
        return Block(body = None)

    block = p_statement_list(p, endmarker='RBRACE')

    if p.current_token == 'RBRACE':
        p.update();
        return Block(body = block)

    return p_error(p, 'RBRACE')

def p_expr(p):
    expr = p_assignment_expr(p)

    if p.current_token == 'SEMI':
        p.update()

    return expr
    
# Helper function
def binary_operator(p, peer, child, operator):
    left = child(p)

    while p.current_token in operator:
        token = p.current_token
        p.update()

        right = peer(p)
        left = (Assign if token == 'EQUALS' else BinOp)(left, right, token)

    return left

def p_assignment_expr(p):
    return binary_operator(p, p_assignment_expr, p_conditional_expr, ['EQUALS'])

def p_conditional_expr(p):
    return p_inclusive_or_expr(p)

def p_inclusive_or_expr(p):
    return binary_operator(p, p_inclusive_or_expr, p_and_expr, ['OR'])

def p_and_expr(p):
    return binary_operator(p, p_and_expr, p_equality_expression, ['AND'])
    
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

    if p.current_token == 'NODE':
        token = p.current_token; p.update()
        return Graph(p_unary_expression(p), token)

    return p_postfix_expression(p)

def p_postfix_expression(p):
    token = p.current_token

    # Argument Expression List
    if p.current_token == 'LBRACKET':
        p.update()

        expr = p_argument_expr_list(p); p.update()
        return List(expr, p.current_token)

    # Indexing
    if p.next_token == 'LBRACKET':
        label = p_primary_expression(p)
        return Indexing(label, p_group_expression(p, 'RBRACKET'), token)

    if p.next_token == 'LPAREN':
        name = p_primary_expression(p); p.update()
        args = p_argument_expr_list(p); p.update()
        return Call(name, args, p.current_token)

    # Composed name (person.name)
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
        return p_declaration(p)
    
    if p.current_token == 'ID':
        return p_literal(p) 

    if p.current_token == 'LPAREN':
        return p_group_expression(p, 'RPAREN')

    return p_constant(p)

def p_group_expression(p, endmarker):
    # group_expression : LPAREN expression RPAREN
    p.update()

    group = p_expr(p)
    if p.current_token == endmarker:
        p.update(); return group
    
    return p_error(p, endmarker)

def p_declaration_list(p):
    if p.current_token == 'LPAREN':
        p.update()

        expr = [p_declaration(p)]
        while p.current_token in ['COMMA']:
            p.update()

            next = p_declaration(p)
            expr = expr + [next]

        return expr
    return p_error(p, 'LPAREN')

def p_declaration(p):
    # declarator : ID COLON type_specifier
    name = p_literal(p)
    p.update()

    type = p_type_identifier(p)
    return Let(name, type, p.current_token)

def p_type_identifier(p):
    # type_identifier : FLOAT
    #                 : INT
    #                 : LIST
    #                 : STR
    
    if p.current_token in BUILTIN_TYPES:
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

    expr = [p_assignment_expr(p)]

    while p.current_token in ['COMMA']:
        p.update()

        next = p_assignment_expr(p)
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