# ----------------------------------------------------------------------
# fxs.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

from core.ast.ast import AssignStatement, BinaryOperation, Block, Float, LetStatement, Literal, Number, Program, String, TypeIdentifier, UnaryOperation
from core.config import EOF
from core.exceptions import ParsingError

OPERATORS = ['PLUS', 'MINUS', 'MULT', 'DIV']

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
    # statement_list: statement SEMI statement_list
    #               | statement SEMI
    statement = [p_statement(p)]
    if p.current_token == 'SEMI':
        if p.next_token != EOF:
            p.update()

            statement.extend(p_statement_list(p))
            return statement
        else:
            return statement

    return p_error(p, 'SEMI')

def p_statement(p):
    # statement : expression_statement
    #           | let_statement
    #           | ... TODO

    if p.current_token == "LET":
        return p_let_statement(p)

    return p_expression_statement(p)

def p_let_statement(p):
    # let_statement : LET ID COLON type_identifier EQUALS expression_statement SEMI
    p.update()
    name = p_literal(p)

    if p.current_token == 'COLON':
        p.update()

        type = p_type_identifier(p)
        if p.current_token == 'EQUALS':
            p.update()

            assign = p_expression_statement(p)
            return LetStatement(name, type, assign)
        else:
            return p_error(p, 'EQUALS')
    else:
        return p_error(p, 'COLON')

def p_expression_statement(p):
    # expression_statement : arithmetic_expression
    #                      | group_expression
    #                      | ... TODO
    if p.current_token == 'LBRACE':
        return p_block_statement(p)

    if p.next_token == 'EQUALS':
        return p_assignment_expression(p)

    expression = p_arithmetic_expression(p)
    return expression

def p_assignment_expression(p):
    # assignment_expression : ID EQUALS expression_statement SEMI
    name = p_literal(p)
    if p.current_token == 'EQUALS':
        p.update()

        assign = p_expression_statement(p)
        return AssignStatement(name, assign)

    return p_error(p, 'EQUALS')

def p_block_statement(p):
    # block_statement : LBRACE expression_statement RBRACE
    p.update()

    group = Block(body = p_expression_statement(p))
    if p.current_token == 'RBRACE':
        return group
    
    return p_error(p, 'RBRACE')

# Helper function
def binary_operator(p, fx, operators):
    left = fx(p)

    while p.current_token.type in operators:
        operator = p.current_token
        p.update()

        right = fx(p)
        left = BinaryOperation(left, right, operator)

    return left

def p_arithmetic_expression(p):
    return binary_operator(p, p_term_expression, ('PLUS', 'MINUS'))

def p_term_expression(p):
    return binary_operator(p, p_factor_expression, ('MULT', 'DIV'))

def p_factor_expression(p):
    if p.current_token.type in ('PLUS', 'MINUS'):
        return p_unary_operator(p)

    return p_primary_expression(p)

def p_unary_operator(p):
    operator = p.current_token
    p.update()

    return UnaryOperation(operator, p_factor_expression(p))

def p_primary_expression(p):    
    if p.current_token == 'LPAREN':
        return p_group_expression(p)

    return p_atom(p)

def p_group_expression(p):
    # group_expression : LPAREN arithmetic_expression RPAREN
    p.update()

    # TODO update to expression statement? maybe
    group = p_arithmetic_expression(p)
    if p.current_token == 'RPAREN':
        p.update()
        return group
    
    return p_error(p, 'RPAREN')

def p_type_identifier(p):
    # type_identifier : INT
    #                 : STR
    #                 : literal
    if p.current_token in ['INT', 'FLOAT', 'STR']:
        type = p.current_token.type
        p.update()

        return TypeIdentifier(type)

    return p_error(p, 'type identifer')

def p_atom(p):
    token = p.current_token

    if token == 'ID':
        return p_literal(p)
    
    if token == 'INTEGER':
        p.update()
        return Number(token.value)

    if token == 'FLOAT':
        p.update()
        return Float(token.value)

    if token == 'STRING':
        p.update()
        return String(token.value)

    return p_error(p, 'atom')

def p_literal(p):
    token = p.current_token

    if token == 'ID':
        p.update()
        return Literal(token.value, token)

    return p_error(p, 'ID')