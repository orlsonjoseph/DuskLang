# ----------------------------------------------------------------------
# condition.py
#
# Condition (Expression)
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Condition(Expression):
    def __init__(self, operator, left, right) -> None:
        super().__init__()

        self.operator = operator if operator else None
        self.left, self.right = left, right
        
    def __str__(self) -> str:
        return f"Condition <{self.left} - {self.operator} - {self.right}>"

    def _eval(self, env):
        super()._eval(env)

        if not self.operator:
            return bool(self.left._eval(env))

        left, right = self.left._eval(env), self.right._eval(env)
        if self.operator == 'GE':
            return left >= right
        
        return  