# ----------------------------------------------------------------------
# undefined.py
#
# Undefined
# ----------------------------------------------------------------------

from core.nodes.__base__ import Expression

class Undefined(Expression):
    def __init__(self) -> None:
        super().__init__()

        self.value = 'undefined'

    def __str__(self) -> str:
        return self.value

    def _eval(self, env):
        super()._eval(env)

        return None