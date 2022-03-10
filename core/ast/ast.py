# ----------------------------------------------------------------------
# ast.py
#
# Abstract Syntactic Tree
# ----------------------------------------------------------------------

from ast import operator
from core.ast.base import Statement, Expression
from core.exceptions import DuskNameError, DuskTypeError

class Program(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body

    def __str__(self) -> str:
        return f"Program - {self.body}"
    
    def _eval(self, env):
        return super()._eval(env)

class Block(Statement):
    def __init__(self, body) -> None:
        super().__init__()

        self.body = body
    
    def __str__(self) -> str:
        return f"Block - {self.body}"

class BinaryOperation(Expression):
    def __init__(self, left, right, operator) -> None:
        super().__init__()

        self.left, self.right = left, right
        self.operator = operator

    def __str__(self) -> str:
        return f"Binary Operation {self.operator.value} [{self.left}] [{self.right}]"

    def _eval(self, env):
        super()._eval(env)

        x, y = self.left._eval(env), self.right._eval(env)
        
        # Type check
        if not isinstance(x, y.__class__):
            raise DuskTypeError(
                "Unable to use operator on {x.__class__} and {y.__class__}. (Line {self.operator.linepos})")

        if self.operator == "PLUS":
            return x + y

        if self.operator == "MULT":
            return x * y

class UnaryOperation(Expression):
    def __init__(self, operator, right) -> None:
        super().__init__()

        self.right, self.operator = right, operator

    def __str__(self) -> str:
        return f"Unary Operation {self.operator.value} [{self.right}]"

    def _eval(self, env):
        super()._eval(env)

        if self.operator == "PLUS":
            return + self.right._eval(env)

        if self.operator == "MINUS":
            return - self.right._eval(env)

class Literal(Expression):
    def __init__(self, token, name) -> None:
        super().__init__()
        
        self.name, self.token = name, token

    def __str__(self) -> str:
        return f"Literal '{self.name}'"

    def _eval(self, env, exists = False):
        super()._eval(env)

        if exists:
            if not env.has_key(self.name):
                raise DuskNameError(f"Name '{self.name}' not defined. (Line {self.token.linepos})")
        # TODO retrieve variable
        return 0

class Number(Expression):
    def __init__(self, value) -> None:
        super().__init__()

        self.value = value

    def __str__(self) -> str:
        return f"Number <{self.value}>"

    def _eval(self, env):
        super()._eval(env)

        return int(self.value)