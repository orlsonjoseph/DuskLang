# ----------------------------------------------------------------------
# ast.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

from core.ast.base import Statement, Expression

class Program(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body

class Literal(Expression):
    def __init__(self, token) -> None:
        super().__init__()
        
        self.token = token
        self.value, self.type = token.value, token.type

    def __str__(self) -> str:
        return 