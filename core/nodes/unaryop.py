# ----------------------------------------------------------------------
# unaryop.py
#
# Unary Operation
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class UnaryOp(Expression):
    def __init__(self, operator, right) -> None:
        super().__init__()

        self.right, self.operator = right, operator

    def __str__(self) -> str:
        return f"Unary Operation {self.operator.value} [{self.right}]"

    def _eval(self, env, **kwargs):        
        x = self.right._eval(env)
        return eval(f"{self.operator.value} x")