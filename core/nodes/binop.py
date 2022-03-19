# ----------------------------------------------------------------------
# binop.py
#
# Binary Operation
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

from core.resources.typing import Typing
from core.resources.exceptions import TypeError, ValueError

class BinOp(Expression):
    def __init__(self, left, right, operator) -> None:
        super().__init__()

        self.left, self.right = left, right
        self.operator = operator

    def __str__(self) -> str:
        return f"Binary Operation {self.operator.value} [{self.left}] [{self.right}]"

    def _eval(self, env):
        super()._eval(env)

        x, y = self.left._eval(env), self.right._eval(env)

         # is not None
        if x is None or y is None:
            raise ValueError(
                f"Undefined value at operands. (Line {self.operator.linepos})")

        # Type check
        if not Typing.compare(x, y):
            raise TypeError(
                f"Unable to use operator on {x} and {y}. (Line {self.operator.linepos})")

        if self.operator == "PLUS":
            return x + y

        if self.operator == "MINUS":
            return x - y

        if self.operator == "MULT":
            return x * y

        if self.operator == "DIV":
            return x / y
